import time
from typing import Dict, List, Tuple, Union

from corneto._graph import Graph
from corneto._settings import LOGGER
from corneto.methods.signaling import create_flow_graph, signflow


def _info(s, show=True):
    if show:
        print(s)


def read_dataset(zip_path):
    """Extracts and processes a graph and its vertex attributes from a zipped dataset.

    The function reads two CSV files from a specified zipfile: 'pkn.csv' and 'data.csv'.
    The 'pkn.csv' contains graph edges with three columns: 'source', 'interaction',
    and 'target'. The 'interaction' column uses integers to denote the type of
    interaction (1 for activation, -1 for inhibition). The 'data.csv' file contains
    vertex attributes with three columns: 'vertex', 'value', and 'type', where 'value'
    can be a continuous measure such as from a t-statistic in differential expression,
    and 'type' categorizes vertices as either inputs ('P' for perturbation) or outputs
    ('M' for measurement).

    Args:
        zip_path (str): The file path to the zip file containing the dataset.

    Returns:
        tuple: A tuple containing:
            - Graph: A graph object initialized with edges from 'pkn.csv'. Each edge is
              defined by a source, a target, and an interaction type.
            - dict: A dictionary mapping each protein (vertex) to a tuple of ('type',
              'value'), where 'type' is either 'P' or 'M' and 'value' represents the
              continuous state of the protein.

    Raises:
        FileNotFoundError: If the zip file cannot be found at the provided path.
        KeyError: If expected columns are missing in the CSV files, indicating incorrect
                  or incomplete data.

    Example:
        >>> graph, vertex_attrs = read_dataset('path/to/dataset.zip')
        >>> print(graph.shape)  # Shape of the imported graph ([vertices, edges])
        >>> print(vertex_attrs) # Displays protein attributes
    """
    import zipfile

    import pandas as pd

    from corneto import Graph

    with zipfile.ZipFile(zip_path, "r") as z:
        with z.open("pkn.csv") as pkn, z.open("data.csv") as data:
            df_pkn = pd.read_csv(pkn)
            df_data = pd.read_csv(data)

    # Convert pkn.csv rows to tuples and create a graph from them
    tpl = [tuple(x) for x in df_pkn.itertuples(index=False)]
    G = Graph.from_sif_tuples(tpl)

    # Process the 'data.csv' for vertex attributes
    df_data["type"] = df_data["type"].replace({"input": "P", "output": "M"})
    data_dict = dict(zip(df_data["vertex"], zip(df_data["type"], df_data["value"])))

    return G, data_dict


# TODO: Return a problem, which is associated to the carnival graph
# think about connecting edge/nodes with variables!
def runVanillaCarnival(
    perturbations: Dict,
    measurements: Dict,
    priorKnowledgeNetwork: Union[List[Tuple], Graph],
    betaWeight: float = 0.2,
    solver=None,
    backend_options=dict(),
    solve=True,
    verbose=True,
    **kwargs,
):
    if backend_options is None:
        backend_options = dict()
    backend_options["verbosity"] = verbose
    start = time.time()
    data = dict()
    for k, v in perturbations.items():
        data[k] = ("P", v)
    for k, v in measurements.items():
        data[k] = ("M", v)
    conditions = {"c0": data}
    if isinstance(priorKnowledgeNetwork, List):
        G = Graph.from_sif_tuples(priorKnowledgeNetwork)
    elif isinstance(priorKnowledgeNetwork, Graph):
        G = priorKnowledgeNetwork
    else:
        raise ValueError("Provide a list of sif tuples or a graph")
    # Prune the graph
    V = set(G.vertices)
    inputs = set(perturbations.keys())
    outputs = set(measurements.keys())
    c_inputs = V.intersection(inputs)
    c_outputs = V.intersection(outputs)
    _info(f"{len(c_inputs)}/{len(inputs)} inputs mapped to the graph", show=verbose)
    _info(f"{len(c_outputs)}/{len(outputs)} outputs mapped to the graph", show=verbose)
    _info(f"Pruning the graph with size: V x E = {G.shape}...", show=verbose)
    Gp = G.prune(list(c_inputs), list(c_outputs))
    _info(f"Finished. Final size: V x E = {Gp.shape}.", show=verbose)
    V = set(Gp.vertices)
    cp_inputs = {input: v for input, v in perturbations.items() if input in V}
    cp_outputs = {output: v for output, v in measurements.items() if output in V}
    _info(f"{len(cp_inputs)}/{len(c_inputs)} inputs after pruning.", show=verbose)
    _info(f"{len(cp_outputs)}/{len(c_outputs)} outputs after pruning.", show=verbose)
    _info("Converting into a flow graph...", show=verbose)
    Gf = create_flow_graph(Gp, conditions)
    _info("Creating a network flow problem...", show=verbose)
    P = signflow(Gf, conditions, l0_penalty_vertices=betaWeight, **kwargs)
    _info("Preprocess completed.", show=verbose)
    if solve:
        P.solve(solver=solver, **backend_options)
    end = time.time() - start
    _info(f"Finished in {end:.2f} s.", show=verbose)
    return P, Gf


def runInverseCarnival(
    measurements: Dict,
    priorKnowledgeNetwork: Union[List[Tuple], Graph],
    betaWeight: float = 0.2,
    solver=None,
    solve=True,
    **kwargs,
):
    raise NotImplementedError()
    if isinstance(priorKnowledgeNetwork, List):
        G = Graph.from_sif_tuples(priorKnowledgeNetwork)
    elif isinstance(priorKnowledgeNetwork, Graph):
        G = priorKnowledgeNetwork
    else:
        raise ValueError("Provide a list of sif tuples or a graph")
    perturbations = {v: 0.0 for v in G.get_source_vertices()}
    return runVanillaCarnival(
        perturbations, measurements, G, betaWeight=betaWeight, solver=solver, **kwargs
    )


def heuristic_carnival(
    priorKnowledgeNetwork: Union[List[Tuple], Graph],
    perturbations: Dict,
    measurements: Dict,
    restricted_search: bool = False,
    prune: bool = True,
    verbose=True,
    max_time=None,
    max_edges=None,
):
    if isinstance(priorKnowledgeNetwork, List):
        G = Graph.from_sif_tuples(priorKnowledgeNetwork)
    elif isinstance(priorKnowledgeNetwork, Graph):
        G = priorKnowledgeNetwork
    else:
        raise ValueError("Provide a list of sif tuples or a graph")
    Gp = G
    perts = set(perturbations.keys())
    meas = set(measurements.keys())
    V = set(G.vertices)
    inputs = V.intersection(perts)
    outputs = V.intersection(meas)
    if verbose:
        print(f"{len(inputs)}/{len(perts)} inputs mapped to the graph")
        print(f"{len(outputs)}/{len(meas)} outputs mapped to the graph")
    if prune:
        if verbose:
            print(f"Pruning the graph with size: V x E = {G.shape}...")
        Gp = G.prune(list(inputs), list(outputs))
        if verbose:
            print(f"Finished. Final size: V x E = {Gp.shape}.")
    V = set(Gp.V)
    inputs = V.intersection(perts)
    outputs = V.intersection(meas)
    # Clean unreachable inputs/outputs
    inputs_p = {k: perturbations[k] for k in inputs}
    outputs_p = {k: measurements[k] for k in outputs}
    selected_edges = None
    if restricted_search:
        selected_edges = reachability_graph(Gp, inputs_p, outputs_p, verbose=verbose)
    selected_edges, paths, stats = bfs_search(
        Gp,
        inputs_p,
        outputs_p,
        subset_edges=selected_edges,
        max_time=max_time,
        max_edges=max_edges,
        verbose=verbose,
    )
    # Estimate error, using inputs and outputs and comparing to what was selected
    predicted_values = {p[0]: p[1][p[0]][1] for p in paths}
    errors = dict()
    for k, v in measurements.items():
        error = abs(v - predicted_values.get(k, 0))
        errors[k] = error
    total_error = sum(errors.values())
    if verbose:
        print(f"Total error: {total_error}")
        print(f"Number of selected edges: {len(selected_edges)}")
    return Gp, selected_edges, paths, stats, errors


def get_result(P, G, condition="c0", exclude_dummies=True):
    V = P.expr["vertex_values_" + condition].value
    E = P.expr["edge_values_" + condition].value
    d_vertices = {"V": G.V, "value": V}
    d_edges = {"E": G.E, "value": E}
    return d_vertices, d_edges


def get_selected_edges(P, G, condition="c0", exclude_dummies=True):
    # Get the indexes of the edges whose value is not zero
    E = P.expr["edge_values_" + condition].value
    selected_edges = []
    for i, v in enumerate(E):
        if v != 0:
            # Check if the edge contains a
            # vertex starting with "_"
            if exclude_dummies:
                s, t = G.get_edge(i)
                s = list(s)
                t = list(t)
                if len(s) > 0 and s[0].startswith("_"):
                    continue
                if len(t) > 0 and t[0].startswith("_"):
                    continue
            selected_edges.append(i)
    return selected_edges


def _str_state(state, max_steps=3):
    v, path = state
    nodes = []
    n_steps = len(path) - 1
    skip = False
    for i, (k, v) in enumerate(path.items()):
        if i < n_steps and skip:
            continue
        pos, val, edge = v
        if max_steps is not None and i >= max_steps and i < n_steps:
            nodes.append("...")
            skip = True
        else:
            if val > 0:
                nodes.append(f"+{k}")
            else:
                nodes.append(f"-{k}")
    return " -> ".join(nodes)


def _extract_nodes(path, values=False, subset=None):
    d = []
    v, pd = path
    for k, v in pd.items():
        e = k
        if values:
            e = (k, v[1])
        if subset is not None:
            if k not in subset:
                continue
        d.append(e)
    return tuple(d)


def reachability_graph(
    G,
    input_nodes,
    output_nodes,
    subset_edges=None,
    verbose=True,
    early_stop=False,
    expand_outputs=True,
    max_printed_outputs=10,
):
    visited = set(input_nodes)
    current = set(input_nodes)
    unreached_outputs = set(output_nodes)
    outs = set(output_nodes)
    selected_edges = set()
    layer = 0
    if verbose:
        print("Starting reachability analysis...")
        print(f"L{layer:<3}: {len(input_nodes):<4} > input(s)")
    while current is not None and len(current) > 0:
        layer += 1
        new = set()
        for v in current:
            for i, (s, t) in G.out_edges(v):
                if subset_edges is not None and i not in subset_edges:
                    continue
                # Add only if t is a new node
                nt = list(t)
                if len(nt) == 0:
                    continue
                vt = nt[0]
                if vt not in visited:
                    new |= {vt}
                    selected_edges.add(i)
        # How many are output nodes?
        reached_outputs = outs.intersection(new)
        unreached_outputs -= reached_outputs
        if verbose:
            print(f"L{layer:<3}: {len(new):<4}", end="")
            if len(reached_outputs) > 0:
                if len(reached_outputs) <= max_printed_outputs:
                    str_reached = "/".join(reached_outputs)
                else:
                    # Get only the first max_printed_outputs items
                    str_reached = (
                        "/".join(list(reached_outputs)[:max_printed_outputs]) + "..."
                    )
                print(f" > {len(reached_outputs):<4} output(s): {str_reached}")
            else:
                print("")
        visited |= new
        current = set(new)
        if not expand_outputs:
            current -= reached_outputs
        if early_stop and len(unreached_outputs) == 0:
            break
    if verbose:
        print(f"Finished reachability analysis ({len(selected_edges)} selected edges).")
    return selected_edges


def _path_conflict(p, paths):
    nodes_in_path = _extract_nodes(p)
    valid = True
    p_a, p_b = None, None
    for path in paths:
        common = set(nodes_in_path).intersection(_extract_nodes(path))
        p_a = _extract_nodes(p, values=True, subset=common)
        p_b = _extract_nodes(path, values=True, subset=common)
        if p_a != p_b:
            valid = False
            break
    return valid, p_a, p_b


def _str_path_nodes(a):
    nodes = []
    for k, v in a:
        if v > 0:
            nodes.append(f"+{k}")
        else:
            nodes.append(f"-{k}")
    return "/".join(nodes)


def bfs_search(
    G,
    initial_dict,
    final_dict,
    max_time=None,
    queue_max_size=None,
    subset_edges=None,
    max_edges=None,
    verbose=True,
):
    Q = []
    reached = set()
    stats = dict(loops=0, iters=0, conflicts=0)
    paths = []
    exit = False
    maxq = 0
    last_level = 0
    selected_edges = set()
    first_level = G.bfs(list(initial_dict.keys()))
    outs = []
    for k in final_dict.keys():
        outs.append(str(k) + f" (L{first_level[k]})")
    if verbose:
        print(", ".join(outs))
    for k, w in initial_dict.items():
        Q.append((k, {k: (0, w, None)}))
    start = time.time()
    while len(Q) > 0 and not exit:
        if max_time is not None and time.time() - start > max_time:
            if verbose:
                print("Timeout reached.")
            break
        current = Q.pop(0)
        n, v = current
        if v[n][0] > last_level:
            last_level = v[n][0]
            if verbose:
                elapsed = time.time() - start
                print(f"L{last_level:<3}: {stats['iters']:>6} iters, {elapsed:.2f} s.")
        for i, (s, t) in G.out_edges(n):
            if subset_edges is not None and i not in subset_edges:
                continue
            val = int(G.get_attr_edge(i).get("interaction", 0))
            nt = list(t)
            if len(nt) == 0:
                continue
            nt = nt[0]
            if nt == n or nt in v:
                stats["loops"] += 1
                continue
            nv = dict(v)
            pos, w, _ = nv[n]
            value = w * val
            nv[nt] = (pos + 1, value, i)
            # State = (vertex, (dist. from source, value=+1/-1, edge index))
            new_state = (nt, nv)
            # Check if the vertex is in the goal set
            if nt not in reached:
                vf = final_dict.get(nt, None)
                if vf is not None and vf == value:
                    valid, p_a, p_b = _path_conflict(new_state, paths)
                    if verbose:
                        print(" >", _str_state(new_state))
                    if not valid:
                        print(
                            "   ! conflict: {} != {}".format(
                                _str_path_nodes(p_a), _str_path_nodes(p_b)
                            )
                        )
                        stats["conflicts"] += 1
                        continue
                    reached |= {nt}
                    paths.append(new_state)
                    # Add edges
                    selected_edges |= set(
                        edge_idx
                        for (_, _, edge_idx) in nv.values()
                        if edge_idx is not None
                    )
                    if max_edges is not None and len(selected_edges) >= max_edges:
                        if verbose:
                            print("Max edges reached.")
                        exit = True
                        break

            if len(reached) >= len(final_dict):
                exit = True
                break
            # No loop, add new state
            Q.append(new_state)
            if len(Q) > maxq:
                maxq = len(Q)
            if (
                queue_max_size is not None
                and queue_max_size > 0
                and len(Q) > queue_max_size
            ):
                break
        stats["iters"] += 1
    if verbose:
        print(f"Finished ({time.time() - start:.2f} s)")
        print(f" > Number of selected edges: {len(selected_edges)}")
        print(f" > Total iterations: {stats['iters']}")
        print(f" > Detected loops: {stats['loops']}")
        print(f" > Conflicts: {stats['conflicts']}")
    return selected_edges, paths, stats

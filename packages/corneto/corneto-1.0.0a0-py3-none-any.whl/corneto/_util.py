from collections import OrderedDict
from itertools import filterfalse
from typing import Any, Callable, Dict, Iterable, Optional, Set, TypeVar

import numpy as np
from numpy.linalg import svd

T = TypeVar("T")


def unique_iter(
    iterable: Iterable[T], key: Optional[Callable[[T], Any]] = None
) -> Iterable[T]:
    # Based on https://iteration-utilities.readthedocs.io/en/latest/generated/unique_everseen.html
    seen: Set[Any] = set()
    seen_add = seen.add
    if key is None:
        for element in filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element


def get_latest_version(
    url="https://raw.githubusercontent.com/saezlab/corneto/main/pyproject.toml",
    timeout=5,
):
    import re
    import urllib.request

    try:
        response = urllib.request.urlopen(url, timeout=timeout)
        content = response.read().decode()
        match = re.search(r'version\s*=\s*"(.*)"', content)
        if match:
            version = match.group(1)
            return version
    except Exception:
        return None


class DisplayInspector:
    # From: https://stackoverflow.com/questions/70768390/detecting-if-ipython-notebook-is-outputting-to-a-terminal
    """Objects that display as HTML or text."""

    def __init__(self) -> None:
        self.status = None

    def _repr_html_(self) -> str:
        self.status = "HTML"
        return ""

    def __repr__(self) -> str:
        self.status = "Plain"
        return ""


def supports_html() -> bool:
    # From: https://stackoverflow.com/questions/70768390/detecting-if-ipython-notebook-is-outputting-to-a-terminal
    import sys

    """Test whether current runtime supports HTML."""
    if "IPython" not in sys.modules or "IPython.display" not in sys.modules:
        return False

    from IPython.display import display

    inspector = DisplayInspector()
    display(inspector)
    return inspector.status == "HTML"


def _get_info() -> Dict[str, Dict]:
    from corneto import __version__
    from corneto.backend import DEFAULT_BACKEND, available_backends

    info: Dict[str, Dict] = OrderedDict()

    latest = get_latest_version()
    if latest == __version__:
        cv = f"v{__version__} (up to date)"
    else:
        if latest:
            cv = f"v{__version__} (latest: v{latest})"
        else:
            cv = f"v{__version__}"
    info["corneto_version"] = {
        "title": "Installed version",
        "message": cv,
        "value": __version__,
    }
    info["backends"] = {
        "title": "Available backends",
        "message": ", ".join(
            [str(e) + f" v{e.version()}" for e in available_backends()]
        ),
        "value": available_backends(),
    }
    info["default_backend"] = {
        "title": "Default backend (corneto.opt)",
        "message": "No backend detected, please install CVXPY or PICOS",
        "value": None,
    }
    info["available_solvers"] = {
        "title": "Installed solvers",
        "message": "No installed solvers",
        "value": [],
    }
    if DEFAULT_BACKEND:
        info["default_backend"]["message"] = str(DEFAULT_BACKEND)
        info["default_backend"]["value"] = DEFAULT_BACKEND
        info["available_solvers"]["message"] = ", ".join(
            [s for s in DEFAULT_BACKEND.available_solvers()]
        )
        info["available_solvers"]["value"] = DEFAULT_BACKEND.available_solvers()
    info["graphviz_version"] = {
        "title": "Graphviz version",
        "message": "Graphviz not installed. To support plotting, please install graphviz with conda",
        "value": None,
    }
    try:
        import graphviz

        info["graphviz_version"]["message"] = f"v{graphviz.__version__}"
        info["graphviz_version"]["value"] = graphviz.__version__
    except Exception:
        pass
    info["repo_url"] = {
        "title": "Repository",
        "message": "https://github.com/saezlab/corneto",
        "value": "https://github.com/saezlab/corneto",
    }
    return info


def info():
    info = _get_info()

    if supports_html():
        import base64
        from importlib.resources import files

        from IPython.core.display import display
        from IPython.display import HTML

        # logo_path = pkg_resources.resource_filename(__name__, "resources/logo.png")
        logo_path = files("corneto").joinpath("resources/logo.png")

        with open(logo_path, "rb") as f:
            img_bytes = f.read()
        b64img = base64.b64encode(img_bytes).decode("utf-8")
        html = f"""
        <table style='background-color:rgba(0, 0, 0, 0);'>
        <tr>
            <td style="min-width:85px">
                <img src="data:image/jpeg;base64,{b64img}" style="width: 100%; max-width:100px;" />
            </td>
            <td>
            <table>
                *
            </table>
            </td>
        </tr>
        </table>"""
        html_info = ""
        for k, v in info.items():
            title = v["title"]
            message = v["message"]
            if "_url" in k:
                message = f"<a href={message}>{message}</a>"
            html_info += (
                f"<tr><td>{title}:</td><td style='text-align:left'>{message}</td></tr>"
            )
        display(HTML(html.replace("*", html_info)))

    else:
        for v in info.values():
            title = v["title"]
            message = v["message"]
            print(f"{title}:", f"{message}")


def _info():
    from corneto import __version__
    from corneto.backend import DEFAULT_BACKEND, available_backends

    latest = get_latest_version()
    if latest == __version__:
        print(f"CORNETO v{__version__} (up to date)")
    else:
        if latest:
            print(f"CORNETO v{__version__} (latest: v{latest})")
        else:
            print(f"CORNETO v{__version__}")
    print(
        "Available backends: ",
        ", ".join([str(e) + f" v{e.version()}" for e in available_backends()]),
    )
    if DEFAULT_BACKEND:
        print("Default backend (corneto.opt):", str(DEFAULT_BACKEND))
        print(
            f"Available solvers for {DEFAULT_BACKEND!s}:",
            ", ".join([s for s in DEFAULT_BACKEND.available_solvers()]),
        )
    else:
        print("No backend detected in the system. Please install CVXPY or PICOS.")

    try:
        import graphviz

        print(f"Graphviz available: v{graphviz.__version__}.")
    except Exception:
        print("Graphviz not installed.")
    print("https://github.com/saezlab/corneto")


def nullspace(A, atol=1e-13, rtol=0):
    # https://scipy-cookbook.readthedocs.io/items/RankNullspace.html
    A = np.atleast_2d(A)
    _, s, vh = svd(A)
    tol = max(atol, rtol * s[0])
    nnz = (s >= tol).sum()
    ns = vh[nnz:].conj().T
    return ns

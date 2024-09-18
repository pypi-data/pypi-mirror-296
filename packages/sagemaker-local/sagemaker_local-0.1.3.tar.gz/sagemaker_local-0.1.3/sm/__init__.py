"""Wrapper code for pyterraform."""

import sys
from pathlib import Path


def get_tf_root() -> Path:
    """Get Terraform root folder."""
    curdir = Path().resolve()
    while curdir != curdir.root:
        if (curdir / ".terraform").is_dir():
            return curdir / ".terraform"
        if (curdir / ".git").is_dir() or (curdir / ".git").is_symlink():
            git_root = curdir
            break
        curdir = curdir.parent
    else:
        raise ValueError("No '.git' or '.terraform' folder found!")
    tf_roots = list(git_root.rglob(".terraform"))
    if not tf_roots:
        raise ValueError("No '.terraform' folder found.")
    if len(tf_roots) > 1:
        raise ValueError(
            f"More than one '.terraform' folder found.\n{tf_roots}",
        )
    return tf_roots[0]


def main():
    """Nfind pyterraform module and evoke it."""
    tf_root = get_tf_root()
    pytf_roots = list((tf_root / "modules").glob("*/pyterraform"))
    if not pytf_roots:
        raise ValueError("No `sm-pipeline` module detected.")
    sys.path.append(str(pytf_roots[0].parent))

    from pyterraform import sm

    sm.main()

"""iqtree interface."""

from gpex.utils import shell


def infer(alignment_path, bootstrap_count):
    shell(
        f"iqtree -m JC -wbtl -redo -o outgroup -s {alignment_path} -bb {bootstrap_count}"
    )

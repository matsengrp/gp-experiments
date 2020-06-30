"""iqtree interface."""

from gpex.utils import shell


def infer(alignment_path, bootstrap_count, seed):
    shell(
        f"iqtree -m JC -wbt -redo -o outgroup -s {alignment_path} -seed {seed} -bb {bootstrap_count}"
    )

"""iqtree interface."""

import subprocess


def shell(command_string):
    return subprocess.check_call(command_string, shell=True)


def infer(phylip_path, bootstrap_count, seed):
    shell(
        f"iqtree -m JC -wbt -redo -o outgroup -s {phylip_path} -seed {seed} -bb {bootstrap_count}"
    )

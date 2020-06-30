"""iqtree interface."""

import subprocess


def shell(command_string):
    return subprocess.check_call(command_string, shell=True)


def infer(phylip_path, seed):
    shell(f"iqtree -m JC -s {phylip_path} -seed {seed}")

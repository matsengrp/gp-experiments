# gp-experiments

## Installation

Assuming that you are in the `libsbn` conda environment:

    conda install -c bioconda iqtree newick_utils
    pip install -e .


### Installing [perf](https://perf.wiki.kernel.org/index.php/Main_Page)

On Debian, the apt package is named `linux-perf` and on my machine everything just worked.

On Ubuntu, I think this is a complete set of commands ([reference](https://superuser.com/questions/980632/run-perf-without-root-rights/980757)).

    sudo apt-get install linux-tools-$(uname -r) linux-tools-generic
    sudo sh -c 'echo -1 >/proc/sys/kernel/perf_event_paranoid'
    sudo sh -c 'echo "kernel.perf_event_paranoid=-1" > /etc/sysctl.d/perf.conf'
    sudo sh -c " echo 0 > /proc/sys/kernel/kptr_restrict"

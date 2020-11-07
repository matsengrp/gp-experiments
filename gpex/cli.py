"""Command line interface."""

import pathlib
import json
import click
import click_config_file
import dendropy
import gpex.ourlibsbn as ourlibsbn
import gpex.iqtree as iqtree
from gpex.sequences import evolve_jc
from gpex.tree import add_outgroup, kingman, set_all_branch_lengths_to
from gpex.utils import from_json_file, make_cartesian_product_hierarchy, shell


def alignment_path_of_prefix(prefix):
    return f"{prefix}.fasta"


def json_provider(file_path, cmd_name):
    """Enable loading of flags from a JSON file via click_config_file."""
    if cmd_name:
        with open(file_path) as config_data:
            config_dict = json.load(config_data)
            if cmd_name not in config_dict:
                if "default" in config_dict:
                    return config_dict["default"]
                # else:
                raise IOError(
                    f"Could not find a '{cmd_name}' or 'default' section in '{file_path}'"
                )
            return config_dict[cmd_name]
    # else:
    return None


def print_method_name_and_locals(method_name, local_variables):
    """Print method name and local variables."""
    if "ctx" in local_variables:
        del local_variables["ctx"]
    print(f"{method_name}{local_variables})")


def restrict_dict_to_params(d_to_restrict, cmd):
    """Restrict the given dictionary to the names of parameters for cmd."""
    param_names = {param.name for param in cmd.params}
    return {key: d_to_restrict[key] for key in d_to_restrict if key in param_names}


def dry_run_option(command):
    return click.option(
        "--dry-run",
        is_flag=True,
        help="Only print paths and files to be made, rather than actually making them.",
    )(command)


# Entry point
@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
def cli():
    pass


@cli.command()
@click.option(
    "--taxon-count", type=int, required=True,
)
@click.option(
    "--seq-len", type=int, required=True,
)
@click.option(
    "--tree-height", type=float, help="If set, scale the tree to have this total height"
)
@click.option(
    "--ingroup-branch-length",
    type=float,
    help="If set, set all branches other than the outgroup to this length",
)
@click.option(
    "--prefix", type=click.Path(), required=True,
)
@dry_run_option
@click_config_file.configuration_option(implicit=False, provider=json_provider)
def simulate(
    taxon_count, seq_len, tree_height, ingroup_branch_length, prefix, dry_run,
):
    """Simulate a colaescent tree with an outgroup. """
    if dry_run:
        print_method_name_and_locals("prep", locals())
        return
    inner_tree = kingman(taxon_count - 1, pop_size=1)
    if ingroup_branch_length is not None:
        set_all_branch_lengths_to(inner_tree, ingroup_branch_length)
    tree = add_outgroup(inner_tree, 0.0)
    if tree_height is not None:
        tree.scale_edges(tree_height / tree.seed_node.distance_from_tip())
    tree.write(path=f"{prefix}.nwk", schema="newick")
    data = evolve_jc(tree, seq_len)
    data.write(path=alignment_path_of_prefix(prefix), schema="fasta")


@cli.command()
@click.argument("alignment_path", required=True, type=click.Path(exists=True))
@click.option(
    "--bootstrap-count", type=int, default=1000,
)
@click_config_file.configuration_option(implicit=False, provider=json_provider)
def infer(alignment_path, bootstrap_count):
    """Infer a tree and bootstraps using iqtree."""
    iqtree.infer(alignment_path, bootstrap_count=bootstrap_count)


@cli.command()
@click.argument("path", required=True, type=click.Path(exists=True))
def reroot(path):
    """ Reroot the trees in `path` on "outgroup".

    Output to `path.rerooted`."""
    shell(f"nw_reroot {path} outgroup > {path}.rerooted")


@cli.command()
@click.argument("tree_path", required=True, type=click.Path(exists=True))
@click.argument("fasta_path", required=True, type=click.Path(exists=True))
@click.argument("out_csv_path", required=True, type=click.Path())
@click.option("--tol", type=float, default=1e-2)
@click.option("--max-iter", type=int, default=10)
@click_config_file.configuration_option(implicit=False, provider=json_provider)
def fit(tree_path, fasta_path, out_csv_path, tol, max_iter):
    """Fit an SBN using generalized pruning.

    Tree file is assumed to be a Newick file unless the path ends with `.nexus`.
    """
    ourlibsbn.fit(tree_path, fasta_path, out_csv_path, tol, max_iter)


@cli.command()
@click.argument("tree_path", required=True, type=click.Path(exists=True))
@click.argument("out_csv_path", required=True, type=click.Path())
def simpleaverage(tree_path, out_csv_path):
    """Fit an SBN using rooted SBN-SA."""
    inst = ourlibsbn.rooted_instance_of_trees(tree_path)
    inst.train_simple_average()
    inst.sbn_parameters_to_csv(out_csv_path)


@cli.command()
@click.argument("tree_path", required=True, type=click.Path(exists=True))
@click.argument("sbn_parameter_csv_path", required=True, type=click.Path())
@click.argument("out_path", required=True, type=click.Path())
def treeprobs(tree_path, sbn_parameter_csv_path, out_path):
    """Calculate tree probabilities using the supplied SBN parameters."""
    ourlibsbn.treeprobs(tree_path, sbn_parameter_csv_path).to_csv(
        out_path, index=False, header=False)


@cli.command()
@click_config_file.configuration_option(
    implicit=False, required=True, provider=json_provider
)
@click.pass_context
def go(ctx):
    """simulate -> infer -> reroot -> fit.

    Then touch a `.sentinel` file to signal successful completion.
    """
    prefix = ctx.default_map["prefix"]
    alignment_path = alignment_path_of_prefix(prefix)
    ufboot_path = alignment_path + ".ufboot"
    rerooted_ufboot_path = alignment_path + ".ufboot.rerooted"
    pathlib.Path(prefix).parent.mkdir(parents=True, exist_ok=True)
    ctx.invoke(simulate, **restrict_dict_to_params(ctx.default_map, simulate))
    ctx.invoke(
        infer,
        alignment_path=alignment_path,
        **restrict_dict_to_params(ctx.default_map, infer),
    )
    ctx.invoke(reroot, path=ufboot_path)
    ctx.invoke(fit, tree_path=rerooted_ufboot_path, fasta_path=alignment_path)
    sentinel_path = prefix + ".sentinel"
    click.echo(f"LOG: `gpex go` completed; touching {sentinel_path}")
    pathlib.Path(sentinel_path).touch()


@cli.command()
@click.argument("in_path", required=True, type=click.Path(exists=True))
@click.argument("out_path", required=True, type=click.Path())
def newick_to_nexus_int_sort(in_path, out_path):
    """Convert a newick file with integer labels to a nexus one in which the taxon block
    is ordered numerically.
    """
    # Parse the trees.
    trees = dendropy.TreeList.get(path=in_path, schema="newick")

    # Sort the namespace.
    tns = dendropy.TaxonNamespace([
        dendropy.Taxon(x) for x in sorted(trees.taxon_namespace.labels(), key=int)
    ])

    # Write back out with the sorted namespace.
    trees = dendropy.TreeList.get(path=in_path, schema="newick", taxon_namespace=tns)
    trees.write(path=out_path, schema="nexus", translate_tree_taxa=True)


@cli.command()
@click.argument("choice_json_path", required=True, type=click.Path(exists=True))
def cartesian(choice_json_path):
    """Take the cartesian product of variable options.

    Put it all in an _output directory."""
    make_cartesian_product_hierarchy(from_json_file(choice_json_path))


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter

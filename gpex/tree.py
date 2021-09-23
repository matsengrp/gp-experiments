"""Tree-handling code."""

from copy import deepcopy
import dendropy
from dendropy.simulate import treesim
from dendropy.datamodel.taxonmodel import Taxon
from dendropy.datamodel.treemodel import Node, Tree

TAXON_PREFIX = "z"


def taxon_namespace_of_count(taxon_count):
    return dendropy.TaxonNamespace(
        [TAXON_PREFIX + str(idx) for idx in range(taxon_count)]
    )


def kingman(taxon_count, pop_size):
    return treesim.pure_kingman_tree(
        taxon_namespace=taxon_namespace_of_count(taxon_count), pop_size=pop_size
    )

def read_tree(newick_path):
    tree = Tree.get(path=newick_path, schema="newick")
    return tree

def birth_death(taxon_count, birth_rate, death_rate):
    return treesim.birth_death_tree(
        birth_rate, death_rate, ntax=taxon_count, repeat_until_success=True
    )


def set_all_branch_lengths_to(tree, length):
    for node in tree:
        node.edge.length = length


def add_outgroup(tree, relative_additional_height):
    desired_height = (
        1 + relative_additional_height
    ) * tree.seed_node.distance_from_tip()

    outgroup = Node(taxon=Taxon("outgroup"), edge_length=desired_height)
    tns = deepcopy(tree.taxon_namespace)
    tns.add_taxon(outgroup.taxon)
    new_root = Node()
    new_root.add_child(outgroup)
    new_root.add_child(tree.seed_node)
    new_tree = Tree(taxon_namespace=tns)
    new_tree.seed_node = new_root
    # Despite my best efforts, I was getting taxon namespace errors. So we round trip
    # from Newick. ¯\_(ツ)_/¯
    new_newick = str(new_tree) + ";"
    return Tree.get(data=new_newick, schema="newick")

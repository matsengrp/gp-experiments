"""Sequence handling."""

from dendropy.model.discrete import simulate_discrete_char_dataset, Jc69


def evolve_jc(tree, seq_len):
    return simulate_discrete_char_dataset(seq_len, tree, Jc69()).char_matrices[0]


# evolver = DiscreteCharacterEvolver(seq_model=Jc69())
# evolver.evolve_states(tree, seq_len)
# evolver.extend_char_matrix_with_characters_on_tree

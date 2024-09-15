import random


def simulate_simple_event(p):
    return random.random() <= p


def simulate_complex_event(probabilities):
    return [random.random() < p for p in probabilities]


def simulate_dependent_event(p_A, p_B_given_A):
    A = random.random() < p_A
    if A:
        B = random.random() < p_B_given_A
    else:
        B = random.random() < (1 - p_B_given_A)

    if A and B:
        return 0  # A and B
    elif A and not B:
        return 1  # A and not B
    elif not A and B:
        return 2  # not A and B
    else:
        return 3  # not A not B


def simulate_complete_group(probabilities):
    assert sum(probabilities) == 1, "Sum of the probabilities must be 1"
    rand_val = random.random()
    cumulative_prob = 0
    for i, p in enumerate(probabilities):
        cumulative_prob += p
        if rand_val < cumulative_prob:
            return i

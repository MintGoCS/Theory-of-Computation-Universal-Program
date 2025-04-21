# universal.py

from decoding import get_input, get_prime_exponents, pairing_function, decoded_program
from config import PRIME_LIST, MAX_STEP


def max_length(prime_list: list) -> int:
    """
    Returns the maximum length of programs
    :param prime_list:
    :return: Maximum length of programs
    """
    return len(prime_list)


def encoded_program_add_one(encoded_program):
    """
    Recovers the encoded program by adding one.
    :param encoded_program: Number of encoded_program.
    :return: Encoded program plus oen.
    """
    return encoded_program + 1


def decoding_program(encoded_pgm_num):
    """
    Decoding the encoded program.
    :param encoded_pgm_num: Number of encoded_program.
    :return: The whole decoded program.
    """
    if encoded_pgm_num is None:
        print("Error! No program to decode.")
        return
    encoded_pgm_num_add_one = encoded_program_add_one(encoded_pgm_num)  # Input number + 1
    print('********** Program Starts **********')
    prime_exponents = get_prime_exponents(encoded_pgm_num_add_one)
    for p in prime_exponents:
        paring_list = pairing_function(p)
        instruction = decoded_program(paring_list)
        print(instruction)
    print('********** End of Program **********\n')


def state_table(total_vars=21) -> list:
    """
    Generate a state table of variables with corresponding prime numbers and initial exponent 0.
        [{'var_name': 'Y', 'prime': 2, 'exp': 0}
        {'var_name': 'X_1', 'prime': 3, 'exp': 0}
        {'var_name': 'Z_1', 'prime': 5, 'exp': 0}
        {'var_name': 'X_2', 'prime': 7, 'exp': 0}
        {'var_name': 'Z_2', 'prime': 11, 'exp': 0}
        ...]
    :param total_vars: The total number of variables.
    :return: A state table of variables with corresponding prime numbers and initial exponent 0.
    """
    state_primes = PRIME_LIST[:21]  # Use the 21st prime member
    state_table = []
    var_names = ["Y"]
    for i in range(1, (total_vars - 1)//2 + 1):
        var_names.extend([f"X_{i}", f"Z_{i}"])

    for i in range(total_vars):
        state_table.append({
            "var_name": var_names[i],
            "prime": state_primes[i],
            "exp": 0
        })
    return state_table


def compute_s(state_table: list) -> int:
    """
    Compute the continued multiplication of primes with their exponent.
    :param state_table: A state table.
    :return: The continued multiplication of primes with their exponent.
    """
    total = 1
    for i in range(len(state_table)):
        total *= state_table[i]["prime"] ** state_table[i]["exp"]
    return total


def Lt(Z: int) -> int:
    """
    Obtain the length of programs
    :param Z: Encoded program number plus 1
    :return: Length of programs
    """
    # print(f"{get_prime_exponents(Z)},length={len(get_prime_exponents(Z))}")
    return len(get_prime_exponents(Z))


def get_abc(num: int):
    """
    Obtain the a, b and c from <a, <b, c>>
    :param num: Number of an exponent
    :return: List [a, b, c]
    """
    return pairing_function(num)


def find_label_target_line(label_idx: int, Z: int) -> int:
    """
    Given label encoding l(U), find the target instruction index K
    :param label_idx: l(U) -> b
    :param Z: Encoded program number plus 1
    :return: The (K-1)th line
    """
    target_num = label_idx - 2
    exp_list = get_prime_exponents(Z)

    abc_tabel = []
    for i in range(len(exp_list)):
        abc_tabel.append(get_abc(exp_list[i]))

    for i, abc in enumerate(abc_tabel):
        if abc[0] == target_num:
            return i  # Return the (k-1)th lines of instructions

    return -1  # If no condition 'GOTO'


def print_snapshots(K: int, state_table: list) -> str:
    """
    Print the snapshot after executing each instruction.
    :param K: Current line number (1-based)
    :param state_table: List of dicts with variable name, prime, and current exponent
    :return: A formatted snapshot string
    """
    # {'var_name': 'X_1', 'prime': 3, 'exp': 0}
    snapshot = f"({K}, "
    var_states = [f"{s['var_name']} = {s['exp']}" for s in state_table]
    snapshot += ", ".join(var_states)
    snapshot += ")"
    return snapshot


def check_if_infinite_loop(x_1, x_2) -> bool:
    """
    Same as main function, aiming to check if program is infinite.
    :param x_1: Input X
    :param x_2: Decoded program Y
    :return: True if program is infinite, otherwise False
    """
    Z = encoded_program_add_one(x_2)   # Plus one to recover the number

    instr_length = Lt(Z)
    S_table = state_table()
    S_table[1]['exp'] = x_1
    S = compute_s(S_table)

    K = 1  # Starts from the 1st instruction

    step = 1
    while step <= MAX_STEP:

        if K > instr_length or instr_length == 0:
            Y = S_table[0]['exp']  # Exponent of 2, which is 'Y'
            return False
        current_instr = get_prime_exponents(Z)[K - 1]  # The Kth instructions
        a, b, c = get_abc(current_instr)  # Decoding the #(I)_k into a, b and c
        P = S_table[c]['prime']  # The prime bounded to the variable

        # IF l(U) = 0 GOTO N
        if b == 0:
            K += 1
        # IF l(U) = 1 GOTO A
        elif b == 1:
            S *= P
            S_table[c]['exp'] += 1
            K += 1

        elif b == 2:
            # If the exponent of prime(c) is not 0, then subtract 1
            if S_table[c]['exp'] != 0:
                S //= P
                S_table[c]['exp'] -= 1
                K += 1
            else:  # If the exponent of prime(c) is 0, then move to the next instruction
                K += 1
        else:  # If b >= 3
            if S_table[c]['exp'] != 0:
                K = find_label_target_line(b, Z) + 1
            else:
                K += 1
        step += 1
    return True

# print(check_if_infinite_loop(10, 153055007))
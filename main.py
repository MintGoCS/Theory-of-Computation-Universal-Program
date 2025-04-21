# main.py
from decoding import get_input, get_prime_exponents, pairing_function, decoded_program
from universal import (encoded_program_add_one, decoding_program, state_table, compute_s, get_abc, Lt,
                       find_label_target_line,print_snapshots,max_length,check_if_infinite_loop)
from config import PRIME_LIST, MAX_STEP


def main(x_1, x_2):
    if check_if_infinite_loop(x_1, x_2):
        print("Warning! Detected an infinite loop. Program will not be executed.")
        return
    decoding_program(x_2)  # Print the decoded the program
    Z = encoded_program_add_one(x_2)   # Plus one to recover the number

    instr_length = Lt(Z)
    if Lt(Z) > max_length(PRIME_LIST):
        return

    S_table = state_table()
    S_table[1]['exp'] = x_1
    S = compute_s(S_table)

    K = 1  # Starts from the 1st instruction

    # is_print = True

    while True:

        snapshot = print_snapshots(K, S_table)
        print(snapshot)

        if K > instr_length or instr_length == 0:
            Y = S_table[0]['exp']  # Exponent of 2, which is 'Y'
            return f"\nOutput: Y = {Y}"
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


if __name__ == '__main__':
    try:
        x_1 = int(input("Please enter the first input x_1："))
        x_2 = int(input("please enter encoded program #(P)："))
    except ValueError:
        print("Please enter a integer number")
        exit(1)  # Invalid input
    output = main(x_1, x_2)
    print(output)
# decoding.py
from config import MIN_VAL, MAX_VAL


def get_input(prompt="Please enter a positive integer number："):
    """
    Obtains the input from the user.
    :param prompt: An integer between 0 ~ 2^64 - 1
    :return: User input
    """
    try:
        user_input = int(input(prompt))
        if not (MIN_VAL <= user_input <= MAX_VAL):
            raise ValueError(f"Input number exceeds the range from {MIN_VAL} to {MAX_VAL}.")
        return user_input
    except ValueError as ve:
        print(f"Error：{ve}")
        return None


def get_prime_exponents(num: int) -> list:
    """
    Divides the given number by prime factors, and return a list of exponent.
    :param num: User input(+1)
    :return: Exponent list
    """
    if num == 1: return [0]
    prime_list = [2, 3, 5, 7, 11,
                  13, 17, 19, 23,
                  29, 31, 37, 41,
                  43, 47, 53, 59,
                  61, 67, 71, 73,
                  79, 83, 89, 97]
    exp_list = []
    for prime in prime_list:
        if num == 1:  # If the number complete division, then exit the loop.
            break
        count = 0
        while num % prime == 0:
            count += 1
            num //= prime
        exp_list.append(count)

    if num != 1:
        raise ValueError(
            f"The number could not be fully factorized using the current prime list.\n"
            f"The remaining part ({num}) may contain a prime factor larger than {prime_list[-1]}."
        )
    return exp_list


def pairing_function(num: int) -> list:
    """
    Decode the pairing function and return the a, b, and c
    :param num: Number of an exponent
    :return: a, b, and c
    """
    a = b = c = 0
    abc = 2 ** a * (2 * (2 ** b * (2 * c + 1) - 1) + 1) - 1

    k = num + 1
    while k % 2 == 0:
        a += 1
        k //= 2

    k = ((k - 1) // 2) + 1
    while k % 2 == 0:
        b += 1
        k //= 2

    c = (k - 1) // 2

    return [a, b, c]


def decoded_program(pairing_list: list) -> str:
    """
    Decodes the given pairing list and returns the encoded program.
    :param pairing_list: contains a, b, and c
    :return: An encoded program
    """
    a, b, c = pairing_list[0], pairing_list[1], pairing_list[2]

    def decoded_label(a):
        """
        Decodes the label of an integer
        :param a: The integer a maps to a label
        :return: Encoded label
        """
        if a == 0:
            label = '\t'
        else:
            subscript = (a - 1) // 5 + 1
            quotient = subscript - 1
            label = f"[{chr(64+(a - quotient * 5))}{subscript}]\t"
        return label

    def decoded_variables(c):
        """
        Decodes the variables of an integer
        :param c: The integer c maps to a variable
        :return: 'X', 'Y', or 'Z'
        """
        c += 1
        if c == 1:
            return 'Y'
        else:
            return f"{'X' if c % 2 == 0 else 'Z'}{c // 2}"

    def decoded_instructions(b, c):
        """
        Decodes the instructions of an integer
        :param b: The integer b maps to a instruction
        :return: One line of instructions
        """
        variable = decoded_variables(c)
        if b == 0:
            instruction = f"{variable} <- {variable}"
        elif b == 1:
            instruction = f"{variable} <- {variable} + 1"
        elif b == 2:
            instruction = f"{variable} <- {variable} - 1"
        else:  # b >= 3
            instruction = f"IF {variable} != 0 GOTO {decoded_label(b-2)}"
        return instruction

    label = decoded_label(a)
    instruction = decoded_instructions(b, c)
    return f"{label} {instruction}"

print(get_prime_exponents(10))
print(pairing_function(1))
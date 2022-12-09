import numpy as np
import random
import time
import matplotlib.pyplot as plt


def generate_keys():
    keys = []

    for i in range(50):
        key = random.getrandbits(64)
        keys.append(key)
    return keys


def generate_messages():
    messages = []

    for i in range(50):
        message = hex(random.randrange(0, 18446744073709551615))
        messages.append(key)
    return messages


def get_info(file_name):
    '''
        opens the file and saves the lines in list.
        returns the the lines as seperate parameters with no newline character
    '''

    with open(file_name, "r") as file:
        lines = file.readlines()

    return int(lines[0].strip()), lines[1].strip(), lines[2].strip()


def hex_to_bin(hex_num, bin_len):
    '''
        converts a hex number into a binary list with size bin_len
    '''

    bin_num = "{0:08b}".format(int(hex_num, 16))

    # adds zero to begining of bin_num until the binary string is desired size
    while len(bin_num) != bin_len:
        bin_num = '0' + bin_num

    # converts binary string to list
    bin_arr = [int(bit) for bit in bin_num]

    return bin_arr


def dec_to_bin(dec_num, bin_len):
    '''
        converts decimal number into binary list of size bin_len
    '''

    bin_num = "{0:b}".format(int(dec_num))

    # adds zero to begining of bin_num until the binary string is desired size
    while len(bin_num) != bin_len:
        bin_num = '0' + bin_num

    # converts binary string to list
    bin_arr = [int(bit) for bit in bin_num]

    return bin_arr


def bin_to_hex(bin_list):
    '''
        converts binary list to hex number
    '''

    # converts binary list to binary string
    bin_num = ''.join([str(bit) for bit in bin_list])

    # converts binary string to decimal number, then hex number
    dec_num = int(bin_num, 2)
    hex_num = hex(dec_num)

    return hex_num


def bin_to_dec(bin_list):
    '''
        converts binary list to dec number
    '''

    # converts binary list to binary string
    bin_num = ''.join([str(bit) for bit in bin_list])

    # converts binary string to decimal number
    dec_num = int(bin_num, 2)

    return dec_num


def get_permuted_choice_1_key(bin_64_key):
    '''
        permutates 64 bit key into 56 bit key by moving
        all of the bits to the location given by the permutation
        table
    '''

    # permutation table given by DES
    permutation = [57, 49, 41, 33, 25, 17, 9,
                   1, 58, 50, 42, 34, 26, 18,
                   10, 2, 59, 51, 43, 35, 27,
                   19, 11, 3, 60, 52, 44, 36,
                   63, 55, 47, 39, 31, 23, 15,
                   7, 62, 54, 46, 38, 30, 22,
                   14, 6, 61, 53, 45, 37, 29,
                   21, 13, 5, 28, 20, 12, 4]

    # loops through all th values in the permutation table inserts the values
    # at the location given in the table into an empty list
    permuted_key = []
    for value in permutation:
        permuted_key.append(bin_64_key[value - 1])

    return permuted_key


def get_permuted_choice_2_key(bin_56_key):
    '''
        permutates 56 bit key into 48 bit key by moving
        all of the bits to the location given by the permutation
        table
    '''

    # permutation table given by DES
    permutation = [14, 17, 11, 24, 1, 5,
                   3, 28, 15, 6, 21, 10,
                   23, 19, 12, 4, 26, 8,
                   16, 7, 27, 20, 13, 2,
                   41, 52, 31, 37, 47, 55,
                   30, 40, 51, 45, 33, 48,
                   44, 49, 39, 56, 34, 53,
                   46, 42, 50, 36, 29, 32]

    # loops through all th values in the permutation table inserts the values
    # at the location given in the table into an empty list
    permuted_key = []
    for value in permutation:
        permuted_key.append(bin_56_key[value - 1])

    return permuted_key


def shift_key_left(bin_key, round_num):
    '''
        shifts the key left by amount given in table based on round
        DES is currently in
    '''

    # shift amount list given by DES
    shift_amounts = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    # shifts the key left by the amount given in table
    for round_idx in range(shift_amounts[round_num]):
        first_elem = bin_key.pop(0)
        bin_key.append(first_elem)

    return bin_key


def get_initial_permutation_list(message):
    '''
        permutates 64 bit message  by moving all of the bits to the
        location given by the permutation table
    '''

    # permutation table given by DES
    initial_permutation = [58, 50, 42, 34, 26, 18, 10, 2,
                           60, 52, 44, 36, 28, 20, 12, 4,
                           62, 54, 46, 38, 30, 22, 14, 6,
                           64, 56, 48, 40, 32, 24, 16, 8,
                           57, 49, 41, 33, 25, 17, 9, 1,
                           59, 51, 43, 35, 27, 19, 11, 3,
                           61, 53, 45, 37, 29, 21, 13, 5,
                           63, 55, 47, 39, 31, 23, 15, 7]

    # loops through all th values in the permutation table inserts the values
    # at the location given in the table into an empty list
    initial_permutation_message = []
    for value in initial_permutation:
        initial_permutation_message.append(message[value - 1])

    return initial_permutation_message


def get_expanded_message_list(initial_list):
    '''
        expands 32 bit message into 48 bit message by moving
        all of the bits to the location given by the permutation
        table
    '''

    # expansion table given by DES
    expansion = [32, 1, 2, 3, 4, 5,
                 4, 5, 6, 7, 8, 9,
                 8, 9, 10, 11, 12, 13,
                 12, 13, 14, 15, 16, 17,
                 16, 17, 18, 19, 20, 21,
                 20, 21, 22, 23, 24, 25,
                 24, 25, 26, 27, 28, 29,
                 28, 29, 30, 31, 32, 1]

    # loops through all th values in the permutation table inserts the values
    # at the location given in the table into an empty list
    expanded_list = []
    for value in expansion:
        expanded_list.append(initial_list[value - 1])

    return expanded_list


def xor_bin_lists(bin_key, message):
    '''
        xores the bin_key and message lists
    '''

    xored_list = []
    for idx in range(len(message)):
        xored_list.append(bin_key[idx] ^ message[idx])

    return xored_list


def get_substituted_message_list(initial_list):
    '''
        converts 48 bit message to 32 bit message by breaking the 48 bit
        message into 8 6 bit messages and using the n substitution table
        for n 6 bit message.
        the first and last bit of the message determines which row the
        conversion value is in, and the middle 4 bits determine which
        value in that row it uses
    '''

    # substitution tables given by DES
    substitutions = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
                      [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
                      [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
                      [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

                     [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
                      [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
                      [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
                      [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

                     [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
                      [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
                      [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
                      [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

                     [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
                      [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
                      [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
                      [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

                     [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
                      [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
                      [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
                      [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

                     [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
                      [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
                      [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
                      [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

                     [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
                      [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
                      [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
                      [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

                     [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
                      [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
                      [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
                      [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

    # splits the message list into 8 lists that are 6 bits long
    matrix = np.reshape(initial_list, (8, 6)).tolist()

    # keeps track of what block of the message the code is currently in
    block_idx = 0

    # calculates what value the given block in the message gets calculated to
    substituted_list = []
    for row in matrix:
        # mid_val is the middle 4 bits of the block
        mid_val = row[1:-1]

        # checks what row of the substitution table the value substituted is in
        # based of the first and last bits
        if row[0] == 0:
            if row[len(row) - 1] == 0:
                # appends value to new list based on middle bits using substitution table
                substituted_list.append(dec_to_bin(substitutions[block_idx][0][bin_to_dec(mid_val)], 4))
            else:
                # appends value to new list based on middle bits using substitution table
                substituted_list.append(dec_to_bin(substitutions[block_idx][1][bin_to_dec(mid_val)], 4))
        else:
            if row[len(row) - 1] == 0:
                # appends value to new list based on middle bits using substitution table
                substituted_list.append(dec_to_bin(substitutions[block_idx][2][bin_to_dec(mid_val)], 4))
            else:
                # appends value to new list based on middle bits using substitution table
                substituted_list.append(dec_to_bin(substitutions[block_idx][3][bin_to_dec(mid_val)], 4))

        block_idx += 1

    return sum(substituted_list, [])


def get_permutation_message_list(message):
    '''
        permutates 32 bit message by moving all of the bits to the
        location given by the permutation table
    '''

    # permutation table given by DES
    permutation = [16, 7, 20, 21, 29, 12, 28, 17,
                   1, 15, 23, 26, 5, 18, 31, 10,
                   2, 8, 24, 14, 32, 27, 3, 9,
                   19, 13, 30, 6, 22, 11, 4, 25]

    # loops through all th values in the permutation table inserts the values
    # at the location given in the table into an empty list
    permuted_list = []
    for value in permutation:
        permuted_list.append(message[value - 1])

    return permuted_list


def get_final_permutation_list(message):
    '''
        permutates 64 bit message by moving all of the bits to the
        location given by the permutation table
    '''

    final_permutation = [40, 8, 48, 16, 56, 24, 64, 32,
                         39, 7, 47, 15, 55, 23, 63, 31,
                         38, 6, 46, 14, 54, 22, 62, 30,
                         37, 5, 45, 13, 53, 21, 61, 29,
                         36, 4, 44, 12, 52, 20, 60, 28,
                         35, 3, 43, 11, 51, 19, 59, 27,
                         34, 2, 42, 10, 50, 18, 58, 26,
                         33, 1, 41, 9, 49, 17, 57, 25]

    # loops through all th values in the permutation table inserts the values
    # at the location given in the table into an empty list
    final_permutation_message = []
    for value in final_permutation:
        final_permutation_message.append(message[value - 1])

    return final_permutation_message


def print_bin(bin_arr):
    '''
        prints bin_list as binary string
    '''

    [print(bit, end="") for bit in bin_arr]
    print()


def des(num_rounds, key, message, false_funct, encryption):
    '''
        converts message in input file using DES
    '''

    bin_key = hex_to_bin(key, 64)
    message = hex_to_bin(message, 64)

    # applies initial permutation table to message
    if false_funct != "Initial Message Permutation":
        initial_permutation_message = get_initial_permutation_list(message)
    else:
        initial_permutation_message = message

    # applies permutation table 1 to key
    bin_56_key = get_permuted_choice_1_key(bin_key)
    bin_56_keys = []
    # splits message in two
    l_message = initial_permutation_message[0:len(initial_permutation_message) // 2]
    r_message = initial_permutation_message[len(initial_permutation_message) // 2:]

    # loops through DES for number of rounds specified in input file
    for key_round_number in range(num_rounds):
        # splits the key in half and shifts each half left by amount
        # given by DES based on what round number the code is on
        if false_funct != "Shift Key Left":
            bin_56_l_key = shift_key_left(bin_56_key[0:28], key_round_number)
            bin_56_r_key = shift_key_left(bin_56_key[28:56], key_round_number)
            bin_56_key = bin_56_l_key + bin_56_r_key
            bin_56_keys.append(bin_56_key)
        else:
            bin_56_keys.append(bin_56_key)

    if not encryption:
        bin_56_keys = bin_56_keys[::-1]

    for round_number in range(num_rounds):

        # makes a new list and copies the values of r_message into it
        temp_l_message = r_message[:]

        # applies expantion table to r_data
        r_message = get_expanded_message_list(r_message)

        # applies permutation table 2 to key
        bin_48_key = get_permuted_choice_2_key(bin_56_keys[round_number])

        # xores the key and message and saves result
        xored_expanded_message_list = xor_bin_lists(bin_48_key, r_message)

        # applies substitution tables to the sum of the key and message
        if false_funct != "Substituted Message":
            substituted_list = get_substituted_message_list(xored_expanded_message_list)
        else:
            substituted_list = xored_expanded_message_list

        # applies permutation table to substitution list
        if false_funct != "Permutation Message":
            permutated_list = get_permutation_message_list(substituted_list)
        else:
            permutated_list = substituted_list

        # saves the value of the sum of the left half of the message list and
        # the permutated list to the right half of the message
        temp_message = xor_bin_lists(l_message, permutated_list)

        # saves the value of the old right half of the message to the
        # left half of the message
        if false_funct != "Switching Message Halves":
            r_message = temp_message
            l_message = temp_l_message
        else:
            l_message = temp_message

    if false_funct != "Switching Message Halves":
        final_message = r_message + l_message
    else:
        final_message = l_message + r_message

    if false_funct != "Final Message Permutation":
        final_message = get_final_permutation_list(final_message)

    return final_message


def output_message(final_message, file_output, file_num):
    '''
        saves the results of the DES encryption to an output file
    '''

    with open(file_output + str(file_num), 'w') as output_file:
        output_file.write(bin_to_hex(final_message))

def arr_to_str(arr):
    str1 = ""
    for elem in arr:
        str1 += str(elem)
    return str1

if __name__ == "__main__":
    # output from generated input
    num_rounds = 16
    key = "0123456789abcdef"
    #key_1 = "0123456789abcdf0"
    num_encryptions = 10000
    functions = ["None", "Initial Message Permutation", "Shift Key Left", "Substituted Message",
                 "Permutation Message", "Switching Messsage Halves", "Final Message Permutation"]

    avg_changed_bits = []
    avg_times = []

    for funct_idx, funct in enumerate(functions):
        encryption_result_list = []
        bits_changed_list = []
        timer_res = []
        for idx in range(num_encryptions):
            message = hex(random.randrange(0, 18446744073709551615))
            message2 = hex(int(message, 16) + 1)

            encryption_list = []

            start = time.time()

            encryption_list.append(arr_to_str(des(num_rounds, key, message, funct, True)))

            end = time.time()

            timer_res.append(end - start)

            encryption_list.append(arr_to_str(des(num_rounds, key, message2, funct, True)))

            encryption_result_list.append(encryption_list)

        for encryption in encryption_result_list:
            xor_res = int(encryption[0], 2) ^ int(encryption[1], 2)
            xor_res = '{0:064b}'.format(xor_res)
            bits_changed_list.append(xor_res.count('1'))

        bit_changed_avg = 0
        for i in bits_changed_list:
            bit_changed_avg += i

        bit_changed_avg /= num_encryptions
        if funct == "None":
            print("avg bits changed: " + str(bit_changed_avg))
        else:
            print("avg bits changed w/o " + funct + ": " + str(bit_changed_avg))

        avg_changed_bits.append(bit_changed_avg)

        time_avg = 0
        for funct_time in timer_res:
            time_avg += funct_time
        time_avg /= num_encryptions

        avg_times.append(time_avg * (2**32) / 86400)
        #avg_times.append(time_avg * (2**23) / 86400)

    fig = plt.figure(figsize = (10, 10))

    plt.bar(functions, avg_changed_bits, color="blue", width = 0.4)

    plt.xlabel("Functions Removed")
    plt.ylabel("Average Number of Bits Changed By Changing One Bit In The Message")
    plt.title("Average Number of Bits Changed By Changing One Bit In The Message With Functions Removed")

    fig2 = plt.figure(figsize = (10, 10))
    plt.bar(functions, avg_times, color="blue", width = 0.4)

    plt.xlabel("Functions Removed")
    plt.ylabel("Average Time of Decryption (days)")
    plt.title("Average Time Taken By DES To Encode With Functions Removed")
    plt.show()

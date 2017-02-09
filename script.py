import numpy as np
import random
import re

G = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1]]
H_transposed = [[0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]

bit_switch = {'1': '0', '0': '1'}
int_switch = {1: 0, 0: 1}


def calculate_code_for_4bit_msg(four_bit_msg, g_matrix):
    bits_of_output = 7
    seven_bit_msg = []

    for i in range(bits_of_output):
        seven_bit_msg.append((np.dot(four_bit_msg, g_matrix[i]))%2)

    return seven_bit_msg


def send_one_line(line, p):
    result = ''
    for letter in line:
        if random.uniform(0, 1) < p:
            result += bit_switch[letter]
        else:
            result += letter

    return result


def message_list_to_code_list(input_file, output_file, g_matrix):
    with open(input_file, 'r') as f:
        data = f.read()

    input_message = data.split('\n')

    f = open(output_file, 'w')
    for line in input_message:
        f.write(re.sub('[], []', '', str(calculate_code_for_4bit_msg(map(int, list(line)), g_matrix))) + '\n')
    f.close()


def send_codes_through_channel(input_file, output_file, prob_of_bit_error):
    with open(input_file, 'r') as f:
        data = f.read()

    input_message = data.split('\n')

    f = open(output_file, 'w')
    for line in input_message:
        f.write(send_one_line(line, prob_of_bit_error) + '\n')
    f.close()


def decode_one_line(line, h_matrix):
    result = []
    parity_bits = 3
    for i in range(parity_bits):
        result.append(np.dot(h_matrix[i], line) % 2)
    return result


def decode(input_file, output_file, h_matrix):
    H = np.transpose(h_matrix)

    with open(input_file, 'r') as f:
        data = f.read()

    input_message = data.split('\n')

    decoded_message = []

    for line in input_message:
        if len(line) > 0:
            dot = decode_one_line(map(int, list(line)), H)
            if dot == [0, 0, 0]:
                decoded_message.append(line[:4])
            else:
                il = H_transposed.index(dot)
                temp_line = line[0:il] + bit_switch[line[il]] + line[il+1:]
                decoded_message.append(temp_line[:4])

    f = open(output_file, 'w')
    for line in decoded_message:
        f.write(line + '\n')
    f.close()


def compare_two_messages(input_file, output_file):
    with open(input_file, 'r') as f:
        input_data = f.read()

    with open(output_file, 'r') as f:
        output_data = f.read()

    input_lines = input_data.split('\n')
    output_lines = output_data.split('\n')

    length = len(input_lines)
    correct = 0
    for i in range(length):
        if input_lines[i] == output_lines[i]:
            correct += 1
    print('Correct: ' + str(correct) + ' of ' + str(length) + ' messages. (' + str((100.0*correct)/(1.0*length)) + '%)')


def main():
    probability_of_one_bit_error = 0
    message_list_to_code_list('input_msg.txt', 'codes_to_send.txt', G)
    send_codes_through_channel('codes_to_send.txt', 'codes_received.txt', probability_of_one_bit_error)
    decode('codes_received.txt', 'decoded_msg.txt', H_transposed)
    compare_two_messages('input_msg.txt', 'decoded_msg.txt')


if __name__ == '__main__':
    main()

import numpy as np

hMatrix = np.array([[1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                    [1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                    [0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                    [1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
                    [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
                    [0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0],
                    [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1]])


def flatten(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]


def ascii_to_bin_list(char):
    bin_list = [int(x) for x in list('{0:0b}'.format(ord(char)))]
    return [*[0] * (8 - len(bin_list)), *bin_list]


def string_to_bin_list(string):
    return [char for char in map(ascii_to_bin_list, string)]


def encode(string):
    return string_to_bin_list(string)


def decode(bits):
    # s = ""
    # for sublist in bits:
    #     s += chr(int(''.join(map(str, sublist[:8])), 2))
    # return s
    return ''.join([chr(int(''.join(map(str, sublist[:8])), 2)) for sublist in bits])


if __name__ == '__main__':
    x = [[0, 1, 1, 0, 0, 0, 0, 1], [0, 1, 1, 0, 0, 0, 1, 0], [0, 1, 1, 0, 0, 0, 1, 1]]
    print(decode(x))


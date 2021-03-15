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
    return flatten([char for char in map(ascii_to_bin_list, string)])


if __name__ == '__main__':
    print(string_to_bin_list('aaa'))
    print(len(string_to_bin_list('aaa')) / 8)


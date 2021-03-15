import numpy as np

hMatrix = np.array([[1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                    [1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                    [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                    [0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                    [1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
                    [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
                    [0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0],
                    [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1]])


def convert(msg):
   msgArray = bytearray(msg)
   msgLength = len(msgArray)
   encodedMsg = np.zeros((msgLength, 16))
   for x in range(msgLength):
       print('jestem glupia')


def flatten(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]


def ascii_to_bin_list(char):
    bin_list = [int(x) for x in list('{0:0b}'.format(ord(char)))]
    return [*[0] * (8 - len(bin_list)), *bin_list]


def check(vector):
    if len(vector) != len(hMatrix[0]):
        print('\nU cannot multiply the matrices')
        return None
    row = []
    checkingArray = [8]
    for i in range(8):
        row = hMatrix[i]
        sum = False
        for j in range(16):
            matrixElem = row[j] == 1
            vectorElem = vector[j] == 1
            sum ^= matrixElem & vectorElem
        if sum:
            checkingArray[i] = 1
        else:
            checkingArray[i] = 0
    return checkingArray


def checkpython(coded):
    checking_arr = []
    for block in coded:
        for vec in hMatrix:
            checking_arr.append(np.dot(np.array(block), vec) % 2)
    return checking_arr


def correct(rMatrix, index, encodedMsg):
    temp = [8]
    for i in range(16):
        j = i + 1
        for j in range(16):
            for k in range(8):
                temp[k] = hMatrix[k][i] ^ hMatrix[k][j]
            if temp == rMatrix:
                encodedMsg[index][i] ^= 1
                encodedMsg[index][j] ^= 1
                return 2
    for i in range(16):
        for j in range(8):
            temp[j] = hMatrix[j][i]
        if temp == rMatrix:
            encodedMsg[index][i] ^= 1
            return 1
    return 0


def string_to_bin_list(string): #to jest w zasadzie prepare
    return [char for char in map(ascii_to_bin_list, string)]


def encode(string):
    before_encoding = string_to_bin_list(string)
    copy = string_to_bin_list(string)
    for iterator, sublist in enumerate(before_encoding):
        for i in range(8):
            parity = np.dot(np.array(sublist), hMatrix[i][:8])
            copy[iterator].append(parity % 2)
    return copy


def decode(bits):
    return ''.join([chr(int(''.join(map(str, sublist[:8])), 2)) for sublist in bits])


if __name__ == '__main__':
    message = "blackpink"
    converted = string_to_bin_list(message)
    encoded = encode(message)
    decoded = decode(encoded)
    print(message)
    print(converted)
    print(encoded)
    print(decoded)
    print(checkpython(encoded))


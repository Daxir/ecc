import numpy as np
import os
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor, QIcon
from bitstring import ConstBitStream

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


def string_to_bin_list(string): #to jest w zasadzie prepare tak naprawde to nie
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


def write_bytes_file(binary_arrays, filename):
    file = open(filename, "wb")
    buffer = "0b"
    for sub in binary_arrays:
        buffer += ''.join([str(char) for char in sub])
    file.write(ConstBitStream(buffer).bytes)
    file.close()


def write_bits_file(binary_arrays, filename):
    file = open(filename, "w")
    for sub in binary_arrays:
        file.write(''.join([str(char) for char in sub]) + " ")
    file.close()


# Gui zone:
widgets = {
    "logo": [],
    "button": []
}

names = ["step1.txt", "step2.txt", "step3.txt", "step4.txt"]
file_openers = [lambda name=name: os.startfile(name) for name in names]


def set_files():
    for filename in names:
        file = open(filename, "w")
        file.close()


def clear_files():
    for filename in names:
        os.remove(filename)


def clear_widgets():
    for widget in widgets:
        if widgets[widget]:
            widgets[widget][-1].hide()
        for i in range(0, len(widgets[widget])):
            widgets[widget].pop()


def frame1(grid):
    logo = QLabel()
    logo.setPixmap(QPixmap("logo.png").scaled(357, 85))
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top: 1px;")
    widgets["logo"].append(logo)

    button = QPushButton("In your area!")
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setStyleSheet(
        '''
        *{
            border: 4px solid '#f5a7bc';
            font-size: 15px;
            color: 'white';
            padding: 5px 0;
            margin: 12px 100px;
        }
        *:hover{
            background: '#f5a7bc';
        }
        '''
    )

    button.clicked.connect(lambda: file_openers[0]())
    widgets["button"].append(button)

    grid.addWidget(widgets["logo"][-1], 0, 0, 1, 2)
    grid.addWidget(widgets["button"][-1], 1, 0, 1, 2)


class Root(QWidget):
    def __init__(self):
        super().__init__()
        set_files()
        self.setWindowTitle("Monika Dyczka, Mateusz Roszkowski")
        self.setFixedWidth(400)
        self.setStyleSheet("background: #1a1918;")
        self.setWindowIcon(QIcon("lisa.png"))

    def closeEvent(self, event):
        # clear_files()
        return


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
    # os.startfile("gui.txt")

    # app = QApplication(sys.argv)
    # window = Root()
    # grid = QGridLayout()
    # frame1(grid)
    #
    # window.setLayout(grid)
    # window.show()
    # sys.exit(app.exec())

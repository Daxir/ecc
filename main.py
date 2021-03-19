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
    return np.array([checking_arr[i:i + 8] for i in range(0, len(checking_arr), 8)])


def correct(rMatrix, index, encodedMsg):
    temp = [None]*8
    for i in range(16):
        for j in range(i+1, 16):
            for k in range(8):
                temp[k] = hMatrix[k][i] ^ hMatrix[k][j]
            if temp == rMatrix.tolist():
                encodedMsg[index][i] ^= 1
                encodedMsg[index][j] ^= 1
                return 2
    for i in range(16):
        for j in range(8):
            temp[j] = hMatrix[j][i]
        if temp == rMatrix.tolist():
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
    print("Bits", bits)
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

def funfun(encodedMsg):
    checkarray = checkpython(encodedMsg)
    errors = 0
    for i in range(len(encodedMsg)):
        if np.sum(checkarray[i]) > 0:
            errors += correct(checkarray[i], i, encodedMsg)
    print(errors)

# Gui zone:
widgets = {
    "logo": [],
    "button": [],
    "next": []
}

names = ["step1.txt", "step2.txt", "step3.txt", "step4.txt"]
file_openers = [lambda name=name: os.startfile(name) for name in names]


def stage2():
    clear_widgets()


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


def create_button(text, l_margin, r_margin):
    button = QPushButton(text)
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    # button.setFixedWidth(150)
    button.setStyleSheet(
        "*{margin-left: " + str(l_margin) + "px;" +
        "margin-right: " + str(r_margin) + "px;" +
        '''
            border: 4px solid '#f5a7bc';
            font-size: 15px;
            color: '#f5a7bc';
            padding: 5px 10px;
        }
        *:hover{
            background: '#f5a7bc';
            color: '#1a1918';
        }
        '''
    )
    return button


def frame1(grid):
    logo = QLabel()
    logo.setPixmap(QPixmap("logo.png").scaled(357, 85))
    # logo.setText("Krok 1: Otwórz plik i wpisz do niego wiadomość")
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet(
        '''
        font-size: 15px;
        color: 'white';
        margin-bottom: 3px; 
        '''
    )
    widgets["logo"].append(logo)

    button = create_button("Otwórz plik", 10, 10)
    button2 = create_button("Dalej", 10, 10)

    # button = QPushButton("Open file")
    # button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    # button.setStyleSheet(
    #     '''
    #     *{
    #         border: 4px solid '#f5a7bc';
    #         font-size: 15px;
    #         color: 'white';
    #         padding: 5px 0;
    #         margin: 12px 100px;
    #     }
    #     *:hover{
    #         background: '#f5a7bc';
    #     }
    #     '''
    # )

    button.clicked.connect(lambda: file_openers[0]())
    button2.clicked.connect(stage2)
    widgets["button"].append(button)
    widgets["next"].append(button2)

    grid.addWidget(widgets["logo"][-1], 0, 0, 1, 2)
    grid.addWidget(widgets["button"][-1], 1, 0)
    grid.addWidget(widgets["next"][-1], 1, 1)

def frame2():
    logo = QLabel()
    logo.setPixmap(QPixmap("logo.png").scaled(357, 85))
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top: 1px;")
    widgets["logo"].append(logo)
    button = create_button("Open file", 10, 10)
    button2 = create_button("Next", 10, 10)
    button.clicked.connect(lambda: file_openers[1]())
    button2.clicked.connect(stage2)
    widgets["button"].append(button)
    widgets["next"].append(button2)

    grid.addWidget(widgets["logo"][-1], 0, 0, 1, 2)
    grid.addWidget(widgets["button"][-1], 1, 0)
    grid.addWidget(widgets["next"][-1], 1, 1)


class Root(QWidget):
    def __init__(self):
        super().__init__()
        set_files()
        self.setWindowTitle("Monika Dyczka, Mateusz Roszkowski")
        self.setFixedWidth(400)
        self.setStyleSheet("background: #1a1918;")
        self.setWindowIcon(QIcon("lisa.png"))

    def closeEvent(self, event):
        clear_files()
        return


if __name__ == '__main__':
    message = "blackpink"
    converted = string_to_bin_list(message)
    encoded = encode(message)

    print(message)
    print(converted)
    print(encoded)
    encoded[0][0] = 1
    encoded[5][6] = 1
    encoded[7][8] = 1
    encoded[7][9] = 0
    print(encoded)
    print(funfun(encoded))
    decoded = decode(encoded)
    print(decoded)
    print(encoded)


    # os.startfile("gui.txt")

    # app = QApplication(sys.argv)
    # window = Root()
    # grid = QGridLayout()
    # frame1(grid)
    #
    # window.setLayout(grid)
    # window.show()
    # sys.exit(app.exec())

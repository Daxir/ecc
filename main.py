import numpy as np
import os
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QGridLayout
from PyQt5 import QtCore
from PyQt5.QtGui import QCursor, QIcon
from bitstring import ConstBitStream


hMatrix = np.array([[1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                    [1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
                    [1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]])


# zamienia znak w tablicę binarną, dodaje padding zerami z lewej strony, żeby każdy znak był ośmiobitowy
def ascii_to_bin_list(char):
    bin_list = [int(x) for x in list('{0:0b}'.format(ord(char)))]
    return [*[0] * (8 - len(bin_list)), *bin_list]


# tworzy listę wektorów sprawdzających i zwraca je jako listę list binarnych
def check(coded):
    checking_arr = []
    for block in coded:  # dla każdego bloku zakodowanej wiadomości
        for vec in hMatrix:  # pobieramy wiersz z macierzy
            checking_arr.append(np.dot(np.array(block), vec) % 2)  # i tworzymy wektor sprawdzający sumą modulo 2
    return np.array([checking_arr[i:i + 8] for i in range(0, len(checking_arr), 8)])  # dzielimy na części


def correct(r_matrix, index, encoded_msg):
    temp = [None]*8
    for i in range(16):
        for j in range(i+1, 16):
            for k in range(8):
                temp[k] = hMatrix[k][i] ^ hMatrix[k][j]
            if temp == r_matrix.tolist():
                encoded_msg[index][i] ^= 1
                encoded_msg[index][j] ^= 1
                return 2
    for i in range(16):
        for j in range(8):
            temp[j] = hMatrix[j][i]
        if temp == r_matrix.tolist():
            encoded_msg[index][i] ^= 1
            return 1
    return 0


# zamienia stringa w listę list binarnych dla każdego znaku
def string_to_bin_list(string):
    return [char for char in map(ascii_to_bin_list, string)]


# dodaje bity parzystości do wiadomości i zwraca jako tablicę tablic binarnych
# (dla wiadomosci 8 bitowej, 8 bitów parzystości)
def encode(string):
    before_encoding = string_to_bin_list(string)  # zamiana na bity
    copy = string_to_bin_list(string)
    for iterator, sublist in enumerate(before_encoding):  # przechodzimy po bitach wiadomosci
        for i in range(8):  # i po wierszach macierzy
            parity = np.dot(np.array(sublist), hMatrix[i][:8])
            copy[iterator].append(parity % 2)  # obliczyamy sumę modulo 2
    return copy


# przyjmuje tablicę tablic binarnych i zamienia je na string z wiadomością
def decode(bits):
    return ''.join([chr(int(''.join(map(str, sublist[:8])), 2)) for sublist in bits])


# zapisuje listę list binarnych do pliku jako bajty
def write_bytes_file(binary_arrays, filename):
    file = open(filename, "wb")
    buffer = "0b"
    for sub in binary_arrays:
        buffer += ''.join([str(char) for char in sub])
    file.write(ConstBitStream(buffer).bytes)
    file.close()


# zapisuje listę list binarnych do pliku jako bity
def write_bits_file(binary_arrays, filename):
    file = open(filename, "w")
    for sub in binary_arrays:
        file.write(''.join([str(char) for char in sub]) + " ")
    file.close()


# odczytuje bajty z pliku
def read_bytes_file(filename):
    file = open(filename, "r")
    mess = file.read()
    file.close()
    return mess


# odczytuje string binarny z pliku
def read_bits_file(filename):
    file = open(filename, "r")
    mess = file.read()
    mess = mess.rstrip()
    file.close()
    return list(map(lambda x: [int(c) for c in x], mess.split(sep=' ')))


def correct_err(encoded_msg):
    checkarray = check(encoded_msg)
    errors = 0
    for i in range(len(encoded_msg)):
        if np.sum(checkarray[i]) > 0:
            errors += correct(checkarray[i], i, encoded_msg)
    return errors


# Gui zone:
widgets = {
    "logo": [],
    "button": [],
    "next": []
}

names = ["step1.txt", "step2.txt", "step3.txt", "step4.txt", "step5.txt"]
texts = ["Krok 1: Otwórz plik i wpisz do niego wiadomość",
         "Krok 2: W pliku znajdują się zakodowane bajty (rozmiar uległ podwojeniu)",
         "Krok 3: W pliku znajdują się zakodowane bity, wprowadź błędy",
         "Krok 4: W pliku znajdują się poprawione odkodowane bity (naprawiono ",
         "Krok 5: W pliku znajdują się poprawione odkodowane bajty, identyczne jak pierwotna wiadomość"]
file_openers = [lambda name=name: os.startfile(name) for name in names]
messages = {
    "plaintext": "",
    "encoded": [],
    "corrected": [],
    "decoded": ""
}


def operate(index):
    if index == 1:
        messages["plaintext"] = read_bytes_file(names[index - 1])
        messages["encoded"] = encode(messages["plaintext"])
        write_bytes_file(messages["encoded"], names[index])
    elif index == 2:
        write_bits_file(messages["encoded"], names[index])
    elif index == 3:
        messages["encoded"] = read_bits_file(names[index - 1])
        messages["corrected"] = messages["encoded"]
        texts[index] += str(correct_err(messages["corrected"])) + ")"
        write_bits_file(messages["corrected"], names[index])
    elif index == 4:
        messages["decoded"] = decode(messages["corrected"])
        file = open(names[index], "w")
        file.write(messages["decoded"])
        file.close()
    else:
        return


def stage(index):
    operate(index)
    clear_widgets()
    frame(texts[index], index)


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


def frame(text, index):
    logo = QLabel()
    logo.setText(text)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setWordWrap(True)
    logo.setStyleSheet(
        '''
        font-size: 15px;
        color: '#f5a7bc';
        margin-bottom: 3px; 
        '''
    )
    widgets["logo"].append(logo)

    button = create_button("Otwórz plik", 10, 10)
    button.clicked.connect(lambda: file_openers[index]())
    if index != 4:
        button2 = create_button("Dalej", 10, 10)
        button2.clicked.connect(lambda: stage(index + 1))
    else:
        button2 = create_button("Zakończ", 10, 10)
        button2.clicked.connect(lambda: window.close())

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
    app = QApplication(sys.argv)
    window = Root()
    grid = QGridLayout()
    stage(0)
    window.setLayout(grid)
    window.show()
    sys.exit(app.exec())

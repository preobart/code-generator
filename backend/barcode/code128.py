import sys

sys.path.append('/Users/admin/Workspace/code_generator/backend')

from tables.code128_symbol_table import *


class CODE128:
    def __init__(self, data):
        self.data = data
        self.alphabet = None

    def get_code_dict(self):
        lines = CODE128_CHART.strip().split('\n')
        code_A = {}
        code_B = {}
        code_C = {}
        values = {}
        symbols = {}

        for line in lines:
            parts = line.split()
            index = parts[0]

            char_A = parts[2]
            char_B = parts[3]
            char_C = parts[4]

            if index == '0':
                char_A = " "
                char_B = " "
                char_C = " "

            code = parts[7]

            symbols[index] = code
            values[code] = index

            code_A[char_A] = code
            code_B[char_B] = code
            code_C[char_C] = code

        return code_A, code_B, code_C, values, symbols

    def data_encoding(self):
        def get_summ():
            s = int(values[text[:11]])
            for i in range(len(text)//11):
                s += int(values[text[i*11:(i+1)*11]]) * i
            return s % 103

        def change_alphabet(item, text):
            if item in codeB:
                text += codeB['StartCodeB'] + codeB[item]
                self.alphabet = codeB
            elif item in codeA:
                text += codeA['StartCodeA'] + codeA[item]
                self.alphabet = codeA
            else:
                text += codeC['StartCodeC'] + codeC[item]
                self.alphabet = codeC
            return text

        codeA, codeB, codeC, values, symbols = self.get_code_dict()

        text = ''
        for item in self.data:
            if not self.alphabet:
                text = change_alphabet(item, text)
                continue
            text += self.alphabet[item]

        text += symbols[str(get_summ())]
        text += codeB['Stop']

        return text
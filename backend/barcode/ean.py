import sys

sys.path.append('/Users/admin/Workspace/code_generator/backend')

from tables.ean_symbol_tables import *


class EAN:
    def __init__(self, data):
        self.data = data
        self.length = len(self.data)

    def get_code(self, code, item):
        match code:
            case 'L':
                return encoding_table_L[int(item)]
            case 'G':
                return encoding_table_G[int(item)]
            case 'R':
                return encoding_table_R[int(item)]

    def data_encoding(self):
        data = ''
        control_chr = 0
        if self.length == 12:
            code_line = first_char_code[int(self.data[0])] + 'RRRRRR'
        else:
            code_line = 'LLLLRRRR'
            control_chr = 1

        for i in range(1-control_chr, self.length):
            data += self.get_code(code_line[i-1+control_chr], self.data[i])
            if i == self.length // 2:
                data = '101' + data + '01010'
            if i == self.length - 1:
                data += self.get_code('R', self.get_control_chr())
        data += '101'
        return data

    def get_control_chr(self):
        control_chr = (10 - (sum([int(self.data[i]) for i in range(1, self.length, 2)]) * 3 + sum(
            [int(self.data[i]) for i in range(0, self.length, 2)])) % 10) % 10
        if self.length == 7:
            control_chr = (10 - (sum([int(self.data[i]) for i in range(0, self.length, 2)]) * 3 + sum(
                [int(self.data[i]) for i in range(1, self.length, 2)])) % 10) % 10

        return control_chr


import unittest

import sys
sys.path.append('/Users/admin/Workspace/code_generators/backend')

from barcode.code128 import *
from barcode.ean import *

class TestEanFunctions(unittest.TestCase):

    code1 = EAN('123456789111')
    code2 = EAN('000000000000')
    code3 = EAN('1234567')
    code4 = EAN('0000000')

    def test_get_control_chr_func(self):
        self.assertEqual(self.code1.get_control_chr(), 8)
        self.assertEqual(self.code2.get_control_chr(), 0)
        self.assertEqual(self.code3.get_control_chr(), 0)
        self.assertEqual(self.code4.get_control_chr(), 0)


    def test_data_encoding_func(self):
        self.assertEqual(self.code1.data_encoding(), '10100100110111101001110101100010000101001000101010100100011101001100110110011011001101001000101')
        self.assertEqual(self.code2.data_encoding(), '10100011010001101000110100011010001101000110101010111001011100101110010111001011100101110010101')
        self.assertEqual(self.code3.data_encoding(), '1010011001001001101111010100011010101001110101000010001001110010101')
        self.assertEqual(self.code4.data_encoding(), '1010001101000110100011010001101010101110010111001011100101110010101')


class TestCode128Functions(unittest.TestCase):

    code1 = CODE128('Hello world!')
    code2 = CODE128('Itmo')
    code3 = CODE128('!-+=')

    def test_get_code_dict_func(self):
        self.assertEqual(len(self.code1.get_code_dict()[1]), 107)
        self.assertEqual(len(self.code1.get_code_dict()[2]), 107)
        self.assertEqual(len(self.code1.get_code_dict()[3]), 107)
        self.assertEqual(len(self.code1.get_code_dict()[4]), 107)
        self.assertEqual(len(self.code1.get_code_dict()[0]), 107)

    def test_data_encoding_func(self):
        self.assertEqual(self.code1.data_encoding(), '110100100001100010100010110010000110010100001100101000010001111010110110011001111001010010001111010100100111101100101000010000100110110011011001000011010011000111010')
        self.assertEqual(self.code2.data_encoding(), '11010010000110001000101001111010011110111010100011110101011000100011000111010')
        self.assertEqual(self.code3.data_encoding(), '11010010000110011011001001101110011000100100111001100101000011001011000111010')


if __name__ == '__main__':
    unittest.main()
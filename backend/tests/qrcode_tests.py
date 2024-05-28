import unittest

import sys
sys.path.append('/Users/admin/Workspace/code_generator/backend')

from qrcode.data_encoding import *
from qrcode.show_barcode import *
from tables.qrcode_correction_levels import *
from tables.qrcode_matrix_templates import *
from tables.qrcode_encoding_fields import *

class TestDataFunctions(unittest.TestCase):
    def test_data_input(self):
        self.assertEqual(get_data_analysis("1234567890"), '0001')
        self.assertEqual(get_data_analysis("HELLO123"), '0010')
        self.assertEqual(get_data_analysis("Hello, world!"), '0100')
        self.assertEqual(get_data_analysis("!_*&#$%&*())###%#^@%#"), '0100')

    def test_version_calculation(self):
        self.assertEqual(get_min_data_version(100, '0001', capacity_data_L), 3)
        self.assertEqual(get_min_data_version(200, '0010', capacity_data_M), 8)
        self.assertEqual(get_min_data_version(300, '0100', capacity_data_H), 18)
        self.assertEqual(get_min_data_version(400, '0001', capacity_data_Q), 11)

    def test_service_fields(self):
        self.assertEqual(get_adding_service_fields(100, '0001', 1), '00010001100100')
        self.assertEqual(get_adding_service_fields(200, '0010', 2), '0010011001000')
        self.assertEqual(get_adding_service_fields(300, '0100', 3), '0100100101100')
        self.assertEqual(get_adding_service_fields(400, '0001', 4), '00010110010000')


class TestConversion(unittest.TestCase):
    def test_conversion(self):
        self.assertEqual(bin_conversion("0000000000"), '0000000000000000000000000000000000')
        self.assertEqual(bin_conversion("1234567890"), '0001111011011100100011000101010000')

        self.assertEqual(alphanum_conversion("HELLO123"), '01100001011011110001101000011100100001011101')
        self.assertEqual(alphanum_conversion('-+*'), '11101011101100111')

        self.assertEqual(byte_conversion("Hello, world!"), '01001000011001010110110001101100011011110010110000100000011101110110111101110010011011000110010000100001')
        self.assertEqual(byte_conversion('Привет, мир!'), '110100001001111111010001100000001101000010111000110100001011001011010000101101011101000110000010001011000010000011010000101111001101000010111000110100011000000000100001')
    
    def test_bin_to_decimal(self):
        self.assertEqual(bin_to_decimal('100101010101101010'), [149, 90, 2])
        self.assertEqual(bin_to_decimal('1111010101010101010101'), [245, 85, 21])
        self.assertEqual(bin_to_decimal('101010110101010'), [171, 42])

class TestBlockFunctions(unittest.TestCase):
    def test_blocks_filling(self):
        self.assertEqual(filling_blocks('10010010', 'L', 1), [[146]])
        self.assertEqual(filling_blocks('1101010101011001', 'M', 2), [[213, 89]])
        self.assertEqual(filling_blocks('100101111011101011011111', 'Q', 3), [[151, 186, 223], []])
        self.assertEqual(filling_blocks('10101010111111010000001111000001', 'H', 4), [[170, 253, 3, 193], [], [], []])

    def test_correction_blocks_creation(self):
        self.assertEqual(creating_correction_blocks([[146]], 'L', 1), [[44, 204, 238, 35, 79, 1, 241]])
        self.assertEqual(creating_correction_blocks([[213, 89]], 'M', 2), [[101, 142, 33, 19, 140, 207, 101, 234, 54, 228, 29, 189, 154, 171, 255, 37]])
        self.assertEqual(creating_correction_blocks([[151, 186, 223], []], 'Q', 3), [[203, 153, 253, 109, 122, 81, 252, 89, 88, 175, 186, 49, 104, 107, 232, 37, 41, 37], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        self.assertEqual(creating_correction_blocks([[170, 253, 3, 193], [], [], []], 'H', 4), [[110, 184, 204, 135, 62, 214, 220, 114, 27, 205, 28, 227, 115, 185, 64, 237], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

class TestEncoding(unittest.TestCase):
    def test_data_encoding(self):
         self.assertEqual(data_encoding('Hello world', 'M'), ('0100000010110100100001100101011011000110110001101111001000000111011101101111011100100110110001100100000000001110110000010001111001001100010110100010100001110001001011011000110010011001011110111011111010010011', 1))
         self.assertEqual(data_encoding('Привет, мир', 'Q'), ('01000001010011010000100111111101000110000000110100001011100011010000101100101101000010110101110100011000001000101100001000001101000010111100110100001011100011010001100000000000111101010111101100011011111101110000100100110111000000010101101001111001010110110100010010000100010011100001011101101010010110001111010110001111101110000110011001111011111001110000000', 2))
   
    def test_get_finale_message(self):
         self.assertEqual(get_finale_message([[213, 89]], [[101, 142, 33, 19, 140, 207, 101, 234, 54, 228, 29, 189, 154, 171, 255, 37]], 2), '1101010101011001011001011000111000100001000100111000110011001111011001011110101000110110111001000001110110111101100110101010101111111111001001010000000')
         self.assertEqual(get_finale_message([[146]], [[44, 204, 238, 35, 79, 1, 241]], 1), '1001001000101100110011001110111000100011010011110000000111110001')

if __name__ == '__main__':
    unittest.main()
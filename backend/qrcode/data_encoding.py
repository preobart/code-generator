import re
import sys
sys.path.append('/Users/admin/Workspace/code_generator/backend')

from tables.qrcode_matrix_templates import *
from tables.qrcode_correction_levels import *

from tables.qrcode_encoding_fields import *

'''Выбор способа шифрования'''

def get_data_analysis(data):
    if data.isdigit():
        return '0001'
    if isalnum(data):
        return '0010'
    else:
        return '0100'

'''Добавление получение уровня коррекции'''

def get_correction_level(level):
    match level:
        case 'L':
            return capacity_data_L
        case 'M':
            return capacity_data_M
        case 'Q':
            return capacity_data_Q
        case 'H':
            return capacity_data_H

'''Анализ данных и определение версии'''

def get_min_data_version(length, method, level):
    match method:
        case '0001':
            for version in level:
                if version[1] >= length:
                    return version[0]
        case '0010':
            for version in level:
                if version[2] >= length:
                    return version[0]
        case '0100':
            for version in level:
                if version[3] >= length:
                    return version[0]

'''Добавление служебных полей - метода кодирования и индикатора длины поля'''

def get_adding_service_fields(length, method, version):
    for field in data_quantity_field:
        if version <= field[0]:
            match method:
                case '0001':
                    return '0001' + '0' * (field[1] - len(format(length, 'b'))) + format(length, 'b')
                case '0010':
                    return '0010' + '0' * (field[2] - len(format(length, 'b'))) + format(length, 'b')
                case '0100':
                    return '0100' + '0' * (field[3] - len(format(length, 'b'))) + format(length, 'b')


def bin_conversion(data):
    bin_data = ''
    for i in range(0, len(data), 3):
        if len(data[i:i + 3]) == 3:
            zeros = '0' * (10 - len(format(int(data[i:i + 3]), 'b')))
        elif len(data[i:i + 3]) == 2:
            zeros = '0' * (7 - len(format(int(data[i:i + 3]), 'b')))
        else:
            zeros = '0' * (4 - len(format(int(data[i:i + 3]), 'b')))
        bin_data += zeros + format(int(data[i:i + 3]), 'b')
    return bin_data


def alphanum_conversion(data):
    alphanum_data = ''
    for i in range(0, len(data), 2):
        if len(data[i:i + 2]) == 2:
            number = str(bin_value[data[i]] * 45 + bin_value[data[i + 1]])
            alphanum_data += '0' * (11 - len(format(int(number), 'b'))) + format(int(number), 'b')
        else:
            number = str(bin_value[data[i]])
            alphanum_data += bin_conversion(number)[1:]
    return alphanum_data


def byte_conversion(data):
    byte_string = data.encode('utf8')

    binary_strings = []
    for byte in byte_string:
        binary_string = format(byte, '08b')
        binary_strings.append(binary_string)

    return ''.join(binary_strings)

def isalnum(data):
    if re.match(r'^[-+*A-Z0-9$%./: ]+$', data):
        return True
    return False

'''Разбиение байтовой строки на блоки'''

def filling_blocks(byte_string, level, version):
    blocks = []
    byte_in_block = info_capacity[level][version] // (8 * amount_of_block[level][version])
    remainder = (info_capacity[level][version] // 8) % byte_in_block
    start = 0
    end = start + (byte_in_block * 8)
    for i in range(1, amount_of_block[level][version] + 1):
        if i >= amount_of_block[level][version] - remainder:
            blocks.append(bin_to_decimal(byte_string[start:end]))
            start = end
            end = start + (byte_in_block + 1) * 8
        else:
            blocks.append(bin_to_decimal(byte_string[start:end]))
            start = end
            end = start + (byte_in_block * 8)
    return blocks

'''Алгоритм создания байтов коррекции'''

def creating_correction_blocks(blocks, level, version):
    bytes = []
    for block in blocks:
        length = len(block)
        arr = block + [0] * (max(correction_bytes[level][version], length) - length)
        polynomials = generating_polynomials[correction_bytes[level][version]]
        for _ in range(length):
            element = arr[0]
            arr = arr[1:] + [0]
            if element:
                for j in range(correction_bytes[level][version]):
                    arr[j] = galua_field[(polynomials[j] + reversed_galua_field[element]) % 255] ^ arr[j]
        bytes.append(arr[:correction_bytes[level][version]])
    return bytes


def bin_to_decimal(byte_string):
    bytes = []
    for i in range(0, len(byte_string), 8):
        byte = byte_string[i:i + 8]
        bytes.append(int(byte, 2))
    return bytes

'''Получение итогового сообщения'''

def get_finale_message(blocks, correction_blocks, version):
    max_data_length = max(len(block) for block in blocks)
    max_correction_length = max(len(block) for block in correction_blocks)

    byte_string = ''
    correction_byte_string = ''

    for i in range(max(max_data_length, max_correction_length)):
        for block in blocks:
            if i < len(block):
                byte_string += format(block[i], '08b')

        for block in correction_blocks:
            if i < len(block):
                correction_byte_string += format(block[i], '08b')
    return byte_string + correction_byte_string + '0' * remainder_bits[version]

'''Перевод в строку байтов вместе со служебными полями и байтами четности'''

def data_encoding(data, level):
    byte_string = ''
    parity_bit = 0
    method = get_data_analysis(data)

    match method:
        case '0001':
            byte_string = bin_conversion(data)
        case '0010':
            byte_string = alphanum_conversion(data)
        case '0100':
            byte_string = byte_conversion(data)


    version = get_min_data_version(len(byte_string) // 8, method, get_correction_level(level))
    service_fields = get_adding_service_fields(len(byte_string) // 8, method, version)

    byte_string = service_fields + byte_string + '0' * (8 - len(byte_string) % 8)

    while len(byte_string) < info_capacity[level][version]:
        if parity_bit % 2 == 0:
            byte_string += '11101100'
            parity_bit += 1
        else:
            byte_string += '00010001'
            parity_bit += 1

    blocks = filling_blocks(byte_string, level, version)
    correction_blocks = creating_correction_blocks(blocks, level, version)

    return get_finale_message(blocks, correction_blocks, version), version
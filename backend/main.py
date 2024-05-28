from flask import abort
from qrcode.data_encoding import *
from qrcode.show_barcode import *
from barcode.ean import EAN
from barcode.code128 import CODE128


def create_qrcode(level, text):
    method = get_data_analysis(text)
    flag = False

    match level:
        case 'L':
            match method:
                case '0001':
                    if 0 < len(text) < 7089:
                        flag = True
                case '0010':
                    if 0 < len(text) < 4296:
                        flag = True
                case '0100':
                    if 0 < len(text) < 2953:
                        flag = True
        case 'M':
            match method:
                case '0001':
                    if 0 < len(text) < 5596:
                        flag = True
                case '0010':
                    if 0 < len(text) < 3391:
                        flag = True
                case '0100':
                    if 0 < len(text) < 2331:
                        flag = True
        case 'Q':
            match method:
                case '0001':
                    if 0 < len(text) < 3993:
                        flag = True
                case '0010':
                    if 0 < len(text) < 2420:
                        flag = True
                case '0100':
                    if 0 < len(text) < 1663:
                        flag = True
        case 'H':
            match method:
                case '0001':
                    if 0 < len(text) < 3057:
                        flag = True
                case '0010':
                    if 0 < len(text) < 1852:
                        flag = True
                case '0100':
                    if 0 < len(text) < 1273:
                        flag = True

    if flag:
        data, version = data_encoding(text, level)
        qrcode = Qr_code(level, version, data)
        qrcode.print_finder_module()
        qrcode.print_alignment_module()
        qrcode.print_temporary_pattern()
        qrcode.reserve_place()
        qrcode.selecting_a_mask()
        qrcode.filling_the_format_string(qrcode.matrix, qrcode.mask)
        return qrcode.matrix
    return abort(400)


def create_barcode(type, text):
    if text.isdigit() and ((type == 'ean13' and len(text) == 12) or (type == 'ean8' and len(text) == 7)):
        barcode = EAN(text)
    elif text.isascii() and type == 'code128' and 0 < len(text) < 71:
        barcode = CODE128(text)
    else:
        return abort(400)
    return barcode.data_encoding()
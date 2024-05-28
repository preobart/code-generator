import sys
sys.path.append('/Users/admin/Workspace/code_generator/backend')

import copy
import math
from tables.qrcode_matrix_templates import *
from itertools import product
from tables.qrcode_encoding_fields import *

class Qr_code():
    def __init__(self, level, version, finale_message):
        self.version = version
        self.level = level
        self.side = ((self.version - 1) * 4) + 21
        self.matrix = [[-1] * self.side for _ in range(self.side)]
        self.finale_message = finale_message
        self.mask = ''


    def is_empty(self, element):
        return element == -1

    '''Добавление шаблонов поиска'''

    def print_finder_module(self):
        # Индексы левого верхнего, левого нижнего, правого верхнего поискового узора
        index = [(0, 0), (self.side - 7, 0), (0, self.side - 7)]
        for i in range(7):

            # Устанавливаем разделители для поисковых узоров (все кроме угловых модулей)
            self.matrix[i][7], self.matrix[7][i] = 0, 0
            self.matrix[-i - 1][7], self.matrix[7][-i - 1] = 0, 0
            self.matrix[i][-8], self.matrix[-8][i] = 0, 0
            for j in range(7):
                for k in index:
                    self.matrix[i + k[0]][j + k[1]] = finder_pattern[i][j]

            # Устанавливаем разделители для углового модуля
            self.matrix[7][7], self.matrix[-8][7], self.matrix[7][-8] = 0, 0, 0

    '''Добавление выравнивающих шаблонов'''

    def print_alignment_module(self):
        if self.version < 2:
            return
        # Инициализация координат центров всех выравнивающих узоров и тех, которые нужно исключить
        coordinates = list(product(alignment_positions[self.version], repeat=2))
        bad_coordinates = [coordinates[0], (coordinates[-1][-1], coordinates[0][0]),
                           (coordinates[0][0], coordinates[-1][-1])]
        for coord in coordinates:
            if coord not in bad_coordinates or self.version <= 6:

                # Находим левый угол
                k = (coord[0] - 2, coord[1] - 2)
                for i in range(5):
                    for j in range(5):
                        self.matrix[i + k[0]][j + k[1]] = alignment_pattern[i][j]

    '''Добавление временных шаблонов'''

    def print_temporary_pattern(self):
        parity_bit = 0
        # Горизонтальный временной шаблон
        for i in range(8, self.side - 8):
            if not self.is_empty(self.matrix[6][i]):
                parity_bit = (parity_bit + 1) % 2
                continue
            parity_bit = (parity_bit + 1) % 2
            self.matrix[6][i] = parity_bit

        # Вертикальный временной шаблон
        parity_bit = 0
        for i in range(8, self.side - 8):
            if not self.is_empty(self.matrix[i][6]):
                parity_bit = (parity_bit + 1) % 2
                continue
            parity_bit = (parity_bit + 1) % 2
            self.matrix[i][6] = parity_bit

    '''Резервация области информации о формате'''

    def reserve_place(self):
        # Маска версии
        if self.version > 6:
            for i in range(3):
                for j in range(6):
                    self.matrix[i - 11][j] = int(version_codes[self.version][6 * i + j])
                    self.matrix[j][i - 11] = int(version_codes[self.version][6 * i + j])

        # Формат для правого верхнего и левого нижнего шаблонов
        for i in range(1, 9):
            self.matrix[-i][8] = -2
            self.matrix[8][-i] = -2

        # Формат для верхнего левого шаблона
        for i in range(0, 9):
            if i != 6:
                self.matrix[i][8] = -2
                self.matrix[8][i] = -2

        # Темный модуль
        self.matrix[-8][8] = 1

    def print_data(self, mask):
        ind = 0
        j = self.side - 1
        copy_matrix = copy.deepcopy(self.matrix)

        # Заполняем данные
        while j > 2 and ind < len(self.finale_message):
            # Заполнение данными вверх
            for i in range(self.side - 1, -1, -1):
                if self.is_empty(copy_matrix[i][j]):
                    copy_matrix[i][j] = mask(int(self.finale_message[ind]), i, j)
                    ind += 1
                    if ind == len(self.finale_message):
                        break

                if self.is_empty(copy_matrix[i][j - 1]):
                    copy_matrix[i][j - 1] = mask(int(self.finale_message[ind]), i, j-1)
                    ind += 1
                    if ind == len(self.finale_message):
                        break

            # Пропуск вертикального временного шаблона
            if j - 2 == 6:
                j -= 1

            # Заполнение данными вниз
            for i in range(0, self.side):
                if self.is_empty(copy_matrix[i][j - 2]):
                    copy_matrix[i][j - 2] = mask(int(self.finale_message[ind]), i, j-2)
                    ind += 1
                    if ind == len(self.finale_message):
                        break

                if self.is_empty(copy_matrix[i][j - 3]):
                    copy_matrix[i][j - 3] = mask(int(self.finale_message[ind]), i, j-3)
                    ind += 1
                    if ind == len(self.finale_message):
                        break
            j -= 4

        return copy_matrix

    '''Заполнение данных о выборе маски в матрицу'''

    def filling_the_format_string(self, matrix, mask):

        mask = mask_codes[self.level][mask]
        k = 0

        # Заполняем данные о маске
        for i in range(7):
            if i == 6:
                k += 1

            matrix[8][i+k] = int(mask[i])
            matrix[-i-1][8] = int(mask[i])

        k = 0
        for i in range(7, 15):
            if i == 9:
                k += 1
            matrix[15-i-k][8] = int(mask[i])
            matrix[8][i-15] = int(mask[i])

    '''Выбор наилучшей маски для кодирования итогового сообщения'''

    def selecting_a_mask(self):

        def first_mask(element, row, col):
            if (row + col) % 2 == 0:
                return int(not element)
            return int(element)

        def second_mask(element, row, _):
            if row % 2 == 0:
                return int(not element)
            return int(element)

        def third_mask(element, _, col):
            if col % 3 == 0:
                return int(not element)
            return int(element)

        def fourth_mask(element, row, col):
            if (row + col) % 3 == 0:
                return int(not element)
            return int(element)

        def fifth_mask(element, row, col):
            if (math.floor(row / 2) + math.floor(col / 3)) % 2 == 0:
                return int(not element)
            return int(element)

        def sixth_mask(element, row, col):
            if ((row * col) % 2) + ((row * col) % 3) == 0:
                return int(not element)
            return int(element)

        def seventh_mask(element, row, col):
            if (((row * col) % 2) + ((row * col) % 3)) % 2 == 0:
                return int(not element)
            return int(element)

        def eighth_mask(element, row, col):
            if (((row + col) % 2) + ((row * col) % 3)) % 2 == 0:
                return int(not element)
            return int(element)

        masks = [first_mask, second_mask, third_mask, fourth_mask, fifth_mask, sixth_mask, seventh_mask, eighth_mask]
        points = []

        for mask in masks:
            matrix = self.print_data(mask)
            self.filling_the_format_string(matrix, masks.index(mask))

            '''Функции штрафов'''

            def first_penalty():
                penalty = 0

                # Проверка горизонтали
                for row in matrix:
                    i = 0
                    while i + 4 < self.side:
                        if row[i] == row[i+1] == row[i+2] == row[i+3] == row[i+4]:
                            penalty += 3
                            i += 4
                            while i+1 < self.side and row[i+1] == row[i]:
                                penalty += 1
                                i += 1
                        i += 1

                # Проверка вертикали
                for j in range(self.side):
                    i = 0
                    while i + 4 < self.side:
                        if matrix[i][j] == matrix[i+1][j] == matrix[i+2][j] == matrix[i+3][j] == matrix[i+4][j]:
                            penalty += 3
                            i += 4
                            while i+1 < self.side and matrix[i+1][j] == matrix[i][j]:
                                penalty += 1
                                i += 1
                        i += 1
                return penalty

            def second_penalty():
                penalty = 0

                # Проверка блоков 2*2
                for i in range(self.side-1):
                    for j in range(self.side-1):
                        if matrix[i][j] == matrix[i+1][j] == matrix[i][j+1] == matrix[i+1][j+1]:
                            penalty += 3
                return penalty

            def third_penalty():
                pattern = [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0]
                penalty = 0

                # Проверка горизонтали
                for i in range(self.side):
                    for j in range(self.side-10):
                        if matrix[i][j:j+11] == pattern or matrix[i][j:j+11] == pattern[::-1]:
                            penalty += 40

                # Проверка вертикали
                for j in range(self.side):
                    for i in range(self.side-10):
                        col = [item[j] for item in matrix[i:i+11]]
                        if col == pattern or col == pattern[::-1]:
                            penalty += 40
                return penalty

            def fourth_penalty():
                # Подсчет черных модулей
                black_count = 0
                for row in matrix:
                    black_count += row.count(1)
                percent = black_count * 100 / self.side ** 2
                num1 = percent - (percent % 5)
                return min(abs(num1 - 50) / 5, abs(num1 - 45) / 5) * 10

            points.append(first_penalty() + second_penalty() + third_penalty() + fourth_penalty())

        ind = points.index(min(points))
        mask = masks[ind]

        self.matrix = self.print_data(mask)
        self.mask = ind





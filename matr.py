import numpy as np
import pandas as pd

def read_excel_matrices(filename):
    first_matrix_df = pd.read_excel(filename, sheet_name=0, header=None)
    first_matrix = first_matrix_df.to_numpy()

    second_matrix_df = pd.read_excel(filename, sheet_name=1, header=None)
    second_matrix = second_matrix_df.to_numpy()

    return first_matrix, second_matrix

def read_coordinates():
    coordinates = []
    for _ in range(3):
        input_str = input("Введите координаты x и y через пробел: ")
        x, y = map(float, input_str.split())
        coordinates.append((x, y))
    return coordinates

def read_coordinates_for_matrices():
    print("Введите координаты для первой матрицы:")
    points1 = read_coordinates()
    print("Введите координаты для второй матрицы:")
    points2 = read_coordinates()
    return points1, points2

def replace_with_nan(matrix, coordinates):
    modified_matrix = matrix.copy()
    for x, y in coordinates:
        modified_matrix[int(y), int(x)] = np.nan
    return modified_matrix



def rotate_matrix(matrix):
    return np.rot90(matrix)

def shift_matrix(matrix, direction):
    shifted_matrix = np.roll(matrix, direction, axis=(0, 1))
    if direction < 0:
        shifted_matrix[:, direction:] = 0
    elif direction > 0:
        shifted_matrix[:, :direction] = 0
    return shifted_matrix

def find_shifts(original_matrix, copied_matrix, points1):
    shifts = []
    rotations = []
    for i in range(4):
        rotated_matrix = copied_matrix.copy()
        for _ in range(4):
            shifted_matrix = shift_matrix(rotated_matrix, i)
            if np.array_equal(shifted_matrix[points1], original_matrix[points1]):
                shifts.append((i, np.count_nonzero(shifted_matrix != 0)))
                rotations.append(_)
            rotated_matrix = rotate_matrix(rotated_matrix)
    return shifts, rotations

def apply_shifts(matrix, shifts, rotations):
    shifted_matrix = matrix.copy()
    for shift, rotation in zip(shifts, rotations):
        shifted_matrix = rotate_matrix(shifted_matrix)
        shifted_matrix = shift_matrix(shifted_matrix, shift)
    return shifted_matrix

def main():
    filename = input("Введите имя файла   ")
    
    first_matrix, second_matrix = read_excel_matrices(filename)

    points1, points2 = read_coordinates_for_matrices()

    modified_second_matrix = replace_with_nan(second_matrix, points2)

    shifts, rotations = find_shifts(first_matrix, modified_second_matrix, points1)

    result_matrix = apply_shifts(modified_second_matrix, shifts, rotations)

    result_df = pd.DataFrame(result_matrix)
    result_df.to_excel("result.xlsx", index=False, header=False)

    print("Программа завершена. Результат сохранен в файле 'result.xlsx'")

main()
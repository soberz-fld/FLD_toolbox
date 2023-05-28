import re


def string_from_two_dimensional_list(table: list[list], cell_width: int = 5) -> str:
    string = ''
    for row in table:
        row_print = ''
        for cell in row:
            row_print += str(cell).ljust(cell_width, ' ')
            row_print += ' '
        string += row_print
        string += '\n'
    return string


def remove_duplicates_from_list(list_that_needs_to_be_cleared: list) -> list:
    list_to_return = []
    for e in list_that_needs_to_be_cleared:
        if e not in list_to_return:
            list_to_return.append(e)
    return list_to_return


def add_ids_to_rows_of_list(list_that_needs_ids: list) -> list:
    list_to_return = []
    id_number = 0
    for e in list_that_needs_ids:
        if isinstance(e, list):
            e.insert(0, id_number)
            list_to_return.append(e)
        else:
            list_to_return.append([id_number, e])
        id_number += 1
    return list_to_return


def get_list_from_stringed_list(stringed_list: str) -> list[str]:
    """
    When typecasting a list of strings, the result is something like "['str1','str2','str']" and if you typecast it back to list, python creates a list of chars. This function instead returns your list of strings. World saved.
    :param stringed_list: A string resulting from a typecast from list[str] to str
    :return: List of strings
    """
    try:
        pattern = "\'((?:[^\']+)+)\',?"
        findings = re.findall(pattern, stringed_list)
    except TypeError as e:
        if 'TypeError: expected string or bytes-like object, got' in str(e):
            findings = list()
        else:
            raise e from None
    return findings

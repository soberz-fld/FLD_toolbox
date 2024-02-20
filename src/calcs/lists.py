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


def string_dynamic_table_from_list_of_tuples(table: list[tuple], first_row_is_headers: bool = True) -> str:
    if not table:
        return '[]'

    # Find the maximum length of any tuple in the table
    max_columns = max(len(row) for row in table)

    # Adjust each row in the table to have the same number of elements
    adjusted_table = [row + ('',) * (max_columns - len(row)) for row in table]

    # Calculate the maximum width for each column
    column_widths = [max(len(str(item)) for item in column) for column in zip(*adjusted_table)]

    def generate_separator():
        return "+" + "+".join("-" * (width + 2) for width in column_widths) + "+"

    output_string = ""  # Initialize the output string
    separator = generate_separator()
    output_string += separator + "\n"

    start_index = 0  # Always start from the first row

    # Format and add the header row to the output string if first_row_is_headers is True
    if first_row_is_headers:
        header = " | ".join(str(item).center(column_widths[i]) for i, item in enumerate(adjusted_table[0]))
        output_string += f"| {header} |\n"
        output_string += separator + "\n"
        start_index = 1  # Skip the first row for data rows if it's a header

    # Format and add data rows to the output string
    for row in adjusted_table[start_index:]:
        formatted_row = " | ".join(str(item).ljust(column_widths[i]) for i, item in enumerate(row))
        output_string += f"| {formatted_row} |\n"
    output_string += separator

    return output_string


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
        if 'expected string or bytes-like object, got' in str(e):
            findings = list()
        else:
            raise e from None
    return findings

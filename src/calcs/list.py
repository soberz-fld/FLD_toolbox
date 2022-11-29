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

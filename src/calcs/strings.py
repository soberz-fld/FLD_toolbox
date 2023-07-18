import Levenshtein


def get_similarity_of_string_beginnings(string1: str, string2: str, length_to_compare: int = 0) -> list[float]:
    """
    Compares the two strings but only the length of the shortest one. If one string is 'Titanium' and one is 'Titanium (Remix)', it only compares the length of 'Titanium' so it would be 100% similarity. But it gives you the ratio of the lengths.
    :param string1: String to compare
    :param string2: String to compare
    :param length_to_compare: (Optional) Length to which both strings are compared
    :return: A list with two values. First one is similarity of the length of the shortest string. Second value is ratio of length.
    """
    if length_to_compare == 0:
        if len(string1) < len(string2):
            length_of_shorter_string = len(string1)
            try:
                ratio_of_length = len(string2) / len(string1)
            except ZeroDivisionError:
                ratio_of_length = 0
        elif len(string1) > len(string2):
            length_of_shorter_string = len(string2)
            try:
                ratio_of_length = len(string1) / len(string2)
            except ZeroDivisionError:
                ratio_of_length = 0
        else:
            length_of_shorter_string = len(string1)
            ratio_of_length = 1
    else:
        length_of_shorter_string = length_to_compare
        ratio_of_length = 0
    t1 = string1[0:length_of_shorter_string].lower()
    t2 = string2[0:length_of_shorter_string].lower()
    levenshtein = Levenshtein.distance(t1, t2)
    try:
        return [float(1 - levenshtein / length_of_shorter_string), float(ratio_of_length)]
    except ZeroDivisionError:
        return [float(-1), float(-1)]

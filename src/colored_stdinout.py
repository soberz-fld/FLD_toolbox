def get_string_colored(text: str, red: int = 255, green: int = 255, blue: int = 255) -> str:
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(red, green, blue, text)


def printr(text: str) -> None:
    print(get_string_colored(text, 255, 0, 0))


def inputr(text: str) -> str:
    return input(get_string_colored(text, 255, 0, 0))


def printg(text: str) -> None:
    print(get_string_colored(text, 0, 255, 0))


def inputg(text: str) -> str:
    return input(get_string_colored(text, 0, 255, 0))


def printb(text: str) -> None:
    print(get_string_colored(text, 96, 96, 255))


def inputb(text: str) -> str:
    return input(get_string_colored(text, 96, 96, 255))


def printy(text: str) -> None:
    print(get_string_colored(text, 255, 128, 0))


def inputy(text: str) -> str:
    return input(get_string_colored(text, 255, 128, 0))

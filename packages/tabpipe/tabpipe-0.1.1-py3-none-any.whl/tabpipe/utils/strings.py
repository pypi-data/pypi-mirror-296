from re import sub


def snake_case(text: str) -> str:
    """Convert a string to snake_case.

    Args:
        text (str): The string to convert

    Returns:
        str: The string in snake_case
    """
    return sub(
        r"^_|_$|(?<=_)_|_+$",
        "",
        # 1. (below) Replace special characters with underscores and add underscores before CamelCase capital letters
        # 2. (above) Remove excess underscores
        sub(r"([^A-Za-z0-9]|(?<!^)(?<!_)(?=[A-Z](?=[a-z])))", "_", str(text)),
    ).lower()

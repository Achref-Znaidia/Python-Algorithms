def check_string_is_palandrome(string: str) -> bool:
    if type(string) is not str:
        raise (TypeError)
    return string == string[::-1]


def main():
    print(check_string_is_palandrome("hahah"))


if __name__ == "__main__":
    main()

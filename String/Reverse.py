



def reverse_string_one(string: str):
    return string[::-1]

def reverse_string_two(string: str):
    return ''.join(reversed(string))

def main():
    print(reverse_string_one("string"))
    print(reverse_string_two("string"))


if __name__ == '__main__':
    main()
      

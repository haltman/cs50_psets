import cs50
import sys

def main():
    # alphabetic ASCII constants
    upper = 65
    lower = 97
    atoz = 26

    # check that two command line arguments were entered
    if len(sys.argv) == 2:

        # convert key entered from string to integer
        k = int(sys.argv[1])

        # request plaintext string from user
        print("plaintext: ", end="")
        p = cs50.get_string()

        # start printing output
        print("ciphertext: ", end="")

        # iterate through each char in plaintext string
        for c in p:

            # check if char is alphabetic
            if c.isalpha():

                # obtain numerical ASCII value of char
                num = ord(c)

                # check case of char to maintain it
                if c.isupper():
                    # rotate uppercase char by key and print
                    num = (((num - upper) + k) % atoz) + upper
                    print(chr(num), end="")

                else:
                    # rotate lowercase char by key and print
                    num = (((num - lower) + k) % atoz) + lower
                    print(chr(num), end="")

            else:
                # print non-alphabetic chars as they are
                print(c, end="")

        print()
        return 0

    # return error message if incorrect number of command line arguments entered
    else:
        print("Usage: python caesar.py k")
        return 1

if __name__ == "__main__":
    main()
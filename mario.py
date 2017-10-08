import cs50

def main():
    # prompt user for height of half pyramid
    while True:
        print("Height: ", end="")
        height = cs50.get_int()

        # break out of loop if valid height entered
        if (height > 0 and height < 24):
            break

    # iterate over height of half pyramid
    for i in range(1, height + 1, 1):

        # print appropriate number of spaces for each row
        for j in range(height - i, 0, -1):
            print(" ", end="")

        # print appropriate number of pound chars for each row
        for k in range(2, i + 3, 1):
            print("#", end="")

            # go to next line when all spaces and pound chars have printed
            if k == i + 2:
                print()

if __name__ == "__main__":
    main()
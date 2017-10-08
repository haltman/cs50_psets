import cs50

def main():
    # money constants
    quarter = 25
    dime = 10
    nickel = 5
    penny = 1
    change = 0

    # get dollar value from user
    while True:
        dollars = cs50.get_float("O hai! How much change is owed? ")
        # break from loop if valid dollar value entered
        if dollars > 0:
            break

    # convert dollar value entered into cents
    cents = int(dollars * 100)

    # count quarters
    while cents >= quarter:
        cents -= quarter
        change += 1
    # count dimes
    while cents >= dime:
        cents -= dime
        change += 1
    # count nickels
    while cents >= nickel:
        cents -= nickel
        change += 1
    # count pennies
    while cents >= penny:
        cents -= penny
        change += 1

    # return minumum number of coins required for change
    print("{}".format(change))

if __name__ == "__main__":
    main()
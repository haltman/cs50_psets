#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main (void)
{
    float dollars;
    int quarter = 25;
    int dime = 10;
    int nickel = 5;
    int penny = 1;
    int change = 0;


    do {
        printf("O hai! How much change is owed?\n");
        dollars = get_float();
    } while (dollars < 0);

    int cents = round(dollars * 100);

    while (cents >= quarter)
    {
        cents = cents - quarter;
        change++;
    }
    while (cents >= dime)
    {
        cents = cents - dime;
        change++;
    }
    while (cents >= nickel)
    {
        cents = cents - nickel;
        change++;
    }
    while (cents >= penny)
    {
        cents = cents - penny;
        change++;
    }

    printf("%i\n", change);
}
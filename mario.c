#include <stdio.h>
#include <cs50.h>

int main (void)
{
    int height;
    do {
        printf("Height: ");
        height = get_int();
    } while (height < 0 || height > 23);

    for (int i = 1; i <= height; i++)
    {
        for (int j = height - i; j > 0; j--)
        {
            printf(" ");
        }
        for (int k = 2; k <= i + 2; k++)
        {
            printf("#");
            if (k == i + 2)
            {
                printf("\n");
            }
        }
    }
}
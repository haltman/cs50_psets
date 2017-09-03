#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#define INITIALS 3

int main (void)
{
    //Get name from user and count length of input
    string s = get_string();
    int len = strlen(s);

    //Create array to store up to three initials and counter to keep track of index of array
    char output[INITIALS] = {'0', '0', '0'};
    int j = 0;

    //Iterate through string and copy initials into array
    for (int i = 0; i < len; i++)
    {
        //Copy first initial into array
        if (i == 0)
        {
            output[j] = toupper(s[i]);
            j++;
        }

        //Copy the char after each space into array - second and third initial
        if (isblank(s[i]))
        {
            output[j] = toupper(s[i + 1]);
            j++;
        }
    }

    //Iterate through length of array
    for (int k = 0; k < INITIALS; k++)
    {
        //Print initials when element is not 0
        if(output[k] != '0')
        {
            printf("%c", output[k]);
        }
    }
    //Print new line after iterating through array
    printf("\n");
}
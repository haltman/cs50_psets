#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#define UPPER 65
#define LOWER 97
#define ATOZ 26

int main (int argc, string argv[])
{
    //Check that only two command line arguments were entered by the user
    if (argc == 2)
    {
        //Convert key entered from string to integer
        int k = atoi(argv[1]);

        //Request plaintext from user
        printf("plaintext: ");
        string p = get_string();

        //Get length of plaintext string and create a char to hold each letter of ciphertext
        int len = strlen(p);
        char c;

        //Print output
        printf("ciphertext: ");

        //Iterate through length of plaintext string, char by char
        for (int i = 0; i < len; i++)
        {
            //Check if char is alphabetical
            if (isalpha(p[i]))
            {
                //Check case of char to maintain it
                if (isupper(p[i]))
                {
                    //Convert char to alphabetical index, rotate by key, covert back to ASCII index, print char
                    c = (((p[i] - UPPER) + k) % ATOZ) + UPPER;
                    printf("%c", c);
                }
                else
                {
                    c = (((p[i] - LOWER) + k) % ATOZ) + LOWER;
                    printf("%c", c);
                }
            }
            //If char is another type of character, print as is
            else
            {
                c = p[i];
                printf("%c", c);
            }
        }
        //Print new line after exiting loop that prints ciphertext
        printf("\n");

        return 0;
    }
    //If the incorrect number of command line arguments were entered by user, return error
    else
    {
        return 1;
    }
}
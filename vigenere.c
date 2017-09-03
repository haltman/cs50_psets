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
    //If two command line arguments entered by user, determine if key entered is entirely alphabetical
    if (argc == 2)
    {
        //Create string to hold key entered by user and get its length
        string key = argv[1];
        int len_k = strlen(key);

        //Integer variable to keep track of whether each char of key is alphabetic
        int proceed = 0;

        //Iterate through length of key entered by user
        for (int i = 0; i < len_k; i++)
        {
            //Convert char to lowercase if alphabetical and increase counter 'proceed'
            if (isalpha(key[i]))
            {
                proceed++;
                key[i] = tolower(key[i]);
            }
            else
            {
                proceed--;
            }
        }

        //Proceed only if the counter equals the length of the key, AKA is entirely alphabetical
        if (proceed == strlen(key))
        {
            //Request plaintext from user and get its length
            printf("plaintext: ");
            string p = get_string();
            int len_p = strlen(p);

            //Char variable to hold ciphertext
            char c;
            //Integer variable used as counter for key
            int k;
            //Integer variable used to modify counter for key if a char is non-alphabetic
            int counter = 0;

            //Print output
            printf("ciphertext: ");

            //Iterate through length of plaintext string, char by char
            for (int j = 0; j < len_p; j++)
            {
                //Check if char is alphabetical
                if (isalpha(p[j]))
                {
                    //Set key counter
                    k = (j - counter) % len_k;

                    //Check if plaintext char is uppercase to cipher it appropriately
                    if (isupper(p[j]))
                    {
                        //Convert char to ciphertext and print
                        c = (((p[j] - UPPER) + (key[k] - LOWER)) % ATOZ) + UPPER;
                        printf("%c", c);

                        //If previous char was non-alphabetic, reduce this counter back to zero
                        if (counter > 0)
                        {
                            counter--;
                        }
                    }

                    //Check if plaintext char is lowercase to cipher it appropriately
                    else if (islower(p[j]))
                    {
                        //Convert char to ciphertext and print
                        c = (((p[j] - LOWER) + (key[k] - LOWER)) % ATOZ) + LOWER;
                        printf("%c", c);

                        //If previous char was non-alphabetic, reduce this counter back to zero
                        if (counter > 0)
                        {
                            counter--;
                        }
                    }
                }

                //If char is another type of character, print as is
                else
                {
                    c = p[j];
                    printf("%c", c);
                    //Increase this counter by one to modify key counter on the next iteration (to reflect pause of key counter for non-alphabetic char)
                    counter++;
                }
            }

            //Print new line after exiting loop
            printf("\n");

            return 0;
        }

        //If the key entered is not entirely alphabetical, return error
        else
        {
            return 1;
        }
    }

    //If the incorrect number of command line arguments are entered by user, return error
    else
    {
        return 1;
    }

}
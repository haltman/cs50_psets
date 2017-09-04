/**
 * generate.c
 *
 * Generates pseudorandom numbers in [0,MAX), one per line.
 *
 * Usage: generate n [s]
 *
 * where n is number of pseudorandom numbers to print
 * and s is an optional seed
 */

#define _XOPEN_SOURCE

#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// upper limit on range of integers that can be generated
#define LIMIT 65536

int main(int argc, string argv[])
{
    // If incorrect number of command line arguments entered by user, return error from main
    // Print what is expected from user (2 or 3 command line arguments)
    if (argc != 2 && argc != 3)
    {
        printf("Usage: ./generate n [s]\n");
        return 1;
    }

    // Convert n entered by user (number of pseudorandom numbers to print) from string to integer
    int n = atoi(argv[1]);

    // If user also entered a seed, convert seed to a long integer and pass that value into srand48 function to initialize it
    // Otherwise, set seed to NULL
    if (argc == 3)
    {
        srand48((long) atoi(argv[2]));
    }
    else
    {
        srand48((long) time(NULL));
    }

    // Print pseudorandom number 'n' times
    // Multiply the output of random number generator (floating point value between 0.0 and 1.0) by upper limit, and convert type to integer
    for (int i = 0; i < n; i++)
    {
        printf("%i\n", (int) (drand48() * LIMIT));
    }

    // success
    return 0;
}

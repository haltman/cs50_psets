/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */

#include <cs50.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    // Return false if the size of array 'values' is non-positive
    if (n <= 0)
    {
        return false;
    }
    // Compare each element in array 'values' with target value
    else
    {
        int start = 0;
        int end = n - 1;

        // Start iteration from mid of array
        for (int i = (start + end) / 2; i >= 0; i = i / 2)
        {
            // Return true if found
            if (value == values[i])
            {
                return true;
            }
            // If value less than mid element, set end of new subarray one element left of mid
            else if (value < values[i])
            {
                end = i - 1;

                // Return false if end of new subarray crosses start
                if (end < start)
                {
                    return false;
                }
                // Else update counter to equal sum of start and end of new subarray
                else
                {
                    i = start + end;
                }
            }
            // If value greater than mid element, set start of new subarray one element right of mid
            else if (value > values[i])
            {
                start = i + 1;

                // Return false if start of new subarray crosses end
                if (start > end)
                {
                    return false;
                }
                // Else update counter to equal sum of start and end of new subarray
                else
                {
                    i = start + end;
                }
            }
        }
        // Return false if not found
        return false;
    }
}

/**
 * Sorts array of n values.
*/
void sort(int values[], int n)
{
    // Initialize swap counter so while loop returns true at least once
    // Variable temp to hold the value of one of the elements to be swapped
    int swap = -1;
    int temp;

    // Sort while swap counter is not equal to zero
    while (swap != 0)
    {
        // Set swap counter to zero
        swap = 0;

        // Iterate through length of array, up until second to last element
        for (int i = 0; i < n - 2; i++)
        {
            // Swap values if 'ith' and 'i + 1th' elements are unsorted
            // Increase swap counter
            if (values[i] > values[i + 1])
            {
                temp = values[i];
                values[i] = values[i + 1];
                values[i + 1] = temp;
                swap++;
            }
        }
    }

    return;
}

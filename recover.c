/**
 * Recovers JPEG files from a corrupted memory card.
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define BLOCK 512

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover infile\n");
        return 1;
    }

    // remember filename
    char *infile = argv[1];

    // open input file
    FILE *card = fopen(infile, "r");
    if (card == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // buffer to store block of 512 bytes
    unsigned char buffer[BLOCK];

    // pointer to store name of new jpeg file
    char *filename = malloc(sizeof(char) * 8);

    // file pointer to store blocks of new jpeg file
    FILE *img = NULL;

    // jpeg file counter
    int jpeg_count = 0;

    // read through blocks of infile until reach EOF
    while (fread(buffer, 1, BLOCK, card) == BLOCK)
    {
        // found a jpeg
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // already found a jpeg
            if (jpeg_count > 0)
            {
                // close previous jpeg file
                fclose(img);
            }

            // create file name to store new jpeg
            sprintf(filename, "%03i.jpg", jpeg_count);

            // open file to store new jpeg
            img = fopen(filename, "w");
            if (img == NULL)
            {
                fprintf(stderr, "Could not open %s.\n", filename);
                return 3;
            }

            // write block to new jpeg file
            fwrite(&buffer, 1, BLOCK, img);

            // iterate jpeg file counter
            jpeg_count++;
        }

        // already found a jpeg
        else if (jpeg_count > 0)
        {
            // write block to jpeg file
            fwrite(&buffer, 1, BLOCK, img);
        }
    }

    // close infile
    fclose(card);

    // close jpeg file
    fclose(img);

    // free dynamically allocated memory
    free(filename);

    // success
    return 0;
}

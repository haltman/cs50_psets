/**
 * Resizes a BMP by a factor of n.
 */

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./resize n infile outfile\n");
        return 1;
    }

    // ensure proper resize factor
    if (atoi(argv[1]) < 0 || atoi(argv[1]) > 100)
    {
        fprintf(stderr, "Resize factor must be greater than 0 and less than or equal to 100\n");
        return 1;
    }

    // remember resize factor and filenames
    int n = atoi(argv[1]);
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 1;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 1;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 1;
    }

    // determine input file padding for scanlines
    int padding_in = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // remember width and height of infile
    int width_in = bi.biWidth;
    int height_in = bi.biHeight;

    // resize BITMAPFILEHEADER and BITMAPINFOHEADER by n
    BITMAPFILEHEADER bf_n = bf;
    BITMAPINFOHEADER bi_n = bi;
    bi_n.biWidth *= n;
    bi_n.biHeight *= n;

    //determine output file padding for scanlines
    int padding_out = (4 - ((bi_n.biWidth) * sizeof(RGBTRIPLE)) % 4) % 4;

    // resize BITMAPFILEHEADER and BITMAPINFOHEADER by n cont'd
    bi_n.biSizeImage = ((sizeof(RGBTRIPLE) * bi_n.biWidth) + padding_out) * abs(bi_n.biHeight);
    bf_n.bfSize = bi_n.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf_n, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi_n, sizeof(BITMAPINFOHEADER), 1, outptr);

    // start cursor at first byte after two headers
    int cursor = sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(height_in); i < biHeight; i++)
    {
        // update current position of infile's cursor
        if (i != 0)
        {
            cursor += (width_in * sizeof(RGBTRIPLE)) + padding_in;
        }

        // iterate over each of infile's scanlines n times
        for (int j = 0; j < n; j++)
        {
            // iterate over pixels in scanline
            for (int k = 0; k < width_in; k++)
            {
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                // write RGB triple to outfile n times
                for (int l = 0; l < n; l++)
                {
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }

            // write outfile's padding
            for (int m = 0; m < padding_out; m++)
            {
                fputc(0x00, outptr);
            }

            // send cursor back to start of current scanline
            if (j != (n - 1))
            {
                fseek(inptr, cursor, SEEK_SET);
            }
        }

        // skip over infile padding, if any
        fseek(inptr, padding_in, SEEK_CUR);
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}

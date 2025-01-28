#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    const int SIZE = 512;
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // open memory card
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("File Not found\n");
        return 1;
    }

    // create buffer for a clock of data
    uint8_t buffer[SIZE];
    int file_count = 0;
    FILE *img = NULL;
    char file[8];

    // while data
    while (fread(buffer, 1, 512, card) == SIZE)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 &&
            buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // close the previous file if needed
            if (img != NULL)
            {
                fclose(img);
            }

            // open file
            sprintf(file, "%03i.jpg", file_count++);
            img = fopen(file, "w");

            // write the first block of file
            fwrite(buffer, 1, SIZE, img);

        }
        else
        {
            // no es principio de jpg
            if (img != NULL)
            {
                fwrite(buffer, 1, SIZE, img);
            }
        }

    }

    if (img != NULL)
    {
        fclose(img);
    }
    fclose(card);
}


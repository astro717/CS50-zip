#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int red = 0;
    int green = 0;
    int blue = 0;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            red = image[i][j].rgbtRed;
            green = image[i][j].rgbtGreen;
            blue = image[i][j].rgbtBlue;
            int grey = round((red + green + blue) / 3.0);
            image[i][j].rgbtRed = grey;
            image[i][j].rgbtGreen = grey;
            image[i][j].rgbtBlue = grey;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen +
                                 .189 * image[i][j].rgbtBlue);
            int sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen +
                                   .168 * image[i][j].rgbtBlue);
            int sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen +
                                  .131 * image[i][j].rgbtBlue);

            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }

            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int tempixel_red = 0;
    int tempixel_green = 0;
    int tempixel_blue = 0;
    int first_half = width / 2;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < first_half; j++)
        {
            tempixel_red = image[i][j].rgbtRed;
            tempixel_green = image[i][j].rgbtGreen;
            tempixel_blue = image[i][j].rgbtBlue;
            image[i][j].rgbtRed = image[i][width - 1 - j].rgbtRed;
            image[i][j].rgbtGreen = image[i][width - 1 - j].rgbtGreen;
            image[i][j].rgbtBlue = image[i][width - 1 - j].rgbtBlue;
            image[i][width - 1 - j].rgbtRed = tempixel_red;
            image[i][width - 1 - j].rgbtGreen = tempixel_green;
            image[i][width - 1 - j].rgbtBlue = tempixel_blue;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int tempixel_red = 0;
            int tempixel_green = 0;
            int tempixel_blue = 0;
            int vecinos = 0;

            copy[i][j] = image[i][j];
            for (int dy = -1; dy <= 1; dy++) // estos son para recorrer los pixeles vecinos
            {
                for (int dx = -1; dx <= 1; dx++)
                {
                    if (i + dy >= 0 && i + dy < height && j + dx >= 0 && j + dx < width)
                    {
                        tempixel_red+= image[i + dy][j + dx].rgbtRed;
                        tempixel_green += image[i + dy][j + dx].rgbtGreen;
                        tempixel_blue += image[i + dy][j + dx].rgbtBlue;
                        vecinos++;
                    }
                }
            }
            copy[i][j].rgbtRed = round(tempixel_red / (float) vecinos);
            copy[i][j].rgbtGreen = round(tempixel_green / (float) vecinos);
            copy[i][j].rgbtBlue = round(tempixel_blue / (float) vecinos);
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = copy[i][j];
        }
    }
    return;
}

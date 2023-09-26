#include "helpers.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int row = 0; row < height; row++) {
        for (int col = 0; col < width; col++){
            RGBTRIPLE pixel = image[row][col];
            int avg = (pixel.rgbtBlue + pixel.rgbtGreen + pixel.rgbtRed) / 3;
            image[row][col].rgbtBlue = avg;
            image[row][col].rgbtGreen = avg;
            image[row][col].rgbtRed = avg;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int row = 0; row < height; row++) {
        for (int col = 0; col < width; col++){
            RGBTRIPLE pixel = image[row][col];
            int sepiaRed = round(.393 * pixel.rgbtRed + .769 * pixel.rgbtGreen + .189 * pixel.rgbtBlue);
            int sepiaGreen = round(.349 * pixel.rgbtRed + .686 * pixel.rgbtGreen + .168 * pixel.rgbtBlue);
            int sepiaBlue = round(.272 * pixel.rgbtRed + .534 * pixel.rgbtGreen + .131 * pixel.rgbtBlue);
            if (sepiaRed > 255) {
                sepiaRed = 255;
            }
            if (sepiaGreen > 255) {
                sepiaGreen = 255;
            }
            if (sepiaBlue > 255) {
                sepiaBlue = 255;
            }
            image[row][col].rgbtBlue = sepiaBlue;
            image[row][col].rgbtGreen = sepiaGreen;
            image[row][col].rgbtRed = sepiaRed;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int halfWidth = width / 2;
    for (int row = 0; row < height; row++) {
        for (int col = 0; col < halfWidth; col++){
            RGBTRIPLE pixel = image[row][col];
            image[row][col] = image[row][width - col - 1];
            image[row][width - col - 1] = pixel;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    int sumRed, sumGreen, sumBlue;
    float count;
    for (int row = 0; row < height; row++) {
        for (int col = 0; col < width; col++){
            sumRed = 0;
            sumGreen = 0;
            sumBlue = 0;
            count = 0.00;
            for (int i = -1; i < 2; i++) {
                if (row + i < 0 || row + i > height - 1) {
                    continue;
                }
                for (int j = -1; j < 2; j++) {
                    if (col + j < 0 || col + j > width - 1) {
                        continue;
                    }
                    sumRed += image[row + i][col + j].rgbtRed;
                    sumGreen += image[row + i][col + j].rgbtGreen;
                    sumBlue += image[row + i][col + j].rgbtBlue;
                    count++;
                }
            }
            temp[row][col].rgbtRed = round(sumRed / count);
            temp[row][col].rgbtGreen = round(sumGreen / count);
            temp[row][col].rgbtBlue = round(sumBlue / count);
        }
    }
    for (int row = 0; row < height; row++) {
        for (int col = 0; col < width; col++){
            image[row][col] = temp[row][col];
        }
    }
    return;
}

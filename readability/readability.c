#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    string text = get_string("Text:");
    int letters = 0;
    int words = 1;
    int sentences = 0;

    for (int i = 0; text[i] != '\0'; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences++;
        }
        else if (text[i] == ' ')
        {
            words++;
        }
        else if (isalpha(text[i]))
        {
            letters++;
        }
    }

    double L = ((double) letters / words) * 100;
    double S = ((double) sentences / words) * 100;
    double grade = 0.0588 * L - 0.296 * S - 15.8;


    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", (int) round(grade));
    }
}
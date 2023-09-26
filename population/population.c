#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int startSize = 0;
    while (startSize < 9)
    {
        startSize = get_int("Start size: ");
    }

    int endSize = 0;
    while (endSize < startSize)
    {
        endSize = get_int("End size: ");
    }


    int years = 0;
    while (startSize < endSize)
    {
        startSize = startSize + (startSize / 3) - (startSize / 4);
        years++;
    }

    printf("Years: %i\n", years);
}
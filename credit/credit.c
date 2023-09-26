#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long long cc_number = get_long_long("Number: ");
    int sum = 0;
    int digit = 0;
    int count = 0;
    long long cc_number_copy = cc_number;
    while (cc_number_copy > 0)
    {
        digit = cc_number_copy % 10;
        if (count % 2 == 0)
        {
            sum += digit;
        }
        else
        {
            int product = digit * 2;
            sum += product / 10 + product % 10;
        }
        cc_number_copy /= 10;
        count++;
    }
    if (sum % 10 == 0)
    {
        if ((cc_number >= 340000000000000 && cc_number < 350000000000000) || (cc_number >= 370000000000000 && cc_number < 380000000000000))
        {
            printf("AMEX\n");
        }
        else if (cc_number >= 5100000000000000 && cc_number < 5600000000000000)
        {
            printf("MASTERCARD\n");
        }
        else if ((cc_number >= 4000000000000 && cc_number < 5000000000000) || (cc_number >= 4000000000000000 && cc_number < 5000000000000000))
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}
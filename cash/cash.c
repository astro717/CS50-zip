#include <stdio.h>
#include <cs50.h>

//hay monedas de 25,10,5,1

int main (void)
{

    int coin_number = 0;
    int cents;

    do
    {
        cents = get_int("Change owed: ");
    }
    while(cents < 1);

    while (cents != 0)
    {

        if (cents >= 25)
        {
            coin_number = cents / 25;
            cents = cents % 25;
        }
        else if (cents >= 10)
        {
            coin_number++;
            cents = cents - 10;
        }
        else if (cents >= 5)
        {
            coin_number++;
            cents = cents - 5;
        }
        else if (cents >= 1)
        {
            coin_number++;
            cents--;
        }
    }
    printf("%i\n",coin_number);
}

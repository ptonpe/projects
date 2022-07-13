#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    float dollar;
    do 
    {
    dollar = get_float("Change owed: ");
    }
    while (dollar <= 0);

    int cents = round(dollar * 100);
    int coins = 0;
    
    while (cents >= 25)
    {
        //if change is higher than 25, continue using quarters to take off 25 until it is less than 25 
        cents-= 25;
        coins++;
    }
    while (cents >= 10)
    {
    //if change is higher than 10, continue using dimes to take off 10 until it is less than 10 
    cents-= 10;
    coins++;
    }

    while (cents >= 5)
    {
    //if change is higher than 5, continue using nickels to take off 5 until it is less than 5 
        cents-=5;
        coins++;
    }
    while (cents >= 1)
    {
    //if change is higher than 1, continue using pennies to take off 1 until change is given 
        cents-= 1;
        coins++;
    }

    printf("You will need at least %i coins\n", coins);
}

    

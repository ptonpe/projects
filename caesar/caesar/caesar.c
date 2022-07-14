#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

bool check_key(string s);

int main(int argc, string argv[])
{
    //checks command line argument; must have 2 words and be an int
    if (argc != 2 || !check_key(argv[1]))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    //converts ascii to int
    int key = atoi(argv[1]);

    string plaintext = get_string("Plaintext: ");

    printf("ciphertext: " );
    for (int i = 0, len = strlen(plaintext); i < len; i++)
    {
        char c = plaintext[i];
        //checks if each char of plaintext is an alphabet and then applies algorithm
        if (isalpha(c))
        {
            char m = 'A';
            if (islower(c))
                //reassigns m with lowercase if plaintext is lowercase
                m = 'a';
                //algorithm
                printf("%c", (c - m + key) % 26 + m);


        }
        else
        {
            //non-alphabet char will stay the same
            printf("%c", c);
        }
    }
    printf("\n");
}

//function for checking key
bool check_key(string s)
{
    for (int i = 0, len = strlen(s); i < len; i++)
        if(!isdigit(s[i]))
        return false;

    return true;

}

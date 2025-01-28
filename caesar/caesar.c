#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int k = 0;

bool only_digits(string argument);

int main(int argc, string argv[]) // podemos asumir que numero positivo
{                                 // pero hay que comprobar si numero
    if (argc != 2 || only_digits(argv[1]) == false)
    {
        printf("Usage: ./caesar key:\n");
        return 1;
    }

    k = atoi(argv[1]);
    string text = get_string("Plain text:  ");
    int length = strlen(text);
    string cipher_text[length + 1]; // asignamos memoria correspondiente al inicializarlo
    printf("ciphertext: ");

    for (int i = 0; i < length; i++)
    {
        if (isupper(text[i]))
        {
            text[i] = ((text[i] - 'A' + k) % 26) + 'A';
        }
        else if (islower(text[i]))
        {
            text[i] = ((text[i] - 'a' + k) % 26) + 'a';
        }

        printf("%c", text[i]);
    }
    printf("\n");
    return 0;
}

bool only_digits(string argument)
{
    bool res = true;
    int l = strlen(argument);
    for (int i = 0; i < l; i++)
    {
        if (isdigit(argument[i]) == false)
        {
            res = false;
        }
    }
    return res;
}

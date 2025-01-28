#include <cs50.h>
#include <ctype.h>

#include <stdio.h>
#include <string.h>


int points = 0;
const char letters[26] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'};
const int points_array[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3,
                            1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};


int get_points(string player_word);


int main(void)
{

    string p1 = get_string("Player 1: ");
    string p2 = get_string("Player 2: ");

    int points1 = get_points(p1); // llamar get_points p1
    int points2 = get_points(p2); // llamar get_points p2

    if (points1 > points2)
    {
        printf("Player 1 wins!\n");
    }
    else if (points1 < points2)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }

}

int get_points(string player_word)
{
    int n = strlen(player_word);
    points = 0;                 // esto muy importante para restablecer los puntos para cada jugador
    for (int j = 0; j < n; j++) // por cada letra de palabra buscarla en abecedario
    {
        for (int i = 0; i < 26; i++)
        {
            char letter_word = toupper(player_word[j]);
            if (letter_word == letters[i])
            {
                points = points + points_array[i];
            }
        }
    }
    return points;
}

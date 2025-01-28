#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int length_char = 0;
string letters;
float l = 0.0;
float s = 0.0;
int grade = 0;
int words = 0;
int sentence_count = 0;
int letter_count = 0;
float num_of_avg = 0.0;

float calculate_L(string input_text);
float calculate_S(string input_text);

int main(void)
{
    string text = get_string("Text: ");

    // call functions
    float L = calculate_L(text);
    float S = calculate_S(text);

    float grade_f = 0.0588 * L - 0.296 * S - 15.8;
    grade = (int) round(grade_f); // redondear al entero mas cercano

    if (grade > 16)
    {
        printf("Grade 16+\n");
    }
    else if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}

float calculate_L(string input_text)
{
    int spaces = 0;

    length_char = strlen(input_text);

    if (length_char == 0)
    {
        l = 0.0;
        return l;
    }

    for (int i = 0; i < length_char; i++)
    {
        if (isalnum(input_text[i]))
        {
            letter_count++;
        }
        else if (isspace(input_text[i])) // para n palabras hay n-1 espacios
        {
            spaces++;
        }
    }

    words = spaces + 1;
    l = letter_count * 100 / (float) words;

    return l;
}

float calculate_S(string input_text)
{
    int punct_count = 0;
    int spaces = 0;
    letter_count = 0;

    length_char = strlen(input_text);

    if (length_char == 0)
    {
        s = 0.0;
        return s;
    }

    for (int i = 0; i < length_char; i++)
    {

        if (isspace(input_text[i]))
        {
            spaces++;
        }

        else if (input_text[i] == '.' || input_text[i] == '!' || input_text[i] == '?')
        {
            punct_count++;
        }
    }

    sentence_count = punct_count;
    words = spaces + 1;

    s = sentence_count * 100.0 / words;

    return s;
}

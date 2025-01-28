// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>



#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1]; // por el caracter nulo
    struct node *next;
} node;

// aprox 1.3x large dictionary
const unsigned int N = 190000;
unsigned int word_count = 0;
bool dic_loaded = false;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int index = hash(word);
    node *cursor = table[index];
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }

        cursor = cursor->next;

    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int hash_value = 0;
    unsigned int index = 0;
    // sumar char ascii por potencias de 2 y se reinicia cada 8 digitos
    for (int i = 0, l = strlen(word); i < l; i++)
    {
        char letter = tolower(word[i]);
        hash_value += letter * (1 << (i % 8 + 1)); // potencia valores 1-8
    }

    index = hash_value % N;
    return index;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    char word[LENGTH + 1];
    FILE *source = fopen(dictionary, "r");

    if (source == NULL)
    {
        printf("File not found\n");
        return false;
    }

    // Leer cada palabra en el diccionario
    while (fscanf(source, "%s", word) != EOF)
    {
        // Crear nodo para la nueva palabra
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            fclose(source);
            return false;
        }

        // Copiar palabra y calcular índice hash
        strcpy(n->word, word);
        int index = hash(word);

        // Si la posición en la tabla está vacía, insertar directamente
        if (table[index] == NULL)
        {
            n->next = NULL;
            table[index] = n;
            word_count++;
        }
        else
        {
            // Verificar si la palabra ya está en la lista del índice actual
            node *cursor = table[index];
            bool is_duplicate = false;

            while (cursor != NULL)
            {
                if (strcasecmp(cursor->word, word) == 0)
                {
                    is_duplicate = true;
                    break;
                }
                cursor = cursor->next; // bucamos duplicados en indice
            }

            // Solo insertar si no es duplicado
            if (!is_duplicate)
            {
                n->next = table[index];
                table[index] = n;
                word_count++;
            }
            else
            {
                free(n); // Liberar nodo si es duplicado
            }
        }
    }

    fclose(source);
    dic_loaded = true;
    return true;
}



// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return dic_loaded ? word_count : 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    node *cursor = table[0];
    for (int i = 0; i < N; i++)
    {
        cursor = table[i];
        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }
    return true;
}

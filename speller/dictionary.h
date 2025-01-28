// Declares a dictionary's functionality

#ifndef DICTIONARY_H  // son para que solo se compile una vez
#define DICTIONARY_H  // aun teniendo en cuenta que se importa en varios archivos

#include <stdbool.h>

// Maximum length for a word
// (e.g., pneumonoultramicroscopicsilicovolcanoconiosis)
#define LENGTH 45

// Prototypes
bool check(const char *word);
unsigned int hash(const char *word);
bool load(const char *dictionary);
unsigned int size(void);
bool unload(void);

#endif // DICTIONARY_H

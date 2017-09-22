/**
 * Implements a dictionary's functionality.
 */

#include <stdbool.h>
#include "dictionary.h"
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

#define ALPHABET 26
#define APOSTROPHE 39

// global struct node to be used by any function
typedef struct node
{
    bool is_word;
    struct node *children[ALPHABET + 1];
}
node;

// global root node to be used by any function
node *root = NULL;

// global integer variable to count number of words in dictionary
int num_words = 0;

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    // build pointer starts at root pointer
    node *build = NULL;
    build = root;

    // iterate through each character of word
    for (int i = 0; i < strlen(word); i++)
    {
        // apostrophe character
        if (word[i] == APOSTROPHE)
        {
            // current node not pointing at character in trie
            if (build -> children[ALPHABET] == NULL)
            {
                return false;
            }

            // move pointer
            build = build -> children[ALPHABET];
        }

        // alphabetical character
        else
        {
            // current node not pointing at character in trie
            if (build -> children[tolower(word[i]) - 97] == NULL)
            {
                return false;
            }

            // move pointer
            build = build -> children[tolower(word[i]) - 97];
        }
    }

    // last node in word
    if (build -> is_word == true)
    {
        return true;
    }

    return false;
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    // allocate memory to root pointer and check if initialized properly
    root = calloc(1, sizeof(node));
    if (root == NULL)
    {
        printf("Calloc() failed to allocate desired memory to root node.\n");
        return 1;
    }

    // build pointer starts at root pointer
    node *build = NULL;
    build = root;

    // open dictionary file if not NULL
    FILE *fp = fopen(dictionary, "r");
    if (fp == NULL)
    {
        printf("Could not open %s.\n", dictionary);
        unload();
        return 1;
    }

    // load characters from dictionary into trie until reach end of file
    while (fgetc(fp) != EOF)
    {
        // move file cursor back to current character
        fseek(fp, -1, SEEK_CUR);

        // get next character from dictionary that isn't a new line character
        for (char c = fgetc(fp); c != '\n'; c = fgetc(fp))
        {
            // apostrophe character
            if (c == APOSTROPHE)
            {
                // build new node if pointer to character doesn't exist in trie
                if (build -> children[ALPHABET] == NULL)
                {
                    build -> children[ALPHABET] = calloc(1, sizeof(node));
                }

                // move pointer
                build = build -> children[ALPHABET];
            }

            // alphabetical character
            else
            {
                // build new node if pointer to character doesn't exist in trie
                if (build -> children[c - 97] == NULL)
                {
                    build -> children[c - 97] = calloc(1, sizeof(node));
                }

                // move pointer
                build = build -> children[c - 97];
            }
        }

        // last node in word
        build -> is_word = true;

        // increase number of words in dictionary counter by one
        num_words++;

        // reset pointer to start at root node again for next word
        build = root;
    }

    // close dictionary file
    fclose(fp);

    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    // return number of words in dictionary using global variable modified in load()
    return num_words;
}

/**
 * Returns memory - to the heap - allocated to each node in trie that is not already NULL.
 */
void free_trie (struct node *node1)
{
    // go through each of node's 27 pointers (from 'a' to '\'')
    for (int c = 97; c <= 123; c++)
    {
        // continue only if the current pointer is not NULL
        if (node1 -> children[c - 97] != NULL)
        {
            // recursive function call to find last pointer in every word in trie
            free_trie(node1 -> children[c - 97]);
        }
    }

    // free memory allocated to each word in trie starting from last node up to first node
    free(node1);
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    // empty dictionary cannot be unloaded
    if (root == NULL)
    {
        return false;
    }

    // otherwise unload dictionary starting from root node
    free_trie(root);
    return true;
}





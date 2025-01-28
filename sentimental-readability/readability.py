from cs50 import get_string


def main():

    text = get_string('Text: ')
    word_count = len(text.split())
    letter_count = sum(1 for c in text if c.isalpha())
    sentences = sum(1 for c in text if (c == '.' or c == '!' or c == '?'))

    L = calculate_L(word_count, letter_count)
    S = calculate_S(word_count, sentences)

    grade = round(0.0588 * L - 0.296 * S - 15.8)

    if grade > 16:
        print("Grade 16+")
    elif grade > 1:
        print(f"Grade {grade}")
    else:
        print("Before Grade 1")


def calculate_L(words, letters):
    L = (letters * 100) / words
    return L


def calculate_S(words, sentences):
    S = (sentences * 100) / words
    return S


main()

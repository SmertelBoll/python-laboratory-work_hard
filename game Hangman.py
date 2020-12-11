# Problem Set 2, hangman.py
# Name: Sholop Lyubomyr
# Collaborators:
# Time spent: 2 days

# Hangman Game


import random
import string

WORDLIST_FILENAME = "words.txt"
SET_OF_VOWELS = {'a', 'o', 'e', 'u', 'i'}
# Number of remaining possible typos.
WARNINGS_INITIAL = 3
# Number of attempts remaining.
GUESSES_INITIAL = 6
# Variable prompt.
HINT = '*'
# Unknown letter.
UNKNOWN_LETTER = '_'


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    """
    for letter in secret_word:
        if letter not in letters_guessed:
            return False
    else:
        return True


def get_guessed_word(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    """
    word = ''.join(c if c in letters_guessed else UNKNOWN_LETTER + ' ' for c in secret_word)
    word = word.strip()

    return word


def get_available_letters(letters_guessed):
    """
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    """
    # abcdefghijklmnopqrstuvwxyz
    remaining_letters = string.ascii_lowercase
    for letter in letters_guessed:
        if letter in string.ascii_lowercase:
            ndx = remaining_letters.index(letter)
            remaining_letters = list(remaining_letters)
            del remaining_letters[ndx]
            remaining_letters = ''.join(remaining_letters)
    return remaining_letters


def match_with_gaps(my_word, other_word, letters_guessed):
    """
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    """
    if len(my_word) != len(other_word):
        return False

    for index in range(len(my_word)):
        if my_word[index] != other_word[index] and my_word[index] != UNKNOWN_LETTER:
            return False
        elif my_word[index] != other_word[index] and other_word[index] in letters_guessed:
            return False
        elif my_word[index] != other_word[index] and my_word.count(other_word[index]) != 0 and \
                other_word.count(other_word[index]) != my_word.count(other_word[index]):
            return False

    return True


def show_possible_matches(my_word, letters_guessed):
    """
    my_word: string with _ characters, current guess of secret word
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.
    """
    list_hints = []
    my_word = my_word.replace(' ', '')
    for word in wordlist:
        if match_with_gaps(my_word, word, letters_guessed):
            list_hints.append(word)

    if not list_hints:
        print('No matches found.')
    else:
        list_hints = ' '.join(list_hints)
        print('Possible word matches are: ', end='')
        print(list_hints)
        print('-------------')


def welcome_message(secret_word):
    """
    secret_word: string, the word the user is guessing
    return: bool, whether the player wants to play with prompts

    Its function is to display the initial text on the screen and
    ask if the user wants to play with prompts.
    """
    print('Welcome to the game Hangman!')
    print('Want to play with hints?')
    while True:
        hints = input('Enter "yes" or "no": ')
        if hints == 'yes' or hints == 'no':
            break
        else:
            print('Sorry, but you can only enter "yes" or "no", try again')
    print(f'I am thinking of a word that is {len(secret_word)} letters long.')
    print('You have 3 warnings left.')
    print('-------------')

    if hints == 'yes':
        return True
    else:
        return False


def non_letter_input(warnings, guesses, letters_guessed):
    """
    warnings: integer, number of remaining warnings
    guesses: integer, number of remaining guesses
    letters_guessed: list (of letters), which letters have been guessed so far
    return: integer, number of remaining warnings; integer, number of remaining guesses

    This function returns the number of guesses and warnings
    """
    if warnings > 0:
        warnings -= 1
        print(f'Oops! That is not a valid letter. You have {warnings} warnings left:',
              get_guessed_word(secret_word, letters_guessed))
    elif warnings <= 0:
        guesses -= 1
        print("Oops! You've already guessed that letter. You have no warnings left so you lose one guess:",
              get_guessed_word(secret_word, letters_guessed))
    print('-------------')
    return warnings, guesses


def only_a_letter(letter_guessed, guesses, letters_guessed):
    """
    letter_guessed: string, entered letter
    guesses: integer, number of remaining guesses
    letters_guessed: list (of letters), which letters have been guessed so far
    return: integer, number of remaining guesses

    This function returns the number of guesses
    """
    if letter_guessed in secret_word:
        print('Goog guess:', get_guessed_word(secret_word, letters_guessed))
        print('-------------')
        return guesses

    elif letter_guessed in SET_OF_VOWELS:
        guesses -= 2
    else:
        guesses -= 1

    print('Oops! That letter is not in my word.', get_guessed_word(secret_word, letters_guessed))
    print('-------------')

    return guesses


def the_end_of_the_game(guesses, letters_guessed):
    """
    guesses: integer, number of remaining guesses
    letters_guessed: list (of letters), which letters have been guessed so far
    return: boolean, True - if you continue the game, False - if you finish the game

    This function decides whether to stop the game (when the player has lost or won) or continue
    """
    if is_word_guessed(secret_word, letters_guessed) or guesses <= 0:
        return False
    return True


def finish_message(guesses):
    """
        guesses: integer, number of remaining guesses
        return: nothing

        The function displays a farewell message
        """
    if guesses <= 0:
        print(f'Sorry, you ran out of guesses. The word was {secret_word}')
    else:
        print(f'Congratulations, you won! Your total score for this game is: {len(set(secret_word)) * guesses}')


def hangman_with_hints(secret_word):
    """
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word.

    Follows the other limitations detailed in the problem write-up.
    """
    # List of used letters.
    letters_guessed = set()
    warnings = WARNINGS_INITIAL
    guesses = GUESSES_INITIAL

    hints = welcome_message(secret_word)

    is_game_continuing = True
    while is_game_continuing:
        print(f'You have {guesses} guesses left.')
        print(f'Available letters: {get_available_letters(letters_guessed)}')
        letter_guessed = input('Please guess a letter: ').lower()

        # User entered "*" and plays with prompts.
        if letter_guessed == HINT and hints:
            show_possible_matches(get_guessed_word(secret_word, letters_guessed), letters_guessed)

        # There are extra characters or more than one character entered.
        elif len(letter_guessed) > 1 or not letter_guessed.isalpha() or (letter_guessed not in get_available_letters(letters_guessed)):
            warnings, guesses = non_letter_input(warnings, guesses, letters_guessed)

        else:
            # The letter has already been entered.
            if letter_guessed in letters_guessed:
                warnings, guesses = non_letter_input(warnings, guesses, letters_guessed)
                letters_guessed.add(letter_guessed)

            else:
                letters_guessed.add(letter_guessed)
                guesses = only_a_letter(letter_guessed, guesses, letters_guessed)

        is_game_continuing = the_end_of_the_game(guesses, letters_guessed)

    finish_message(guesses)


if __name__ == "__main__":

    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)

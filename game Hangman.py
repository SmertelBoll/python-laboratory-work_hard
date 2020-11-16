# Problem Set 2, hangman.py
# Name:
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


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


# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for letter in secret_word:
        if letter not in letters_guessed:
            return False
    else:
        return True


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    my_word1 = secret_word
    for letter in secret_word:
        if letter in letters_guessed:
            pass
        else:
            my_word1 = my_word1.replace(letter, '_ ')
    return my_word1


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    remaining_letters = string.ascii_lowercase
    for letter in string.ascii_lowercase:
        if letter in letters_guessed:
            remaining_letters = remaining_letters.replace(letter, '')
    return remaining_letters


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    '''
    warnings = 3
    guesses = 6
    print('Welcome to the game Hangman!')
    print(f'I am thinking of a word that is {len(secret_word)} letters long.')
    print(f'You have {warnings} warnings left.')
    letters_guessed = []
    print('-----------------')
    game = True
    while game == True:
        print(f'You have {guesses} guesses left.')
        print(f'Available letters: {get_available_letters(letters_guessed)}')
        letter_guessed = input('Please guess a letter: ')  # Ввід букви

        if letter_guessed.isalpha() == False:  # Якщо Є лишні символи
            if warnings > 0:
                warnings -= 1
            else:
                if guesses > 0:
                    guesses -= 1
                else:
                    print(f'Sorry, you ran out of guesses. The word was {secret_word}')
                    game = False
            print(f'Oops! That is not a valid letter. You have {warnings} warnings left:',
                  get_guessed_word(secret_word, letters_guessed))
            print('-----------------')
        else:
            letter_guessed.lower()  # малий регіст
            if letter_guessed in letters_guessed:
                if warnings > 0:
                    warnings -= 1
                else:
                    if guesses > 0:
                        guesses -= 1
                    else:
                        print(f'Sorry, you ran out of guesses. The word was {secret_word}')
                        game = False
                print(f"Oops! You've already guessed that letter. You have {warnings} warnings left:",
                      get_guessed_word(secret_word, letters_guessed))
                print('-----------------')
            else:
                letters_guessed.append(letter_guessed)  # Додаєм букву до всіх введених букв раніше
                if letter_guessed in secret_word:
                    print('Goog guess: ', get_guessed_word(secret_word, letters_guessed))
                    print('-----------------')
                else:
                    if letter_guessed == 'a' or letter_guessed == 'e' or letter_guessed == 'o' or letter_guessed == 'i' or letter_guessed == 'u':
                        if guesses > 1:
                            guesses -= 2
                        else:
                            print(f'Sorry, you ran out of guesses. The word was {secret_word}')
                            game = False
                    else:
                        if guesses > 0:
                            guesses -= 1
                        else:
                            print(f'Sorry, you ran out of guesses. The word was {secret_word}')
                            game = False
                    print('Oops! That letter is not in my word.', get_guessed_word(secret_word, letters_guessed))
                    print('-----------------')

        if is_word_guessed(secret_word, letters_guessed) == True:
            print(f'Congratulations, you won! Your total score for this game is: {(len(secret_word)+1)*guesses}')
            game = False
        elif guesses <= 0:
            print(f'Sorry, you ran out of guesses. The word was {secret_word}')
            game = False
        else:
            pass


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
# (hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    '''

    my_word = my_word.replace('_ ', '_')
    if len(my_word) == len(other_word):  # "te_t", "tact"
        for num in range(len(my_word)):
            if my_word[num] == other_word[num]:
                pass
            elif my_word[num] != other_word[num] and my_word[num] != '_':
                return False
            else:
                if other_word[num] in lst:
                    return False
                elif my_word.count(other_word[num]) == 0:
                    pass
                elif other_word.count(other_word[num]) != my_word.count(other_word[num]):
                    return False

                else:
                    pass

        else:
            return True

    else:
        return False


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    str = ''
    for word in wordlist:
        if match_with_gaps(my_word, word) == True:
            str = str + word + ' '

        else:
            pass
    if str == '':
        print('No matches found.')
    else:
        return str

def hangman_with_hints(secret_word):
    '''
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
    '''
    secret_word = "apple"
    global lst
    lst = []
    warnings = 3
    guesses = 6
    print('Welcome to the game Hangman!')
    print(f'I am thinking of a word that is {len(secret_word)} letters long.')
    print(f'You have {warnings} warnings left.')
    letters_guessed = []
    print('-----------------')
    game = True
    while game == True:
        print(f'You have {guesses} guesses left.')
        print(f'Available letters: {get_available_letters(letters_guessed)}')
        letter_guessed = input('Please guess a letter: ').lower()  # Ввід букви

        if letter_guessed == '*':
            print('Possible word matches are: ', end ='')
            print(show_possible_matches(get_guessed_word(secret_word, letters_guessed)))
            print('-----------------')
        elif letter_guessed.isalpha() == False:  # Якщо Є лишні символи
            if warnings > 0:
                warnings -= 1
            else:
                if guesses > 0:
                    guesses -= 1
                else:
                    print(f'Sorry, you ran out of guesses. The word was {secret_word}')
                    game = False
            print(f'Oops! That is not a valid letter. You have {warnings} warnings left:',
                  get_guessed_word(secret_word, letters_guessed))
            print('-----------------')
        else:
            lst.append(letter_guessed)
            if letter_guessed in letters_guessed:
                if warnings > 0:
                    warnings -= 1
                else:
                    if guesses > 0:
                        guesses -= 1
                    else:
                        print(f'Sorry, you ran out of guesses. The word was {secret_word}')
                        game = False
                print(f"Oops! You've already guessed that letter. You have {warnings} warnings left:",
                      get_guessed_word(secret_word, letters_guessed))
                print('-----------------')
            else:
                letters_guessed.append(letter_guessed)  # Додаєм букву до всіх введених букв раніше
                #lst.append(letter_guessed)
                if letter_guessed in secret_word:
                    print('Goog guess:', get_guessed_word(secret_word, letters_guessed))
                    print('-----------------')
                else:
                    if letter_guessed == 'a' or letter_guessed == 'e' or letter_guessed == 'o' or letter_guessed == 'i' or letter_guessed == 'u':
                        if guesses > 1:
                            guesses -= 2
                        else:
                            print(f'Sorry, you ran out of guesses. The word was {secret_word}')
                            game = False
                    else:
                        if guesses > 0:
                            guesses -= 1
                        else:
                            print(f'Sorry, you ran out of guesses. The word was {secret_word}')
                            game = False
                    print('Oops! That letter is not in my word.', get_guessed_word(secret_word, letters_guessed))
                    print('-----------------')

        if is_word_guessed(secret_word, letters_guessed) == True:
            print(f'Congratulations, you won! Your total score for this game is: {(len(secret_word)+1)*guesses}')
            game = False
        elif guesses <= 0:
            print(f'Sorry, you ran out of guesses. The word was {secret_word}')
            game = False
        else:
            pass


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.

    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

    ###############

    # To test part 3 re-comment out the above lines and
    # uncomment the following two lines.

    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
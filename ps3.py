# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <Sholop Lyubomyr>
# Collaborators : <None>
# Time spent    : <3 days>

import math
import random

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7
WILDCARD = '*'
STOP_GAME = '!!'
WORDLIST_FILENAME = "words(Word_Game).txt"
SCRABBLE_LETTER_VALUES = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5,
                          'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4,
                          'w': 4, 'x': 8, 'y': 4, 'z': 10}


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x, 0) + 1
    return freq


def get_frequency_list(sequence):
    """
    Returns a list of only the letters of the dictionary
    that are repeated as many times as specified in the
    dictionary values

    sequence: dictionary
    return: string or list
    """
    lst = []
    for key in sequence:
        for f in range(sequence[key]):
            lst.append(key)
    return lst


def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters,
    or the empty string "". You may not assume that the string will only contain
    lowercase letters, so you will have to handle uppercase and mixed case strings
    appropriately.

    The score for a word is the product of two components:

    The first component is the sum of the points for letters in the word.
    The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

    Letters are scored as in Scrabble; A is worth 1, B is
    worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    word = word.lower()

    # The sum of points for the letters in the word.
    first_component = 0
    for letter in word:
        first_component += SCRABBLE_LETTER_VALUES.get(letter, 0)

    # The value of the expression [7 * word length - 3 * (n - word length)]:
    #   word_length is the number of letters used in the word;
    #   n is the number of letters available in the current hand.
    the_second_component = max((HAND_SIZE * len(word)) - (3 * (n - len(word))), 1)

    return first_component * the_second_component


def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
            # print all on the same line
            print(letter, end=' ')
    # print an empty line
    print()


def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand = {WILDCARD: 1}
    # Number of vowels
    num_vowels = int(math.ceil(n / 3))

    # Randomly choose vowels. There will be one less than num_vowels of them, because one of the vowels "becomes" "*".
    for i in range(1, num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    # Randomly choose consonants.
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    return hand


def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured).

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    word = word.lower()
    lst_hand = get_frequency_list(hand)

    for letter in word:
        if letter in lst_hand:
            lst_hand.remove(letter)
    return get_frequency_dict(lst_hand)


def word_with_wildcard(word, word_set):
    """
    The function checks if a word with "*" can be in the word_set

    word: string
    word_set: set of lowercase strings
    returns: boolean
    """
    # Create a list of all possible words with vowels instead of "*".
    new_words = [word.replace(WILDCARD, i) for i in VOWELS]
    # List of intersections of the set of all words in the game and the set of the new_words list.
    crossing = list(word_set & set(new_words))

    # List is not empty.
    if crossing:
        return True
    # List is empty.
    else:
        return False


def is_valid_word(word, hand, word_set):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_set: set of lowercase strings
    returns: boolean
    """
    word = word.lower()
    lst_hand = get_frequency_list(hand)

    for letter in word:
        if letter in lst_hand:
            lst_hand.remove(letter)
        else:
            return False

    return word_with_wildcard(word, word_set)


def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    return len(get_frequency_list(hand))


def play_hand(hand, word_set):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
    """
    total_score = 0
    game_is_continuing = True

    while game_is_continuing:
        # As long as there are still letters left in the hand:
        if hand:
            # Display the hand
            print('Current Hand: ', end='')
            display_hand(hand)
            # Ask user for input
            word = input('Enter word, or “!!” to indicate that you are finished: ')
            if word == STOP_GAME:
                # End the game (break out of the loop)
                break

            # If the word is valid:
            elif is_valid_word(word, hand, word_set):
                # Tell the user how many points the word earned, and the updated total score
                total_score += get_word_score(word, calculate_handlen(hand))
                print(f'“{word}” earned {get_word_score(word, calculate_handlen(hand))} points. '
                      f'Total: {total_score} points')

            # Otherwise (the word is not valid):
            else:
                # Reject invalid word (print a message)
                print('This is not a valid word. Please choose another word.')
            print()

            # Update the user's hand by removing the letters of their inputted word
            hand = update_hand(hand, word)

        # Game is over (user entered '!!' or ran out of letters), so tell user the total score
        else:
            print('Ran out of letters.')
            game_is_continuing = False

    print(f'Total score: {total_score} points')

    # Return the total score as result of function
    return total_score


def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    new_hand = {}

    alphabet = VOWELS + CONSONANTS
    # We remove from the possible letters those that are in the hand.
    for key in hand:
        alphabet = alphabet.replace(key, '')
    new_letter = random.choice(alphabet)

    for char in hand:
        if char == letter:
            new_hand[new_letter] = hand[char]
        else:
            new_hand[char] = hand[char]

    return new_hand


def ask_user(start_text, **kwargs):
    """
    This function processes the input of variables according
    to the conditions given in the variables of the function

    start_text: string, shown when entering a variable.
    returns: string, or integer or bool, the value of a variable
    """
    if 'validator' in kwargs:
        while True:
            variable = input(start_text)
            if not kwargs['validator'](variable):
                if 'warn_msg' in kwargs:
                    print(kwargs['warn_msg'])
                continue
            break

    elif 'values' in kwargs:
        while True:
            variable = input(start_text)
            if variable not in kwargs['values']:
                if 'warn_msg' in kwargs:
                    print(kwargs['warn_msg'])
                continue
            break

    return variable


def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    all_store = 0
    word_set = set(word_list)
    replay_hand = False

    # Inputting number of hands in the game.
    number_of_hands = int(ask_user('Enter total number of hands: ',
                                   validator=lambda char: char.isdecimal() and int(char) > 0,
                                   warn_msg="You entered invalid input. Please enter a positive integer."))

    while number_of_hands > 0:
        hand = deal_hand(HAND_SIZE)
        print('Current hand: ', end='')
        display_hand(hand)
        if replay_hand:
            print()

        # Checking if the player wants to change the letter.
        if ask_user('Would you like to substitute a letter?(yes/no) ',
                    values=('yes', 'no')) == 'yes':
            # Change the letter.
            letter = ask_user('Which letter would you like to replace: ',
                              validator=lambda char: char in CONSONANTS or char in VOWELS,
                              warn_msg="Sorry, but you don't have this letter in your hand. Try another.")
            hand = substitute_hand(hand, letter)
        print()

        # Displaying the number of points per hand.
        local_store = play_hand(hand, word_set)
        print('--------')

        replay_hand = True
        # Checking if the player wants to replay the game.
        if ask_user('Would you like to replay the hand?(yes/no) ',
                    values=('yes', 'no')) == 'yes':
            local_store = play_hand(hand, word_set)
            replay_hand = False

        all_store += local_store
        number_of_hands -= 1

    print('--------')
    print(f'Total score over all hands: {all_store}')


if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)

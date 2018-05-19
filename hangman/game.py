from .exceptions import *
import random

# Complete with your own, just for fun :)
LIST_OF_WORDS = []


def _get_random_word(list_of_words):

    listlen = len(list_of_words)
    if listlen :
        randomint = random.randint(0, listlen - 1)
    else:
        raise InvalidListOfWordsException()
    return list_of_words[randomint]

def _mask_word(word):
    strlen = len(word)
    strmask = ""

    if strlen > 0:
        for i in range(0,strlen):
            strmask = strmask + '*'
    else:
        raise InvalidWordException()
    return strmask


def _uncover_word(answer_word, masked_word, character):

    if not answer_word or not masked_word:
        raise InvalidWordException()

    if len(character) == 0 or len(character) > 1:
        raise InvalidGuessedLetterException()

    if len(masked_word) > len(answer_word):
        raise InvalidWordException()

    mask_list = list(masked_word)
    answer_list = list(answer_word)
    for i, c in enumerate(answer_list):
        if c.lower() == character.lower():
            mask_list[i] = character.lower()

    masked_word = ''.join(mask_list)
    return masked_word


def guess_letter(game, letter):
    # handle case insensitive cases
    letter = letter.lower()
    answer_word = game['answer_word'].lower()
    masked_word = game['masked_word']

    # Game has already completed
    if game['remaining_misses'] == 0 or answer_word == masked_word:
        raise GameFinishedException()

    # Assert if duplicated letter used
    for i, v in enumerate(game['previous_guesses']):
        if v == letter:
            raise InvalidGuessedLetterException()

    # Find for letter in answer_word
    edited_mask_word = _uncover_word(answer_word, masked_word, letter)

    # Invalid character
    if masked_word == edited_mask_word:
        game['remaining_misses'] = game['remaining_misses'] - 1

        if game['remaining_misses'] == 0:
            raise GameLostException()

    # Completed word guessed
    if game['answer_word'] == edited_mask_word:
        game['masked_word'] = edited_mask_word
        raise GameWonException()

    # Save status for next round
    game['masked_word'] = edited_mask_word
    game['previous_guesses'].append(letter)

    return game['masked_word']


def start_new_game(list_of_words=None, number_of_guesses=5):
    if list_of_words is None:
        list_of_words = LIST_OF_WORDS

    word_to_guess = _get_random_word(list_of_words)
    masked_word = _mask_word(word_to_guess)
    game = {
        'answer_word': word_to_guess,
        'masked_word': masked_word,
        'previous_guesses': [],
        'remaining_misses': number_of_guesses,
    }

    return game

# if __name__ == '__main__':
    # pass


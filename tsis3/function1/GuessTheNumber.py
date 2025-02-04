import random

def game():
    name = input('Hello! What is your name?\n')

    number = random.randint(1, 21)
    print(f'\nWell, {name}, I am thinking of a number between 1 and 20.')

    attempts = 1
    guess = int(input('Take a guess.\n'))
    while guess != number:
        attempts += 1
        if guess > number:
            print('\nYour guess is too high.')
        else:
            print('\nYour guess is too low.')

        guess = int(input('Take a guess.\n'))

    print(f'\nGood job, {name}! You guessed my number in {attempts} guesses!')


if __name__ == '__main__':
    game()
import random

def main():
    """The main function to generate and print random numbers."""
    #1. Create an initial number list.
    numbers = [16.2, 75.1, 52.3]
    print(f"Initial numbers: {numbers}")

    #2. Call an append_random_number with an only arguement.
    append_random_number(numbers)
    print(f'After add 1: {numbers}')

    #3. Call an append_random_number with both arguements.
    append_random_number(numbers, 3)
    print(f'After add 3 more: {numbers}')

    print("-" * 30)

    # Enhancement: Words list
    words = ["python", "code", "logic"]
    print(f"Initial words: {words}")

    # add 2 random words
    append_random_word(words, 2)
    print(f'After add 2 more words: {words}')

def append_random_number(numbers_list, quantity=1):
    """ Generate float random numbers and append them to the given list.
        Parameters:
        numbers_list (list): The list to which random numbers will be appended.
        quantity: How much numbers added. Default is 1.
    """
    for _ in range(quantity):
        random_num = (random.uniform(0, 100), 1)
        numbers_list.append(random_num)
    
def append_random_word(words_list, quantity=1):
    """ Select random words from a predefined list and append them to the given list.
    """
    candidates = ["apple", "banana", "cherry", "date", "fig", "grape", "kiwi"]
    for _ in range(quantity):
        word = random.choice(candidates)
        words_list.append(word)

# Start the program
if __name__ == "__main__":
    main()



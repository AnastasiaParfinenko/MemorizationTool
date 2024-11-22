import sys

main_menu = {'1': 'Add flashcards', '2': 'Practice flashcards', '3': 'Exit'}
add_menu = {'1': 'Add a new flashcard', '2': 'Exit'}
flashcards = {}


def print_menu(menu):
    print()
    for num in menu:
        print(f'{num}. {menu[num]}')


def work_main_menu():
    print_menu(main_menu)
    num = input()
    if num == '1':
        work_add_menu()
    elif num == '2':
        work_practice()
    elif num == '3':
        print('\nBye!')
        sys.exit()
    else:
        print(f'{num} is not an option')
        work_main_menu()


def work_add_menu():
    print_menu(add_menu)
    num = input()
    if num == '1':
        add_flashcards()
    elif num == '2':
        work_main_menu()
    else:
        print(f'{num} is not an option')
        work_add_menu()


def add_flashcards():
    q = ''
    while not q:
        q = input('Question:\n').strip()
    a = ''
    while not a:
        a = input('Answer:\n').strip()
    flashcards[q] = a
    work_add_menu()


def work_practice():
    for card in flashcards:
        print()
        print(f'Question: {card}')
        y_or_n = input('Please press "y" to see the answer or press "n" to skip:\n')
        if y_or_n == 'y':
            print(f'Answer: {flashcards[card]}')
        elif y_or_n == 'n':
            continue

    work_main_menu()


def main():
    work_main_menu()


if __name__ == '__main__':
    main()

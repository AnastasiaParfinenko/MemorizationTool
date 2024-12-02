import sys
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from textwrap import dedent

Base = declarative_base()


class Flashcard(Base):
    __tablename__ = 'flashcards'

    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    box = Column(Integer)
    session = Column(Integer)


engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def print_menu(menu):
    print()
    for num in menu:
        print(f'{num}. {menu[num]}')


def main_menu():
    menu = {'1': 'Add flashcards', '2': 'Practice flashcards', '3': 'Exit'}
    print_menu(menu)
    num = input()
    if num == '1':
        add_menu()
    elif num == '2':
        practice()
    elif num == '3':
        print('\nBye!')
        sys.exit()
    else:
        print(f'{num} is not an option')
        main_menu()


def add_menu():
    menu = {'1': 'Add a new flashcard', '2': 'Exit'}
    print_menu(menu)
    num = input()
    if num == '1':
        add_flashcards()
    elif num == '2':
        main_menu()
    else:
        print(f'{num} is not an option')
        add_menu()


def add_flashcards():
    q = ''
    while not q:
        q = input('Question:\n').strip()
    a = ''
    while not a:
        a = input('Answer:\n').strip()

    new_card = Flashcard(question=q, answer=a, box=1, session=1)
    session.add(new_card)
    session.commit()

    add_menu()


def practice():
    flashcards = session.query(Flashcard).filter(Flashcard.box <= Flashcard.session)

    empty = True
    for card in flashcards:
        empty = False
        print()
        print(f'Question: {card.question}')
        while True:
            y_n_u = input(dedent('''\
                press "y" to see the answer:
                press "n" to skip:
                press "u" to update:\n'''))
            if y_n_u in "ynu":
                break
            else:
                print(f'{y_n_u} is not an option')
                print()
        if y_n_u == 'y':
            print(f'Answer: {card.answer}')
            learning_menu(card)
        elif y_n_u == 'n':
            continue
        elif y_n_u == 'u':
            update_flashcards(card)

    all_flashcards = session.query(Flashcard)
    all_flashcards.update({'session': (Flashcard.session + 1) % 3 + 1})
    session.commit()

    if empty:
        print('There is no flashcard to practice!')

    main_menu()


def update_flashcards(card):
    query = session.query(Flashcard).filter(Flashcard.question == card.question)

    d_or_e = input(dedent('''\
        press "d" to delete the flashcard:
        press "e" to edit the flashcard:\n'''))
    if d_or_e == 'd':
        query.delete()
    elif d_or_e == 'e':
        print(f'current question: {card.question}')
        new_q = input('please write a new question:\n') or card.question
        print(f'current answer: {card.answer}')
        new_a = input('please write a new answer:\n') or card.answer
        query.update({
            "question": new_q,
            "answer": new_a
        })

    session.commit()


def learning_menu(card):
    query = session.query(Flashcard).filter(Flashcard.question == card.question)

    y_or_n = input(dedent('''\
    press "y" if your answer is correct:
    press "n" if your answer is wrong:\n'''))
    if y_or_n == 'y':
        if card.box == 3:
            query.delete()
        else:
            query.update({'box': card.box + 1})
    elif y_or_n == 'n':
        new_box = card.box - 1 if card.box > 1 else 1
        query.update({'box': new_box})

    session.commit()


if __name__ == '__main__':
    main_menu()

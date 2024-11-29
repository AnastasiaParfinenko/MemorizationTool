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


engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


main_menu = {'1': 'Add flashcards', '2': 'Practice flashcards', '3': 'Exit'}
add_menu = {'1': 'Add a new flashcard', '2': 'Exit'}


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

    new_card = Flashcard(question=q, answer=a)
    session.add(new_card)
    session.commit()

    work_add_menu()


def work_practice():
    flashcards = session.query(Flashcard).all()
    for card in flashcards:
        print()
        print(f'Question: {card.question}')
        y_or_n = input(dedent('''\
            press "y" to see the answer:
            press "n" to skip:
            press "u" to update:\n'''))
        if y_or_n == 'y':
            print(f'Answer: {card.answer}')
        elif y_or_n == 'n':
            continue
        elif y_or_n == 'u':
            update_flashcards(card)

    work_main_menu()


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


def main():
    work_main_menu()


if __name__ == '__main__':
    main()

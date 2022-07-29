import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from Models import Base, Publisher, Sale, Shop, Stock, Book
import json


user = input('Введите имя пользователя БД: ')
password = input('Введите пароль пользователя БД: ')
database = input('Введите имя базы данных: ')
DSN = f'postgresql://{user}:{password}@localhost:5432/{database}'
engine = sq.create_engine(DSN)


def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def populate_db():
    open_file = input('Введите путь к файлу, в котором хранятся данные для БД: ')
    with open(open_file) as file:
        data = json.load(file)

        for d in data:
            print(d)
            if d['model'] == 'publisher':
                instance = Publisher(id=d['pk'], name=d['fields']['name'])
            if d['model'] == 'book':
                instance = Book(id=d['pk'], title=d['fields']['title'], id_publisher=d['fields']['id_publisher'])
            if d['model'] == 'stock':
                instance = Stock(id=d['pk'], id_shop=d['fields']['id_shop'], id_book=d['fields']['id_book'], count=d['fields']['count'])
            if d['model'] == 'shop':
                instance = Shop(id=d['pk'], name=d['fields']['name'])
            if d['model'] == 'sale':
                instance = Sale(id=d['pk'], price=d['fields']['price'], date_sale=d['fields']['date_sale'], count=d['fields']['count'], id_stock=d['fields']['id_stock'])
            session.add(instance)
            session.commit()


def find_publisher():
    choice = input('Найти издателя по имени(1), по id(2)? ')
    if choice == '1':
        publisher_data = input('Введите имя издателя:')
        chek = (publisher_data,)
        if chek not in session.query(Publisher.name).all():
            print("Такого издателя нет!")
            return
        result = session.query(Publisher).filter(Publisher.name == publisher_data).one()
    elif choice == '2':
        publisher_data = int(input('Введите id издателя:'))
        chek = (publisher_data,)
        if chek not in session.query(Publisher.id).all():
            print("Такого издателя нет!")
            return
        result = session.query(Publisher).filter(Publisher.id == publisher_data).one()

    return result


Session = sessionmaker(bind=engine)
session = Session()

res = find_publisher()
print(res)

session.close()

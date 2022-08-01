import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from Models import Base, Publisher, Sale, Shop, Stock, Book
import json
import os


def get_connection():
    user = os.getenv('db_user')
    if user is None:
        user = 'postgres'
    password = os.getenv('db_password')
    if password is None:
        password = 'postgres'
    database = os.getenv('db_name')
    if database is None:
        database = 'publishing_house'
    DSN = f'postgresql://{user}:{password}@localhost:5432/{database}'
    engine = sq.create_engine(DSN)
    return engine


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
        publisher_name = input('Введите имя издателя:')
        chek = (publisher_name,)
        if chek not in session.query(Publisher.name).all():
            print("Такого издателя нет!")
            return
        publisher_data = session.query(Publisher).filter(Publisher.name == publisher_name).one()
        print(publisher_data)
        for s in session.query(Shop.name).join(Stock).join(Book).join(Publisher).filter(Publisher.name == publisher_name).all():
            print(f'Shop: {s[0]}')
    elif choice == '2':
        publisher_id = int(input('Введите id издателя:'))
        chek = (publisher_id,)
        if chek not in session.query(Publisher.id).all():
            print("Такого издателя нет!")
            return
        publisher_data = session.query(Publisher).filter(Publisher.id == publisher_id).one()
        print(publisher_data)
        for s in session.query(Shop.name).join(Stock).join(Book).join(Publisher).filter(Publisher.id == publisher_id).all():
            print(f'Shop: {s[0]}')

    return


Session = sessionmaker(bind=get_connection())

session = Session()

# create_tables()
# populate_db()
find_publisher()

session.close()



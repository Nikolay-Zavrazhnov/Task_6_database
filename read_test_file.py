import json

import sqlalchemy

from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Shop, Stock, Sale, Book

User = 'postgres'
Password = ''
Host = 'localhost'
Port = '5432'
database = ''

DSN = f"postgresql://{User}:{Password}@{Host}:{Port}/{database}"

engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()


def data_tester(session):
    with open('fixtures/tests_data.json', 'r') as datatest:
        data = json.load(datatest)
    for record in data:
        model = {'publisher': Publisher,
                 'shop': Shop,
                 'book': Book,
                 'stock': Stock,
                 'sale': Sale}[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
data_tester(session)
publ_id = input('введите id издателя: ')

#  вывоводит издателя по его id введеного через "input"
subq_1 = session.query(Book).filter(Book.id_publisher == int(publ_id)).subquery()
session.query(Publisher).join(subq_1, Publisher.id == subq_1.c.id_publisher).all()
for pb in session.query(Publisher).join(subq_1, Publisher.id == subq_1.c.id_publisher).all():
    print(f"publisher с id-{publ_id} - {pb.name}")


# магазины, в которых продаются книги издателя (введенного через input)
shops = set()
for books in session.query(Book).filter(Book.id_publisher == int(publ_id)).all():
    for stocks in session.query(Stock).filter(Stock.id_book == books.id).all():
        shops.add(stocks.shop.name)

print(f"книги автора с id [{int(publ_id)}] продаются в магазинах: {', '.join(shops)}")
session.commit()




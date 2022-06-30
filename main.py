
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

publisher_1 = Publisher(name='Pushkin')
publisher_2 = Publisher(name='Tolstoi')
publisher_3 = Publisher(name='Pelevin')

session.add_all([publisher_1, publisher_2, publisher_3])


book_1 = Book(title='Ruslan-i-Lyudmila', publisher=publisher_1)
book_1_1 = Book(title='Impire_v', publisher=publisher_3)
book_2 = Book(title='Voina-i-Mir', publisher=publisher_2)
book_3 = Book(title='Transhumanism-inc', publisher=publisher_3)

session.add_all([book_1, book_2, book_3])

shop_1 = Shop(name='box_books')
shop_2 = Shop(name='My_Book')

session.add_all([shop_1, shop_2])

stock_1 = Stock(book=book_1_1, shop=shop_1, count=5)
stock_2 = Stock(book=book_1, shop=shop_2, count=3)
stock_3 = Stock(book=book_3, shop=shop_2, count=10)

session.add_all([stock_1, stock_1, stock_2])

sale_1 = Sale(price=455.50, date_sale='22/06/2022', stock=stock_1)
sale_2 = Sale(price=455.50, date_sale='24/06/2022', stock=stock_1)
sale_3 = Sale(price=1520.50, date_sale='23/06/2022', stock=stock_2)
sale_4 = Sale(price=758.50, date_sale='25/06/2022', stock=stock_3)

session.add_all([sale_1, sale_2, sale_3, sale_4])
session.commit()


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

session.close()
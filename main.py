import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
DNS = os.getenv('DNS')

engine = sqlalchemy.create_engine(DNS)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
def create_table(engine):
    Base.metadata.create_all(engine)

class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=100), unique=True)

create_table(engine)

pub1 = Publisher(name='Pushkin')
pub2 = Publisher(name='Mark Twen')
pub3 = Publisher(name='Aleksandr Solzenicin')
pub4 = Publisher(name='Igor Senchin')

class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=100), unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    publisher = relationship(Publisher, backref='book')


create_table(engine)

b1 = Book(title='Captain doughter', id_publisher=1)
b2 = Book(title='Tom Soyer', id_publisher=2)
b3 = Book(title='Gek Finn', id_publisher=2)
b4 = Book(title='In the first circle', id_publisher=3)
b5 = Book(title='rain in Paris', id_publisher=4)

class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=100), unique=True)


create_table(engine)

s1 = Shop(name='Knigi')
s2 = Shop(name='Bukvi')

class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=True)

    book = relationship(Book, backref='book')
    shop = relationship(Shop, backref='book')
    
create_table(engine)

st1 = Stock(id_book=1, id_shop=2, count=115)
st2 = Stock(id_book=2, id_shop=1, count=10)
st3 = Stock(id_book=2, id_shop=2, count=22)
st4 = Stock(id_book=3, id_shop=1, count=222)
st5 = Stock(id_book=4, id_shop=1, count=5)
st6 = Stock(id_book=5, id_shop=2, count=8)
st7 = Stock(id_book=3, id_shop=2, count=16)


class Sale(Base):

    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Numeric(5, 2))
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=True)
    stock = relationship(Stock, backref='stock')

create_table(engine)

sa1 = Sale(price=200, date_sale='03-05-2023', id_stock=1, count=2)
sa2 = Sale(price=185, date_sale='20-04-2023', id_stock=2, count=5)
sa3 = Sale(price=190, date_sale='20-04-2023', id_stock=3, count=15)
sa4 = Sale(price=220, date_sale='15-02-2023', id_stock=4, count=2)
sa5 = Sale(price=250, date_sale='08-04-2023', id_stock=5, count=8)
sa6 = Sale(price=180, date_sale='08-04-2023', id_stock=6, count=4)
sa7 = Sale(price=240, date_sale='15-03-2023', id_stock=7, count=8)
sa8 = Sale(price=215, date_sale='16-03-2023', id_stock=2, count=6)
sa9 = Sale(price=218, date_sale='16-03-2023', id_stock=3, count=3)


session.add_all([pub1, pub2, pub3, pub4])
session.add_all([b1, b2, b3, b4, b5])
session.add_all([s1, s2])
session.add_all([st1, st2, st3, st4, st5, st6, st7])
session.add_all([sa1, sa2, sa3, sa4, sa5, sa6, sa7, sa8, sa9])

#доработанная часть кода
#вроде бы учёл все ваши замечания

writer = input('Input writer name or id')
query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock).join(Shop).join(Sale)
if writer.isdigit():
    query = query.filter(Publisher.id == writer).all()
else:
    query = query.filter(Publisher.name == writer).all()

for title, name, price, date_sale in query:
    print(f"{title:<40} | {name:<10} | {price:<8} | {date_sale}")

session.commit()
    

from app.extensions import db 
from app.models.books import Books 
from app.models.transactions import Transactions
from app.models.payments import Payments
from sqlalchemy import and_,func, or_ 
from datetime import datetime
from datetime import timedelta
from app.books.constants import DAILY_BOOK_RENT


def add_books(book):
    books = Books()
    books.bookID = book["bookID"]
    books.title = book["title"]
    books.authors = book["authors"]
    books.average_rating = book["average_rating"]
    books.isbn = book["isbn"]
    books.isbn13 = book["isbn13"]
    books.language_code = book["language_code"]
    books.num_pages = book["  num_pages"]
    books.rating_count = book["ratings_count"]
    books.text_reviews_count = book["text_reviews_count"]
    books.publication_date = book["publication_date"]
    books.publisher = book["publisher"]
    db.session.add(books)
    db.session.commit()
    print("Book details inserted in books table")
    
def check_if_bookID_exists(bookID):
    query = db.session.query(Books.bookID).filter(Books.bookID==bookID).all()
    for row in query:
        return row[0]
    return None 

def get_books():
    books = db.session.query(Books.bookID, 
                             Books.authors, 
                             Books.average_rating,
                             Books.isbn, 
                             Books.isbn13,
                             Books.language_code, 
                             Books.publication_date, 
                             Books.publisher,
                             Books.num_pages,
                             Books.text_reviews_count,
                             Books.title,
                             Books.stock,
                             Books.books_available).all()
    result = []
    for row in books:
        result.append(row._asdict())
    return result


def delete_book(bookid):
    query = db.session.query(Books).filter(Books.bookID==bookid).first()
    if query:
        db.session.delete(query)
        db.session.commit()
        return bookid 
    

def get_book(bookid):
    query = db.session.query(Books).filter(Books.bookID==bookid).all()
    for row in query:
        return {
            "book_id": row.bookID,
            "title": row.title,
            "authors": row.authors,
            "stock": row.stock,
            "books_available": row.books_available,
            "publisher": row.publisher,
            "average_rating": row.average_rating,
            "isbn": row.isbn,
            "publication_date": row.publication_date,
            "num_pages": row.num_pages,
            "language_code": row.language_code
        }
        

def save_stock(bookid, stock):
    db.session.query(Books).filter(Books.bookID==bookid).update({"stock": stock})
    db.session.commit()


def search_book(payload):
    title = payload["title"]
    title=f'%{title}%'
    authors = payload["authors"]
    authors = f'%{authors}%'
    query = db.session.query(Books).filter(or_(and_(Books.title.like(title),
                                                    Books.authors.like(authors)),
                                               and_(Books.title == title,
                                                    Books.authors == authors)
                                                )).all()
    result = []
    for row in query:
        result.append([row.title, 
                       row.publisher,
                       row.authors,
                       row.books_available,
                       ])
    return result


def add_transaction(book_id, member_id):
    transactions = Transactions()
    transactions.book_id = book_id
    transactions.member_id = member_id
    db.session.add(transactions)
    db.session.commit()


def get_transactions_by_member_id(member_id):
    query = db.session.query(Transactions).filter(and_(
        Transactions.member_id==member_id,
        Transactions.book_returned_date==None))
    result = []
    for row in query:
        difference = datetime.today().date() - row.book_issued_date.date()
        print(difference.days)
        result.append({
            "book_id": row.book_id,
            "member_id": row.member_id,
            "book_issue_date": row.book_issued_date.date().strftime("%d-%b-%Y"),
            "book_return_date": row.book_returned_date,
            "total_days": difference.days,
            "total_rent_due": difference.days* DAILY_BOOK_RENT,
            "current_date": datetime.today().date().strftime("%d-%b-%Y")
        })
    return result

def update_book_returned_date(book_id, member_id):
    db.session.query(Transactions).filter(and_(
        Transactions.member_id == member_id,
        Transactions.book_id == book_id
    )).update({
        "book_returned_date": datetime.today().date()
    })
    db.session.commit()


def fetch_transaction_details(member_id):
    query = db.session.query(Transactions.id, 
                            Transactions.member_id,
                            Transactions.book_issued_date,
                            Transactions.book_returned_date).filter(and_(
        func.date(Transactions.book_returned_date<=datetime.today().date()),
        Transactions.member_id==member_id))
    result = []
    for row in query:
        result.append(row._asdict())
    return result 


def add_payment_records(data):
    payments = Payments()
    for row in data:
        difference = row["book_returned_date"] - row["book_issued_date"]
        amount_due = difference.days * DAILY_BOOK_RENT
        payments.amount_due = amount_due
        payments.transaction_id = row["id"]
        payments.member_id = row["member_id"]
        db.session.add(payments)
        db.session.commit()

def check_book_availability(book_id):
    query = db.session.query(Books.stock,Books.books_available).filter(Books.bookID==book_id).all()
    for row in query:
        if row.books_available > 0:
            return row._asdict()
        else:
            return {"books_available": 0, "stock": row.stock}


def get_payment_details(member_id):
    query = db.session.query(Payments.member_id, 
                            func.sum(Payments.amount_due), 
                            func.sum(Payments.amount_paid),
                            Payments.transaction_id).filter(
        Payments.member_id == member_id
    ).group_by(Payments.member_id)
    for row in query:
        return {"member_id": row.member_id, 
                "amount_due": row[1], 
                "amount_paid":row[2]
                }
    return {}     

def update_books_available(book_id, available):
    books_available = available["books_available"]
    db.session.query(Books).filter(Books.bookID == book_id).update({"books_available": books_available - 1})
from flask import render_template, request
from app.books import bp
from app.books.helper import query_books_api
from app.books import database_helper
from app.payments.database_helper import check_total_debt


@bp.route('/')
def books():
    books = database_helper.get_books()
    return render_template('books/books.html', books=books)


@bp.route('/add_books')
def add_books():
    return render_template('books/add_books.html')

@bp.route('/get_books', methods=['POST'])
def get_books():
    response = request.get_json()
    page = 1
    total_books_requested = int(response["quantity"])
    total_books_fetched = 0
    books_left_to_fetch = total_books_requested
    MAX_BOOKS_PER_PAGE = 20
    while total_books_fetched != total_books_requested:
        data = query_books_api(response, page)
        books_items = len(data["message"])
        if "message" in data:
            if books_items > 0 and books_left_to_fetch <= MAX_BOOKS_PER_PAGE:
                result = data["message"][:books_left_to_fetch]
                total_books_fetched += books_left_to_fetch
            elif books_items == 20 and books_left_to_fetch > MAX_BOOKS_PER_PAGE:
                result = data["message"]
                total_books_fetched += books_items
                books_left_to_fetch = total_books_requested - total_books_fetched
                page += 1
            row_count = 0
            for row in result:
                row_count += 1
                book_is_exists = database_helper.check_if_bookID_exists(row['bookID'])
                if book_is_exists is None:
                    try:
                        database_helper.add_books(row)
                    except Exception as e:
                        print(page, row["title"])
                print(f"total books fetched: {row_count}, total books requested: {total_books_requested}")

    return data

@bp.route('/delete', methods=["POST"])
def delete():
    response = request.get_json()
    bookID = int(response["bookID"].split("_")[1])
    result = database_helper.delete_book(bookID)
    return f"{result} deleted from the database. Kindly refresh the page\
    to see updated list of books."
    
@bp.route('/save', methods=["POST", "GET"])
def save():
    response = request.get_json()
    book_id = response["bookID"]
    stock = response["stock"]
    database_helper.save_stock(book_id, stock)
    return f"Stock details saved for bookID: {book_id}"


@bp.route('/book/<book_id>', methods=["GET"])
def book_details(book_id):
    book_details = database_helper.get_book(book_id)
    return render_template('books/show_book.html', book_details=book_details)


@bp.route('/search', methods=["GET"])
def search():
    return render_template('books/search_book.html')

@bp.route('/search/book', methods=["POST"])
def search_book():
    response = request.get_json()
    result = database_helper.search_book(response)
    return result

@bp.route('/issue_book', methods=["GET"])
def issue_book():
    response = request.url
    member_id = response.split("=")[1]
    return render_template('books/issue_book.html', member_id=member_id)


@bp.route('/search/book', methods=["GET"])
def search_book_by_id():
    url = request.url
    query_params = url.split("?")[1]
    book_id = (query_params.split("&")[0]).split("=")[1]
    member_id = (query_params.split("&")[1]).split("=")[1]
    result = database_helper.get_book(book_id)
    result["member_id"] = member_id
    return result


@bp.route('/issue', methods=["GET"])
def issue_book_to_member():
    url = request.url
    query_params = url.split("?")[1]
    member_id = (query_params.split("&")[0]).split("=")[1]
    book_id = (query_params.split("&")[1]).split("=")[1]
    availability = database_helper.check_book_availability(book_id)
    total_debt = check_total_debt(member_id)
    if availability["books_available"] > 0 and total_debt < 500:
        database_helper.add_transaction(book_id, member_id)
        database_helper.update_books_available(book_id, availability)
        return f"Book has been issued to member ID: {member_id}"
    elif availability["books_available"] == 0:
        return f"Book ID {book_id}, OUT OF STOCK"
    elif total_debt >= 500:
        return f"New book cannot be issued. Total Debt greater or equal to 500."


@bp.route('/return_book', methods=["GET"])
def return_book():
    url = request.url
    member_id = url.split("=")[1]
    result = database_helper.get_transactions_by_member_id(member_id)
    return render_template('books/return_book.html', result=result)

@bp.route('/issue_return', methods=["GET"])
def issue_return():
    url = request.url
    query_params = url.split("?")[1]
    member_id = (query_params.split("&")[0]).split("=")[1]
    book_id = (query_params.split("&")[1]).split("=")[1]
    database_helper.update_book_returned_date(book_id, member_id)
    transactions = database_helper.fetch_transaction_details(member_id)
    database_helper.add_payment_records(transactions)
    return f"Return issued for Book ID {book_id}, Member ID {member_id}"


@bp.route('/make_payment', methods=["GET"])
def make_payment():
    url = request.url
    member_id = url.split("=")[1]
    payment_details = database_helper.get_payment_details(member_id)
    return render_template("payments/payments.html", payment_details=payment_details)
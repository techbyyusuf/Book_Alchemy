from data_models import db, Author, Book
from flask import Flask, redirect, render_template, request, url_for
from datetime import date, datetime
from sqlalchemy import or_
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data', 'library.sqlite')}"


db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    """
    Render the homepage and display a list of books.
    Supports sorting by title or author name and filtering by search keyword.
    """
    sort_by = request.args.get('sort_by', 'title')
    search = request.args.get('search', '').lower()

    query = Book.query.join(Author)

    if search:
        query = query.filter(
            or_(
                Book.title.ilike(f'%{search}%'),
                Author.name.ilike(f'%{search}%')
            )
        )

    if sort_by == 'author':
        query = query.order_by(Author.name)
    else:
        query = query.order_by(Book.title)

    books = query.all()
    return render_template('home.html', books=books, sort_by=sort_by, search=search)


@app.route("/add_author", methods=['GET', 'POST'])
def add_author():
    """
    Add a new author to the database.
    On GET: display the form to create an author.
    On POST: process form data, create a new author, and show success message.
    """
    if request.method == 'POST':
        author_name = request.form.get('name')
        birth_input = request.form.get('birthdate')
        death_input = request.form.get('date_of_death')

        if not author_name:
            return render_template('add_author.html',
                                   message="Name is required.")

        try:
            author_birthdate = datetime.strptime(birth_input, "%Y-%m-%d").date()
        except ValueError:
            return render_template('add_author.html',
                                   message="Invalid birthdate format.")

        if author_birthdate > date.today():
            return render_template('add_author.html',
                                   message="Birthdate cannot be in the future.")

        author_date_of_death = None
        if death_input:
            try:
                author_date_of_death = datetime.strptime(death_input,
                                                         "%Y-%m-%d").date()
            except ValueError:
                return render_template('add_author.html',
                                       message="Invalid death date format.")

            if author_date_of_death > date.today():
                return render_template('add_author.html',
                                       message="Death date cannot be in the future.")

            if author_date_of_death < author_birthdate:
                return render_template('add_author.html',
                                       message="Death date must be after birth date.")

        author = Author(
            name=author_name,
            birth_date=author_birthdate,
            date_of_death=author_date_of_death
        )

        db.session.add(author)
        db.session.commit()
        return render_template('add_author.html',
                               message="Author has been added!")

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_books():
    """
    Add a new book to the database.
    On GET: display the form to create a book.
    On POST: process form data, create a new book, and show success message.
    """
    authors = Author.query.all()
    if request.method == 'POST':
        book_title = request.form.get('title')
        book_isbn = request.form.get('isbn')
        publication_input = request.form.get('publication_year')
        author_id = request.form.get('author_id')

        if not book_title or not book_isbn or not publication_input:
            return render_template('add_book.html', authors=authors,
                                   message='All fields are required.')

        try:
            book_publication_year = datetime.strptime(publication_input,
                                                      "%Y-%m-%d").date()
        except ValueError:
            return render_template('add_book.html', authors=authors,
                                   message="Invalid publication date.")

        if book_publication_year > date.today():
            return render_template('add_book.html', authors=authors,
                                   message="Publication date can't be in the future.")

        book = Book(
            title=book_title,
            isbn=book_isbn,
            publication_year=book_publication_year,
            author_id=author_id
        )

        db.session.add(book)
        db.session.commit()
        return render_template('add_book.html', authors=authors,
                               message='Book has been added!')

    return render_template('add_book.html', authors=authors)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """
    Delete a book by ID from the database.
    Also deletes the author if this was their only book.
    Redirects back to the homepage with a success message.
    """
    try:
        book = Book.query.get_or_404(book_id)
        author = book.author

        db.session.delete(book)
        db.session.flush()

        remaining_books = Book.query.filter_by(author_id=author.id).count()
        if remaining_books == 0:
            db.session.delete(author)

        db.session.commit()
        return redirect(
            url_for('index', message=f'"{book.title}" has been deleted!'))

    except Exception as e:
        db.session.rollback()
        return redirect(
            url_for('index', message=f"Error deleting book: {str(e)}"))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)

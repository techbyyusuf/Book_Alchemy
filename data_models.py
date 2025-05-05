from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, ForeignKey

db = SQLAlchemy()

class Author(db.Model):
    """
    Represents an author in the library system.

    Attributes:
        id (int): Primary key for the author.
        name (str): Full name of the author.
        birth_date (datetime): Birth date of the author.
        date_of_death (datetime): Date of death of the author (optional).
    """

    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    birth_date = Column(Date)
    date_of_death = Column(Date)

    def __repr__(self):
        """
        Return a readable representation of the author.
        """
        return f"Author(id={self.id}, name='{self.name}')"


class Book(db.Model):
    """
    Represents a book in the library system.

    Attributes:
        id (int): Primary key for the book.
        author_id (int): Foreign key referencing the book's author.
        isbn (str): ISBN number of the book.
        title (str): Title of the book.
        publication_year (datetime): Publication date of the book.
        author (Author): Relationship to the corresponding Author object.
    """

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey('authors.id'))
    isbn = Column(String)
    title = Column(String)
    publication_year = Column(Date)

    author = db.relationship('Author', backref='books')

    def __repr__(self):
        """
        Return a readable representation of the book.
        """
        return f"Book(id={self.id}, title='{self.title}')"

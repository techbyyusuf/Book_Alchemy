# 📚 Book Alchemy – Flask Library Manager

A web application to manage a library of famous books and their authors using Flask and SQLAlchemy.

---

## 🚀 Features

- 📖 Add, view, and delete books and authors
- 🧠 Sort books by title or author
- 🔍 Search books by title or author name
- 📸 Automatically show book covers using ISBN (via Open Library)
- ✅ Automatically remove authors with no books
- 🧼 Clean, modern UI using custom CSS

---

## 🛠 Tech Stack

- **Python 3**
- **Flask**
- **Flask-SQLAlchemy**
- **SQLite**
- **HTML + CSS (Jinja2 templates)**

---

## ▶️ Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/dein-benutzername/book-alchemy.git
cd book-alchemy
```

### 2. Start the app

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_RUN_PORT=5002
export FLASK_RUN_HOST=0.0.0.0
python3 -m flask run
```

Open in your browser: `http://localhost:5002`

> On Codio, use the browser preview for port 5002

---

## 📂 Project Structure

```
Book_Alchemy/
│
├── app.py                # Flask app with routes
├── data_models.py        # SQLAlchemy models (Author, Book)
├── static/
│   └── style.css         # Custom stylesheet
├── templates/
│   ├── home.html
│   ├── add_book.html
│   └── add_author.html
└── data/
    └── library.sqlite    # SQLite database file
```

---

## ✅ To-Do / Improvements

- 📂 Pagination for large book lists
- 📝 Edit forms for books/authors
- 🔐 User authentication (admin panel)
- 🌐 API support for external use

---

## 📃 License

MIT License – feel free to fork and modify ✨
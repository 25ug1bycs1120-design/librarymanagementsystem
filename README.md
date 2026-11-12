# Library Management System

A beginner-friendly library dashboard built with Python, Streamlit, and SQLite. The app creates `library.db` and its `books` table automatically when it starts.

## Requirements

- Python 3.9 or newer
- pip

## Installation

Open a terminal in the project folder and create a virtual environment:

```powershell
python -m venv venv
```

Activate it in PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the required package:

```powershell
python -m pip install -r requirements.txt
```

## Run the application

```powershell
streamlit run app.py
```

Streamlit opens the dashboard in your browser. The SQLite database is stored as `library.db` in the project folder.

## Features

- Add a book with its title, author, category, and available copies.
- View all saved books.
- See the total number of available copies and the book with the most copies.
- See the number of book titles and total available copies for each category.

Titles, authors, and categories must not be blank. Available copies must be a non-negative whole number.

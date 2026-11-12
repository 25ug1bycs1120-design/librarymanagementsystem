import sqlite3

import streamlit as st

import database


st.set_page_config(page_title="Library Management System", page_icon="📚", layout="wide")

st.title("📚 Library Management System")
st.caption("Manage your collection and see what is available at a glance.")

try:
    database.initialize_database()
except sqlite3.Error as error:
    st.error(f"Could not initialize the library database: {error}")
    st.stop()

try:
    books = database.get_all_books()
    total_copies = database.get_total_available_copies()
    most_available_book = database.get_most_available_book()
    category_summary = database.get_category_summary()
except sqlite3.Error as error:
    st.error(f"Could not load library data: {error}")
    st.stop()

metric_columns = st.columns(3)
metric_columns[0].metric("Book titles", len(books))
metric_columns[1].metric("Available copies", total_copies)
if most_available_book:
    metric_columns[2].metric(
        "Most available",
        most_available_book["book_title"],
        f'{most_available_book["available_copies"]} copies',
    )
else:
    metric_columns[2].metric("Most available", "No books yet")

add_tab, books_tab, categories_tab = st.tabs(
    ["Add a book", "View books", "Category summary"]
)

with add_tab:
    st.subheader("Add a book")
    with st.form("add_book_form", clear_on_submit=True):
        title = st.text_input("Book title")
        author = st.text_input("Author")
        category = st.text_input("Category")
        copies = st.number_input("Available copies", min_value=0, step=1, value=1)
        submitted = st.form_submit_button("Save book", type="primary")

    if submitted:
        if not title.strip() or not author.strip() or not category.strip():
            st.error("Please enter a title, author, and category.")
        else:
            try:
                database.add_book(title, author, category, copies)
            except ValueError as error:
                st.error(str(error))
            except sqlite3.Error as error:
                st.error(f"Could not save the book: {error}")
            else:
                st.success(f'"{title.strip()}" was added to the library.')
                st.rerun()

with books_tab:
    st.subheader("All books")
    if books:
        st.dataframe(books, use_container_width=True, hide_index=True)
    else:
        st.info("No books have been added yet.")

with categories_tab:
    st.subheader("Books by category")
    if category_summary:
        st.dataframe(category_summary, use_container_width=True, hide_index=True)
    else:
        st.info("Add a book to see the category summary.")

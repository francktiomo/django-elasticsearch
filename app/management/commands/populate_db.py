import json
from django.core.management.base import BaseCommand
from app.models import Book
import requests
from bs4 import BeautifulSoup
import json
import re

def clean_name(name):
    return re.sub(r",\s*\d{4}-\d{4}", "", name).strip()

def get_books():
    books = []

    for i in range(1, 501):
        book = {}
        # Fetch the page content
        url = f"https://www.gutenberg.org/ebooks/{i}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        print(f"Scraping {url}")

        try:
            # Extract author
            author = soup.find("th", string="Author").find_next_sibling("td").text.strip()
            book['author'] = clean_name(author)

            # Extract title
            title = soup.find("th", string="Title").find_next_sibling("td").text.strip()
            book['title'] = title

            # Extract summary
            summary = soup.find("th", string="Summary").find_next_sibling("td").text.strip()
            book['summary'] = summary[:-45]

            books.append(book)
        except Exception as e:
            continue

    return books

BOOKS = get_books()

class Command(BaseCommand):
    help = "Populates the database with books from books.json."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Started database population process..."))

        # Check if the database already has books
        if Book.objects.exists():
            self.stdout.write(self.style.WARNING("Database already populated. Cancelling operation."))
            return

        # Insert books into the database
        book_count = 0
        for book in BOOKS:
            title = book.get("title", "").strip()
            author = book.get("author", "").strip()
            description = book.get("summary", "").strip()  # Mapping 'summary' to 'description'

            if title and author:
                book = Book.objects.create(title=title, author=author, description=description)
                book.save()
                book_count += 1
                self.stdout.write(self.style.SUCCESS(f"Added: {title} by {author}"))

        self.stdout.write(self.style.SUCCESS(f"Successfully populated the database with {book_count} books!"))

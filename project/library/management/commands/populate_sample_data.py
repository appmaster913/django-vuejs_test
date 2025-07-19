from django.core.management.base import BaseCommand
from django.utils import timezone
from library.models import Student, Book, BookLoan
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Populates the database with sample data for Students, Books, and BookLoans'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate sample data...'))

        # Clear existing data (optional, comment out if you want to append)
        BookLoan.objects.all().delete()
        Book.objects.all().delete()
        Student.objects.all().delete()

        # Sample data for Students
        students_data = [
            {"student_id": "S001", "full_name": "Alice Johnson", "email": "alice@university.com"},
            {"student_id": "S002", "full_name": "Bob Smith", "email": "bob@university.com"},
            {"student_id": "S003", "full_name": "Carol Williams", "email": "carol@university.com"},
            {"student_id": "S004", "full_name": "David Brown", "email": "david@university.com"},
            {"student_id": "S005", "full_name": "Emma Davis", "email": "emma@university.com"},
        ]

        # Create Students
        students = []
        for data in students_data:
            student = Student.objects.create(
                student_id=data["student_id"],
                full_name=data["full_name"],
                email=data["email"],
                enrolled_date=timezone.now().date() - timedelta(days=random.randint(30, 365))
            )
            students.append(student)
            self.stdout.write(self.style.SUCCESS(f'Created student: {student.full_name}'))

        # Sample data for Books
        books_data = [
            {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "isbn": "9780743273565",
                "published_date": "1925-04-10",
                "total_copies": 5,
                "available_copies": 5
            },
            {
                "title": "To Kill a Mockingbird",
                "author": "Harper Lee",
                "isbn": "9780446310789",
                "published_date": "1960-07-11",
                "total_copies": 3,
                "available_copies": 3
            },
            {
                "title": "1984",
                "author": "George Orwell",
                "isbn": "9780451524935",
                "published_date": "1949-06-08",
                "total_copies": 4,
                "available_copies": 4
            },
            {
                "title": "Pride and Prejudice",
                "author": "Jane Austen",
                "isbn": "9780141439518",
                "published_date": "1813-01-28",
                "total_copies": 2,
                "available_copies": 2
            },
            {
                "title": "The Catcher in the Rye",
                "author": "J.D. Salinger",
                "isbn": "9780316769488",
                "published_date": "1951-07-16",
                "total_copies": 3,
                "available_copies": 3
            },
        ]

        # Create Books
        books = []
        for data in books_data:
            book = Book.objects.create(
                title=data["title"],
                author=data["author"],
                isbn=data["isbn"],
                published_date=data["published_date"],
                total_copies=data["total_copies"],
                available_copies=data["available_copies"]
            )
            books.append(book)
            self.stdout.write(self.style.SUCCESS(f'Created book: {book.title}'))

        # Sample data for BookLoans
        # loan_data = [
        #     {
        #         "student": students[0],
        #         "book": books[0],
        #         "loan_date": timezone.now().date() - timedelta(days=20),
        #         "due_date": timezone.now().date() - timedelta(days=6),  # Overdue
        #         "return_date": None
        #     },
        #     {
        #         "student": students[1],
        #         "book": books[1],
        #         "loan_date": timezone.now().date() - timedelta(days=10),
        #         "due_date": timezone.now().date() + timedelta(days=4),
        #         "return_date": None
        #     },
        #     {
        #         "student": students[2],
        #         "book": books[2],
        #         "loan_date": timezone.now().date() - timedelta(days=15),
        #         "due_date": timezone.now().date() - timedelta(days=1),  # Overdue
        #         "return_date": None
        #     },
        #     {
        #         "student": students[3],
        #         "book": books[3],
        #         "loan_date": timezone.now().date() - timedelta(days=5),
        #         "due_date": timezone.now().date() + timedelta(days=9),
        #         "return_date": timezone.now().date() - timedelta(days=2)  # Returned
        #     },
        #     {
        #         "student": students[4],
        #         "book": books[4],
        #         "loan_date": timezone.now().date() - timedelta(days=8),
        #         "due_date": timezone.now().date() + timedelta(days=6),
        #         "return_date": None
        #     },
        # ]

        # Create BookLoans
        # for data in loan_data:
        #     book = data["book"]
        #     if book.available_copies > 0:
        #         book.available_copies -= 1
        #         book.save()
        #         loan = BookLoan.objects.create(
        #             student=data["student"],
        #             book=data["book"],
        #             loan_date=data["loan_date"],
        #             due_date=data["due_date"],
        #             return_date=data["return_date"]
        #         )
        #         self.stdout.write(self.style.SUCCESS(f'Created loan: {loan.student.full_name} - {loan.book.title}'))
        #     else:
        #         self.stdout.write(self.style.WARNING(f'Skipped loan for {data["book"].title} due to no available copies'))

        self.stdout.write(self.style.SUCCESS('Sample data population completed!'))
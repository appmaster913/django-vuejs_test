from django.test import TestCase
from rest_framework.test import APIClient
from library.models import Student, Book, BookLoan
from django.utils import timezone
from datetime import datetime

class BookLoanTests(TestCase):
    def setUp(self):
        Student.objects.all().delete()
        Book.objects.all().delete()
        BookLoan.objects.all().delete()

        self.student1 = Student.objects.create(student_id="S001", full_name="John Doe", email="john@example.com")
        self.student2 = Student.objects.create(student_id="S002", full_name="Jane Smith", email="jane@example.com")
        self.book1 = Book.objects.create(title="The Great Gatsby", author="F. Scott Fitzgerald", isbn="9780743273565", available_copies=3)
        self.book2 = Book.objects.create(title="1984", author="George Orwell", isbn="9780451524935", available_copies=2)
        self.client = APIClient()

    def test_get_students(self):
        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]['student_id'], "S001")
        self.assertEqual(response.json()[1]['full_name'], "Jane Smith")

    def test_get_books(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]['title'], "The Great Gatsby")
        self.assertEqual(response.json()[1]['isbn'], "9780451524935")

    def test_get_bookloans(self):
        BookLoan.objects.create(
            student=self.student1,
            book=self.book1,
            loan_date=datetime.strptime("2025-07-01", "%Y-%m-%d").date(),
            due_date=datetime.strptime("2025-07-08", "%Y-%m-%d").date()
        )
        response = self.client.get('/api/bookloans/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 1)
        self.assertEqual(response.json()['results'][0]['loan_date'], "2025-07-01")
        self.assertEqual(response.json()['results'][0]['due_date'], "2025-07-08")
        self.assertIsNone(response.json()['results'][0]['return_date'])
        self.assertEqual(response.json()['results'][0]['student']['full_name'], "John Doe")
        self.assertEqual(response.json()['results'][0]['book']['title'], "The Great Gatsby")

    def test_create_bookloan(self):
        data = {
            "student_id": self.student1.id,
            "book_id": self.book1.id,
            "loan_date": "2025-07-17",
            "due_date": "2025-07-24",
            "return_date": None
        }
        response = self.client.post('/api/bookloans/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(BookLoan.objects.count(), 1)
        loan = BookLoan.objects.first()
        self.assertEqual(loan.loan_date.strftime("%Y-%m-%d"), "2025-07-17")
        self.assertEqual(loan.due_date.strftime("%Y-%m-%d"), "2025-07-24")
        self.assertIsNone(loan.return_date)
        self.assertEqual(Book.objects.get(id=self.book1.id).available_copies, 2)

    def test_create_bookloan_default_loan_date(self):
        data = {
            "student_id": self.student1.id,
            "book_id": self.book1.id,
            "due_date": "2025-07-24",
            "return_date": None
        }
        response = self.client.post('/api/bookloans/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(BookLoan.objects.count(), 1)
        loan = BookLoan.objects.first()
        self.assertEqual(loan.loan_date.strftime("%Y-%m-%d"), "2025-07-17")
        self.assertEqual(loan.due_date.strftime("%Y-%m-%d"), "2025-07-24")
        self.assertIsNone(loan.return_date)
        self.assertEqual(Book.objects.get(id=self.book1.id).available_copies, 2)

    def test_create_bookloan_no_copies(self):
        self.book1.available_copies = 0
        self.book1.save()
        data = {
            "student_id": self.student1.id,
            "book_id": self.book1.id,
            "loan_date": "2025-07-17",
            "due_date": "2025-07-24",
            "return_date": None
        }
        response = self.client.post('/api/bookloans/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("No copies available", str(response.json()))

    def test_update_bookloan(self):
        loan = BookLoan.objects.create(
            student=self.student1,
            book=self.book1,
            loan_date=datetime.strptime("2025-07-01", "%Y-%m-%d").date(),
            due_date=datetime.strptime("2025-07-08", "%Y-%m-%d").date()
        )
        data = {
            "student_id": self.student2.id,
            "book_id": self.book2.id,
            "loan_date": "2025-07-01",
            "due_date": "2025-07-08",
            "return_date": "2025-07-07"
        }
        response = self.client.put(f'/api/bookloans/{loan.id}/', data, format='json')
        self.assertEqual(response.status_code, 200)
        loan.refresh_from_db()
        self.assertEqual(loan.student.id, self.student2.id)
        self.assertEqual(loan.book.id, self.book2.id)
        self.assertEqual(loan.return_date.strftime("%Y-%m-%d"), "2025-07-07")
        self.assertEqual(Book.objects.get(id=self.book1.id).available_copies, 3)
        self.assertEqual(Book.objects.get(id=self.book2.id).available_copies, 1)

    def test_delete_bookloan(self):
        loan = BookLoan.objects.create(
            student=self.student1,
            book=self.book1,
            loan_date=datetime.strptime("2025-07-01", "%Y-%m-%d").date(),
            due_date=datetime.strptime("2025-07-08", "%Y-%m-%d").date()
        )
        response = self.client.delete(f'/api/bookloans/{loan.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(BookLoan.objects.count(), 0)
        self.assertEqual(Book.objects.get(id=self.book1.id).available_copies, 3)
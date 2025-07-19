from django.db import models
from django.utils import timezone

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    enrolled_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.full_name} ({self.student_id})"

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField(null=True, blank=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.title} by {self.author} (Total: {self.total_copies}, Available: {self.available_copies})"

    class Meta:
        indexes = [models.Index(fields=['isbn'])]

class BookLoan(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='loans')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='loans')
    loan_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'book', 'loan_date')
        ordering = ['-loan_date']
        indexes = [
            models.Index(fields=['student', 'book', 'return_date']),
            models.Index(fields=['loan_date']),
            models.Index(fields=['return_date']),
        ]

    def is_overdue(self):
        return not self.return_date and timezone.now().date() > self.due_date

    def __str__(self):
        return f"{self.student.full_name} - {self.book.title} (Loaned: {self.loan_date})"
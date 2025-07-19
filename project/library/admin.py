from django.contrib import admin
from .models import BookLoan, Student, Book

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'full_name', 'email', 'enrolled_date')
    search_fields = ('student_id', 'full_name', 'email')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'total_copies', 'available_copies')
    search_fields = ('title', 'author', 'isbn')
    list_filter = ('published_date',)

@admin.register(BookLoan)
class BookLoanAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'loan_date', 'due_date', 'return_date', 'is_overdue')
    search_fields = ('student__full_name', 'book__title')
    list_filter = ('loan_date', 'due_date', 'return_date')
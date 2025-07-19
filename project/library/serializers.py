from rest_framework import serializers
from .models import Student, Book, BookLoan
from django.utils import timezone
from django.db import transaction
from datetime import timedelta

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'student_id', 'full_name', 'email']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'total_copies', 'available_copies']

class BookLoanSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    book = BookSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), source='student')
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), source='book')
    loan_date = serializers.DateField(default=timezone.now().date)
    due_date = serializers.DateField()
    return_date = serializers.DateField(allow_null=True, required=False)

    class Meta:
        model = BookLoan
        fields = ['id', 'student', 'book', 'student_id', 'book_id', 'loan_date', 'due_date', 'return_date']

    def validate(self, data):
        loan_date = data.get('loan_date', timezone.now().date())
        due_date = data.get('due_date')
        book = data.get('book')
        student = data.get('student')

        # Date validations
        if due_date < loan_date:
            raise serializers.ValidationError({"due_date": "Due date must be on or after loan date."})
        if due_date > loan_date + timedelta(days=30):
            raise serializers.ValidationError({"due_date": "Due date cannot be more than 30 days from loan date."})
        if data.get('return_date') and data['return_date'] < loan_date:
            raise serializers.ValidationError({"return_date": "Return date must be on or after loan date."})

        # Book availability check (only for new loans or if book changes)
        if not self.instance or self.instance.book != book:
            if book.available_copies <= 0:
                raise serializers.ValidationError({"book": f"No copies available for {book.title}."})
        print("validate data:", data)
        # Active loan check (only for new loans or if student/book changes)
        if not self.instance or self.instance.student != student or self.instance.book != book:
            print(BookLoan.objects.filter(student=student, book=book, return_date__isnull=True).exists())
            if BookLoan.objects.filter(student=student, book=book, return_date__isnull=True).exists():
                print("Active loan exists for student and book")
                raise serializers.ValidationError({"non_field_errors": f"{student.full_name} already has an active loan for {book.title}."})
        print(data)
        return data

    @transaction.atomic
    def create(self, validated_data):
        book = validated_data['book']
        if book.available_copies <= 0:
            raise serializers.ValidationError({"book": f"No copies available for {book.title}."})
        book.available_copies -= 1
        book.save()
        return super().create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        old_book = instance.book
        new_book = validated_data.get('book', old_book)
        old_return_date = instance.return_date
        new_return_date = validated_data.get('return_date', old_return_date)

        if new_book != old_book:
            old_book.available_copies += 1
            old_book.save()
            if new_book.available_copies <= 0:
                raise serializers.ValidationError({"book": f"No copies available for {new_book.title}."})
            new_book.available_copies -= 1
            new_book.save()
        elif not old_return_date and new_return_date:
            old_book.available_copies += 1
            old_book.save()
        elif old_return_date and not new_return_date:
            if old_book.available_copies <= 0:
                raise serializers.ValidationError({"book": f"No copies available for {old_book.title}."})
            old_book.available_copies -= 1
            old_book.save()

        return super().update(instance, validated_data)
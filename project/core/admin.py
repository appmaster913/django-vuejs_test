from django.contrib import admin
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from library.models import BookLoan, Student, Book
from library.serializers import BookLoanSerializer, StudentSerializer, BookSerializer
from django.utils import timezone

class BookLoanAdminViewSet(viewsets.ModelViewSet):
    queryset = BookLoan.objects.all()
    serializer_class = BookLoanSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['loan_date', 'return_date', 'student', 'book']
    search_fields = ['student__full_name', 'book__title']
    pagination_class = PageNumberPagination

    @action(detail=False, methods=['get'], pagination_class=None)
    def check_active_loan(self, request):
        student_id = request.query_params.get('student')
        book_id = request.query_params.get('book')
        loans = BookLoan.objects.filter(
            student_id=student_id,
            book_id=book_id,
            return_date__isnull=True
        )
        serializer = self.get_serializer(loans, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def bulk_return(self, request):
        loan_ids = request.data.get('loan_ids', [])
        loans = BookLoan.objects.filter(id__in=loan_ids, return_date__isnull=True)
        updated_count = 0
        for loan in loans:
            loan.return_date = timezone.now().date()
            loan.book.available_copies += 1
            loan.book.save()
            loan.save()
            updated_count += 1
        return Response({"status": f"{updated_count} loans marked as returned"})

class StudentAdminViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class BookAdminViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
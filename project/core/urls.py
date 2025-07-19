from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from .admin import BookLoanAdminViewSet, StudentAdminViewSet, BookAdminViewSet

router = DefaultRouter()
router.register(r'bookloans', BookLoanAdminViewSet, basename='bookloan')
router.register(r'students', StudentAdminViewSet, basename='student')
router.register(r'books', BookAdminViewSet, basename='book')

urlpatterns = [
    path('api/', include(router.urls)),
    path('', TemplateView.as_view(template_name='index.html'), name='admin_panel'),
]
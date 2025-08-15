from rest_framework import viewsets

from books.models import Books
from books.serializers import BooksSerializer


# Create your views here.
class BooksViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer

    def get_queryset(self):
        autor = self.request.query_params.get("author")
        publish_date_after = self.request.query_params.get("publish_date")
        publish_date_before = self.request.query_params.get("publish_date")
        if autor:
            queryset = Books.objects.filter(author=autor)
        elif publish_date_after:
            queryset = Books.objects.filter(published_date__lt=publish_date_after)
        elif publish_date_before:
            queryset = Books.objects.filter(published_date__gt=publish_date_before)
        else:
            queryset = Books.objects.all()
        return queryset

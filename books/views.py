from rest_framework import viewsets

from books.models import Books
from books.serializers import BooksSerializer


# Create your views here.
class BooksViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer

    def get_queryset(self):
        queryset = Books.objects.all()
        autor = self.request.query_params.get("author")
        publish_date_after = self.request.query_params.get("publish_date_after")
        publish_date_before = self.request.query_params.get("publish_date_before")
        if autor:
            queryset = queryset.filter(author=autor)
        if publish_date_after:
            queryset = queryset.filter(published_date__gt=publish_date_after)
            # queryset = Books.objects.filter(published_date__gt=publish_date_after)
        if publish_date_before:
            queryset = queryset.filter(published_date__lt=publish_date_after)

            # queryset = Books.objects.filter(published_date__lt=publish_date_before)

        return queryset

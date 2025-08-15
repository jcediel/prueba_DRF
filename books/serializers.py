from rest_framework import serializers
from django.core.validators import RegexValidator
from .models import Books
from datetime import date


class BooksSerializer(serializers.ModelSerializer):

    isbn = serializers.IntegerField(
        validators=[
            RegexValidator(
                regex=r"^\d{10}$", message="El valor de isbn debe ser de 10 digitos"
            )
        ]
    )

    class Meta:
        model = Books
        fields = ["title", "author", "published_date", "isbn", "pages"]
        read_only_fields = [
            "isbn",
        ]

    def validate_published_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("La fecha no puede ser futura")
        return value

    def validate_isbn(self, value):
        if Books.objects.filter(isbn=value).exists():
            raise serializers.ValidationError("El ISBN ya existe")
        return value

    def pages(self, value):
        if value < 0:
            raise serializers.ValidationError("Las paginas no pueden ser negativas")
        return value

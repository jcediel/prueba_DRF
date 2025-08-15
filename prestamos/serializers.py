from rest_framework import serializers
from .models import Member, Loan


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ["name", "email", "role"]


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ["member", "book", "start_date", "end_date", "returned_at"]
        read_only_fields = ["returned_at"]

    def end_date(self, value):
        if value < self.instance.start_date:
            raise serializers.ValidationError(
                "La fecha de finalizacion no puede ser anterior a la de inicio"
            )
        return value

    def book(self, value):
        if Loan.objects.filter(book=value, returned_at=None).exists():
            raise serializers.ValidationError("El libro ya esta prestado")
        return value

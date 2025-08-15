from rest_framework import serializers
from .models import Loan, Member, Payment, Penalty, Reservation
from decimal import Decimal
from django.db import transaction


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


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["id", "book", "member", "status", "created_at"]
        read_only_fields = ["created_at", "status"]

    def validate(self, data):
        member = data.get("member") or self.instance.member
        book = data.get("book") or self.instance.book

        has_active_loan = Loan.objects.filter(
            member=member, book=book, returned_at__isnull=True
        ).exists()

        if has_active_loan:
            raise serializers.ValidationError("El usuario ya tiene un prestamo activo")

        return data


class ReservationCancelSerializer(serializers.ModelSerializer):
    confirm = serializers.BooleanField(default=True)

    def save(self, **kwargs):
        reservation: Reservation = self.context["reservation"]
        if reservation.status != Reservation.Status.PENDING:
            raise serializers.ValidationError("La reserva no esta pendiente")
        reservation.status = Reservation.Status.CANCELLED
        reservation.save(update_fields=["status"])
        return reservation


class PenaltySerializer(serializers.ModelSerializer):
    class Meta:
        model = Penalty
        fields = ["loan", "rate_per_day", "days_late", "amount_cached", "status"]


class PaymentSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "member", "amount", "paid_at", "external_ref", "penalty"]
        read_only_fields = [
            "paid_at",
        ]

    def validate(self, data):
        penalty: Penalty = data["penalty"]
        if penalty.status != Penalty.Status.PENDING:
            raise serializers.ValidationError("La penalidad no esta pendiente")
        with transaction.atomic():
            penality = Penalty.objects.select_for_update().get(pk=penalty.pk)
            penality.calc_amount()
            penalty.status = Penalty.Status.PAID
            penalty.save(update_fields=["amount_cached"])
            if Decimal(data["amount"]) != penalty.amount_cached:
                raise serializers.ValidationError(
                    "El monto de pago no coincide con la penalidad"
                )
        return data

    def create(self, validated):

        external_ref = validated["external_ref"]
        penalty = validated["penalty"]
        amount = validated["amount"]
        member = validated["member"]

        with transaction.atomic():
            pen = Penalty.objects.select_for_update().get(pk=penalty.pk)
            pen.calc_amount()
            pen.save(update_fields=["amount_cached"])

            obj, created = Payment.objects.get_or_create(
                external_ref=external_ref,
                defaults={"member": member, "amount": amount, "penalty": pen},
            )
            if not created:
                if (
                    obj.penalty_id != pen.id
                    or obj.amount != amount
                    or obj.member_id != member.id
                ):
                    raise serializers.ValidationError("El pago ya existe")

                return obj

            if obj.amount != pen.amount_cached:
                raise serializers.ValidationError(
                    "El monto de pago no coincide con la penalidad"
                )

            if pen.status != Penalty.Status.PENDING:
                raise serializers.ValidationError(
                    "La multa ya no esta en estado pending"
                )
            pen.status = Penalty.Status.PAID
            pen.save(update_fields=["status"])
            return obj

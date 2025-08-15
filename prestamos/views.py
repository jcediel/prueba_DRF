from datetime import datetime
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from prestamos.permissions import IsStaffOrBasic, IsStaffOrSelfbasic
from .models import Loan, Member, Penalty, Reservation
from .serializers import (
    LoanSerializer,
    MemberSerializer,
    PenaltySerializer,
    ReservationCancelSerializer,
    ReservationSerializer,
    PaymentSeralizer,
)
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class MembersViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated, IsStaffOrSelfbasic]

    def get_queryset(self):
        if self.request.user.role == "staff":
            return self.queryset
        return Member.objects.filter(id=self.request.user.id)

    def perform_create(self, serializer):
        if self.request.user.role != "staff":
            serializer.save(role="basic")
        else:
            serializer.save()


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all().select_related("member", "book")
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated, IsStaffOrBasic]

    def get_queryset(self):
        query_set = Loan.objects.all()
        member_id = self.request.query_params.get("member_id")
        book_id = self.request.query_params.get("book_id")
        active = self.request.query_params.get("active")
        user = self.request.user
        if user.role == "basic":
            query_set = query_set.filter(member=user)

        if member_id:
            query_set = query_set.filter(member_id=member_id)
        elif book_id:
            query_set = query_set.filter(book_id=book_id)
        elif active is not None:
            if active.lower() == "true":
                queryset = queryset.filter(returned_at__isnull=True)
            elif active.lower() == "false":
                queryset = queryset.filter(returned_at__isnull=False)

        return query_set

    def perform_create(self, serializer):
        if self.request.user.role == "basic":
            serializer.save(member=self.request.user)
        else:
            serializer.save()

    @action(detail=True, methods=["post"])
    def return_loan(self, request, pk=None):
        loan = Loan.objects.get(pk=pk)
        if loan.returned_at:
            return Response(
                "El prestamo ya fue devuelto", status=status.HTTP_400_BAD_REQUEST
            )
        loan.returned_at = datetime.now()
        loan.save()
        return Response("prestamo devuelto con exito", status=status.HTTP_200_OK)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all().select_related("member", "book")
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated, IsStaffOrBasic]
    ordering_fields = ["created_at"]

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        serializer = ReservationCancelSerializer(
            data=request.data or {"confirm": True}, context={"reservation": reservation}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Reserva cancelada con exito", status=status.HTTP_200_OK)


class PenaltyViewSet(viewsets.ModelViewSet):
    queryset = Penalty.objects.all().select_related(
        "loan", "loan__member", "loan__book"
    )
    serializer_class = PenaltySerializer
    permission_classes = [IsAuthenticated, IsStaffOrBasic]

    @action(detail=True, methods=["post"])
    def pay(self, request, pk=None):
        penalty = self.get_object()
        serializer = PaymentSeralizer(
            data=penalty,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Penalizacion pagada con exito", status=status.HTTP_200_OK)

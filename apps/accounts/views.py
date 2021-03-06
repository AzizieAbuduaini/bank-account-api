from rest_framework import status
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from .serializer import ThunesUserAccountSerializer, ThunesUserTransactionSerializer, ThunesUserAccountTopupSerializer
from rest_framework.generics import CreateAPIView, ListCreateAPIView, ListAPIView
from .models import UserAccount, Transaction
from rest_framework.response import Response
from apps.accounts.utils.pagination import PaginationWithDefaults
# Create your views here.


class ThunesUserAccountAPI(CreateAPIView):
    permission_required = (IsAuthenticated,)
    serializer_class = ThunesUserAccountSerializer

    def get(self, request):
        user_id = request.user.id
        user_account = UserAccount.objects.filter(user_id=user_id).first()
        serializer = ThunesUserAccountSerializer(user_account)
        return Response(serializer.data)


class ThunesUserAccountTopupAPI(CreateAPIView):
    permission_required = (IsAuthenticated,)
    serializer_class = ThunesUserAccountTopupSerializer



class ThunesTransactionAPI(ListCreateAPIView):
    permission_required = [IsAuthenticated]
    serializer_class = ThunesUserTransactionSerializer
    pagination_class = PaginationWithDefaults

    def get_queryset(self):
        # get all transaction
        transactions = Transaction.objects.filter(Q(sender_id=self.request.user.id) | Q(
            receiver_id=self.request.user.id))
        return transactions
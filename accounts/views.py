from rest_framework import status
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from .serializer import ThunesUserAccountSerializer, ThunesUserTransactionSerializer
from rest_framework.generics import CreateAPIView, ListCreateAPIView, ListAPIView
from .models import UserAccount, Transaction
from rest_framework.response import Response
from rest_framework.views import  APIView
# Create your views here.


class ThunesUserAccountAPI(CreateAPIView):
    permission_required = [IsAuthenticated]
    serializer_class = ThunesUserAccountSerializer

    def get(self, request):
        user_id = request.user.id
        user_account = UserAccount.objects.filter(user_id=user_id).first()
        serializer = ThunesUserAccountSerializer(user_account, context={'request': request})
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.error)


class ThunesTransactionAPI(ListAPIView):
    permission_required = [IsAuthenticated]
    serializer_class = ThunesUserTransactionSerializer

    def get_queryset(self):
        # get all transaction
        transactions = Transaction.objects.filter(Q(sender_id=self.request.user.id) | Q(
            receiver_id=self.request.user.id))
        return transactions




import random
import string
from django.db import transaction
from rest_framework import serializers
from .models import UserAccount, Transaction, TransactionStatuses, TransactionTypes


class ThunesUserAccountSerializer(serializers.Serializer):
    name = serializers.CharField()

    def validate_name(self, name):
        if UserAccount.objects.filter(name=name).exists():
            raise serializers.ValidationError(
                detail='{} is already taken, please choice diffrent name.'.format(name),
                code=400)
        request = self.context.get('request')
        if UserAccount.objects.filter(user_id=request.user.id).exists():
            raise serializers.ValidationError(detail='User has account.', code=400)
        return name

    def get_name(self, name):
        return name

    def get_id(self, instance: UserAccount):
        return str(instance.id)

    @transaction.atomic()
    def create(self, validated_data):
        request = self.context.get('request')
        instance = UserAccount.objects.create(**{
            'user_id': request.user.id,
            'is_active': True,
            'account': int(''.join(random.choices(string.digits, k=12))),
            'name': validated_data.get('name'),
            'balance': 0
        })
        return instance

class ThunesUserTransactionSerializer(serializers.Serializer):
    amount =  serializers.DecimalField(max_digits=15, decimal_places=4)
    receiver_account_number = serializers.IntegerField()

    def validate_amount(self, amount):
        if amount <= 0:
            raise serializers.ValidationError(details='Amount can be negative', code=401)
        request = self.context.get('request')
        user_accounts = UserAccount.objects.filter(user_id=request.user.id)
        if not user_accounts:
            raise serializers.ValidationError(details='User account not found, please try again', code=401)

        if user_accounts.first() and user_accounts.first().blance < amount:
            raise serializers.ValidationError(details='Insufficient balance', code=401)

        return amount

    def validate_receiver_account_number(self, receiver_account_number):
        if not UserAccount.objects.filter(account=receiver_account_number):
            raise serializers.ValidationError(details='Receiver account not found', code=404)

        return receiver_account_number

    @transaction.atomic()
    def create(self, validated_data):
        request = self.context.get('request')
        kwargs = {
            'sender_id': request.user.id,
            'receiver_id': UserAccount.objects.filter(
                account=validated_data.get('receiver_account_number')).first().user_id,
            'status': TransactionStatuses.COMPLETED,
            'type': TransactionTypes.ACCOUNT,
            'is_send': True
        }

        instance = Transaction.objects.create(**kwargs)
        return instance
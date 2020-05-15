import random
import string
from django.db import transaction
from rest_framework import serializers
from .models import UserAccount, Transaction, TransactionStatuses, TransactionTypes


class ThunesUserAccountSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    name = serializers.CharField()
    acount = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()
    last_modified_timestamp = serializers.SerializerMethodField()

    def validate_name(self, name):
        if UserAccount.objects.filter(name=name).exists():
            raise serializers.ValidationError(
                detail='{} is already taken.'.format(name),
                code=400)
        request = self.context.get('request')
        if not request.user.id:
            raise serializers.ValidationError(detail='Permission denied', code=401)

        if UserAccount.objects.filter(user_id=request.user.id).exists():
            raise serializers.ValidationError(detail='This user has an account already.', code=400)
        return name

    def get_name(self, name):
        return name

    def get_balance(self, instance: UserAccount):
        return instance.balance

    def get_acount(self, instance: UserAccount):
        return instance.account

    def get_id(self, instance: UserAccount):
        return str(instance.id)

    def get_last_modified_timestamp(self, instance: UserAccount):
        return instance.last_modified_timestamp

    @transaction.atomic()
    def create(self, validated_data):
        request = self.context.get('request')
        instance = UserAccount.objects.create(**{
            'user_id': request.user.id,
            'is_active': True,
            'account': int(''.join(random.choices(string.digits, k=8))),
            'name': validated_data.get('name'),
            'balance': 0
        })
        return instance


class ThunesUserAccountTopupSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    balance =  serializers.DecimalField(max_digits=15, decimal_places=4)
    last_modified_timestamp = serializers.SerializerMethodField()

    def validate_amount(self, balance):
  
        request = self.context.get('request')
        if not request.user.id:
            raise serializers.ValidationError(detail='Permission denied', code=401)

        if not UserAccount.objects.filter(user_id=request.user.id).exists():
            raise serializers.ValidationError('You do not have account please create one.')
        
        if amount <= 0:
            raise serializers.ValidationError('Please provide valid topup amount.')

        return amount

    def get_id(self, id):
        return str(id)

    def get_last_modified_timestamp(self, instance: UserAccount):
        return instance.last_modified_timestamp

    @transaction.atomic()
    def create(self, validated_data):
        print('validated_data {}'.format(validated_data))
        request = self.context.get('request')
        instance = UserAccount.objects.filter(user_id=request.user.id).first()
        instance.balance = instance.balance + validated_data.get('balance')
        instance.save()
        return instance


class ThunesUserTransactionSerializer(serializers.Serializer):
    amount =  serializers.DecimalField(max_digits=15, decimal_places=4)
    receiver = serializers.IntegerField()
    last_modified_timestamp = serializers.SerializerMethodField()

    def validate_amount(self, amount):
        if amount <= 0:
            raise serializers.ValidationError(details='Amount can be negative', code=401)
        request = self.context.get('request')
        user_accounts = UserAccount.objects.filter(user_id=request.user.id)
        if not user_accounts:
            raise serializers.ValidationError('User account not found, please try again')

        if user_accounts.first() and user_accounts.first().balance < amount:
            raise serializers.ValidationError('Insufficient balance')

        return amount

    def validate_receiver_account_number(self, receiver):
        if not UserAccount.objects.filter(receiver_id=receiver):
            raise serializers.ValidationError('Receiver account not found')

        return receiver

    def get_last_modified_timestamp(self, instance: Transaction):
        return instance.last_modified_timestamp

    @transaction.atomic()
    def create(self, validated_data):
        request = self.context.get('request')
        kwargs = {
            'sender_id': request.user.id,
            'owner_id': request.user.id,
            'amount': validated_data.get('amount'),
            'receiver_id': receiver,
            'status': TransactionStatuses.COMPLETED,
            'type': TransactionTypes.ACCOUNT
        }

        instance = Transaction.objects.create(**kwargs)
        return instance
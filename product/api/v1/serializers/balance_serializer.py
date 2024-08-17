from rest_framework import serializers
from users.models import Balance

class UserBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ['user', 'balance']
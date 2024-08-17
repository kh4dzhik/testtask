from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from users.models import Balance
from api.v1.serializers.balance_serializer import UserBalanceSerializer



class UserBalanceViewSet(viewsets.ModelViewSet):
    queryset = Balance.objects.all()
    serializer_class = UserBalanceSerializer
    permission_classes = [IsAdminUser]
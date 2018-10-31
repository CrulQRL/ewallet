from .models import Customer
from rest_framework import serializers
from .services import is_valid_user_id

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('user_id', 'nama', 'ip')

    def validate(self, data):
        ip = is_valid_user_id(data['user_id'])
        if ip:
            data['ip'] = ip
            return data
        else:
            raise ValueError('Invalid user_id, not include in quorum')

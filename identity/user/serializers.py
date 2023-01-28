from .models import MyUser
from rest_framework import serializers


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        # fields = '__all__'
        exclude = ('groups', 'user_permissions')
        read_only_fields = ('is_superuser', 'is_staff',
                            'created_at', 'last_login')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = MyUser.objects.create_user(**validated_data)
        return user

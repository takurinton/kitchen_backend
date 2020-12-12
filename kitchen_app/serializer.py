from rest_framework import serializers
from .models import User

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('email', 'password', )

    def create(self, data):
        email = self.data['email']
        password = data['password']
        return User.objects.create_user(email=email, password=password)
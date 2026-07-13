from rest_framework import serializers
from .models import Usuario
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'cedula', 'telefono', 'direccion', 'rol']
        extra_kwargs = {'password': {'write_only': True}}

        # Uses create_user to encrypt the password
    def create(self, validated_data):
        user = Usuario.objects.create_user(**validated_data)
        return user
    
class CustomTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        data['rol'] = self.user.rol
        data['username'] = self.user.username
        return data
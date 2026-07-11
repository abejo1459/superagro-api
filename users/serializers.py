from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'cedula', 'telefono', 'direccion', 'rol']
        extra_kwargs = {'password': {'write_only': True}} # La contraseña no se mostrará al consultar

    def create(self, validated_data):
        # Usamos create_user para que encripte la contraseña automáticamente
        user = Usuario.objects.create_user(**validated_data)
        return user
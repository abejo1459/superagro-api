from rest_framework import viewsets
from .models import Usuario
from .serializers import UsuarioSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer
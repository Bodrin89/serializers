
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from users.models import User, Location
from users.serializers import PersonCreateSerializer, LocationSerializer, PersonListSerializer, PersonDetailSerializer, \
    PersonUpdateSerializer, PersonDestroySerializer


class UserListView(ListAPIView):
    """Получение всех пользователей"""
    queryset = User.objects.all()
    serializer_class = PersonListSerializer


class UserDetailView(RetrieveAPIView):
    """Получение пользователей по id"""
    queryset = User.objects.all()
    serializer_class = PersonDetailSerializer


class UserCreateView(CreateAPIView):
    """Создание пользователя"""
    queryset = User.objects.all()
    serializer_class = PersonCreateSerializer


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = PersonUpdateSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = PersonDestroySerializer


class LocationsViewSet(ModelViewSet):
    """CRUD для локаций"""
    queryset = Location.objects.all()
    serializer_class = LocationSerializer



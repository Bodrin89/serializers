
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from users.models import Person, Location
from users.serializers import PersonCreateSerializer, LocationSerializer, PersonListSerializer, PersonDetailSerializer, \
    PersonUpdateSerializer, PersonDestroySerializer


class UserListView(ListAPIView):
    """Получение всех пользователей"""
    queryset = Person.objects.all()
    serializer_class = PersonListSerializer


class UserDetailView(RetrieveAPIView):
    """Получение пользователей по id"""
    queryset = Person.objects.all()
    serializer_class = PersonDetailSerializer


class UserCreateView(CreateAPIView):
    """Создание пользователя"""
    queryset = Person.objects.all()
    serializer_class = PersonCreateSerializer


class UserUpdateView(UpdateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonUpdateSerializer


class UserDeleteView(DestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonDestroySerializer


class LocationsViewSet(ModelViewSet):
    """CRUD для локаций"""
    queryset = Location.objects.all()
    serializer_class = LocationSerializer



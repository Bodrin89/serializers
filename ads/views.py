from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from ads.models import Ad, Category

import json

from ads.permissions import CheckAuthorPermission
from ads.serializers import AdListSerializer, AdDetailSerializer, AdUpdateSerializer, AdDeleteSerializer
from users.models import User


def index(request):
    return JsonResponse({"status": "ok"})


class AdListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdListSerializer

    def get(self, request, *args, **kwargs):
        """Получение всех объявлений, по id категории, по вхождению слова в строку, по локации"""
        categories = request.GET.getlist('cat', None)
        if categories:
            cat_q = None
            for cat in categories:
                if cat_q is None:
                    cat_q = Q(category__in=cat)
                else:
                    cat_q |= Q(category__in=cat)
            if cat_q:
                self.queryset = self.queryset.filter(cat_q)

        search_text = request.GET.get('text', None)
        if search_text:
            self.queryset = self.queryset.filter(description__icontains=search_text)

        location = request.GET.get('location', None)
        if location:
            user = User.objects.all().filter(location__name__icontains=location)
            self.queryset = self.queryset.filter(author_id__in=user)

        price_from = request.GET.get('price_from', None)
        price_to = request.GET.get('price_to', None)
        if price_from and price_to:
            price = [i for i in range(int(price_from), int(price_to))]
            self.queryset = self.queryset.filter(price__in=price)

        return super().get(request, *args, **kwargs)


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer
    permission_classes = [IsAuthenticated]


class AdUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdUpdateSerializer
    permission_classes = [CheckAuthorPermission]


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ['name', 'price', 'description', 'image', 'is_published', 'author_id', 'category_id']


    def post(self, request, *args, **kwargs):
        """Создание объявления"""
        ad_data = json.loads(request.body)

        new_ad = Ad.objects.create(
            name=ad_data['name'],
            price=ad_data['price'],
            description=ad_data['description'],
            is_published=ad_data['is_published']
        )
        new_ad.image = ad_data.get('image', None)
        new_ad.author = get_object_or_404(User, pk=ad_data['author'])
        new_ad.category = get_object_or_404(Category, pk=ad_data['category'])

        new_ad.save()
        response = {
            "name": new_ad.name,
            "price": new_ad.price,
            "description": new_ad.description,
            "image": None,
            "is_published": new_ad.is_published,
            "author": new_ad.author_id,
            "category": new_ad.category_id
        }
        if new_ad.image:
            response['image'] = new_ad.image.url
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdImageLoadView(UpdateView):
    model = Ad
    fields = ['name', 'price', 'description', 'image', 'is_published', 'author_id', 'category_id']

    def post(self, request, *args, **kwargs):
        """Добавление картинки"""
        self.object = self.get_object()

        self.object.image = request.FILES['image']
        self.object.save()
        return JsonResponse({
            "id": self.object.pk,
            "name": self.object.name,
            "image": self.object.image.url
        })


class AdDeleteView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDeleteSerializer
    permission_classes = [CheckAuthorPermission]


class CategoryDetailView(DetailView):
    model = Category

    def get(self, *args, **kwargs):
        """Получение категории по id"""
        categories = self.get_object()
        return JsonResponse({
            "id": categories.pk,
            "name": categories.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CatListView(View):

    def get(self, request):
        """Получение всех категорий"""

        cat_list = Category.objects.all()
        cat_list = cat_list.order_by('name')
        return JsonResponse([
            {"id": i.pk, "name": i.name}
            for i in cat_list], safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CatCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        """Создание категории"""
        cat_data = json.loads(request.body)

        new_cat = Category.objects.create(name=cat_data['name'])
        return JsonResponse({"name": new_cat.name})


@method_decorator(csrf_exempt, name='dispatch')
class CatUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        """Обновление категории"""
        super().post(self, request, *args, **kwargs)

        cat_data = json.loads(request.body)

        self.object.name = cat_data.get('name', self.object.name)
        self.object.save()
        return JsonResponse({"name": self.object.name})


@method_decorator(csrf_exempt, name='dispatch')
class CatDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        """Удаление категории"""
        super().delete(self, request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)

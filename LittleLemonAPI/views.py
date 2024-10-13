from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from .serializers import MenuItemSerializer
from .models import MenuItem
from rest_framework.response import Response 
from rest_framework.decorators import api_view 
from rest_framework import generics, status
from django.core.cache import cache
from rest_framework.pagination import PageNumberPagination



class CustomPagination(PageNumberPagination):
    page_size = 2  
    page_size_query_param = 'page_size' 
    max_page_size = 3

class MenuItemsView(generics.ListCreateAPIView):
    serializer_class = MenuItemSerializer
    pagination_class = CustomPagination
    def get_queryset(self):
        # محاولة الحصول على البيانات من الكاش أولاً
        queryset = cache.get('menu_items')

        if queryset is None:
            # إذا لم يكن موجودًا في الكاش، قم بجلب البيانات من قاعدة البيانات
            queryset = MenuItem.objects.select_related("category").all()
            # تخزين البيانات في الكاش لمدة 60 ثانية
            cache.set('menu_items', queryset, 60)

        
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)

        search = self.request.query_params.get('search', None)
        if search is not None:
            queryset = queryset.filter(name__icontains=search)

        to_price = self.request.query_params.get('to_price', None)
        if to_price is not None:
            queryset = queryset.filter(price__lte=to_price)

        ordering = self.request.query_params.get('ordering', None)
        if ordering is not None:
            ordering_fields =ordering.split(",")
            queryset = queryset.order_by(*ordering_fields)

        return queryset

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     page = self.paginate_queryset(queryset)

    #     if page is not None:
    #         serialized_items = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serialized_items.data)

    #     serialized_items = self.get_serializer(queryset, many=True)
    #     return Response(serialized_items.data, status=status.HTTP_200_OK)

    # def create(self, request, *args, **kwargs):
    #     # معالجة إنشاء عنصر جديد
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)

    #     # عند إضافة عنصر جديد، يمكن أن يتم تحديث الكاش
    #     cache.delete('menu_items')  # حذف الكاش عند إضافة عنصر جديد

    #     return Response(serializer.data, status=status.HTTP_201_CREATED)



class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import MenuItem
from .serializers import MenuItemSerializer

@api_view(['GET', 'POST'])
def menu_items(request):
    items = MenuItem.objects.all()
    category_name = request.query_params.get('category')  
    if category_name:
        items = items.filter(category__title=category_name)

    serialized_items = MenuItemSerializer(items, many=True)
    return Response(serialized_items.data, status=status.HTTP_200_OK)


from .models import Category 
from .serializers import CategorySerializer


@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category,pk=pk)
    serialized_category = CategorySerializer(category)
    return Response(serialized_category.data) 
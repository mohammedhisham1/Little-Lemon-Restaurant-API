from rest_framework import serializers
from.models import MenuItem , Category



class CategorySerializer(serializers.ModelSerializer):
    class Meta: 
        model = Category
        fields = "__all__"


class MenuItemSerializer(serializers.ModelSerializer):
    # category = CategorySerializer()
    category = serializers.HyperlinkedRelatedField(
        queryset = Category.objects.all(),
        view_name='category-detail'
)
    class Meta: 
        model = MenuItem
        fields=['id','name', 'price', 'inventory','category']
        # fields = "__all__"
        # extra_kwargs = {
        #     'price': {'min_value': 2},
        #     'inventory':{'min_value':0}
        # }
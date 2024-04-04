from rest_framework import serializers
from .models import *
from datetime import datetime
from rest_framework.validators import UniqueValidator


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer class for the Category model.

    This serializer is used to convert Category model instances into JSON
    representation and vice versa. It specifies the fields to be included in
    the serialized output and provides validation for the 'title' field.

    Attributes:
        model (Category): The Category model class to be serialized.
        fields (list): The list of fields to be included in the serialized output.
        extra_kwargs (dict): Additional keyword arguments for field-level configuration.
    """
    class Meta:
        model = Category
        fields = ['id', 'title']
        extra_kwargs = {
            'title': {
                'validators': [
                    UniqueValidator(
                        queryset=Category.objects.all(),
                        message="This category already exists"
                    )
                ]
            },
        }

class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='title', required=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']
        extra_kwargs = {
            'title': {
                'validators': [
                    UniqueValidator(
                        queryset=MenuItem.objects.all(),
                        message="This title already exists"
                    )
                ]
            },
        }
        depth = 1

class UserSerializer(serializers.ModelSerializer):
    Date_Joined = serializers.SerializerMethodField()
    date_joined = serializers.DateTimeField(write_only=True, default=datetime.now)
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'Date_Joined']

    def get_Date_Joined(self, obj):
        return obj.date_joined.strftime('%Y-%m-%d')

class CartHelpSerializer(serializers.ModelSerializer):
    class Meta():
        model = MenuItem
        fields = ['id','title','price']

class CartSerializer(serializers.ModelSerializer):
    menuitem = CartHelpSerializer()
    class Meta():
        model = Cart
        fields = ['menuitem','quantity','price']

class AddToCartSerializer(serializers.ModelSerializer):
    class Meta():
        model = Cart
        fields = ['menuitem','quantity']
        extra_kwargs = {
            'menuitem': {'required': True},
            'quantity': {'required': True}
        }

class RemoveFromCartSerializer(serializers.ModelSerializer):
    class Meta():
        model = Cart
        fields = ['menuitem']
        extra_kwargs = {
            'menuitem': {'required': True},
        }

class OrdersSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta():
        model = Order
        fields = ['id','user','total','status','delivery_crew','date']
        extra_kwargs = {
            'user': {'required': True},
            'total': {'required': True},
            'status': {'required': True},
            'delivery_crew': {'required': True},
            'date': {'required': True}
        }

class SingleHelperSerializer(serializers.ModelSerializer):
    class Meta():
        model = MenuItem
        fields = ['title','price']

class SingleOrderSerializer(serializers.ModelSerializer):
    menuitem = SingleHelperSerializer()
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, source='menuitem.price', read_only=True)
    price = serializers.SerializerMethodField()
    name = serializers.CharField(source='menuitem.title', read_only=True)
    def get_price(self, obj):
        return obj.quantity * obj.menuitem.price
    
    class Meta():
        model = OrderItem
        fields = ['quantity', 'menuitem', 'unit_price', 'price', 'name']
        extra_kwargs = {
            'menuitem': {'read_only': True}
        }


class OrderPutSerializer(serializers.ModelSerializer):
    class Meta():
        model = Order
        fields = ['delivery_crew']
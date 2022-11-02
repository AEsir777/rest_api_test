from rest_framework import serializers
from store.models import Product, ShoppingCartItem

class CartItemSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1, max_value=100)
    class Meta:
        model = ShoppingCartItem
        fields = ['product', 'quantity']

class ProductSerializer(serializers.ModelSerializer):
    # read_only: whether or not the field can be written to through the serializer
    # source: where the data for the serializer field will be populated from
    is_on_sale = serializers.BooleanField(read_only=True) 
    current_price = serializers.FloatField(read_only=True)
    description = serializers.CharField(min_length=2, max_length=200) # override the seralizer field
    cart_items = serializers.SerializerMethodField()
    # price = serializers.FloatField(min_value=1.00, max_value=100000)
    # DecimalField more powerful
    price = serializers.DecimalField(
        min_value=1.00, max_value=100000, 
        max_digits=None, decimal_places=2,
    )
    # input_formats, format(output default:DataTime object), help_text, style
    sale_start = serializers.DateTimeField(
        input_formats=['%I:%M %p %d %B %Y'], format=None, allow_null=True, 
        help_text='Accepted format is "12:01 PM 15 April 2019"',
        style={'input_type': 'text', 'placeholder': '00: 00 PM 01 January 01'}
    )
    sale_end = serializers.DateTimeField(
        input_formats=['%I:%M %p %d %B %Y'], format=None, allow_null=True, 
        help_text='Accepted format is "12:01 PM 15 April 2019"',
        style={'input_type': 'text', 'placeholder': '00: 00 PM 01 January 01'}
    )
    photo = serializers.ImageField(default=None) 
    # write_only: no show in API
    warranty = serializers.FileField(write_only=True, default=None)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'sale_start', 'sale_end', 
            'is_on_sale', 'current_price', 'cart_items', 'photo', 'warranty']


    # get_ is the prefix to the field name for the method that is called
    def get_cart_items(self, instance):
        items = ShoppingCartItem.objects.filter(product=instance)
        # many=True: creates a list of serialized model instances, false: only 1
        return CartItemSerializer(items, many=True).data

        """     def to_representation(self, instance):
        data = super().to_representation(instance)
        data['is_on_sale'] = instance.is_on_sale()
        data['current_price'] = instance.current_price()
        return data """
    
    # validated_data: data that has already passed through serializer and model validation process
    # used to create or update a model
    def update(self, instance, validated_data):
        if validated_data.get('warranty', None):
            instance.description += '\n\nWarranty Information: \n'
            instance.description += b'; '.join(
                validated_data['warranty'].readlines()
            ).decode()
        return instance

class ProductStatSerializer(serializers.Serializer):
    stats = serializers.DictField(
        child = serializers.ListField(
            child = serializers.IntegerField()
        )
    )
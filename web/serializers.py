from rest_framework import serializers
from product.models import Product

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'starp_color',
            'highlights',
            'price',
            'stock',
            'status',
            'image',
            )

    def get_image(self,instance) :
        request = self.context.get('request')
        return request.build_absolute_uri(instance.image.url)
from rest_framework import serializers
from market_app.models import Market, Seller, Product


# aus der class ausgelagert, über validators=[valida_no_x] wird es dann aufgerufen 
# def validate_no_x(value):
#           errors = []

#           if 'X' in value:
#                  errors.append('no X in location')
#           if 'Y' in value:
#                            errors.append('no Y in location')

#           if errors:
#                   raise serializers.ValidationError(errors)
          
#           return value
        

# Umgebaut zum Model Serializer
class MarketSerializer(serializers.ModelSerializer):

        # gibt uns den seller namen mit aus 
#    sellers = serializers.StringRelatedField(many=True, read_only=True)
        # HyberLinkedRelatedField
    sellers = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='seller_single')


# Auskommentiert wird mit ModelSerilizer einfacher gelöst     

#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=255)
#     location = serializers.CharField(max_length=255) # validators=[validate_no_x]
#     description = serializers.CharField()
#     net_worth = serializers.DecimalField(max_digits=100, decimal_places=2)

#     def create(self, validated_data):
#               return Market.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#          instance.name = validated_data.get('name', instance.name)
#          instance.location = validated_data.get('location', instance.location)
#          instance.description = validated_data.get('description', instance.description)
#          instance.net_worth = validated_data.get('net_worth', instance.net_worth)
#          instance.save()
#          return instance

    class Meta:
        model = Market

         # 1. zwei varianten von fields und der Anzeige um alles anzeigen
        #fields = '__all__'
        exclude = []
        
        # 2. varianten um nur ein Teil an zu zeigen 
        # fields = ['id', 'name', 'location', 'description']
        # exclude = ['name']
       

        # validation benötigt die Field bezeichnung im NAmen 
    def validate_name(self, value):
                errors = []

                if 'X' in value:
                        errors.append('no X in name')
                if 'Y' in value:
                        errors.append('no Y in name')

                if errors:
                        raise serializers.ValidationError(errors)
          
                return value




        # Erbt alles von Marketserializer und Hyperserializer
        # muss im GET in der View verwendet werden MarketHyperlinnkedSerializer
class MarketHyperlinkedSerializer(MarketSerializer, serializers.HyperlinkedModelSerializer):
        sellers = None  # lässt sellers aus der view raus beim GET 
        class Meta:
            model = Market
            exclude = []

    




# nested ModelSerializer
        # GET und POST zusammen 

class SellerSerializer(serializers.ModelSerializer):

        markets = MarketSerializer(many=True, read_only=True)
        market_ids = serializers.PrimaryKeyRelatedField(
               queryset=Market.objects.all(),
               many=True,
               write_only=True,
               source='markets'
        )

        market_count = serializers.SerializerMethodField()


        class Meta:
                model = Seller
                exclude = []

        # obj = ist das was wir Serialisieren oder deserialisieren 
        # dadurch bekommen wir ein market_count bei der GET abfrage mit ausgegeben z.b. "market_count": 1,
        def get_market_count(self, obj):
               return obj.markets.count()
               


# wurde durch Nested SellerSeriializer ersetzt 

class SellerDetailSerializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField(max_length=255)
        contact_info = serializers.CharField()

        # Hier verwenden wir einen bereits vorhandenen Serializer
        # innerhalb eines anderen Serializers.
        # Genau das bezeichnet man als Nested Serializer.

        # markets = MarketSerializer(many=True, read_only=True)


        # ändert die ansicht in der Api view, wie markets id's zugrodnet werden. 
        makets = serializers.StringRelatedField(many=True)



# wurde durch Nested SellerSeriializer ersetzt 
class SellerCreateSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255)
        contact_info = serializers.CharField()

        # hier erben wir das Listfield vom Serializer, wir wollen nur createn deshalb write_only= True
        # hier mit heben wir die Primarykeys von market mit child=serializers.IntegerField()
        markets = serializers.ListField(child=serializers.IntegerField(), write_only=True )

        def validate_markets(self, value):
               markets = Market.objects.filter(id__in=value) # wir holen uns alle markets mit der id
               if len(markets) != len(value): # wir prüfen ob alles 
                       raise serializers.ValidationError("One or more Makrts not found")
               return value

        def create (self, validated_data):
                market_ids= validated_data.pop('markets')
                seller = Seller.objects.create(**validated_data)
                markets = Market.objects.filter(id__in=market_ids)
                seller.markets.set(markets)
                return seller



class ProductSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=50, decimal_places=2)

    # Foreign Keys mit PrimaryKeyRelatedField ersetzen
    market = serializers.PrimaryKeyRelatedField(
        queryset=Market.objects.all()
    )

    seller = serializers.PrimaryKeyRelatedField(
        queryset=Seller.objects.all()
    )

    def create(self, validated_data):
              return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
         instance.name = validated_data.get('name', instance.name)
         instance.description = validated_data.get('description', instance.description)
         instance.price = validated_data.get('price', instance.price)
         instance.market = validated_data.get('market', instance.market)
         instance.seller = validated_data.get('seller', instance.seller)
         instance.save()
         return instance

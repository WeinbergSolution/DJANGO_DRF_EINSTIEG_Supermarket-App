from rest_framework import serializers
from market_app.models import Market, Seller


# aus der class ausgelagert, über validators=[valida_no_x] wird es dann aufgerufen 
def valida_no_x(value):
          errors = []

          if 'X' in value:
                 errors.append('no X in location')
          if 'Y' in value:
                           errors.append('no Y in location')

          if errors:
                  raise serializers.ValidationError(errors)
          
          return value
        


class MarketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255, validators=[valida_no_x])
    description = serializers.CharField()
    net_worth = serializers.DecimalField(max_digits=100, decimal_places=2)

    def create(self, validated_data):
              return Market.objects.create(**validated_data)

    def update(self, instance, validated_data):
         instance.name = validated_data.get('name', instance.name)
         instance.location = validated_data.get('location', instance.location)
         instance.description = validated_data.get('description', instance.description)
         instance.net_worth = validated_data.get('net_worth', instance.net_worth)
         instance.save()
         return instance


class SellerDetailSerializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField(max_length=255)
        contact_info = serializers.CharField()

        # Hier verwenden wir einen bereits vorhandenen Serializer
        # innerhalb eines anderen Serializers.
        # Genau das bezeichnet man als Nested Serializer.
        markets = MarketSerializer(many=True, read_only=True)

class SellerCreateSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255)
        contact_info = serializers.CharField()

        # hier erben wir das Listfield vom Serializer, wir wollen nur createn deshalb write_only= True
        # hier mit heben wir die Primarykeys von market mit child=serializers.IntegerField()
        markets = serializers.ListField(child=serializers.IntegerField(), write_only=True )

        def validate_markets(self, value):
               markets = Market.objects.filter(id__in=value) # wir holen uns alle markets mit der id
               if(markets) != len(value): # wir prüfen ob alles 
                       raise serializers.ValidationError("One or more Makrts not found")
               return value

        def create (self, validated_data):
                market_ids= self.validate_data.pop('markets')
                seller = Seller.objects.create(**validated_data)
                markets = Market.objects.filter(id__in=market_ids)
                seller.markets.set(markets)
                return seller
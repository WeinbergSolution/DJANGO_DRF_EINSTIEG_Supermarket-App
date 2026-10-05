from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MarketSerializer, ProductSerializer, SellerSerializer, ProductModelSerializer
from market_app.models import Market, Seller, Product
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import viewsets



class ProductViewSet(viewsets.ViewSet):

     queryset = Product.objects.all()
     
     def list(self, request):
        serializer = ProductModelSerializer(self.queryset, many=True)
        return Response(serializer.data)

     def retrieve(self, request, pk=None):
        
        product = get_object_or_404(self.queryset, pk=pk)
        serializer = ProductModelSerializer(product)
        return Response(serializer.data)





# CLass Based views # GenericAPIView
#ListAPIView ist selbst eine Generic View und baut auf GenericAPIView plus dem passenden List-Verhalten auf.

class MarketsView(generics.ListCreateAPIView):
     

     queryset = Market.objects.all()
     serializer_class = MarketSerializer


# Singleview mit gerneric viel effizenter und hat auch die Crud operationen mit drin.

class MarketSingleView(generics.RetrieveUpdateDestroyAPIView):
  
     queryset = Market.objects.all()
     serializer_class = MarketSerializer

# CLass Based views # GenericAPIView + Mixins
class MarketsClassbasedView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
   
    queryset = Market.objects.all()
    serializer_class = MarketSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


    

class SellerOfMarketList(generics.ListAPIView):
     serializer_class = SellerSerializer

     def get_queryset(self):
          pk = self.kwargs.get('pk')
          market = Market.objects.get(pk = pk)
          return market.sellers.all()


    


@api_view(['GET', 'POST']) # dekorater
def markets_view(request):


    if request.method == 'GET':
        markets = Market.objects.all()
        serializer = MarketSerializer(markets, many=True)
        return Response(serializer.data)


    if request.method == 'POST':
          serializer = MarketSerializer(data=request.data)
          if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
          else:
              return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE', 'PUT']) # dekorater
def market_single_view(request, pk):


    if request.method == 'GET':
        market = Market.objects.get(pk=pk)
        serializer = MarketSerializer(market)
        return Response(serializer.data)

    if request.method == 'DELETE':
            market = Market.objects.get(pk=pk)
            serializer = MarketSerializer(market)
            market.delete()
            return Response(serializer.data)

    if request.method == 'PUT':
            market = Market.objects.get(pk=pk)
            serializer = MarketSerializer(market, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)



@api_view(['GET', 'POST']) # dekorater
def sellers_view(request):

    if request.method == 'GET':
        sellers = Seller.objects.all()
        serializer = SellerSerializer(sellers, many=True)
        return Response(serializer.data)


    if request.method == 'POST':
          serializer = SellerSerializer(data=request.data)
          if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
          else:
              return Response(serializer.errors)



@api_view(['GET', 'DELETE', 'PUT']) # dekorater
def seller_single_view(request, pk):


    if request.method == 'GET':
        seller = Seller.objects.get(pk=pk)
        serializer = SellerSerializer(seller, context={'request': request})
        return Response(serializer.data)

    if request.method == 'DELETE':
            seller = Seller.objects.get(pk=pk)
            serializer = SellerSerializer(seller)
            seller.delete()
            return Response(serializer.data)

    if request.method == 'PUT':
            seller = Seller.objects.get(pk=pk)
            serializer = SellerSerializer(seller, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)

# Example 16

@api_view(['GET', 'POST']) # dekorater
def product_view(request):


    if request.method == 'GET':
        product = Product.objects.all()
        serializer = ProductModelSerializer(product, many=True)
        return Response(serializer.data)


    if request.method == 'POST':
          serializer = ProductModelSerializer(data=request.data)
          if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
          else:
              return Response(serializer.errors)

@api_view(['GET', 'DELETE', 'PUT']) # dekorater
def product_single_view(request, pk):


    if request.method == 'GET':
        product = Product.objects.get(pk=pk)
        serializer = ProductModelSerializer(product)
        return Response(serializer.data)

    if request.method == 'DELETE':
            product = Product.objects.get(pk=pk)
            serializer = ProductModelSerializer(product)
            product.delete()
            return Response(serializer.data)

    if request.method == 'PUT':
            product = Product.objects.get(pk=pk)
            serializer = ProductModelSerializer(product, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MarketSerializer, SellerDetailSerializer, SellerCreateSerializer, ProductSerializer, SellerSerializer
from market_app.models import Market, Seller, Product



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
            return Response(serializer.data)
          else:
              return Response(serializer.errors)
  



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
        serializer = SellerSerializer(seller)
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
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)


    if request.method == 'POST':
          serializer = ProductSerializer(data=request.data)
          if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
          else:
              return Response(serializer.errors)

@api_view(['GET', 'DELETE', 'PUT']) # dekorater
def prduct_single_view(request, pk):


    if request.method == 'GET':
        prduct = Product.objects.get(pk=pk)
        serializer = ProductSerializer(prduct)
        return Response(serializer.data)

    if request.method == 'DELETE':
            prduct = Product.objects.get(pk=pk)
            serializer = ProductSerializer(prduct)
            prduct.delete()
            return Response(serializer.data)

    if request.method == 'PUT':
            prduct = Product.objects.get(pk=pk)
            serializer = ProductSerializer(prduct, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
 
  

       
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from .models import Item
from .serializers import ItemSerializer


class ItemListCreateView(APIView):
    """
    API view for listing and creating items.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Retrieve a list of items.

        Args:
            request: The HTTP request object.

        Returns:
            Response: A response object containing the list of items.
        """
        items = cache.get('item_list')

        if items is None:
            try:
                items = Item.objects.all()
                serializer = ItemSerializer(items, many=True)
                cache.set('item_list', serializer.data, timeout=60*15)  # Cache for 15 minutes
                return Response(serializer.data)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

        return Response(items)

    def post(self, request):
        """
        Create a new item.

        Args:
            request: The HTTP request object containing item data.

        Returns:
            Response: A response object with the created item data.
        """
        try:
            serializer = ItemSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                cache.delete('item_list')  # Invalidate cache after creating a new item
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ItemDetailView(APIView):
    """
    API view for retrieving, updating, and deleting a specific item.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        """
        Retrieve an item by its primary key.

        Args:
            request: The HTTP request object.
            pk (int): The primary key of the item.

        Returns:
            Response: Contains the item data or an error message if not found.
        """
        cache_key = f'item_{pk}'
        item_data = cache.get(cache_key)

        if item_data is None:
            item = Item.objects.filter(pk=pk).first()
            if item:
                serializer = ItemSerializer(item)
                cache.set(cache_key, serializer.data, timeout=60*15)  # Cache for 15 minutes
                return Response(serializer.data)

            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(item_data)

    def put(self, request, pk):
        """
        Update a specific item.

        Args:
            request: The HTTP request object containing updated item data.
            pk (int): The primary key of the item.

        Returns:
            Response: A response object with the updated item data.
        """
        item = Item.objects.filter(pk=pk).first()
        if item is None:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ItemSerializer(item, data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                cache.delete(f'item_{pk}')  # Invalidate cache for this item
                cache.delete('item_list')     # Invalidate the list cache as well
                return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a specific item.

        Args:
            request: The HTTP request object.
            pk (int): The primary key of the item.

        Returns:
            Response: An empty response with a status of 204 No Content.
        """
        item = Item.objects.filter(pk=pk).first()
        if item is None:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            item.delete()
            cache.delete(f'item_{pk}')  # Invalidate cache for this item
            cache.delete('item_list')     # Invalidate the list cache
            return Response({'success message': 'Item deleted'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from datetime import date
from decimal import Decimal
from .serializers import *
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import generics
from django.contrib.auth.models import User, Group
from .permissions import IsManager, IsDeliveryCrew
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from rest_framework.response import Response
from rest_framework import status


class LogoutAllView(APIView):
    """
    API view for logging out the user from all devices.

    Requires the user to be authenticated.

    Methods:
    - post(request): Logs out the user from all devices and returns a JSON response.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Logs out the user from all devices and returns a JSON response.

        Retrieves all outstanding tokens for the authenticated user and creates
        corresponding blacklisted tokens. Returns a JSON response with a success
        message and a status code of 205 (RESET_CONTENT).

        Parameters:
        - request: The HTTP request object.

        Returns:
        - JsonResponse: A JSON response with a success message and a status code of 205 (RESET_CONTENT).
        """
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return JsonResponse({'message': 'Logout successful from all devices'}, status=status.HTTP_205_RESET_CONTENT)

class SingleItemView(generics.RetrieveUpdateDestroyAPIView, generics.RetrieveAPIView):
    """
    A view for retrieving, updating, and deleting a single MenuItem.

    Inherits from:
        - generics.RetrieveUpdateDestroyAPIView: Provides the implementation for retrieving, updating, and deleting a model instance.
        - generics.RetrieveAPIView: Provides the implementation for retrieving a model instance.

    Attributes:
        queryset (QuerySet): The queryset of MenuItem objects.
        serializer_class (Serializer): The serializer class for MenuItem objects.
        throttle_classes (list): The list of throttle classes to apply for rate limiting.

    Methods:
        get_permissions: Returns the list of permission classes based on the request method.
        patch: Updates the featured status of a MenuItem and returns a JSON response.

    """

    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_permissions(self):
        """
        Returns the list of permission classes based on the request method.

        Returns:
            list: The list of permission classes.

        """
        permission_classes = [IsAuthenticated]
        if self.request.method == 'PATCH':
            permission_classes = [IsAuthenticated, IsManager | IsAdminUser]
        if self.request.method == "DELETE":
            permission_classes = [IsAuthenticated, IsAdminUser]
        return[permission() for permission in permission_classes]

    def patch(self, request, *args, **kwargs):
        """
        Updates the featured status of a MenuItem and returns a JSON response.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            JsonResponse: The JSON response containing the updated featured status.

        """
        menuitem = MenuItem.objects.get(pk=self.kwargs['pk'])
        menuitem.featured = not menuitem.featured
        menuitem.save()
        return JsonResponse(
            status=200, 
            data={'message':'Featured status of {} changed to {}'.format(str(menuitem.title) ,str(menuitem.featured))}
        )

class CategoryView(generics.ListAPIView, generics.ListCreateAPIView):
    """
    A view for retrieving and creating Category objects.

    Inherits from `generics.ListAPIView` and `generics.ListCreateAPIView`.
    Provides a list view for retrieving Category objects and a create view for creating new Category objects.

    Attributes:
        queryset (QuerySet): The queryset of Category objects to be used for retrieving data.
        serializer_class (Serializer): The serializer class to be used for serializing and deserializing Category objects.
        search_fields (list): The fields to be used for searching Category objects.
        throttle_classes (list): The throttle classes to be used for rate limiting.

    Methods:
        get_permissions: Returns the list of permissions classes based on the request method.

    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ['title']
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_permissions(self):
        """
        Returns the list of permissions classes based on the request method.

        If the request method is POST, returns a list containing `IsAdminUser` permission class.
        Otherwise, returns a list containing `AllowAny` permission class.

        Returns:
            list: The list of permissions classes.

        """
        if self.request.method == 'POST': 
            return [IsAdminUser()]
        return [AllowAny()]


class MenuItemView(generics.ListAPIView, generics.ListCreateAPIView):
    """
    API view for managing menu items.

    Inherits from `generics.ListAPIView` and `generics.ListCreateAPIView`.
    Provides endpoints for listing and creating menu items.

    Attributes:
        queryset (QuerySet): The queryset of all menu items.
        serializer_class (Serializer): The serializer class for menu items.
        ordering_fields (list): The fields that can be used for ordering menu items.
        search_fields (list): The fields that can be used for searching menu items.
        throttle_classes (list): The throttle classes applied to the view.

    Methods:
        get_permissions: Returns the permissions required for the request method.

    """
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'category']
    search_fields = ['title', 'category__title']
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_permissions(self):
        """
        Returns the permissions required for the request method.

        Returns:
            list: A list of permission classes required for the request method.
        """
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]


class ManagerUsersView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.filter(groups__name='Managers')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsManager | IsAdminUser]

    def get_queryset(self):
        manager_group = Group.objects.get(name='Manager')
        queryset = User.objects.filter(groups=manager_group)
        return queryset

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name='Manager')
            managers.user_set.add(user)
            return JsonResponse(status=201, data={'message':'User added to Managers group'})
        
class ManagerSingleUserView(generics.RetrieveDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        manager_group = Group.objects.get(name='Manager')
        queryset = User.objects.filter(groups=manager_group)
        return queryset
    
class Delivery_crew_management(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsManager | IsAdminUser]
    queryset = User.objects.filter(groups=Group.objects.get(name="Delivery Crew"))

    def post(self, request, *args, **kwargs):
        # Assign user to delivery crew
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            delivery_crew = Group.objects.get(name='Delivery Crew')
            delivery_crew.user_set.add(user)
            return JsonResponse(status=201, data={'message':'User added to Delivery Crew'})

class Delivery_crew_management_single_view(generics.RetrieveDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, IsManager]

    def get_queryset(self):
        delivery_crew = Group.objects.get(name='Delivery Crew')
        queryset = User.objects.filter(groups=delivery_crew)
        return queryset

class Customer_Cart(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        cart = Cart.objects.filter(user=self.request.user)
        return cart

    def post(self, request, *args, **kwargs):
        serialized_item = AddToCartSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        id = request.data['menuitem']
        quantity = request.data['quantity']
        item = get_object_or_404(MenuItem, id=id)
        price = int(quantity) * item.price
        try:
            Cart.objects.create(user=request.user, quantity=quantity, unit_price=item.price, price=price, menuitem_id=id)
        except Exception as e:
            return JsonResponse(data={'message': f'{e}'})
        return JsonResponse(status=201, data={'message':'Item added to cart!'})

    def delete(self, request, *arg, **kwargs):
        if 'menuitem' in request.data:
            serialized_item = RemoveFromCartSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            menuitem = request.data['menuitem']
            cart = get_object_or_404(Cart, user=request.user, menuitem=menuitem )
            cart.delete()
            return JsonResponse(status=200, data={'message':'Item removed from cart'})
        else:
            Cart.objects.filter(user=request.user).delete()
            return JsonResponse(status=201, data={'message':'All Items removed from cart'})


class OrdersView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = OrdersSerializer

    def get_queryset(self, *args, **kwargs):
        if self.request.user.groups.filter(name='Manager').exists() or self.request.user.is_superuser == True:
            query = Order.objects.all()
        elif self.request.user.groups.filter(name='Delivery Crew').exists():
            query = Order.objects.filter(delivery_crew=self.request.user)
        else:
            query = Order.objects.filter(user=self.request.user)
        return query

    def get_permissions(self):
        if self.request.method == 'GET' or 'POST' :
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsManager | IsAdminUser]
        return[permission() for permission in permission_classes]

    def post(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=request.user)
        total = self.calculate_total(cart_items)
        order = Order.objects.create(user=request.user, status=False, total=total, date=date.today())
        for i in cart_items.values():
            menuitem = get_object_or_404(MenuItem, id=i['menuitem_id'])
            orderitem = OrderItem.objects.create(order=order, menuitem=menuitem, quantity=i['quantity'])
            orderitem.save()
        cart_items.delete()
        return JsonResponse(status=201, data={'message':'Your order has been placed! Your order number is {}'.format(str(order.id))})

    def calculate_total(self, cart_items):
        total = Decimal(0)
        for item in cart_items:
            total += item.price
        return total

class SingleOrderView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = SingleOrderSerializer
    
    def get_permissions(self):
        order = Order.objects.get(pk=self.kwargs['pk'])
        if self.request.user == order.user and self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        elif self.request.method == 'PUT' or self.request.method == 'DELETE':
            permission_classes = [IsAuthenticated, IsManager | IsAdminUser]
        else:
            permission_classes = [IsAuthenticated, IsDeliveryCrew | IsManager | IsAdminUser]
        return[permission() for permission in permission_classes] 

    def get_queryset(self, *args, **kwargs):
            query = OrderItem.objects.filter(order_id=self.kwargs['pk'])
            return query


    def patch(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])
        order.status = not order.status
        order.save()
        return JsonResponse(status=200, data={'message':'Status of order #'+ str(order.id)+' changed to '+str(order.status)})

    def put(self, request, *args, **kwargs):
        serialized_item = OrderPutSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        order_pk = self.kwargs['pk']
        crew_pk = request.data['delivery_crew'] 
        order = get_object_or_404(Order, pk=order_pk)
        crew = get_object_or_404(User, pk=crew_pk)
        order.delivery_crew = crew
        order.save()
        return JsonResponse(status=201, data={'message':str(crew.username)+' was assigned to order #'+str(order.id)})

    def delete(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])
        order_number = str(order.id)
        order.delete()
        return JsonResponse(status=200, data={'message':'Order #{} was deleted'.format(order_number)})    
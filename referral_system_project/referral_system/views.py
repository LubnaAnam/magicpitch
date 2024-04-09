# Create your views here.
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response


# @api_view(['POST'])
# def user_registration(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def user_details(request):
#     user = request.user
#     serializer = UserSerializer(user)
#     return Response(serializer.data)

# @api_view(['GET'])
# def referrals(request):
#     user = request.user
#     referrals = User.objects.filter(referral_code=user.referral_code)
#     serializer = UserSerializer(referrals, many=True)
#     return Response(serializer.data)

# .............................................................


from django.shortcuts import render
from .models import User
from .serializers import UserRegistrationSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from rest_framework.pagination import PageNumberPagination
from .models import Referral
from .serializers import ReferralSerializer
from rest_framework import authentication , permissions
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

@api_view(['POST'])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'id': user.id, 'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_details(request):
    user = request.user  # This assumes you are using token-based authentication
    serializer = UserSerializer(user)
    return Response(serializer.data)






@api_view(['GET'])
@permission_classes([IsAuthenticated])
def referrals_list(request):
    referrals = Referral.objects.filter(referrer=request.user)
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(referrals, request)
    serializer = ReferralSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

class CustomPagination(PageNumberPagination):
    page_size = 20





class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
    


class ListUsers(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes =[permissions.IsAuthenticated]

    def get(self , request , format=None):
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)



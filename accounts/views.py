from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm


# Third
from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import CustomUserSerializer, RegistrationSerializer, CustomUserDetailSerializer
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import CustomUser
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from django.db.models.signals import pre_save
from django.dispatch import receiver
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
import os


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                #return redirect("/")
                return render( request, 'dash/index.html' )
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(email=email, password=raw_password)

            msg = 'User account created successfully.'
            success = True

            #return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})



@api_view(['POST', ])
def registration_view(request):
    if request.method == 'POST':
        data = {}

        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'successfully registered new user.'
            # data['email'] = account.email
            # data['username'] = account.username
            # token = Token.objects.get(user=account).key
            # data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


# First get the all the users and then display in a way mentioned in UserSerializers.
class CustomUserViewset(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ['get','put','delete']
    permission_classes = [IsAuthenticatedOrReadOnly]

    # @receiver(pre_save, sender=User)
    # def delete_old_file(self,sender,attr,**kwargs):
    #     # on creation, signal callback won't be triggered
    #     if self._state.adding and not self.pk:
    #         return False
    
    #     try:
    #         if attr=='profile_pic':
    #             old_file = sender.objects.get(pk=self.pk).profile_pic.file
    #         else:
    #             old_file = sender.objects.get(pk=self.pk).cover_pic.file
    
    #     except sender.DoesNotExist:
    #         return False
    #     # comparing the new file with the old one
    #     if attr == 'profile_pic':
    #         file = self.profile_pic.file
    #     else:
    #         file = self.cover_pic.file
    #     print(type(old_file),old_file.name)
    #     if not old_file == file:
    #         if os.path.isfile(old_file.name):
    #             os.remove(old_file.name)

    @action(detail=True, methods=['PUT'])
    # this method is for update
    def update_user(self, request, pk=None):
        CustomUser = CustomUser.objects.get(email=request.user.email)
        serializer = CustomUserSerializer(instance=obj)
        if serializer.is_valid():
            serializer.save()
        return Response()


        if 'profile_pic' in request.data:
            # old_file = User.objects.get(pk=user.pk).profile_pic.file
            # # comparing the new file with the old one
            # file = user.profile_pic.file
            # print(type(old_file), old_file.name)
            # if 'defaults'!=str(file).split("/")[-2]:
            #     if not old_file == file:
            #         if os.path.isfile(old_file.name):
            #             os.remove(old_file.name)
            print(request.data['profile_pic'])
            setattr(CustomUser, "profile_pic", request.data['profile_pic'])
            CustomUser.save()

        if 'cover_pic' in request.data:
            # old_file = User.objects.get(pk=user.pk).cover_pic.file
            # # comparing the new file with the old one
            # file = user.cover_pic.file
            # print(type(old_file), old_file.name)
            # if 'defaults'!=str(file).split("/")[-2]:
            #     if not old_file == file:
            #         if os.path.isfile(old_file.name):
            #             os.remove(old_file.name)
            # print(request.data['cover_pic'])
            setattr(CustomUser, "cover_pic", request.data['cover_pic'])
            CustomUser.save()


        if 'email' in request.data:
            setattr(CustomUser, "email", request.data['email'])
            CustomUser.save()
        serializer = CustomUserSerializer(CustomUser, many=False)
        return Response(serializer.data)



    @action(detail=True, methods=['DELETE'])
    # this method is for update
    def delete_profile_pic(self, request, pk=None):
        CustomUser = CustomUser.objects.get(id=pk)
        CustomUser.profile_pic.delete(save=False)
        CustomUser.profile_pic = 'defaults/profile.svg'
        CustomUser.save()

        serializer = CustomUserSerializer(CustomUser, many=False)
        return Response(serializer.data)

    @action(detail=True, methods=['DELETE'])
    # this method is for update
    def delete_cover_pic(self, request, pk=None):
        CustomUser = CustomUser.objects.get(id=pk)
        CustomUser.cover_pic.delete(save=False)
        CustomUser.cover_pic = 'defaults/cover.jpg'
        CustomUser.save()

        serializer = CustomUserSerializer(CustomUser, many=False)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    # this method is for update
    def no_of_follow(self, request,pk=None,format=None):
        CustomUser = CustomUser.objects.get(id=pk)
        return Response({"no_followers":len(CustomUserSerializer(CustomUser).data['followers']),"no_following": len(CustomUserSerializer(CustoUser).data['following'])})

class CustomUserDetailViewset(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserDetailSerializer
    http_method_names = ['get']
    permission_classes = [IsAuthenticatedOrReadOnly]

# To see following and followers of all the users.
# class CustomUserFollowingViewSet(viewsets.ModelViewSet):
#     queryset = CustomUserFollowing.objects.all()
#     serializer_class = CustomUserFollowingSerializer
#     http_method_names = ['get']


# # For follow and Unfollow
# class CustomUserFollow(APIView):
#     # return user if user exist
#     def get_object(self, pk):
#         try:
#             return CustomUser.objects.get(pk=pk)
#         except CustomUser.DoesNotExist:
#             raise ValueError

#     # get the users follow details.
#     def get(self, request, pk, format=None):
#         try:
#             CustomUser = self.get_object(pk)
#         except Exception:
#             return Response({'message': 'User does not exists '})
#         serializer = UserSerializer(CustomUser)
#         return Response(serializer.data)

#     # follow another users
#     def post(self, request, pk, format=None):
#         # user = User.objects.get(pk=request.data['user'])
#         CustomUser = request.CustomUser
#         try:
#             follow = self.get_object(pk)
#         except Exception:
#             return Response({'message': 'User does not exists '})
#         try:
#             if CustomUser != follow:
#                 CustomUserFollowing.objects.create(user_id=CustomUser, following_user_id=follow)
#             else:
#                 return Response({"message": "You can't follow yourself"})
#         except Exception as e:
#             return Response({"message": f"You already follow {follow}"})

#         # serializer = UserSerializer(follow)
#         return Response({'message': f'You follow {follow}'})

#     # unfollow users.
#     def delete(self, request, pk, format=None):
#         # user = User.objects.get(pk=request.data['user'])
#         CustomUser = request.CustomUser
#         try:
#             follow = self.get_object(pk)
#         except Exception:
#             return Response({'message': 'User does not exists '})
#         try:
#             connection = CustomUserFollowing.objects.filter(user_id=CustomUser, following_user_id=follow).first()
#             connection.delete()
#         except Exception:
#             return Response({'message': f"You don't follow {follow}"})
#         # serializer = UserSerializer(follow)
#         return Response({'message': f'You unfollowed {follow}'})

# class WaitFollow(APIView):
#     # return user if user exist
#     def get_object(self, pk):
#         try:
#             return CustomUser.objects.get(pk=pk)
#         except CustomUser.DoesNotExist:
#             raise ValueError

#     # get the users follow details.
#     def get(self, request, pk, format=None):
#         try:
#             CustomUser = self.get_object(pk)
#         except Exception:
#             return Response({'message': 'User does not exists '})
#         serializer = CustomUserSerializer(CustomUser)
#         return Response(serializer.data)

#     # follow another users
#     def post(self, request, pk, format=None):
#         # user = User.objects.get(pk=request.data['user'])
#         CustomUser = request.CustomUser
#         try:
#             follow = self.get_object(pk)
#         except Exception:
#             return Response({'message': 'User does not exists '})
#         try:
#             if CustomUser != follow:
#                 WaitingList.objects.create(user_id=CustomUser, following_user_id=follow)
#             else:
#                 return Response({"message": "You can't follow yourself"})
#         except Exception as e:
#             return Response({"message": f"You already follow {follow}"})

#         # serializer = UserSerializer(follow)
#         return Response({'message': f'You follow {follow}'})

#     # unfollow users.
#     def delete(self, request, pk, format=None):
#         # user = User.objects.get(pk=request.data['user'])
#         follow = request.CustomUser
#         try:
#             CustomUser = self.get_object(pk)
#         except Exception:
#             return Response({'message': 'User does not exists '})
#         try:
#             connection = WaitingList.objects.filter(user_id=CustomUser, following_user_id=follow).first()
#             connection.delete()
#         except Exception:
#             return Response({'message': f"You don't follow {follow}"})
#         # serializer = UserSerializer(follow)
#         return Response({'message': f'You unfollowed {follow}'})

'''
Token Authentication needed so we use custome auth_token instead of ObatainAuthToken
because it gives more flexibility.
'''


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        # in cutome User model email is essential for login but internally User takes
        # username attribute in django.
        if CustomUser.objects.filter(email=request.data['email']).exists():
            serializer = self.serializer_class(data=request.data,
                                               context={'request': request})
            print(request.data)
            if serializer.is_valid():
                print(request.data)
                CustomUser = serializer.validated_data['CustomUser']
                token, created = Token.objects.get_or_create(user=CustomUser)
                user_data = UserSerializer(CustomUser).data
                return Response({
                    'token': token.key,

                    'CustomUser': user_data,
                })

            return Response({"chk_uname_or_pwd": "Please check your Password"},
                            status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"user_not_found": "User does not exixts with this email address"},
                            status=status.HTTP_404_NOT_FOUND)





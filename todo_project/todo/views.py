from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from django.contrib.auth.models import User
from todo.serializers import (RegistrationSerializer, LoginSerializer,
                              ToDoSerializer)
from todo.models import Company, ToDo
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, logout
from rest_framework.permissions import IsAuthenticated
from todo.permissions import GetAccessCompany


class Registration(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    def get_object(self):
        queryset = self.get_queryset()
        data = self.request.data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        user = queryset.filter(username=username, email=email).first()

        if user is None:
            if User.objects.filter(username=username).exists():
                raise ValidationError('username already exist')
            elif User.objects.filter(email=email).exists():
                raise ValidationError('email already exist')
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password)

        return user

    def create(self, request, *args, **kwargs):
        user = self.get_object()
        company_id = request.data.get('company_id')
        company = Company.objects.filter(id=company_id).first()

        if company is None:
            raise ValidationError('Company not found')
        elif company.members.filter(id=user.id).exists():
            raise ValidationError(
                'This user is already registered with the company')

        company.members.add(user)
        company.save()

        return Response(status=status.HTTP_200_OK)


class Login(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def get_object(self):
        queryset = self.get_queryset()
        data = self.request.data
        email = data.get('email')
        password = data.get('password')

        user = queryset.filter(email=email).first()

        if user is None:
            raise ValidationError('email or password invalid')
        elif not user.check_password(password):
            raise ValidationError('email or password invalid')

        return user

    def create(self, request, *args, **kwargs):
        user = self.get_object()
        company_id = request.data.get('company_id')

        if not user.members.filter(id=company_id).exists():
            raise ValidationError('Company not found')

        login(request=request, user=user)
        request.session['company_id'] = company_id

        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class ToDoViewSet(ModelViewSet):
    queryset = ToDo.objects.all()
    serializer_class = ToDoSerializer
    permission_classes = (IsAuthenticated, GetAccessCompany)

    def get_queryset(self):
        queryset = super().get_queryset()
        session = self.request.session
        company_id = session.get('company_id')
        return queryset.filter(company_id=company_id).order_by('-created_at')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['company_id'] = self.request.session.get('company_id')
        return context

from . import models
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


User = get_user_model()


def extra_kwargs_factory(fields, **options):
    return {k: options for k in fields}


class LoginCustomerSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        allow_null=False,
    )

    def _find_user(self, data):
        return User.objects.filter(username=data['username']).first()

    def extract_token(self):
        user = self._find_user(self.validated_data)
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

    def validate_username(self, username):
        return username.lower()

    def validate(self, data):
        user = self._find_user(data)
        password = data.get('password', None)

        if not user or not user.check_password(password):
            raise serializers.ValidationError('No user with such credentials')

        return data


class CustomerSerializer(serializers.ModelSerializer):
    addition_info = serializers.SerializerMethodField()
    token = serializers.SerializerMethodField()

    def get_addition_info(self, customer):
        return f'addition information for {customer}'

    def get_token(self, customer):
        return customer.token.key

    def create(self, validated_data):
        return User.objects.create_customer(
            validated_data.pop('email').lower(),
            validated_data.pop('password'),
            **validated_data
        )

    class Meta:
        model = User

        required_fields = (
            'username',
            'email',
            'password',
        )
        fields = required_fields + (
            'id',
            'date_joined',
            'token',
            'addition_info',
            'first_name'
        )
        extra_kwargs = extra_kwargs_factory(
            required_fields,
            required=True,
            allow_null=False
        )
        read_only_fields = ('date_joined',)
        extra_kwargs.update(extra_kwargs_factory(('password',), write_only=True))


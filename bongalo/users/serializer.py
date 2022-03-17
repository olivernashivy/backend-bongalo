from .models import User
from string import ascii_letters
import random
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name','' 'email')

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'}, required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(self.context['request'], email=email, password=password)
        # Did we get back an active user?
        if user is None:
            msg = _('Unable to log in with provided credentials.')
            raise ValidationError(msg)

        # TODO: If required, is the email verified?

        attrs['user'] = user
        return attrs
# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
            user = super(RegisterSerializer, self).create(validated_data)
            user.set_password(validated_data['password'])
            user.save()
            return user


class SendVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if User.objects.filter(email=email, is_active=True).exists():
            raise ValidationError('User already exists with this email.')
        return email

    def create(self, validated_data):
        user = User.objects.filter(email=validated_data['email']).first()
        if user is None:
            # All protons in the universe have decayed by the time you guess this password.
            user = User.objects.create_user(
                validated_data['email'],
                ''.join(random.sample(ascii_letters, 50)),
                is_active=False,
            )
        #email.send_verification_code(user)
        return user

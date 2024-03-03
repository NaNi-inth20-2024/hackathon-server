from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "email", "first_name", "last_name", "role"]


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user with their username and password.

    Attributes:
        email: Should be unique
        username: Should be unique
        password
        first_name: optional
        second_name: optional
    """

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())],
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    role = serializers.CharField(
        write_only=True, required=False, default=CustomUser.Roles.STUDENT
    )

    def validate_role(self, value):
        valid_roles = [choice[0] for choice in CustomUser.Roles.choices]
        if value not in valid_roles:
            raise serializers.ValidationError("Invalid role value.")
        return value

    def create(self, validated_data):
        user = get_user_model().objects.create(
            email=validated_data["email"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            role=validated_data["role"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user

    class Meta:
        model = get_user_model()
        fields = ("id", "password", "email", "first_name", "last_name", "role")
        extra_kwargs = {
            "first_name": {"required": False},
            "last_name": {"required": False},
            "role": {"required": False}
        }
        read_only_fields = ["id"]


class EmailTokenObtainSerializer(TokenObtainSerializer):
    username_field = get_user_model().EMAIL_FIELD


class CustomTokenObtainPairSerializer(EmailTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data

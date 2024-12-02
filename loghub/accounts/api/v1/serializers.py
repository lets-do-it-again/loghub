from django.contrib.auth import authenticate
from rest_framework import serializers
from accounts.models import Professional
from . import validators
from accounts.models import User
from .utils import add_professionals

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["phone", "username", "email", "password"]

    def create(self, validated_data):
        phone = validated_data.pop("phone")
        username = validated_data.pop("username")
        password = validated_data.pop("password")
        email = validated_data.pop("email", None)

        user = User.objects.create_user(
            phone=phone,
            username=username,
            password=password,
            email=email
        )

        return user

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone = data.get("phone")
        password = data.get("password")

        user = authenticate(phone=phone, password=password)
        if not user:
            raise serializers.ValidationError("Invalid username or password")

        data["user"] = user
        return data


class ProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = ["id", "specialty", "level"]


class AdminUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "last_login", "created_at", "updated_at"]


class BasicUserDetailSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, required=False, write_only=True)
    new_password = serializers.CharField(max_length=128, required=False, write_only=True)
    professional = ProfessionalSerializer(many=True, required=True)

    class Meta:
        model = User
        fields = [
            "phone",
            "username",
            "email",
            "first_name",
            "last_name",
            "image_file",
            "professional",
            "password",
            "new_password",
        ]
        read_only_fields = ["phone"]

    def update(self, instance, validated_data):
        new_password = validated_data.pop("new_password", None)
        password = validated_data.pop("password", None)

        request = self.context.get("request")
        validators.validate_profile(new_password, password, request)

        if new_password:
            instance.set_password(new_password)

        professional_data = validated_data.pop("professional", None)
        if professional_data is not None:
            instance.professional.clear()
            for prof_data in professional_data:
                prof_instance, _ = Professional.objects.update_or_create(
                    **prof_data
                )
                instance.professional.add(prof_instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class AdminUserListSerializer(serializers.ModelSerializer):
    detail_user = serializers.HyperlinkedIdentityField(
        view_name="accounts:api-v1:user_detail"
    )

    class Meta:
        model = User
        fields = [
            "detail_user",
            "id",
            "phone",
            "username",
            "email",
            "is_active",
            "is_superuser",
        ]


class AdminUserCreateSerializer(serializers.ModelSerializer):
    professionals = ProfessionalSerializer(many=True, required=False)
    professional_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, default=[]
    )

    class Meta:
        model = User
        exclude = [
            "password",
            "user_permissions",
            "groups",
            "professional",
            "last_login",
        ]

    def create(self, validated_data):
        professionals_data = validated_data.pop("professionals", [])
        professional_ids = validated_data.pop("professional_ids", [])

        user = User.objects.create(**validated_data)
        add_professionals(user, professionals_data, professional_ids)
        return user


class BasicUserCreateSerializer(serializers.ModelSerializer):
    professionals = ProfessionalSerializer(many=True, required=False)
    professional_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, default=[]
    )
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = [
            "phone",
            "username",
            "email",
            "password",
            "professionals",
            "professional_ids",
        ]

    def validate(self, attrs):
        request = self.context.get("request", None)
        password = attrs.get("password")
        validators.validate_new_password(password, request)

        return attrs

    def create(self, validated_data):
        professionals_data = validated_data.pop("professionals", [])
        professional_ids = validated_data.pop("professional_ids", [])

        user = User.objects.create_user(**validated_data)
        add_professionals(user, professionals_data, professional_ids)

        return user
















from rest_framework import serializers
from .models import Classroom


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model: Classroom
        fields = "__all__"

    def validate_capacity(self, value):
        if value < 5:
            raise serializers.ValidationError("error")
        return value

    def validate_area(self, value):
        if value >= 0:
            raise serializers.ValidationError("error")
        return value
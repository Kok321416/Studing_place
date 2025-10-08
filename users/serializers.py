from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Payment

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователей"""

    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "password_confirm",
            "first_name",
            "last_name",
            "phone",
            "city",
        ]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "phone": {"required": True},
            "city": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля пользователя"""

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "phone", "city", "avatar"]
        read_only_fields = ["id", "email"]


class UserListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка пользователей"""

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "phone", "city"]


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для платежей"""

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = [
            "user",
            "payment_date",
            "stripe_payment_intent_id",
            "stripe_session_id",
            "stripe_product_id",
            "stripe_price_id",
            "payment_url",
            "status",
        ]


class PaymentCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания платежа"""

    course_id = serializers.IntegerField(write_only=True, required=False)
    lesson_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Payment
        fields = ["course_id", "lesson_id", "amount", "payment_method"]
        read_only_fields = [
            "user",
            "payment_date",
            "stripe_payment_intent_id",
            "stripe_session_id",
            "stripe_product_id",
            "stripe_price_id",
            "payment_url",
            "status",
        ]

    def validate(self, attrs):
        course_id = attrs.get("course_id")
        lesson_id = attrs.get("lesson_id")

        if not course_id and not lesson_id:
            raise serializers.ValidationError("Необходимо указать либо курс, либо урок")

        if course_id and lesson_id:
            raise serializers.ValidationError(
                "Нельзя указать и курс, и урок одновременно"
            )

        return attrs


class PaymentResponseSerializer(serializers.ModelSerializer):
    """Сериализатор для ответа с данными платежа"""

    course_title = serializers.CharField(source="course.title", read_only=True)
    lesson_title = serializers.CharField(source="lesson.title", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "amount",
            "payment_method",
            "payment_date",
            "status",
            "status_display",
            "payment_url",
            "course_title",
            "lesson_title",
            "stripe_session_id",
        ]

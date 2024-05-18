from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db.transaction import atomic
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from authentication.const import GenderChoice

from .models import Doctor, Patient

User = get_user_model()


class UserSerializerMixin(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True)

    def make_user(self, validated_data):
        user = User(
            username=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
        )
        user.password = make_password(validated_data["password"])
        user.save()
        return user


class DoctorSerializer(UserSerializerMixin):
    def create(self, validated_data):
        with atomic():
            user = self.make_user(validated_data)
            doctor, _ = Doctor.objects.update_or_create(user=user)
            return {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            }


class PatientSerializer(UserSerializerMixin):
    dob = serializers.DateField()
    gender = serializers.ChoiceField(choices=GenderChoice.model_choice())

    def create(self, validated_data):
        with atomic():
            user = self.make_user(validated_data)
            patient, _ = Patient.objects.update_or_create(
                user=user,
                defaults=dict(
                    dob=validated_data["dob"], gender=validated_data["gender"]
                ),
            )
        return {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "dob": patient.dob,
            "gender": patient.gender,
        }

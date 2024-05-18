from rest_framework.generics import CreateAPIView

from authentication.serializers import DoctorSerializer, PatientSerializer


class DoctorRegistrationView(CreateAPIView):
    serializer_class = DoctorSerializer


class PatientRegistrationView(CreateAPIView):
    serializer_class = PatientSerializer

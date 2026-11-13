from rest_framework import serializers
from clinic.models import DoctorDb,AppointmentDb
from django.utils import timezone
class Doctor_serializer(serializers.ModelSerializer):
    class Meta:
        model=DoctorDb
        fields="__all__"
        #fields=["id","doctor_name","specializtion"]
        read_only_field=["id"]

#Automatic field generation
#Default validation
#Conversion between model instances and serilaized data
#class Meta:Defines the serializer's configuration

class Appointment_serializer(serializers.ModelSerializer):
    class Meta:
        model=AppointmentDb
        fields="__all__"
        read_only_field=["id"]


    def validate(self,validated_data):
        phone=validated_data.get("phone")
        appointment_date=validated_data.get("appointment_date")

        #adding new dates only 
        if appointment_date<timezone.localdate():
            raise serializers.ValidationError("no such date available..!")
        
        if AppointmentDb.objects.filter(
            phone=phone,
            appointment_date=appointment_date).exists():
            raise serializers.ValidationError("Already Booked...!")
        else:
            return validated_data
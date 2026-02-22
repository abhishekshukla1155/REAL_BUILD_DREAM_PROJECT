from rest_framework import serializers
from .models import Worker

class WorkerSerializer(serializers.ModelSerializer):
    distance = serializers.FloatField(read_only=True)
    class Meta:
        model = Worker
        fields = '__all__'
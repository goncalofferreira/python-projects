from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    # Validador de título personalizado
    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("O título deve ter pelo menos 3 caracteres.")
        return value

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['owner']

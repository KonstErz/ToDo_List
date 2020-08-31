from rest_framework import serializers
from todo.models import ToDo


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})
    company_id = serializers.IntegerField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'},
                                     write_only=True)
    company_id = serializers.IntegerField()


class ToDoSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d.%m.%Y %H:%M',
                                           read_only=True)

    class Meta:
        model = ToDo
        fields = '__all__'

    def create(self, validated_data):
        company_id = self.context['company_id']
        validated_data['company_id'] = company_id
        return super().create(validated_data)

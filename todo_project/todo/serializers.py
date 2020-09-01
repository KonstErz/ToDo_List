from rest_framework import serializers
from todo.models import ToDo


class RegistrationSerializer(serializers.Serializer):
    """
    Serializes data for registration of a user with a link to a company.
    """

    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})
    company_id = serializers.IntegerField()


class LoginSerializer(serializers.Serializer):
    """
    Serializes data for user authorization in a specific company.
    """

    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'},
                                     write_only=True)
    company_id = serializers.IntegerField()


class ToDoSerializer(serializers.ModelSerializer):
    """
    Serializes data to create a company ToDo object.
    """

    created_at = serializers.DateTimeField(format='%d.%m.%Y %H:%M',
                                           read_only=True)

    class Meta:
        model = ToDo
        fields = '__all__'

    def create(self, validated_data):
        company_id = self.context['company_id']
        validated_data['company_id'] = company_id
        return super().create(validated_data)

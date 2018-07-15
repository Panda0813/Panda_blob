from rest_framework import serializers
from mainapp.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','name','passwd','phone','image')

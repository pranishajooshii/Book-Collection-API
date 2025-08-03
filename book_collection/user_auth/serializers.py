

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User=get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['fullname','email','password']

    
    def create(self,validated_data):

        try:
            user=User.objects.create_user(
                email=validated_data['email'],
                password=validated_data['password'],
                fullname=validated_data['fullname']
            )
            user.save()
            return user
        
           
        except Exception as e:
            raise serializers.ValidationError({"error": f"User creation failed: {str(e)}"})


class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self,data):
        email=data.get('email')
        password=data.get('password')

        
        if password and email:
             user=authenticate(request=self.context.get('request'),email=email, password=password)

             if user:
                 data['user']=user
                 return data
             else:
                 raise serializers.ValidationError("Invalid email or password")
        else:
            raise serializers.ValidationError("Email and password are required fields!!")

                 
        

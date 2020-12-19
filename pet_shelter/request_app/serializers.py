from rest_framework import serializers
from .models import PetRequest
from datetime import date
from pet_app.serializers import PetSerializerWithType
from users_app.serializers import CustomerSerializerShortDescription


def extra_kwargs_factory(fields, **options):
    return {k: options for k in fields}


class PetRequestInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = PetRequest

        required_fields = (
            'pet',
            'user',
            'date_arrive',
        )
        optional_fields = (
            'comment',
            'status',
        )

        fields = required_fields + optional_fields + ('id',)

        extra_kwargs = extra_kwargs_factory(required_fields, required=True, allow_null=False)
        extra_kwargs.update(
            extra_kwargs_factory(optional_fields, required=False)
        )

    def validate_date_arrive(self, date_arrive_value):
        today = date.today()
        if today >= date_arrive_value:
            raise serializers.ValidationError('date_arrive should be more than today date')

        return date_arrive_value


class PetRequestOutputSerializer(PetRequestInputSerializer):
    pet = PetSerializerWithType()
    user = CustomerSerializerShortDescription()


class PetSerializer(PetRequestInputSerializer):

    def to_representation(self, instance):
        return PetRequestOutputSerializer(instance=instance).data

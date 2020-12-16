from rest_framework import serializers
from .models import Pet, Animal
from datetime import date


def extra_kwargs_factory(fields, **options):
    return {k: options for k in fields}


class AnimalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Animal
        fields = '__all__'


class PetInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pet

        required_fields = (
            'type',
            'name',
            'species',
            'sex',
        )
        optional_fields = (
            'date_of_birth',
            'is_dangerous',
            'additional_info',
        )

        fields = required_fields + optional_fields + ('id',)

        extra_kwargs = extra_kwargs_factory(required_fields, required=True, allow_null=False)
        extra_kwargs.update(
            extra_kwargs_factory(optional_fields, required=False)
        )

    def validate(self, attrs):
        print(attrs)

        return attrs

    def validate_date_of_birth(self, date_of_birth_value):
        today = date.today()
        if today < date_of_birth_value:
            raise serializers.ValidationError('date_of_birth should be above today date')

        return date_of_birth_value


class PetOutputSerializer(PetInputSerializer):
    type = AnimalSerializer()


class PetSerializer(PetInputSerializer):

    def to_representation(self, instance):
        return PetOutputSerializer(instance=instance).data

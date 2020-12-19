from rest_framework import serializers
from .models import Pet, Animal
from datetime import date


def extra_kwargs_factory(fields, **options):
    return {k: options for k in fields}


class AnimalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Animal
        fields = '__all__'


class AnimalSerializerWithType(serializers.ModelSerializer):

    class Meta:
        model = Animal
        fields = ('animal_type', )

    def to_representation(self, instance):
        return str(instance)


class PetInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pet

        required_fields = (
            'type',
            'name',
            'date_of_appear',
            'date_of_birth',
            'sex',
        )
        optional_fields = (
            'has_vaccination',
            'is_sterilized',
            'is_prioritized',
            'additional_info',
            'photo_url',
            'breed',
        )

        fields = required_fields + optional_fields + ('id',)

        extra_kwargs = extra_kwargs_factory(required_fields, required=True, allow_null=False)
        extra_kwargs.update(
            extra_kwargs_factory(optional_fields, required=False)
        )

    def validate_date_of_birth(self, date_of_birth_value):
        today = date.today()
        if today < date_of_birth_value:
            raise serializers.ValidationError('date_of_birth should be above today date')

        return date_of_birth_value

    def validate_date_of_appear(self, date_of_appear_value):
        today = date.today()
        if today < date_of_appear_value:
            raise serializers.ValidationError('date_of_appear should be above or today date')

        return date_of_appear_value


class PetOutputSerializer(PetInputSerializer):
    type = AnimalSerializer()


class PetOutputSerializerWithType(PetInputSerializer):
    type = AnimalSerializerWithType()


class PetSerializer(PetInputSerializer):

    def to_representation(self, instance):
        return PetOutputSerializer(instance=instance).data


class PetSerializerWithType(PetInputSerializer):

    def to_representation(self, instance):
        return PetOutputSerializerWithType(instance=instance).data

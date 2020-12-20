from rest_framework import viewsets, permissions, response, status
from .models import Pet, Animal
from .serializers import PetSerializer, AnimalSerializer
from users_app.permissions import IsVolunteer


class AnimalView(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = [IsVolunteer, ]


class PetView(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticated, ]
        else:
            permission_classes = [IsVolunteer, ]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        query_params = self.request.query_params
        if query_params:
            filter_args = dict()
            type = query_params.get('type', '')
            sex = query_params.get('sex', '')

            if sex in ['F', 'M']:
                filter_args['sex'] = sex

            if type:
                animal = Animal.objects.all().filter(animal_type=type).first()
                if animal:
                    filter_args['type'] = animal.id

            sort_age = query_params.get('sort_age', '')
            sort_date = query_params.get('sort_date', '')
            sort_args = []
            if sort_age in ['ASC', 'DESC']:
                sort_args.append('date_of_birth' if sort_age == 'ASC' else '-date_of_birth')

            if sort_date in ['ASC', 'DESC']:
                sort_args.append('date_of_appear' if sort_date == 'ASC' else '-date_of_appear')

            data = self.queryset.filter(**filter_args).order_by(*sort_args)

            serializer = self.get_serializer(data, many=True)

            return response.Response(status=status.HTTP_201_CREATED, data=serializer.data)

        return super(PetView, self).list(request, *args, **kwargs)

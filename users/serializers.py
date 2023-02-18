from rest_framework import serializers

from users.models import Person, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class PersonListSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = Person
        fields = '__all__'


class PersonDetailSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = Person
        fields = '__all__'


class PersonCreateSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field="name"
    )

    class Meta:
        model = Person
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        self._locations = self.initial_data.pop('location')
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = Person.objects.create(**validated_data)
        for location in self._locations:
            loc_obj, _ = Location.objects.get_or_create(name=location)
            user.location.add(loc_obj)
        user.save()
        return user


class PersonUpdateSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(
        many=True,
        required=False,
        queryset=Location.objects.all(),
        slug_field="name"
    )

    class Meta:
        model = Person
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        self.location = self.initial_data.pop("location")
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        user = super().save()
        for location in self.location:
            loc_obj, _ = Location.objects.get_or_create(
                name=location,
                defaults={'lat': None, 'lng': None}
            )
            user.location.add(loc_obj)
        user.save()
        return user


class PersonDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id"]

from rest_framework import serializers
from .models import Project, Pledge, Category
from django.db.models import Sum

class PledgeSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    amount = serializers.IntegerField()
    comment = serializers.CharField()
    anonymous = serializers.BooleanField()
    supporter = serializers.ReadOnlyField(source='supporter.username')
    project_id = serializers.IntegerField()

    def create (self, validated_data):
        return Pledge.objects.create(**validated_data)

class OwnerSerializer(serializers.Serializer):
    username = serializers.ReadOnlyField(source='user.username')
    profile_image_url = serializers.URLField()
    user_bio = serializers.CharField(max_length=200)

#ProjectSerializer
class ContentSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length = 200)
    goal = serializers.IntegerField()
    image = serializers.URLField()
    is_open = serializers.BooleanField()
    date_created = serializers.DateTimeField()
    owner = OwnerSerializer()
    category = serializers.SlugRelatedField('category', queryset=Category.objects.all())

    def create(self, validated_data):
        return Project.objects.create(**validated_data)
        
#ProjectDetailSerializer
class ContentDetailSerializer(ContentSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)
    pledge_total = serializers.SerializerMethodField('get_total')

    def get_total(self, project):
        return project.pledges.aggregate(sum=Sum('amount'))['sum']

    def update(self, instance, validated_data):
        # Very limited
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        instance.save()
        return instance

class ImageSerializer(serializers.Serializer):
    content_img_name = serializers.CharField(max_length=200)
    content_img = serializers.URLField()

class SupporterContentDetailSerializer(ContentDetailSerializer):
    images = ImageSerializer(many=True)
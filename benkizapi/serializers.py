from rest_framework import serializers
from main.models import *
from benkizapi.models import *
from django.contrib.auth.models import User

class CakeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CakeCategory
        fields = ["id", "name"]


class ItemSerializer(serializers.ModelSerializer):
    category = CakeCategorySerializer(many=True, read_only=True)
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = "__all__"

    def get_thumbnail_url(self, obj):
        request = self.context.get("request")

        if not obj.thumbnail:
            return None

        url = obj.thumbnail.url

        if request:
            return request.build_absolute_uri(url)

        return f"https://benkizbakers.pythonanywhere.com{url}"

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class ItemModifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'numberOfItems', 'category']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class UserProfileSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'


class CartItemDetailSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'item', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'inittotal', 'deliveryfee', 'vat', 'totalcost']


class WishItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)

    class Meta:
        model = WishItem
        fields = ['id', 'item']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    profile_pic = serializers.ImageField(source='profile.profilepic', read_only=True)
    county = serializers.CharField(source='profile.county', read_only=True)
    rating = serializers.IntegerField(source='rating.stars', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'username', 'profile_pic', 'county', 'body', 'rating']


class TeamMemberSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user_username', 'job', 'profilepic', 'is_team']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class HeroBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroBanner
        fields = '__all__'


class ConfirmPayment(serializers.ModelSerializer):
    class Meta:
        pass

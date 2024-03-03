from rest_framework import serializers
from tasks.models import Grades, Task
from users.views import CustomUser
from users.serializers import UserSerializer


class GradesSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Grades
        fields = ["id", "value", "is_passed", "user"]

    def create(self, validated_data):
        user = validated_data.pop("user")
        task = validated_data.pop("task")
        grade = Grades.objects.create(user=user, task=task, **validated_data)
        return grade


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ["is_finished, subject"]

    def create(self, validated_data):
        subject = validated_data.pop("subject")
        task = Task.objects.create(subject=subject, **validated_data)
        return task

# class AuctionSerializer(serializers.ModelSerializer):
#     author = UserSerializer(many=False, read_only=True)
#     images = serializers.SerializerMethodField()
#     leader_bid = serializers.SerializerMethodField()
#     def create(self, validated_data):
#         """
#         Method to create auction instance with id from author model
#         :param validated_data:
#         :return:
#         """
#         author = validated_data.pop("author")
#         bid = Auction.objects.create(author=author, **validated_data)
#         return bid
#     def get_images(self, obj):
#         images = AuctionPhoto.objects.filter(auction=obj)
#         return AuctionPhotoSerializer(images, many=True, read_only=True).data
#
#     def get_leader_bid(self, obj):
#         leader_bid = Bid.objects.filter(auction=obj, leader=True).first()
#         if leader_bid:
#             return BidSerializer(leader_bid).data
#         return None
#
#     class Meta:
#         model = Auction
#         fields = [
#             "id",
#             "title",
#             "description",
#             "initial_price",
#             "min_bid_price_gap",
#             "images",
#             "author",
#             "started",
#             "finished",
#             "start_time",
#             "end_time",
#             "active",
#             "leader_bid"
#
#         ]
#         read_only_fields = ["started", "finished", "id", "author", "images",]
#
#     def validate(self, data):
#         """
#         Validates start and finish time to not be the same.
#         :param data:
#         """
#         start_time = data.get("start_time")
#         end_time = data.get("end_time")
#         duration = end_time - start_time
#         if duration.total_seconds() < MIN_AUCTION_DURATION.total_seconds():
#             raise ValidationError("The duration between start and end of auction must be at least 1 minute.")
#         return data
#
#     def update(self, instance, validated_data):
#         """
#         Updates the instance only for allowed fields.
#         :param instance:
#         :param validated_data:
#         :return:
#         """
#         allowed_fields = ["title", "description", "initial_price", "min_bid_price_gap", "start_time", "end_time"]
#         for field in validated_data:
#             if field not in allowed_fields:
#                 raise serializers.ValidationError(f"Field '{field}' cannot be updated.")
#
#         instance.title = validated_data.get("title", instance.title)
#         instance.description = validated_data.get("description", instance.description)
#         instance.initial_price = validated_data.get("initial_price", instance.initial_price)
#         instance.min_bid_price_gap = validated_data.get("min_bid_price_gap", instance.min_bid_price_gap)
#         instance.start_time = validated_data.get("start_time", instance.start_time)
#         instance.end_time = validated_data.get("end_time", instance.end_time)
#         instance.active = validated_data.get("active", instance.active)
#         instance.save()
#
#         return instance
#

#
#
# class BidSerializer(serializers.ModelSerializer):
#     author = UserSerializer(many=False, read_only=True)
#
#     class Meta:
#         model = Bid
#         fields = ["id", "price", "author", "won", "created", "leader"]
#         read_only_fields = ["created", "won", "leader"]
#
#     def create(self, validated_data):
#         """
#         Method to create bid instance with ids from author and auction models
#         :param validated_data:
#         :return:
#         """
#         author = validated_data.pop("author")
#         auction = validated_data.pop("auction")
#         bid = Bid.objects.create(author=author, auction=auction, **validated_data)
#         return bid

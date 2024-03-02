from django.db import models
from users.models import CustomUser
from education.models import Subject

MAX_TITLE_LEN = 1024
MAX_DESC_NAME = 4096


class Task(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    deadline = models.DateTimeField()
    title = models.CharField(max_length=MAX_TITLE_LEN)
    description = models.CharField(max_length=MAX_DESC_NAME)
    is_finished = models.BooleanField(default=False)
    max_points = models.PositiveIntegerField()


class Grades(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # TODO
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    value = models.IntegerField()
    is_passed = models.BooleanField(default=False)

# class Auction(models.Model):
#     title = models.CharField(max_length=MAX_AUCTION_TITLE_LENGTH)
#     description = models.TextField()
#     initial_price = models.PositiveIntegerField()
#     min_bid_price_gap = models.PositiveIntegerField()
#     author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
#     active = models.BooleanField(default=True)
#     started = models.BooleanField(default=False)
#     finished = models.BooleanField(default=False)
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()


# class Bid(models.Model):
#     price = models.PositiveIntegerField()
#     author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
#     auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)
#     won = models.BooleanField(default=False)
#     leader = models.BooleanField(default=True)
#
#     class Meta:
#         ordering = ["created"]


# class Test(models.Model):
#     id = ;
#     name = models.CharField(max_length=1024)
#     test_start = ;
#     test_end = ;
#     subject = models.ForeignKey();
#     is_finished = ;
#
#
#
# class TestQuestions(models.Model):
#     id = ;
#     test = models.ForeignKey(Test, on_delete=models.CASCADE)
#     description = ;
#     max_points = ;
#
#
#
#
# class TestAnswers(models.Model):
#     pass
#
#
# class TestChoises(models.Model):
#     pass

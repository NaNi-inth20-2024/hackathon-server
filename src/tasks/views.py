from datetime import datetime

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from tasks.models import Task, Grades
from tasks.serializers import GradesSerializer, TaskSerializer
from users.models import CustomUser


class GradesView(viewsets.ModelViewSet):
    queryset = Grades.objects.all()
    serializer_class = GradesSerializer


class TaskView(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        task = serializer.validated_data
        subject = task["subject"]
        # current_year = datetime.now().year
        # if subject.year
        users = CustomUser.objects.filter(subject__id=subject.id)
        for user in users:
            Grades(user=user, task=task, value=0)
        CustomUser.objects.get()

    # TODO create empty grade to each user who have this task(subj)

    @action(detail=True, methods=["PUT"], name="Submit task")
    def submit(self, request, pk=None):
        pass

    @action(detail=True, methods=["PUT"], name="Unsubmit task")
    def unsumbit(self, request, pk=None):
        pass

# class AuctionViewSet(viewsets.ModelViewSet):
#     """
#     AuctionViewSet provides AuthenticatedOrReadOnly auction permission while restricting PUT/PATCH for non-authors.
#     Auctions cannot be edited while being already started or finished.
#
#     Methods:
#         *CRUD*
#         activate: Activate auction
#         deactivate: Deactivate auction
#         get_winner_bid: Get winner of the auction
#         get_bids: Get bids of the auction
#     """
#
#     queryset = Auction.objects.all()
#     serializer_class = AuctionSerializer
#     validator = auction_validator
#     bid_validator = bid_validator
#     permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadAndCreateOnly)
#
#     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
#     ordering_fields = [
#         "title",
#         "initial_price",
#         "min_bid_price_gap",
#         "start_time",
#         "end_time",
#     ]
#     search_fields = [
#         "title",
#     ]
#     filterset_class = AuctionFilter
#
#     @extend_schema(
#         responses={
#             200: AuctionSerializer(),
#             409: "Conflict: Trying to update state of the instance while it is already started or finished.",
#         },
#     )
#     @action(detail=True, methods=["PUT"], name="Activate auction")
#     def activate(self, request, pk=None):
#         auction = self.get_object()
#         self.validator.is_not_finished_or_raise(auction)
#         auction.active = True
#         auction.save()
#         return Response(self.get_serializer(auction).data)
#
#     @extend_schema(
#         responses={
#             200: AuctionSerializer(),
#             409: "Conflict: Trying to update state of the instance while it is already started or finished.",
#         },
#     )
#     @action(detail=True, methods=["PUT"], name="Deactivate auction")
#     def deactivate(self, request, pk=None):
#         auction = self.get_object()
#         self.validator.is_not_finished_or_raise(auction)
#         auction.active = False
#         auction.save()
#         return Response(self.get_serializer(auction).data)
#
#     @action(detail=True, name="Winner bid of auction", url_path="winner")
#     def get_winner_bid(self, request, pk=None):
#         auction = self.get_object()
#         self.validator.is_finished_or_raise(auction)
#         winner_bid = Bid.objects.filter(auction_id=auction.id, won=True).first()
#         self.bid_validator.is_bid_winner_or_throw(winner_bid)
#         serializer = BidSerializer(winner_bid)
#         return Response(serializer.data)
#
#     @extend_schema(
#         responses={
#             200: AuctionSerializer(),
#             409: "Conflict: Trying to update state of the instance while it is already started or finished.",
#         },
#     )
#     def update(self, request, *args, **kwargs):
#         auction = self.get_object()
#         self.validator.is_not_started_or_raise(auction)
#         super().update(request, *args, **kwargs)
#
#     def destroy(self, request, *args, **kwargs):
#         auction = self.get_object()
#         self.validator.is_not_started_or_raise(auction)
#         super().destroy(request, *args, **kwargs)
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         author_username = request.user
#         author = User.objects.get(username=author_username)
#         serializer.save(author=author)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#
#     @action(detail=True, url_path="bids", name="get bids by auction id")
#     def get_bids(self, request, pk):
#         bids = Bid.objects.filter(auction_id=pk).order_by("-created")
#         page = self.paginate_queryset(bids)
#         if page is not None:
#             serializer = BidSerializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#
#         serializer = BidSerializer(bids, many=True)
#         return Response(serializer.data)

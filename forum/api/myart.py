from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin


class ForumCommentCreateRetrieveUpdateDestroyAPIView(GenericAPIView,
                                                     CreateModelMixin, RetrieveModelMixin,
                                                     UpdateModelMixin, DestroyModelMixin
                                                     ):
    """This class do the Retrieve, create, update and delete"""


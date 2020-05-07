import graphene
from .models import (
    Events
)
from django.db.models import Q, F, Prefetch
from graphene_django.filter import DjangoFilterConnectionField

from graphql_auth.schema import UserQuery, MeQuery

from .myapplication_schema import *

'''
NOTE: class name should not be the same as model
'''


class Mutation(AuthMutation, graphene.ObjectType):
    CreateUpdateEvent = CreateUpdateEvent.Field()

class Query(UserQuery, MeQuery, graphene.ObjectType):
    all_events = DjangoFilterConnectionField(
        GraphEventsType,
        getid=graphene.ID(),
        title=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int()
    )

    def resolve_all_events(self, info, title=None, getid=None, first=None, skip=None, **kwargs):
        qs = Events.objects.order_by('-creation_date')

        total_count = qs.all().count()

        if getid:
            qs = qs.filter(id=from_global_id(getid)[1]).order_by('-creation_date')

        if title:
            qs = qs.filter(title__icontains=title).order_by('-creation_date')

        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        info.context.total_count = total_count

        return qs


schema = graphene.Schema(query=Query, mutation=Mutation, auto_camelcase=False)

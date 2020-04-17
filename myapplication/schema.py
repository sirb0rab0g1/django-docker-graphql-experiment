import graphene
from graphql import GraphQLError
from graphene_django import DjangoObjectType

from .models import (
    BasicInformation,
    Events
)
from .serializers import (
    EventsSerializer
)

from django.contrib.auth.models import User

from django.db.models import Q, F, Prefetch

from graphene import relay, ObjectType
from graphene_django.filter import DjangoFilterConnectionField

from core.upload_path import generate_soa_report, generate_excell_from_filter
from graphene_django.rest_framework.mutation import SerializerMutation

'''
NOTE: class name should not be the same as model
'''


class GraphEventsType(DjangoObjectType):
    class Meta:
        model = Events
        filter_fields = {
            'id': ['exact'],
            'title': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node, )


class EventsInput(graphene.InputObjectType):
    title = graphene.String()
    description = graphene.String()
    link = graphene.String()


class EventsObject(graphene.ObjectType):
    title = graphene.String()
    description = graphene.String()
    link = graphene.String()


class EventMutation(graphene.Mutation):
    class Arguments:
        event_data = EventsInput()

    event = graphene.Field(GraphEventsType)
    @staticmethod
    def mutate(self, info, event_data=None):
        event = Events.objects.create(**event_data) # kung same params sa model pwede ra mag **
        return EventMutation(event=event)

class Mutation(graphene.ObjectType):
    crudEvent = EventMutation.Field()

class Query(graphene.ObjectType):
    all_events = DjangoFilterConnectionField(GraphEventsType)

    def resolve_all_events(self, info, **kwargs):
        return Events.objects.all()



schema = graphene.Schema(query=Query, mutation=Mutation, auto_camelcase=False)

"""
NOTE: TRY THIS INTO http://localhost:8000/api/admin/graphiql URL

{
  search_user (first_name: "pasmo123") {
    id,
    email,
    first_name,
    last_name,
    profile {
      role
    }
  }

  all_events {
    pageInfo {
        startCursor
        endCursor
        hasNextPage
        hasPreviousPage
    },
    edges {
      cursor,
      node{
        id,
        title
      }
    }
  }

  search_event (first: 2, skip:0) {
    id,
    title
  }
}
"""

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
from graphql_relay import from_global_id

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

    extra_field = graphene.String()
    # just add extra_field in query
    '''
    edges {
      node{
        id,
        title,
        extra_field
      }
    }
    '''
    def resolve_extra_field(self, info):
        return 'title : ' + self.title


class EventsInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    description = graphene.String()
    link = graphene.String()


class EventsObject(graphene.ObjectType):
    id = graphene.ID()
    title = graphene.String()
    description = graphene.String()
    link = graphene.String()

class CreateUpdateEvent(graphene.Mutation):
    class Arguments:
        event_data = EventsInput()

    event = graphene.Field(GraphEventsType)
    @staticmethod
    def mutate(self, info, event_data=None):
        if event_data.id is not None and len(list(event_data.keys())) > 1:
            event_data['id'] = from_global_id(event_data.id)[1]
            event = Events(**event_data)
            event.save()
        elif event_data.id is not None and len(list(event_data.keys())) == 1:
            event_data['id'] = from_global_id(event_data.id)[1]
            event = Events.objects.get(pk=event_data['id'])
            event.delete()
        else:
            event = Events.objects.create(**event_data)
        return CreateUpdateEvent(event=event)

class Mutation(graphene.ObjectType):
    CreateUpdateEvent = CreateUpdateEvent.Field()

class Query(graphene.ObjectType):
    all_events = DjangoFilterConnectionField(
        GraphEventsType,
        first=graphene.Int(),
        skip=graphene.Int()
    )

    def resolve_all_events(self, info, first=None, skip=None, **kwargs):
        qs = Events.objects.all()
        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        return qs


schema = graphene.Schema(query=Query, mutation=Mutation, auto_camelcase=False)

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
from core.extras import validate_fields

# image upload
from django.core.files.base import ContentFile
import base64
'''
NOTE: class name should not be the same as model
'''


class GraphEventsType(DjangoObjectType):
    class Meta:
        model = Events
        filter_fields = {}
        interfaces = (relay.Node, )

    extra_field = graphene.String()
    # just add extra_field in query
    def resolve_extra_field(self, info):
        if self.title is not None:
            return 'title : ' + self.title


class EventsInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    description = graphene.String()
    link = graphene.String()
    data_url = graphene.String() # holding data:image
    file_name = graphene.String() # holdile image file name


class EventsObject(graphene.ObjectType):
    id = graphene.ID()
    title = graphene.String()
    description = graphene.String()
    link = graphene.String()
    data_url = graphene.String() # holding data:image
    file_name = graphene.String() # holdile image file name

class CreateUpdateEvent(graphene.Mutation):
    class Arguments:
        event_data = EventsInput()

    event = graphene.Field(GraphEventsType)

    def mutate(self, info, event_data=None, image_data=None):
        if event_data.id is not None and len(list(event_data.keys())) > 1:
            event_data['id'] = from_global_id(event_data.id)[1]
            validate_fields(event_data)
            event = Events(**event_data)
            event.save()
        elif event_data.id is not None and len(list(event_data.keys())) == 1:
            event_data['id'] = from_global_id(event_data.id)[1]
            event = Events.objects.get(id=event_data['id'])
            event.delete()
        else:
            img_str = ''
            img = None
            if event_data["data_url"] is not '' or event_data["file_name"] is not None:
                img_str = event_data["data_url"].split(";base64,")[1]
                img = event_data["file_name"]

            del event_data["file_name"]
            del event_data["data_url"]

            validate_fields(event_data)
            event = Events.objects.create(**event_data)
            if img_str is not '' or img is not None:
                Events.objects.get(id=event.id).image.save(
                    img, ContentFile(base64.b64decode(img_str))
                )
        return CreateUpdateEvent(event=event)

class Mutation(graphene.ObjectType):
    CreateUpdateEvent = CreateUpdateEvent.Field()

class Query(graphene.ObjectType):
    all_events = DjangoFilterConnectionField(
        GraphEventsType,
        getid=graphene.ID(),
        title=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int()
    )

    def resolve_all_events(self, info, title=None, getid=None, first=None, skip=None, **kwargs):
        qs = Events.objects.order_by('-creation_date')

        if getid:
            qs = qs.filter(id=from_global_id(getid)[1]).order_by('-creation_date')

        if title:
            qs = qs.filter(title__icontains=title).order_by('-creation_date')

        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        return qs


schema = graphene.Schema(query=Query, mutation=Mutation, auto_camelcase=False)

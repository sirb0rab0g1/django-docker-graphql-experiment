import graphene
from graphql import GraphQLError
from graphene_django import DjangoObjectType

from .models import (
    BasicInformation,
    Events
)

from django.contrib.auth.models import User

from django.db.models import Q, F, Prefetch

from graphene import relay, ObjectType
from graphene_django.filter import DjangoFilterConnectionField

from core.upload_path import generate_soa_report, generate_excell_from_filter

'''
NOTE: class name should not be the same as model
'''


class GraphEvents(DjangoObjectType):
    class Meta:
        model = Events
        # Allow for some more advanced filtering here
        filter_fields = {
            'title': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node, )



class Query(graphene.ObjectType):
    # get_user = graphene.Field(UserType, id=graphene.Int())
    all_events = DjangoFilterConnectionField(GraphEvents)


schema = graphene.Schema(query=Query, auto_camelcase=False)

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

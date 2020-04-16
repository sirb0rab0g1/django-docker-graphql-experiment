from django.conf.urls import include
from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework_jwt import views as jwt_views

#graphql
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from .views import (
    LoginViewSet,
    SignupViewSet,
    EventsViewSet
)
from . import views

from myapplication.schema import schema

router = DefaultRouter()
router.register(r'events', views.EventsViewSet)

urlpatterns = [
    path('graphiql', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))), # view for graphql. csrf_exept = to bypass CSRF cookie not set.
    path('sign-in/', LoginViewSet.as_view(), name='sign-in'),  # making private view
    path('sign-up/', SignupViewSet.as_view(), name='sign-up'),
    path('api-token-auth/', jwt_views.obtain_jwt_token),
    path('api-token-refresh/', jwt_views.refresh_jwt_token),
    path('api-token-verify/', jwt_views.verify_jwt_token),
    path('', include(router.urls)),
]

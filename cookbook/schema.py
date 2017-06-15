import graphene
from graphene_django.debug import DjangoDebug

from ingredients.schema import CategoryMutation, IngredientMutation, Query


class Query(Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    debug = graphene.Field(DjangoDebug, name='__debug')
# schema = graphene.Schema(query=Query)


class Mutation(CategoryMutation, IngredientMutation, graphene.ObjectType):
    pass
schema = graphene.Schema(query=Query,mutation=Mutation)

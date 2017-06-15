# cookbook/ingredients/schema.py
import graphene
from graphene import relay, ObjectType, AbstractType
from graphene.relay.mutation import ClientIDMutation
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from ingredients.models import Category, Ingredient


# Graphene will automatically map the Category model's fields onto the CategoryNode.
# This is configured in the CategoryNode's Meta class (as you can see below)
class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ['name', 'ingredients']
        interfaces = (relay.Node, )


class IngredientNode(DjangoObjectType):
    class Meta:
        model = Ingredient
        # Allow for some more advanced filtering here
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'notes': ['exact', 'icontains'],
            'category': ['exact'],
            'category__name': ['exact'],
        }
        interfaces = (relay.Node, )


class Query(AbstractType):
    category = relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)

    ingredient = relay.Node.Field(IngredientNode)
    all_ingredients = DjangoFilterConnectionField(IngredientNode)


class NewCategory(ClientIDMutation):
    category = graphene.Field(CategoryNode)

    class Input:
        name = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        category = Category(name=input.get('name'))
        category.save()
        return NewCategory(category=category)


class NewIngredient(ClientIDMutation):
    ingredient = graphene.Field(IngredientNode)

    class Input:
        name = graphene.String()
        notes = graphene.String()
        category = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        ingredient = Ingredient(
            name=input.get('name'),
            notes=input.get('notes'),
            category=Category.objects.get(name=input.get('category'))
        )
        ingredient.save()
        return NewIngredient(ingredient=ingredient)


class CategoryMutation(AbstractType):
    new_category = NewCategory.Field()


class IngredientMutation(AbstractType):
    new_ingredient = NewIngredient.Field()

from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from products.models import Products,Brands,Categories,Properties


# @registry.register_document
# class BrandsDocument(Document):
#     class Index:
#         name = 'brands'
#         settings = {'number_of_shards': 1,
#                     'number_of_replicas': 0}
        
#     class Django:
#         model = Brands
#         fields = ['name',]
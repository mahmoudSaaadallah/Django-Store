from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class Tag(models.Model):
    label = models.CharField(max_length=255)

class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    # To make a generic relation we need two important attributes(Type and ID)
    # Type is the type of the object that we are going to relate
    # ID is the id of the object that we are going to relate
    # content_type which specifiy the type of the object that we are going to relate with
    # objec_id which specifiy the id of the object
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    # This is the field that will be used to retrieve the object as it store the id for the object type and the id for the object itself.
    content_object = GenericForeignKey('content_type', 'object_id')

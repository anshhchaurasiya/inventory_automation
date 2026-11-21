from django.db import models


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)


    class Meta:
        # Set your custom table name here
        db_table = 'Category'

    def __str__(self):
        return self.name
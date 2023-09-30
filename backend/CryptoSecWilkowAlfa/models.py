from django.db import models


class Name(models.Model):
    name_text = models.CharField(max_length=200)

    def __str__(self):
        return self.name_text

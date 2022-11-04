from django.db import models

class Pokemon(models.Model):
  name = models.CharField(max_length = 200)
  pokemon_id = models.SmallIntegerField()
  heigth = models.SmallIntegerField()
  weigth =  models.SmallIntegerField()
  

from django.db import models

# Create your models here.
class Dishes(models.Model):
    d_id = models.IntegerField("Dish ID",primary_key='true')
    d_name= models.CharField("Dishes name",max_length=20)
    price=models.IntegerField("Prices")
    status=models.BooleanField()
    def __str__(self):
        return '%s '% (self.d_name)
class Place(models.Model):
    Pin=models.IntegerField("Place ID",primary_key='true')
    p_name=models.CharField("Place Name",max_length=20)
    def __str__(self):
        return '%s '%(self.p_name)

class Restorent(models.Model):
    r_id=models.IntegerField("Restorent ID",primary_key='true')
    r_name= models.CharField("Restorent name",max_length=20)
    r_place=models.ForeignKey(Place,on_delete=models.CASCADE)
    dishes=models.ManyToManyField(Dishes)

    def __str__(self):
        return '%s '%(self.r_name)


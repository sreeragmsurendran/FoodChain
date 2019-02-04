from django.db import models
import uuid
from django.contrib.auth.models import User


# Create your models here.
class Dishes(models.Model):
    d_id = models.IntegerField("Dish ID", primary_key=True)
    d_name = models.CharField("Dishes name", max_length=20)
    price = models.IntegerField("Prices")
    status = models.BooleanField()

    def __str__(self):
        return self.d_name


class Place(models.Model):
    Pin = models.IntegerField("Place ID", primary_key=True)
    p_name = models.CharField("Place Name", max_length=20)

    def __str__(self):
        return self.p_name


class Address(models.Model):
    housename = models.CharField("House Name", max_length=50)
    district = models.CharField("District", max_length=20)
    village = models.CharField("Vilage", max_length=20)
    landmark = models.CharField("Landmark", max_length=50)
    pincode = models.IntegerField("PIN code")

    def __str__(self):
        return self.housename


class Restorent(models.Model):
    r_id = models.IntegerField("Restorent ID", primary_key=True)
    r_name = models.CharField("Restorent name", max_length=20)
    r_place = models.ForeignKey(Place, on_delete=models.CASCADE)
    dishes = models.ManyToManyField(Dishes)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, verbose_name='Address', null=True)

    def __str__(self):
        return self.r_name


class DishOrder(models.Model):
    O_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    dish = models.ForeignKey(Dishes, on_delete=models.CASCADE)

    def __str__(self):
        return '{}-{}'.format(self.O_id, self.dish)


class UserProfile(User):
    DelivaryAddress = models.OneToOneField(Address, on_delete=models.CASCADE, verbose_name="Delivery Address")
    image = models.ImageField("Profile", blank=True, upload_to='pro_pic/', default='pro_pic/Non_pic/download.jpg')

    def __str__(self):
        return self.username

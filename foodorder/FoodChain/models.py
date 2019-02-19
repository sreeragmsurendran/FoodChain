from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Dish(models.Model):
    d_id = models.IntegerField("Dish ID", primary_key=True)
    d_name = models.CharField("Dishes name", max_length=20)
    image = models.ImageField(null=True, upload_to="media/dish_pic/")

    def __str__(self):
        return self.d_name


class Place(models.Model):
    def validate(x):
        if len(str(x)) != 6:
            raise ValidationError("PIN number must be 6 digit number")

    Pin = models.IntegerField("Place ID", primary_key=True, validators=[validate])
    p_name = models.CharField("Place Name", max_length=20)

    def __str__(self):
        return '{}-{}'.format(self.p_name, self.Pin)


class Address(models.Model):
    def validate(x):
        if len(str(x)) != 6:
            raise ValidationError("PIN number must be 6 digit number")

    housename = models.CharField("House Name", max_length=50)
    district = models.CharField("District", max_length=20)
    village = models.CharField("Vilage", max_length=20)
    landmark = models.CharField("Landmark", max_length=50)
    pincode = models.IntegerField("PIN code", validators=[validate])

    def __str__(self):
        return self.housename


class Restorent(models.Model):
    r_id = models.IntegerField("Restorent ID", primary_key=True)
    r_name = models.CharField("Restorent name", max_length=20)
    dish = models.ManyToManyField(Dish, verbose_name="dishes")
    r_place = models.ForeignKey(Place, on_delete=models.CASCADE)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, verbose_name='Address')
    image_resr = models.ImageField(null=True, default='media/pro_pic/Non_pic/download.jpj/',
                                   upload_to="media/rest_pic/")
    userdetails = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="userdetails", null=True)

    def __str__(self):
        return self.r_name


class Customer(models.Model):
    def validate(x):
        if len(str(x)) != 10:
            raise ValidationError("Mobile number must be 10 digit number")
    name = models.CharField('Name', max_length=50, null=True)
    DelivaryAddress = models.OneToOneField(Address, verbose_name="delivaryAddress", on_delete=models.PROTECT, null=True)
    image = models.ImageField("Profile", upload_to='pro_pic/', default='pro_pic/Non_pic/download.jpg')
    phono = models.IntegerField("phoneno", validators=[validate])
    details = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='details')

    def __str__(self):
        return self.details.username


class DishItem(models.Model):
    #name = models.CharField('Name', max_length=100, default=dish.d_name)
    price = models.IntegerField("Prices")
    status = models.BooleanField("Available", default=False)
    restaurent = models.ForeignKey(Restorent, on_delete=models.CASCADE, verbose_name="rest")
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name="dish")

    def __str__(self):
        return self.dish.d_name


class DishOrder(models.Model):
    O_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    dishitem = models.ForeignKey(DishItem, on_delete=models.CASCADE, verbose_name="dishitem", null=True)
    quantity = models.IntegerField("Qty", validators=[MaxValueValidator(99), MinValueValidator(1)], default=1)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    restaurent = models.ForeignKey(Restorent, on_delete=models.CASCADE)

    def __str__(self):
        return '{}-{}'.format(self.dishitem, self.quantity)


class RestaurantOrder(models.Model):
    restorderid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    restaurant = models.ForeignKey(Restorent, verbose_name='Restaurant', on_delete=models.CASCADE)
    dishitem = models.OneToOneField(DishItem, verbose_name='Dishitem', on_delete=models.CASCADE)
    quantity = models.IntegerField('Quantity', default=0)
    customer = models.ForeignKey(Customer, verbose_name='Customer', on_delete=models.CASCADE)
    dishorder = models.OneToOneField(DishOrder, verbose_name='Dish order', on_delete=models.CASCADE)

    def __str__(self):
        return '{}-{}'.format(self.dishitem.name, str(self.quantity))

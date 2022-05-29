from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):

    name        = models.CharField('Name', max_length=30)
    description = models.CharField('Description', max_length=250)
    
    def __str__(self):
        return self.name


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):

    car_type_choices = (
        ('HT', 'Hatch'),
        ('PU', 'PickUp'),
        ('SD', 'Sedan'),
        ('SU', 'SUV'),
        ('WG', 'Wagon'),
    )

    car_make  = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField('Dealer ID', default=0)
    name      = models.CharField('Name', max_length=30)
    car_type  = models.CharField('Type', max_length=2, choices=car_type_choices)
    year      = models.DateField('Year')

    def __str__(self):
        return str(self.car_make) + ' ' + self.name

# <HINT> Create a plain Python class `CarDealer` to hold dealer data

class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, state, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state code
        self.st = st
        # Dealer state code
        self.state = state
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data

class DealerReview:

    def __init__(self, dealership, name, purchase, review, purchase_date, 
                 car_make, car_model, car_year, review_id):

        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.id = review_id
        self.sentiment = "neutral"        
        
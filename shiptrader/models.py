from django.db import models


class Starship(models.Model):
    starship_class = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)

    length = models.FloatField()
    hyperdrive_rating = models.FloatField()
    cargo_capacity = models.BigIntegerField()

    crew = models.IntegerField()
    passengers = models.IntegerField()

    def __str__(self):
        return '{} {}-{}'.format(self.id, self.starship_class, self.manufacturer)

class Listing(models.Model):
    name = models.CharField(max_length=255)
    ship_type = models.ForeignKey(Starship, related_name='listings')
    price = models.IntegerField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} {}-{}'.format(self.id, self.name)

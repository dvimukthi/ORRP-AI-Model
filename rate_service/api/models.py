from django.db import models

# Create your models here.
class Event(models.Model):
    event_name = models.CharField(max_length=100)
    event_code = models.BigIntegerField(auto_created=False)
    event_type_name = models.CharField(max_length=100)
    event_type_code = models.BigIntegerField(auto_created=False)
    event_demography = models.CharField(max_length=100)
    event_demography_code = models.CharField(max_length=100)
    show_time_code = models.BigIntegerField(auto_created=False, default=0)

    def __str__(self):
        return 'event_name = {} , event_type_name = {} , event_demography = {} '.format(self.event_name, self.event_type_name, self.event_demography)

class RoomType(models.Model):
    roomtype_name = models.CharField(max_length=100)
    roomtype_code = models.BigIntegerField()

    def __str__(self):
        return 'name = {} , code = {}  '.format(self.roomtype_name, self.roomtype_code)


class RoomCateory(models.Model):
    roomcategory_name = models.CharField(max_length=100)
    roomcategory_code = models.BigIntegerField()
    max_occupancy = models.BigIntegerField()

    def __str__(self):
        return 'name = {} , code = {} , max_occupancy = {} '.format(self.roomcategory_name, self.roomcategory_code, self.max_occupancy)

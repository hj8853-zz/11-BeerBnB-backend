from django.db import models

class Room(models.Model): 
    title         = models.CharField(max_length = 256)
    address       = models.CharField(max_length = 256)
    max_personnal = models.CharField(max_length = 48)
    bed_room      = models.CharField(max_length = 48)
    bed           = models.CharField(max_length = 48)
    bath_room     = models.CharField(max_length = 48)
    price         = models.DecimalField(max_digits = 10, decimal_places = 2)
    latitude      = models.DecimalField(max_digits = 13, decimal_places = 8)
    longitude     = models.DecimalField(max_digits = 13, decimal_places = 8)
    description   = models.CharField(max_length = 4096)
    amenity       = models.ManyToManyField('Amenity', through = 'RoomAmenity')
    host          = models.ForeignKey('user.Host', on_delete = models.CASCADE, null = True)

    class Meta: 
        db_table = 'rooms'

class BuildingType(models.Model): 
    sub_title = models.CharField(max_length = 256)
    room      = models.ForeignKey(Room, on_delete = models.CASCADE)

    class Meta: 
        db_table = 'buildingtypes'

class Image(models.Model): 
    image_url = models.URLField()
    room      = models.ForeignKey(Room, on_delete = models.CASCADE)

    class Meta: 
        db_table = 'images'

class Tag(models.Model): 
    title  = models.CharField(max_length = 96, null = True)
    detail = models.CharField(max_length = 1024, null = True)
    room   = models.ForeignKey(Room, on_delete = models.CASCADE)

    class Meta: 
        db_table = 'tags'
    
class RuleUse(models.Model): 
    rules_of_use = models.CharField(max_length = 512)
    room         = models.ForeignKey(Room, on_delete = models.CASCADE)

    class Meta: 
        db_table = 'rules_of_uses'

class HealthSafety(models.Model): 
    health_and_safety = models.CharField(max_length = 512)
    room              = models.ForeignKey(Room, on_delete = models.CASCADE)

    class Meta: 
        db_table = 'health_safeties'

class RefundPolicy(models.Model): 
    refund_policy = models.CharField(max_length = 512)
    room          = models.ForeignKey(Room, on_delete = models.CASCADE)

    class Meta: 
        db_table = 'refund_policies'

class Amenity(models.Model): 
    name = models.CharField(max_length = 1024)

    class Meta: 
        db_table = 'amenities'

class RoomAmenity(models.Model): 
    room    = models.ForeignKey(Room, on_delete = models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete = models.CASCADE)

    class Meta: 
        db_table = 'room_amenities'

class BedType(models.Model): 
    name    = models.CharField(max_length = 64, null = True)
    bedroom = models.ManyToManyField('BedRoom', through = 'BedTypeRoom')

    class Meta: 
        db_table = 'bedtypes'

class BedRoom(models.Model): 
    name = models.CharField(max_length = 256, null = True)

    class Meta: 
        db_table = 'bedrooms'

class BedTypeRoom(models.Model): 
    bedtype = models.ForeignKey(BedType, on_delete = models.CASCADE)
    bedroom = models.ForeignKey(BedRoom, on_delete = models.CASCADE)
    room    = models.ForeignKey(Room, on_delete = models.CASCADE)

    class Meta: 
        db_table = 'bed_type_rooms'
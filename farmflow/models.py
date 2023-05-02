from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Cluster(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ProducerGroup(models.Model):
    name = models.CharField(max_length=255)
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='producer_groups')

    def __str__(self):
        return f"{self.name} ({self.cluster})"

class ValueChainChoice(models.Model):
    VALUE_CHAIN_CHOICE = [
        ("Poultry", "Poultry"),
        ("Vegetable", "Vegetable"),
        ("Herbs", "Herbs"),
        ("Dairy", "Dairy"),

    ]
    name = models.CharField(max_length=255, choices=VALUE_CHAIN_CHOICE)


    def __str__(self):
        return self.name

class SoilTestResult(models.Model):
    RESPONSES = [
        ("Y", "YES"),
        ("N", "NO"),
    ]
    TYPE_CHOICES = [
        ("Complete", "Complete"),
        ("Partial", "Partial"),
    ]
    type = models.CharField(max_length=255, choices=TYPE_CHOICES)
    done = models.CharField(max_length=255, choices=RESPONSES)
    reason = models.CharField(max_length=255, blank=True)


    def __str__(self):
        return f"{self.type} - {self.done}"
    
class InputUsed(models.Model):
    AMOUNT_CHOICES = [
        ('kg', 'kg'),
        ('litres', 'litres'),
    ]
    TYPE_CHOICES = [
        ('Fertilizer', 'Fertilizer'),
        ('Pesticides', 'Pesticides'),
    ]
    type = models.CharField(max_length=255, choices=TYPE_CHOICES)
    value_chain = models.ForeignKey(ValueChainChoice, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    # quantity = models.PositiveSmallIntegerField(blank=True, null=True)
    amount = models.CharField(max_length=255, choices=AMOUNT_CHOICES)

    farms = models.ManyToManyField('Farm', through='FarmInputUsed')

    def __str__(self):
        return f"{self.name} ({self.amount} of {self.type})"   

class FarmingType(models.Model):
    FARMING_CHOICES = [
        ("Outdoor", "Outdoor"),
        ("Greenhouse", "Greenhouse"),

    ]
    type = models.CharField(max_length=255, choices=FARMING_CHOICES)

    def __str__(self):
        return self.type

class WaterSource(models.Model):
    WATER_SOURCE_CHOICES = [
        ("Borehole", "Borehole"),
        ("River", "River"),
        ("Dam", "Dam"),
        ("Rain", "Rain"),
        ("Swamp", "Swamp"),
        ('Other', 'other')
    ]
    type = models.CharField(max_length=255, choices=WATER_SOURCE_CHOICES)

    def __str__(self):
        return self.type

class Profile(models.Model):
    GENDER_CHOICES =[
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email= models.EmailField(max_length=255, unique=True, blank=True, null=True)
    avatar = CloudinaryField('image', default='https://res.cloudinary.com/fevercode/image/upload/v1654534329/default_n0r7rf.png')
    bio = models.TextField(max_length=500, default='This is my bio')
    name = models.CharField(max_length=255, blank=True)
    producer_group = models.ForeignKey(ProducerGroup, on_delete=models.SET_NULL, null=True, blank=True)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES)
    id_number = models.PositiveBigIntegerField(unique=True, blank=True, null=True)
    phone_number = PhoneNumberField(unique=True, null=True, blank=True)
    plot_size = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, default=0)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def create_profile(self):
        self.save()
        
    def update_profile(self, new_bio):
        self.bio = new_bio
        self.save()

    def __str__(self):
        return f"{self.user.username} ({self.producer_group}) Profile"


class Farm(models.Model):
    owner = models.ForeignKey(User, related_name='farmer', on_delete=models.CASCADE)
    location = models.CharField(max_length=55)
    crops = models.ManyToManyField('Crop', related_name='crops', blank=True)
    length = models.PositiveIntegerField(default=0)
    width = models.PositiveIntegerField(default=0)
    is_leased = models.BooleanField(default=False)
    soil_test = models.ForeignKey(SoilTestResult, on_delete=models.CASCADE)
    water_source = models.ForeignKey(WaterSource, on_delete=models.CASCADE)
    farming_type = models.ForeignKey(FarmingType, on_delete=models.CASCADE)
    value_chain = models.ForeignKey(ValueChainChoice, on_delete=models.CASCADE)

    input_used = models.ManyToManyField('InputUsed', through='FarmInputUsed')

    @classmethod
    def my_farms(cls, user_id):
        return cls.objects.filter(owner__id=user_id)

    def __str__(self):
        crop_names = ', '.join([crop.name for crop in self.crops.all()])
        return f"{self.owner.get_full_name()}'s farm ({self.value_chain}): {crop_names}"

    
class FarmInputUsed(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    input_used = models.ForeignKey(InputUsed, on_delete=models.CASCADE)
    quantity_used = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.farm} used {self.quantity_used} {self.input_used.amount} of {self.input_used.name}"
class Crop(models.Model):
    name = models.CharField(max_length=55,)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class CropProductionStage(models.Model):
    planted_date = models.DateField(auto_now_add=True)
    harvested_date = models.DateField(auto_now=True)
    ploughing = models.DateField()
    weeding = models.DateField()
    harvesting = models.DateField()
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    inputs = models.ManyToManyField(InputUsed, blank=True)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.crop} Production Stage on {self.farm}"
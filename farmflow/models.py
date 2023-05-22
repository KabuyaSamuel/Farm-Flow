from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from phonenumber_field.modelfields import PhoneNumberField
import uuid
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Q


# Create your models here.
class Cluster(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ProducerGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)
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
    name = models.CharField(max_length=255, choices=VALUE_CHAIN_CHOICE, unique=True)


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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['type', 'done'], name='unique_test_result'),
            models.CheckConstraint(
                check=Q(done='Y') | ~Q(done='N') | ~Q(reason=''),
                name='reason_required_for_no',
            ),
        ]

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
    amount = models.CharField(max_length=255, choices=AMOUNT_CHOICES)
    farms = models.ManyToManyField('Farm', through='FarmInputUsed')

    def __str__(self):
        return f"{self.name} ({self.amount} of {self.type})"   

class FarmingType(models.Model):
    FARMING_CHOICES = [
        ("Outdoor", "Outdoor"),
        ("Greenhouse", "Greenhouse"),

    ]
    type = models.CharField(max_length=255, choices=FARMING_CHOICES, unique=True)

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
    type = models.CharField(max_length=255, choices=WATER_SOURCE_CHOICES, unique=True)

    def __str__(self):
        return self.type

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
    input_used = models.ManyToManyField('InputUsed', through='FarmInputUsed')
    value_chains = models.ManyToManyField(ValueChainChoice, blank=True)
    STATUS_CHOICES = [
        ('Pending', 'Pending Approval'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ]
    approval_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    @classmethod
    def my_farms(cls, user_id):
        return cls.objects.filter(owner__id=user_id)

    def __str__(self):
        value_chain_names = ', '.join([value_chain.name for value_chain in self.value_chains.all()])
        crop_names = [crop.name for crop in self.crops.all()]
        crop_str = crop_names[0] if len(crop_names) == 1 else ', '.join(crop_names)
        return f"{self.owner.get_full_name()}'s farm ({value_chain_names}) growing {crop_str} in {self.location} - {self.approval_status}"

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
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, null=True)
      
    def create_profile(self):
        self.save()
        
    def update_profile(self, new_bio):
        self.bio = new_bio
        self.save()
    
    def save(self, *args, **kwargs):
        self.name = f"{self.user.first_name} {self.user.last_name}"  # set the name as the user's first and last name
        self.email = self.user.email
        super().save(*args, **kwargs)  # call the original save method

    def __str__(self):
        return f"{self.user.username} ({self.producer_group}) Profile"

class Crop(models.Model):
    name = models.CharField(max_length=55,unique=True)
    description = models.CharField(max_length=255)
    value_chain = models.ForeignKey(ValueChainChoice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.value_chain})"
    
class FarmInputUsed(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    input_used = models.ForeignKey(InputUsed, on_delete=models.CASCADE)
    quantity_used = models.PositiveSmallIntegerField(blank=True, null=True)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    date_used =  models.DateField()

    def __str__(self):
        return f"{self.farm} used {self.quantity_used} {self.input_used.amount} of {self.input_used.name} on {self.date_used}"

class CropProductionStage(models.Model):
    planted_date = models.DateField()
    harvested_date = models.DateField()
    ploughing = models.DateField()
    weeding = models.DateField()
    harvesting = models.DateField()
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    inputs = models.ManyToManyField(InputUsed, blank=True)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)

    def clean(self):
        if self.harvested_date < self.planted_date:
            raise ValidationError('Harvested date cannot be before planted date')

        if self.harvesting > self.harvested_date:
            raise ValidationError('Harvesting date cannot be greater than harvested date')

        if self.harvesting > timezone.now().date():
            raise ValidationError('Harvesting date cannot be in the future')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.crop} production stage at {self.farm} ({self.planted_date} - {self.harvested_date})"
    
class Produce(models.Model):
    GRADE_CHOICES = [
    ('Grade A', 'Grade A'),
    ('Grade B', 'Grade B'),
    ('Grade C', 'Grade C'),
    ]
    farmer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    grade = models.CharField(max_length=255, choices=GRADE_CHOICES)
    production_date = models.DateField()
    value_chain = models.ForeignKey(ValueChainChoice, on_delete=models.CASCADE)
    # Add a field to track the status of the produce (e.g., harvested, in transit, at the market, sold).
    STATUS_CHOICES = [
        ('Harvested', 'Harvested'),
        ('In Transit', 'In Transit'),
        ('At the Market', 'At the Market'),
        ('Sold', 'Sold'),
    ]
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    # Add a field to track the location of the produce, such as the name of the market or the name of the buyer.
    location = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.type} - {self.quantity}kg of {self.grade} by ({self.farmer.user.username}) on {self.production_date} currently {self.status}'
    
class Tag(models.Model):
    tag_id = models.CharField(max_length=36, unique=True, editable=False)
    farmer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    produce = models.ForeignKey(Produce, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='Harvested')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.tag_id:
            self.tag_id = str(uuid.uuid4())

    def save(self, *args, **kwargs):
        if self.produce:
            self.status = self.produce.status
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Tag #{self.tag_id} ({self.produce.type} from {self.farmer.user.username})"
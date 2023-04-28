from django.db import models

# Create your models here.
class Cluster(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

class ProducerGroup(models.Model):
    name = models.CharField(max_length=255)
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE)

class ValueChainChoice(models.Model):
    VALUE_CHAIN_CHOICE = [
        ("Poultry", "Poultry"),
        ("Vegetable", "Vegetable"),
        ("Herbs", "Herbs"),
        ("Dairy", "Dairy"),

    ]

    name = models.CharField(max_length=255, choices=VALUE_CHAIN_CHOICE)

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
    
class InputUsed(models.Model):
    type = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    amount = models.CharField(max_length=255)

class FarmingType(models.Model):
    FARMING_CHOICES = [
        ("Outdoor", "Outdoor"),
        ("Greenhouse", "Greenhouse"),

    ]
    type = models.CharField(max_length=255, choices=FARMING_CHOICES)

class WaterSource(models.Model):
    WATER_SOURCE_CHOICES = [
        ("Borehole", "Borehole"),
        ("River", "River"),
        ("Dam", "Dam"),
        ("Rain", "Rain"),
        ("Swamp", "Swamp")
    ]
    type = models.CharField(max_length=255, choices=WATER_SOURCE_CHOICES)
class Farmer(models.Model):
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    id_number = models.FloatField(max_length=8)
    mobile_number = models.CharField(max_length=13)
    plot_size = models.FloatField()
    producer_group = models.ForeignKey(ProducerGroup, on_delete=models.CASCADE)
    value_chain_choice = models.ForeignKey(ValueChainChoice, on_delete=models.CASCADE)
    farming_type = models.ForeignKey(FarmingType, on_delete=models.CASCADE)
    water_source = models.ForeignKey(WaterSource, on_delete=models.CASCADE)
    soil_test_result = models.ForeignKey(SoilTestResult, on_delete=models.CASCADE)
    inputs_used = models.ForeignKey(InputUsed, on_delete=models.CASCADE)
    
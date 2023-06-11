from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from datetime import datetime, date, timedelta
from django.utils import timezone
from django.test import TestCase
from ..models import (
    Cluster, ProducerGroup, ValueChainChoice, SoilTestResult, InputUsed,
    FarmingType, WaterSource, Farm, Profile, Crop, FarmInputUsed,
    CropProductionStage, Produce, Tag
)


class ClusterModelTest(TestCase):
    def test_cluster_creation(self):
        cluster = Cluster.objects.create(name="Test Cluster", location="Test Location")
        self.assertEqual(cluster.name, "Test Cluster")
        self.assertEqual(cluster.location, "Test Location")
        self.assertEqual(str(cluster), "Test Cluster")

class ProducerGroupModelTest(TestCase):
    def setUp(self):
        self.cluster = Cluster.objects.create(name="Test Cluster", location="Test Location")

    def test_producer_group_creation(self):
        producer_group = ProducerGroup.objects.create(name="Test Group", cluster=self.cluster)
        self.assertEqual(producer_group.name, "Test Group")
        self.assertEqual(producer_group.cluster, self.cluster)
        self.assertEqual(str(producer_group), "Test Group (Test Cluster)")


class ValueChainChoiceModelTest(TestCase):
    def test_value_chain_choice_creation(self):
        value_chain_choice = ValueChainChoice.objects.create(name="Poultry")
        self.assertEqual(value_chain_choice.name, "Poultry")
        self.assertEqual(str(value_chain_choice), "Poultry")

class SoilTestResultModelTest(TestCase):
    def test_soil_test_result_creation(self):
        soil_test_result = SoilTestResult.objects.create(type="Complete", done="Y")
        self.assertEqual(soil_test_result.type, "Complete")
        self.assertEqual(soil_test_result.done, "Y")
        self.assertEqual(str(soil_test_result), "Complete - Y")


    def test_soil_test_result_complete_with_reason(self):
        soil_test_result = SoilTestResult.objects.create(type="Complete", done="Y", reason="Test Reason")
        self.assertEqual(soil_test_result.type, "Complete")
        self.assertEqual(soil_test_result.done, "Y")
        self.assertEqual(soil_test_result.reason, "Test Reason")
        self.assertEqual(str(soil_test_result), "Complete - Y")

    def test_soil_test_result_unique_constraint(self):
        # Create a soil test result with the same type and "done" value
        SoilTestResult.objects.create(type="Complete", done="Y")
        
        # Attempt to create another soil test result with the same values
        with self.assertRaises(IntegrityError):
            SoilTestResult.objects.create(type="Complete", done="Y")

class InputUsedModelTest(TestCase):
    def setUp(self):
        self.value_chain = ValueChainChoice.objects.create(name="Poultry")
        
    def test_input_used_creation(self):
        input_used = InputUsed.objects.create(
            type="Fertilizer",
            value_chain=self.value_chain,
            name="Nitrogen",
            amount="kg"
        )
        self.assertEqual(input_used.type, "Fertilizer")
        self.assertEqual(input_used.value_chain, self.value_chain)
        self.assertEqual(input_used.name, "Nitrogen")
        self.assertEqual(input_used.amount, "kg")
        self.assertEqual(
            str(input_used),
            "Nitrogen (kg of Fertilizer)"
        )

    def test_input_used_str_representation(self):
        input_used = InputUsed(
            type="Pesticides",
            value_chain=self.value_chain,
            name="Insecticide",
            amount="litres"
        )
        self.assertEqual(
            str(input_used),
            "Insecticide (litres of Pesticides)"
        )
class FarmingTypeModelTest(TestCase):
    def test_farming_type_creation(self):
        farming_type = FarmingType.objects.create(type="Outdoor")
        self.assertEqual(str(farming_type), "Outdoor")

    def test_farming_type_unique_constraint(self):
        FarmingType.objects.create(type="Outdoor")
        with self.assertRaises(IntegrityError):
            FarmingType.objects.create(type="Outdoor")

class WaterSourceModelTest(TestCase):
    def test_water_source_creation(self):
        water_source = WaterSource.objects.create(type="Borehole")
        self.assertEqual(str(water_source), "Borehole")

    def test_water_source_unique_constraint(self):
        WaterSource.objects.create(type="Borehole")
        with self.assertRaises(IntegrityError):
            WaterSource.objects.create(type="Borehole")

# class FarmModelTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#         self.value_chain = ValueChainChoice.objects.create(name="Poultry")
#         self.crop1 = Crop.objects.create(name='Crop 1', value_chain=self.value_chain)
#         self.crop2 = Crop.objects.create(name='Crop 2', value_chain=self.value_chain)

#     def test_farm_creation(self):
#         farm = Farm.objects.create(
#             owner=self.user,
#             location='Test Location',
#             approval_status='Pending'
#         )
#         farm.crops.add(self.crop1, self.crop2)
#         farm.save()

#         self.assertEqual(farm.owner, self.user)
#         self.assertEqual(farm.location, 'Test Location')
#         self.assertEqual(farm.approval_status, 'Pending')
#         self.assertCountEqual(farm.crops.all(), [self.crop1, self.crop2])
#         self.assertEqual(
#             str(farm),
#             "Testuser's farm () growing Crop 1, Crop 2 in Test Location - Pending"
#         )

# class ProfileModelTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create(username='testuser')
#         self.cluster = Cluster.objects.create(name='Test Cluster')
#         self.producer_group = ProducerGroup.objects.create(name='Test Producer Group', cluster=self.cluster)
#         self.farm = Farm.objects.create(name='Test Farm')

#     def test_profile_creation(self):
#         profile = Profile.objects.create(
#             user=self.user,
#             gender='Male',
#             farm=self.farm,
#             producer_group=self.producer_group
#         )
#         self.assertEqual(profile.name, f"{self.user.first_name} {self.user.last_name}")
#         self.assertEqual(profile.email, self.user.email)
#         self.assertEqual(profile.producer_group, self.producer_group)

class CropModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a value chain choice for testing
        value_chain = ValueChainChoice.objects.create(name='Test Value Chain')

        # Create a crop for testing
        Crop.objects.create(name='Test Crop', description='Test Description', value_chain=value_chain)

    def test_crop_str_representation(self):
        crop = Crop.objects.get(name='Test Crop')
        expected_str = 'Test Crop (Test Value Chain)'
        self.assertEqual(str(crop), expected_str)

# class FarmModelTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
        
#         # Create a valid SoilTestResult object
#         soil_test = SoilTestResult.objects.create(type='Complete', done='Y')
#         water_source = WaterSource.objects.create(type='Borehole')
#         # Create a valid FarmingType object
#         farming_type = FarmingType.objects.create(type='Farming Type')
#         # Associate the SoilTestResult with the Farm instance
#         self.farm = Farm.objects.create(
#             owner=self.user,
#             location='Test Location',
#             soil_test=soil_test,  # Associate the SoilTestResult
#             farming_type=farming_type,
#             water_source=water_source,
        
#         )
        
#     def test_farm_str_representation(self):
#         expected_str = "'s farm () growing in Test Location - Pending"
#         self.assertEqual(str(self.farm), expected_str)
        
# class FarmInputUsedModelTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create(username='testuser')
#         self.soil_test_result = SoilTestResult.objects.create(type='Complete', done='Y')
#         self.water_source = WaterSource.objects.create(type='River')
#         self.farming_type = FarmingType.objects.create(type='Outdoor')
#         self.value_chain = ValueChainChoice.objects.create(name='Poultry')  # Add a ValueChainChoice instance
#         self.farm = Farm.objects.create(
#             owner=self.user,
#             location='Test Location',
#             soil_test=self.soil_test_result,
#             water_source=self.water_source,
#             farming_type=self.farming_type,
#             approval_status='Approved'
#         )
#         self.input_used = InputUsed.objects.create(
#             type='Fertilizer',
#             value_chain=self.value_chain,  # Set the value_chain field
#             name='Fertilizer A',
#             amount='kg'
#         )
#         self.crop = Crop.objects.create(
#             name='Test Crop',
#             description='Crop description',
#             value_chain=self.value_chain  # Set the value_chain field
#         )
#         self.farm_input_used = FarmInputUsed.objects.create(
#             farm=self.farm,
#             input_used=self.input_used,
#             quantity_used=10,
#             crop=self.crop,
#             date_used=date.today()
#         )

#     def test_farm_input_used_str_representation(self):
#         value_chain_names = ', '.join([value_chain.name for value_chain in self.farm.value_chains.all()])
#         crop_name = self.farm_input_used.crop.name
#         print("Crop name:", crop_name)
#         expected_str = f"{self.farm.owner.get_full_name()}'s farm ({value_chain_names}) growing {crop_name} in {self.farm.location} - {self.farm.approval_status} used {self.farm_input_used.quantity_used} {self.farm_input_used.input_used.amount} of {self.farm_input_used.input_used.name} on {self.farm_input_used.date_used}"
#         self.assertEqual(str(self.farm_input_used), expected_str)

class CropProductionStageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.soil_test_result = SoilTestResult.objects.create(type='Complete', done='Y')
        self.water_source = WaterSource.objects.create(type='River')
        self.farming_type = FarmingType.objects.create(type='Outdoor')
        self.value_chain = ValueChainChoice.objects.create(name='Poultry')
        self.crop = Crop.objects.create(
            name='Test Crop',
            description='Crop description',
            value_chain=self.value_chain
        )
        self.input_used = InputUsed.objects.create(
            type='Fertilizer',
            value_chain=self.value_chain,
            name='Fertilizer A',
            amount='kg'
        )
        self.farm = Farm.objects.create(
            owner=self.user,
            location='Test Location',
            soil_test=self.soil_test_result ,
            water_source=self.water_source,
            farming_type=self.farming_type,
            approval_status='Approved'
        )
        self.crop_production_stage = CropProductionStage.objects.create(
            planted_date=date(2023, 1, 1),
            harvested_date=date(2023, 2, 1),
            ploughing=date(2023, 1, 2),
            weeding=date(2023, 1, 15),
            harvesting=date(2023, 1, 30),
            crop=self.crop,
            farm=self.farm
        )

    def test_valid_crop_production_stage(self):
        expected_str = f"{self.crop} production stage at {self.farm} ({self.crop_production_stage.planted_date} - {self.crop_production_stage.harvested_date})"
        self.assertEqual(str(self.crop_production_stage), expected_str)

    def test_planted_date_greater_than_harvested_date(self):
        self.crop_production_stage.planted_date = date(2023, 2, 1)
        self.crop_production_stage.harvested_date = date(2023, 1, 1)  # Set an earlier harvested_date

        with self.assertRaises(ValidationError) as context:
            self.crop_production_stage.full_clean()

        self.assertEqual(
            context.exception.message_dict,
            {'__all__': ['Harvested date cannot be before planted date']}
        )

    def test_invalid_crop_production_stage_harvesting_date(self):
        self.crop_production_stage.planted_date = date(2023, 1, 1)
        self.crop_production_stage.harvested_date = date(2023, 2, 1)
        self.crop_production_stage.harvesting = date(2023, 2, 2)  # Set a harvesting date after the harvested_date

        with self.assertRaises(ValidationError) as context:
            self.crop_production_stage.full_clean()

        self.assertEqual(
            context.exception.message_dict,
            {'__all__': ['Harvesting date cannot be greater than harvested date']}
        )

    

    def test_invalid_crop_production_stage_planted_date(self):
        self.crop_production_stage.planted_date = date(2023, 2, 1)
        self.crop_production_stage.harvested_date = date(2023, 1, 1)  # Set an earlier harvested_date

        with self.assertRaises(ValidationError) as context:
            self.crop_production_stage.full_clean()

        self.assertEqual(
            context.exception.message_dict,
            {'__all__': ['Harvested date cannot be before planted date']}
        )

    def test_invalid_crop_production_stage_future_harvesting_date(self):
        future_date = timezone.now().date() + timedelta(days=7)  # Set a future date

        self.crop_production_stage.planted_date = date(2023, 1, 1)
        self.crop_production_stage.harvested_date = date(2023, 2, 1)
        self.crop_production_stage.harvesting = future_date

        with self.assertRaises(ValidationError) as context:
            self.crop_production_stage.full_clean()

        self.assertEqual(
            context.exception.message_dict,
            {'__all__': ['Harvesting date cannot be greater than harvested date']}
        )


  


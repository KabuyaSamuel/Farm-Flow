from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from datetime import datetime
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
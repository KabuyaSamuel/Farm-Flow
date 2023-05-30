from django.test import TestCase
from ..models import Cluster, ProducerGroup, ValueChainChoice


class ModelsTestCase(TestCase):
    def setUp(self):
        # Create a sample Cluster instance
        self.cluster = Cluster.objects.create(
            name='Sample Cluster',
            location='Sample Location'
        )

        # Create a sample ProducerGroup instance
        self.producer_group = ProducerGroup.objects.create(
            name='Sample Producer Group',
            cluster=self.cluster
        )

        # Create a sample ValueChainChoice instance
        self.value_chain_choice = ValueChainChoice.objects.create(
            name='Sample Value Chain Choice'
        )

    def test_cluster_str(self):
        self.assertEqual(str(self.cluster), 'Sample Cluster')

    def test_producer_group_str(self):
        expected_str = 'Sample Producer Group (Sample Cluster)'
        self.assertEqual(str(self.producer_group), expected_str)

    def test_value_chain_choice_str(self):
        self.assertEqual(str(self.value_chain_choice), 'Sample Value Chain Choice')

import unittest
from pySidraData.models import Aggregate, Research, RootData


class TestModels(unittest.TestCase):

    def test_aggregate(self):
        """Test the Aggregate data class."""
        aggregate = Aggregate(id="1234", nome="Test Aggregate")
        self.assertEqual(aggregate.id, "1234")
        self.assertEqual(aggregate.nome, "Test Aggregate")

    def test_research(self):
        """Test the Research data class."""
        aggregate1 = Aggregate(id="1234", nome="Test Aggregate 1")
        aggregate2 = Aggregate(id="5678", nome="Test Aggregate 2")
        research = Research(
            id="0001", nome="Test Research", agregados=[aggregate1, aggregate2]
        )
        self.assertEqual(research.id, "0001")
        self.assertEqual(research.nome, "Test Research")
        self.assertEqual(len(research.agregados), 2)

    def test_root_data(self):
        """Test the RootData data class."""
        research1 = Research(id="0001", nome="Test Research 1", agregados=[])
        research2 = Research(id="0002", nome="Test Research 2", agregados=[])
        root_data = RootData(research_list=[research1, research2])
        self.assertEqual(len(root_data.research_list), 2)


if __name__ == "__main__":
    unittest.main()

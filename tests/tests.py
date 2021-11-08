import unittest
# from tests import BaseAPITestClass
import unittest
from  api.schemas import CreateBoulderRequestBody, CreateBoulderRequestValidator, BoulderFields
from marshmallow import ValidationError

# class BaseAPITestClass(unittest.TestCase):
#     """
#     BaseClass for testing
#     """

#     def setUp(self):
#         """
#         Set up method that will run before every test
#         """
#         pass

#     def tearDown(self):
#         """
#         Tear down method that will run after every test
#         """
#         pass


class BoulderCreationTests(unittest.TestCase):

    def test_create_boulder(self):
        """
        """
        # Given 
        fields = BoulderFields()
        data = {
            fields.raters: 'a',
            fields.rating: 'a',
            fields.section: 1,
            fields.creator: 2,
            fields.difficulty: [],
            fields.feet: dict(),
            fields.name: 5,
            fields.time: 23,
            fields.notes: None,
            fields.holds: 'holds'
        }
        # When 
        with self.assertRaises(ValidationError) as context:
            _ = CreateBoulderRequestValidator().load(data)
        # Then
        self.assertIn('raters', context.exception.messages)
        self.assertIn('rating', context.exception.messages)
        self.assertIn('section', context.exception.messages)
        self.assertIn('creator', context.exception.messages)
        self.assertIn('difficulty', context.exception.messages)
        self.assertIn('feet', context.exception.messages)
        self.assertIn('name', context.exception.messages)
        self.assertIn('time', context.exception.messages)
        self.assertIn('notes', context.exception.messages)
        self.assertIn('holds', context.exception.messages)

if __name__ == '__main__':
    unittest.main()

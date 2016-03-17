import unittest
from phonebook import Phonebook


class PhonebookTest(unittest.TestCase):

	def setUp(self):
		self.phonebook = Phonebook()

	def test_lookup_entry_by_name(self):
		phonebook = self.phonebook
		number = "12343"
		phonebook.add("Tania",number)
		self.assertEqual(number,phonebook.lookup("Tania"))
	def test_missing_entry_raises_KeyError(self):
		phonebook = self.phonebook
		with self.assertRaises(KeyError):
			phonebook.lookup("mising")

	def test_empty_phonebook_is_consistent(self):
		self.assertTrue(self.phonebook.is_consistent())
	
	def test_duplicate_number(self):
		number = "12334"
		self.phonebook.add("bob",number)
		self.phonebook.add("mary",number)
		self.assertFalse(self.phonebook.is_consistent())

	def test_phonebook_with_numbers_that_prefix_other_number_is_consistent(self):
		self.phonebook.add("bob","123")
		self.phonebook.add("mary","12334")
		self.assertFalse(self.phonebook.is_consistent())

	def test_phonebook_adds_names_and_numbers(self):
		self.phonebook.add("sue","1234")
		self.assertIn("sue",self.phonebook.get_names())
		self.assertIn("1234",self.phonebook.get_numbers())
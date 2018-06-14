from unittest.mock import patch, Mock
from django.test import TestCase

from django_oaipmh.models import OAIItem
from django_oaipmh.exceptions import CannotDisseminateFormat

class TestOAIItem(TestCase):

    def test_get_oai_queryset(self):
        # Should only be implemented / called on subclasses
        with self.assertRaises(NotImplementedError):
            OAIItem.get_oai_queryset()

    def test_get_oai_record(self):
        # Create a class that implements OAIItem
        class Book(OAIItem):
            def get_oai_record_dc(self): # has dublin core md
                return 'foo'
        book = Book()
        # Looking for dublin core prefix should work
        assert book.get_oai_record('dc') == 'foo'
        # Metadata formats without methods should raise CannotDisseminateFormat
        with self.assertRaises(CannotDisseminateFormat):
            book.get_oai_record('ead')

    def test_oai_identifier(self):
        # Instance method; raises if not implemented on subclass
        class Rock(OAIItem):
            pass
        rock = Rock()
        with self.assertRaises(NotImplementedError):
            rock.oai_identifier()

    def test_oai_datestamp(self):
        # Instance method; raises if not implemented on subclass
        class Bone(OAIItem):
            pass
        bone = Bone()
        with self.assertRaises(NotImplementedError):
            bone.oai_datestamp()

    def test_oai_sets(self):
        # Returns empty set if not implemented on subclass
        class Tooth(OAIItem):
            pass
        tooth = Tooth()
        assert tooth.oai_sets() == []

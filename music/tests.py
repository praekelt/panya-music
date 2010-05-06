import unittest
        
from django.db.models.query import QuerySet

from music.views import ListenLive

class ListenLiveViewTestCase(unittest.TestCase):
    def test_get_queryset(self):
        queryset = ListenLive().get_queryset()
        
        # should return a queryset
        self.failUnlessEqual(queryset.__class__, QuerySet)

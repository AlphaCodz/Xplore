from django.test import TestCase
from touragency.models import TourAgency

# Create your tests here.
class TourAgencyTest(TestCase):
    
    def setUp(self):
        TourAgency.objects.create(
            name= "TourSP Travels and Tours",
            logo = "http://127.0.0.1:8000/media/media/tour_agency/license/16154101ac0c2fe5134722030b820030.jpg",
            email = "testpy@gmail.com",
            address = "test stree Lagos country",
            phone_number = int("09052435027"),
            license = "http://127.0.0.1:8000/media/media/tour_agency/CAC/image-jpg-t-1609860722-size-Large.jpg",
            cac = "http://127.0.0.1:8000/media/media/tour_agency/CAC/image-jpg-t-1609860722-size-Large.jpg",
        )
    
    def test_tour_agency(self):
        agency_TourSP = TourAgency.objects.get(name="TourSP Travels and Tours")
        agency_logo = TourAgency.objects.get(logo = "http://127.0.0.1:8000/media/media/tour_agency/license/16154101ac0c2fe5134722030b820030.jpg")
        self.assertEqual(
            agency_logo.get_agency(), "Tour Agency: TourSP Travels and Tours"
        )
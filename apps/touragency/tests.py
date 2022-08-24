from django.test import TestCase
from touragency.models import TourAgency
from tours.models import Tour

# Create your tests here.
class TourAgencyTest(TestCase):
    
    def setUp(self):
        TourAgency.objects.create(
            name= "TourSP Travels and Tours",
            profile_pic = "http://127.0.0.1:8000/media/media/tour_agency/license/16154101ac0c2fe5134722030b820030.jpg",
            email = "testpy@gmail.com",
            address = "test stree Lagos country",
            phone_number = int("09052435027"),
            license = "http://127.0.0.1:8000/media/media/tour_agency/CAC/image-jpg-t-1609860722-size-Large.jpg",
            cac = "http://127.0.0.1:8000/media/media/tour_agency/CAC/image-jpg-t-1609860722-size-Large.jpg",
        )
    
    def test_tour_agency(self):
        agency_TourSP = TourAgency.objects.get(name="TourSP Travels and Tours")
        agency_logo = TourAgency.objects.get(profile_pic = "http://127.0.0.1:8000/media/media/tour_agency/license/16154101ac0c2fe5134722030b820030.jpg")
        self.assertEqual(
            agency_logo.get_agency(), "Tour Agency: TourSP Travels and Tours"
        )
        self.assertEqual(
             agency_TourSP.get_agency(), "Tour Agency: TourSP Travels and Tours"
        )
        
# CREATE TOUR
class AddTourTest(TestCase):
    
    def setUp(self):
        Tour.objects.create(
            name = "LASU Campus Tour",
            description = "LASU",
            location = "LASU",
            start_date = "2022-05-15",
            end_date = "2022-05-20",
            image = "http://127.0.0.1:8000/media/media/tour_agency/license/16154101ac0c2fe5134722030b820030.jpg"    
        )
    def test_add_tour(self):
        tour_name = Tour.objects.get(name="LASU Campus Tour")
        tour_description = Tour.objects.get(description= "LASU")
        self.assertEqual(
            tour_name.get_tour(), "Tour: LASU Campus Tour"
        )
        self.assertEqual(
            tour_description.get_tour(), "Tour: LASU Campus Tour"
        )
        
        self.assertEqual(
            tour_name.get_tour(), "Tour: LASU Campus Tour"
        )
        
        
        
        

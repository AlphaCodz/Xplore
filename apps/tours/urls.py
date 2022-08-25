from django.urls import path, re_path
from .views import (
    TourList, BookTour, tourPackageList,
    BookingList, BookingDetail, SubmitPayment, TourSearchList,
    rate_package, RequestTour
    )

urlpatterns = [
    path("list", TourList.as_view(), name="tourlist"),
    path('book', BookTour.as_view(), name='book-tour'),
    path('request', RequestTour.as_view(), name='request-tour'),
    path("<id>/packages", tourPackageList, name="packages"),
    path('bookings', BookingList.as_view(), name='booking-list'),
    path('booking/<pk>/detail', BookingDetail.as_view(), name='booking-detail'),
    path('booking/<pk>/pay', SubmitPayment.as_view() , name="submit-payment"),
    path('', TourSearchList.as_view(), name="tour-search" ),
    path('package/rate', rate_package , name='rate-package'),
]

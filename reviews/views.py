from django.db.models import Avg
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Review
from bookings.models import Booking
from workers.models import Worker


class CreateReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id):

        booking = get_object_or_404(Booking, id=booking_id)

        # Only customer who booked can review
        if booking.customer != request.user:
            return Response(
                {"error": "You cannot review this booking"},
                status=status.HTTP_403_FORBIDDEN
            )

        if booking.status != "completed":
            return Response(
                {"error": "Booking must be completed before review"},
                status=status.HTTP_400_BAD_REQUEST
            )

        rating = request.data.get("rating")
        comment = request.data.get("comment", "")

        review = Review.objects.create(
            booking=booking,
            rating=rating,
            comment=comment
        )

        # Update worker average rating
        worker = booking.worker

        avg_rating = Review.objects.filter(
            booking__worker=worker
        ).aggregate(Avg("rating"))["rating__avg"]

        worker.rating = round(avg_rating, 2)
        worker.save()

        return Response({"message": "Review added successfully"})

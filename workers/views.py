from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Worker
from .serializers import WorkerSerializer
from .utils import calculate_distance


class WorkerSearchView(APIView):

    def get(self, request):
        category = request.GET.get('category')
        client_lat = request.GET.get('latitude')
        client_lon = request.GET.get('longitude')

        if not category or not client_lat or not client_lon:
            return Response(
                {"error": "Category, latitude and longitude required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        client_lat = float(client_lat)
        client_lon = float(client_lon)

        workers = Worker.objects.filter(
            category=category,
            is_available=True,
            city="Kanpur"
        )

        nearby_workers = []

        for worker in workers:
            distance = calculate_distance(
                client_lat,
                client_lon,
                worker.latitude,
                worker.longitude
            )

            if distance <= 5:   # 5 km radius
                worker.distance = round(distance, 2)
                nearby_workers.append(worker)

        # Sort by distance first, then rating
        nearby_workers.sort(key=lambda w: (w.distance, -w.rating))

        serializer = WorkerSerializer(nearby_workers[:10], many=True)
        return Response(serializer.data)


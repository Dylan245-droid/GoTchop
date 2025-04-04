from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.gis.geos import Point
import json


@csrf_exempt  # ou gère CSRF différemment si utilisateur connecté
def save_location(request):
    if request.method == "POST":
        data = json.loads(request.body)
        lat = data.get("lat")
        lon = data.get("lon")

        if lat is not None and lon is not None:
            user_location = Point(lon, lat, srid=4326)
            if request.user.is_authenticated:
                profile = request.user.profile
                profile.location = user_location
                profile.save()
            return JsonResponse({"status": "ok", "lat": lat, "lon": lon})
        return JsonResponse({"status": "error", "message": "Données invalides"}, status=400)

    return JsonResponse({"status": "error", "message": "Méthode non autorisée"}, status=405)

from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Point
from django.contrib.gis.geos import Point as GEOSPoint
import json

class MapView(TemplateView):
    template_name = 'map_app/map.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        points = Point.objects.all()
        
        # Prepare JSON data with ID
        points_data = [{
            'id': point.id,  # Add ID
            'lat': point.location.y,
            'lng': point.location.x,
            'name': point.name,
            'description': point.description
        } for point in points]
        
        context['points'] = points
        context['points_json'] = json.dumps(points_data)
        return context

@csrf_exempt
def add_point(request):
    print("Received request to add_point view")
    if request.method == 'POST':
        try:
            print("Received POST data:", request.POST)
            
            name = request.POST.get('name')
            description = request.POST.get('description')
            lat = float(request.POST.get('lat'))
            lng = float(request.POST.get('lng'))
            
            # Validate data
            if not all([name, lat, lng]):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Missing required fields'
                })
            
            # Create point
            location = GEOSPoint(lng, lat)  # Note: GEOSPoint accepts (x,y), i.e., (longitude,latitude)
            point = Point.objects.create(
                name=name,
                description=description or '',  # Handle empty description
                location=location
            )
            
            # Add success log
            print(f"Successfully added point: {point.name} at ({point.location.y}, {point.location.x})")
            
            return JsonResponse({
                'status': 'success',
                'point': {
                    'lat': lat,
                    'lng': lng,
                    'name': name,
                    'description': description
                }
            })
        except ValueError as e:
            print(f"ValueError in add_point: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f'Invalid data format: {str(e)}'
            })
        except Exception as e:
            print(f"Error in add_point: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def test_db_connection(request):
    try:
        db_conn = connections['default']
        db_conn.cursor()
        logger.info("Database connection successful")
        return HttpResponse("Database connection successful!")
    except OperationalError as e:
        error_msg = f"Database connection failed: {str(e)}"
        logger.error(error_msg)
        return HttpResponse(error_msg, status=500) 

def test_view(request):
    try:
        from django.contrib.gis.geos import Point
        test_point = Point(0, 0)
        print("GEOS/GDAL is working", file=sys.stderr)
        return HttpResponse("GEOS/GDAL test successful!")
    except Exception as e:
        error_detail = traceback.format_exc()
        print(f"Error: {error_detail}", file=sys.stderr)
        return HttpResponse(f"Error: {str(e)}\n{error_detail}", status=500) 

def your_view(request):
    points = Point.objects.all()
    print("All points in database:")
    for point in points:
        print(f"ID: {point.id}, Longitude: {point.longitude}, Latitude: {point.latitude}")
    # ... remaining code

def delete_point(request, point_id):
    if request.method == 'POST':
        try:
            point = Point.objects.get(id=point_id)
            point.delete()
            return JsonResponse({'status': 'success'})
        except Point.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Point does not exist'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
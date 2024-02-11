import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

earthquake_data = {}
@csrf_exempt
def set_data(request):
    if request.method == 'POST':
        new_data = json.loads(request.body)
        print(new_data)
        id = new_data['data']['id']
        earthquake_data[id] = new_data
        return JsonResponse({'message': 'Data updated'})
    else:
        return JsonResponse({'error': 'POST ERROR'})

 # Work in Progress - haven't decided how I want GET to respond yet
 # May need to wait for the DB to be ready
@csrf_exempt
def get_data(request):
    return JsonResponse(
        {'data': earthquake_data.get('earthquake_data', 'No data available')})

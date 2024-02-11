from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

data = {}
@csrf_exempt
def set_data(request):
    if request.method == 'POST':
        new_data = request.POST.get('data')
        data['current_data'] = new_data
        print(data['current_data'])
        return JsonResponse({'message': 'Data updated'})
    else:
        return JsonResponse({'error': 'POST ERROR'})


@csrf_exempt
def get_data(request):
    return JsonResponse(
        {'data': data.get('current_data', 'No data available')})

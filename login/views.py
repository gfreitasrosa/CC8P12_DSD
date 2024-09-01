import json
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login_view(request):
    if request.method == 'OPTIONS':
        response = HttpResponse(status=200)
        response['Allow'] = 'POST, OPTIONS'
        return response

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if email is None or password is None:
                return JsonResponse({'message': 'Email e senha são obrigatórios'}, status=400)

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Login bem-sucedido'}, status=200)
            else:
                return JsonResponse({'message': 'Credenciais inválidas'}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Erro no formato do JSON'}, status=400)

    return JsonResponse({'message': 'Método não permitido'}, status=405)
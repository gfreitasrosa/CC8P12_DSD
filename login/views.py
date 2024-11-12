import json
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Definindo os parâmetros esperados para a requisição POST
login_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email do usuário'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='Senha do usuário'),
    },
    required=['email', 'password'],
)

login_response_200 = openapi.Response(
    description='Login bem-sucedido',
    schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={'message': openapi.Schema(type=openapi.TYPE_STRING)}),
)

login_response_400 = openapi.Response(
    description='Erro no formato do JSON ou parâmetros obrigatórios faltando',
    schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={'message': openapi.Schema(type=openapi.TYPE_STRING)}),
)

login_response_401 = openapi.Response(
    description='Credenciais inválidas',
    schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={'message': openapi.Schema(type=openapi.TYPE_STRING)}),
)

@csrf_exempt
@swagger_auto_schema(
    methods=['POST'],
    request_body=login_request_body,
    responses={200: login_response_200, 400: login_response_400, 401: login_response_401}
)
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

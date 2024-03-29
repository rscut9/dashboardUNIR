from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from pymongo import MongoClient

# Conexión a la base de datos MongoDB
client = MongoClient('mongodb://admin:admin+123+@mongodb:27017/?authMechanism=SCRAM-SHA-1&authSource=admin')
mydatabase = client.dashboard_unir


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirigir a la página principal después del login
        else:
            # Un mensaje de error de login fallido
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')
    
    
def logout_view(request):
    logout(request)
    return redirect('home')



def home_view(request):
    return render(request, 'home.html')

@login_required
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})



@login_required
# Mostrar la lista de colecciones disponibles
def coleccion_view(request):
    try:
        # Obtiene la lista de colecciones y las ordena alfabéticamente
        colecciones = sorted(mydatabase.list_collection_names())

        # Renderiza la página 'ver_coleccion' con la lista de colecciones
        return render(request, 'ver_coleccion.html', {'colecciones': colecciones})
    except Exception as e:
        # Maneja cualquier excepción e imprime el mensaje de error
        print(f"Error: {e}")
        # Redirige a la página 'error_template' con el mensaje de error
        return render(request, 'error_template.html', {'error_message': str(e)})

    
@login_required
# Mostrar los detalles de una colección
def mostrar_coleccion_view(request):
    try:
        # Si se ha enviado el formulario
        if request.method == 'GET':
            # Obtén el nombre de la colección desde la solicitud GET
            selected_collection = request.GET.get('coleccion', '')

            # Verifica que el nombre de la colección sea válido
            if selected_collection and selected_collection in mydatabase.list_collection_names():
                # Realiza la consulta a la colección seleccionada
                data = mydatabase[selected_collection].find()
                lista_datos = list(data)

                # Redirige a la página 'detalle_coleccion' con los datos
                return render(request, 'detalle_coleccion.html', {'coleccion': selected_collection, 'datos': lista_datos})
            else:
                mensaje = 'Colección no válida'
                # Redirige a la página 'ver_coleccion' con un mensaje de error
                return render(request, 'ver_coleccion.html', {'colecciones': mydatabase.list_collection_names(), 'mensaje': mensaje})

    except Exception as e:
        # Maneja cualquier excepción e imprime el mensaje de error
        print(f"Error: {e}")
        # Redirige a la página 'error_template' con el mensaje de error
        return render(request, 'error_template.html', {'error_message': str(e)})

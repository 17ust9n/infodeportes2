from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse
from .models import Equipo, PartidoAmistoso
from .forms import RegistroForm
import random

# --- VISTAS GENERALES ---
def inicio(request):
    return render(request, 'inicio.html')

def acerca(request):
    return render(request, 'acerca.html')


# --- VISTAS DE EQUIPOS ---
@login_required
def lista_equipos(request):
    equipos = Equipo.objects.all()
    return render(request, 'equipos.html', {'equipos': equipos})

@login_required
def detalle_equipo(request, pk):
    equipo = get_object_or_404(Equipo, pk=pk)
    return render(request, 'equipo_detalle.html', {'equipo': equipo})

@login_required
def seleccion_argentina(request):
    return render(request, 'seleccion_argentina.html')

@login_required
def noticias(request):
    equipos = Equipo.objects.all()
    return render(request, 'noticias.html', {'equipos': equipos})


# --- VISTA PARTIDO AMISTOSO ---
@login_required
def amistoso(request):
    equipos = Equipo.objects.all()
    resultado = None
    goles_vos = goles_pc = None
    equipo_vos = equipo_pc = None
    guardado = False

    if request.method == "POST" and 'equipo_vos' in request.POST:
        equipo_vos_id = request.POST.get("equipo_vos")
        if not equipo_vos_id:
            return render(request, "amistoso.html", {
                "equipos": equipos,
                "error": "Debes elegir un equipo antes de jugar."
            })

        equipo_vos = Equipo.objects.get(id=int(equipo_vos_id))
        equipo_pc = random.choice(Equipo.objects.exclude(id=equipo_vos.id))

        goles_vos = int(request.POST.get("goles_vos", 0))
        goles_pc = random.randint(0, 5)

        if goles_vos > goles_pc:
            resultado = "¡Ganaste! 🎉"
        elif goles_vos < goles_pc:
            resultado = "¡Gana la PC! 🤖"
        else:
            resultado = "¡EMPATE! ⚖️"

        # Si venís de guardar, enviamos guardado=True
        if request.GET.get('guardado') == '1':
            guardado = True

    return render(request, "amistoso.html", {
        "equipos": equipos,
        "resultado": resultado,
        "goles_vos": goles_vos,
        "goles_pc": goles_pc,
        "equipo_vos": equipo_vos,
        "equipo_pc": equipo_pc,
        "guardado": guardado
    })


# --- VISTA GUARDAR PARTIDO ---
@login_required
@require_POST
def guardar_partido(request):
    equipo_vos = Equipo.objects.get(id=int(request.POST['equipo_vos_id']))
    equipo_pc = Equipo.objects.get(id=int(request.POST['equipo_pc_id']))
    goles_vos = int(request.POST['goles_vos'])
    goles_pc = int(request.POST['goles_pc'])
    resultado = request.POST['resultado']

    # Guardamos en la base de datos
    PartidoAmistoso.objects.create(
        usuario=request.user,
        equipo_vos=equipo_vos,
        equipo_pc=equipo_pc,
        goles_vos=goles_vos,
        goles_pc=goles_pc,
        resultado=resultado
    )

    # Redirigimos a la misma página de amistoso con parámetro de guardado
    return redirect(f"{reverse('amistoso')}?guardado=1")


# --- VISTA LISTA DE PARTIDOS ---
@login_required
def lista_partidos(request):
    historial = PartidoAmistoso.objects.filter(usuario=request.user).order_by('-id')
    return render(request, 'lista_partidos.html', {'historial': historial})


@login_required
def eliminar_partido(request, partido_id):
    partido = get_object_or_404(PartidoAmistoso, id=partido_id, usuario=request.user)
    partido.delete()
    return redirect('lista_partidos')

# --- VISTAS DE USUARIO ---
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('inicio')
    else:
        form = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login_view')

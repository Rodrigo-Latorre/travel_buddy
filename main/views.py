from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .decorators import login_required
from .models import Travels, User

@login_required
def index(request):
    return redirect('/travels')

@login_required
def travels(request):
    user_id = request.session['user']['id']
    owner = User.objects.get(id=user_id)
    mytravels = Travels.objects.filter(planner=owner).filter(joined__id=user_id)
    noviajo = Travels.objects.filter(planner=owner).exclude(joined__id=user_id)
    ontravels = owner.other_travel.all().exclude(planner=owner)
    other = Travels.objects.exclude(joined__id=user_id)
    context = {
        'mytravels':mytravels,
        'noviajo':noviajo,
        'ontravels':ontravels,
        'others':other
    }
    return render(request, 'index.html', context)

@login_required
def add(request):
    user_id = request.session['user']['id']
    owner = User.objects.get(id=user_id)

    if request.method == 'GET':
        return render(request, 'create.html')

    errors = Travels.objects.validador_viaje(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/travels/add')
    destino = request.POST["destination"]
    inicio = request.POST["starttrip"]
    termino = request.POST["endtrip"]
    plan = request.POST["plantrip"]

    this_trip = Travels.objects.create(destination=destino,starttrip=inicio,endtrip=termino,plan=plan,planner=owner)
    owner.other_travel.add(this_trip)
    return redirect('/travels')

@login_required
def show(request,id):
    trip = Travels.objects.get(id=id)
    joining = trip.joined.all().exclude(id = trip.planner.id)
    context = {
        'trip':trip,
        'joining':joining
    }
    return render(request, 'show.html', context)

@login_required
def join(request,id):
    user_id = request.session['user']['id']
    owner = User.objects.get(id=user_id)
    trip = Travels.objects.get(id=id)
    owner.other_travel.add(trip)
    return redirect('/travels')

@login_required
def cancel(request,id):
    user_id = request.session['user']['id']
    owner = User.objects.get(id=user_id)
    trip = Travels.objects.get(id=id)
    owner.other_travel.remove(trip)
    return redirect('/travels')

@login_required
def destroy(request,id):
    trip = Travels.objects.get(id=id)
    trip.delete()
    return redirect('/travels')
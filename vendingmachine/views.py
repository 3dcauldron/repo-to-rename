from vendingmachine.location import Location
from vendingmachine.machine import Machine
from vendingmachine.database import Database
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from pprint import pprint

db = Database()
def index(request):
    id = request.POST.get('delete_item', '')
    if(not id == ''):
        j = db.getLocationsData({'_id':id})
        db.deleteLocation(id)
    locations_list = db.getLocationsData({})
    l = {}
    for loc in locations_list:
        l[loc['_id']] = loc
    context = {'out': l.items()}
    return render(request, 'vendingmachine/index.html', context)

def addvendingmachine(request):
    name = request.POST.get('name', '')
    number = request.POST.get('number', '')
    address = request.POST.get('address', '')
    lat = request.POST.get('lat', 0)
    lon = request.POST.get('lon', 0)
    types = request.POST.get('type', '')
    capacity = request.POST.get('capacity', '')
    quantity = request.POST.get('quantity', '')
    price = request.POST.get('price', '')
    user = request.POST.get('user', '')
    change = request.POST.get('change', '')
    contract = request.POST.get('contract', '')

    if lat == 0 and lat == 0:
        return render(request, 'vendingmachine/addvendingmachine.html')

    machine = Machine(product={},size=capacity,quantity=quantity,price=price,key = {'id':'01AB', 'user':user}, change = change)
    location = Location(name=name, contact_number=number, address=address, GPS={'lat':lat,'lon':lon}, contract=contract)
    location.update_machine(machine,user)
    db.insertLocation(location)

    return render(request, 'vendingmachine/addvendingmachine.html')

def editvendingmachine(request):
    id = request.POST.get('edit_item', '')
    if(not id == ''):
        l = {}
        location = db.getLocationById(id)
        context = {'out': location}
        return render(request, 'vendingmachine/editvendingmachine_finish.html', context)
    else:
        return redirect('/vendingmachine')


def editvendingmachine_finish(request):
    id = request.POST.get('id', '')
    name = request.POST.get('name', '')
    number = request.POST.get('number', '')
    address = request.POST.get('address', '')
    lat = request.POST.get('lat', 0)
    lon = request.POST.get('lon', 0)
    types = request.POST.get('type', '')
    capacity = request.POST.get('capacity', '')
    quantity = request.POST.get('quantity', '')
    price = request.POST.get('price', '')
    user = request.POST.get('user', '')
    change = request.POST.get('change', '')
    contract = request.POST.get('contract', '')

    updates = name,number,address,lat,lon,machine,contract

    if lat == 0 and lat == 0:
        return render(request, 'vendingmachine/editvendingmachine_finish.html')

    loc = db.getLocationsData({'_id':id})
    location.update_all(updates)
    db.updateLocation(id,location)
    return render(request, 'vendingmachine/editvendingmachine_finish.html')

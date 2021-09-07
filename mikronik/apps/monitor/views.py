from django.shortcuts import render
from .models import Mikrot
from django.http import Http404, HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from . import mikropi

api = mikropi.newMikrotApi()
	
def index(request):
	arrM = api.viewListMikrot()


	return render(request, 'monitor/list.html', {'arr': arrM})


def detail(request, mikrot_id):
	listDevice = api.viewAllDevice(mikrot_id)
	name = api.viewHostName(mikrot_id)		
	try:
		a = Mikrot.objects.get(id = mikrot_id)
		
	except:
		raise Http404("Узел не найден")

	return render(request, 'monitor/detail.html', {'mikrot': a, 'hostname': name, 'listDevice':listDevice})



def view_host(request, mikrot_id):
	try:
		a = Mikrot.objects.get(id = mikrot_id)
		
	except:
		raise Http404("Узел не найден")

	cmd =  request.POST['command']
	name = api.viewHostName(mikrot_id)
	listDevice = api.viewAllDevice(mikrot_id)
	resCommand = ''
	if cmd:
		resCommand = api.cmdExecution(cmd, mikrot_id)

		for res in resCommand:
			for r in res:
				print(r)
			print('-----------------')

	return render(request, 'monitor/detail.html', {'mikrot': a, 'hostname': name, 'listDevice':listDevice, 'result': resCommand})


def sort_host(request, mikrot_id):

	try:
		a = Mikrot.objects.get(id = mikrot_id)
		
	except:
		raise Http404("Узел не найден")

	deviceHost = request.POST['device']


	name = api.viewHostName(mikrot_id)
	listDevice = api.changeDevice(deviceHost, api.viewAllDevice(mikrot_id))

	return render(request, 'monitor/detail.html', {'mikrot': a, 'hostname': name, 'listDevice':listDevice})



def all_device(request):

	listDev = api.viewAllHost()
	return render(request, 'monitor/all_device.html', {'listDevice': listDev})


def sort_all_device(request):
	deviceHost = request.POST['device']

	listDev = api.viewAllHost()

	listDevice = api.changeDevice(deviceHost, listDev)

	return render(request, 'monitor/all_device.html', {'listDevice': listDevice})


def group(request):

	all_mikrot = Mikrot.objects.all()
	iterat = []
	j = 1
	arrMain = []

	while j <= len(all_mikrot):
		iterat.append(j)
		j = j + 1


	
	return render(request, 'monitor/group.html', {'all_mikrot': all_mikrot, 'iteration': iterat})



def group_command(request):
	groupCommand = ''
	all_mikrot = Mikrot.objects.all()
	iterat = []
	j = 1
	arrMain = []

	while j <= len(all_mikrot):
		iterat.append(j)
		j = j + 1


	groupCommand =  request.POST['command']
	groupDevice = []
	
	for a in all_mikrot:
			
		statusDevice = request.POST.get(str(a.id), False)
			
		arrMain.append(a.id)
		arrMain.append(statusDevice)

		groupDevice.append(arrMain)
		arrMain = []

	api.groupCommand(groupCommand, groupDevice)

	
	return render(request, 'monitor/group.html', {'all_mikrot': all_mikrot, 'iteration': iterat})




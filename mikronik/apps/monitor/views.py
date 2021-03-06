from django.shortcuts import render
from .models import Mikrot, InventPrinter, InventPC, InventNote
from django.http import Http404, HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from . import mikropi
import pandas as pd
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files import File

api = mikropi.newMikrotApi()
	
def invent(request):
	try:
		deviceHost = request.POST['device']

		listDev = api.viewAllHost()
		
		
	
		
		if deviceHost == '1':
			listNote = InventNote.objects.all()
			listDeviceNote = []
			for note in listNote:
				arr = []
				
				arr.append(note.hostNameNote)
				arr.append(note.userNote)
				arr.append(note.modelNote)
				arr.append(note.hardDriveNote)
				arr.append(note.ramNote)
				arr.append(note.processorNote)
				arr.append(note.placeNote)
				arr.append(note.dateInvent)
				listDeviceNote.append(arr)
				arr = []
			
			return render(request, 'monitor/nb.html', {'listDevice': listDeviceNote})

		if deviceHost == '5':
			listPC = InventPC.objects.all()
			listDevicePC = []
			for note in listPC:
				arr = []
			
				arr.append(note.hostNamePC)
				arr.append(note.userPC)
				arr.append(note.motherBandPC)
				arr.append(note.hardDrivePC)
				arr.append(note.ramPC)
				arr.append(note.processorPC)
				arr.append(note.placePC)
				arr.append(note.dateInvent)
				listDevicePC.append(arr)
				arr = []
			

			return render(request, 'monitor/pc.html', {'listDevice': listDevicePC})

		if deviceHost == '2':
			print('pr')
			listDevice = api.parsePrinters(deviceHost, listDev)
			return render(request, 'monitor/invent.html', {'listDevice': listDevice})
		

		

	except:
		listDev = '|'
		return render(request, 'monitor/invent.html', {'listDevice': listDev})

	return render(request, 'monitor/invent.html', {'listDevice': listDevice})




@permission_required('mikronik.index')
def index(request):
	arrM = api.viewListMikrot()

	return render(request, 'monitor/list.html', {'arr': arrM})

@permission_required('mikronik.detail')
def detail(request, mikrot_id):
	listDevice = api.viewAllDevice(mikrot_id) 
	name = api.viewHostName(mikrot_id)		
	try:
		a = Mikrot.objects.get(id = mikrot_id)
		
	except:
		raise Http404("???????? ???? ????????????")

	return render(request, 'monitor/detail.html', {'mikrot': a, 'hostname': name, 'listDevice':listDevice})


@permission_required('mikronik.index')
def view_host(request, mikrot_id):
	try:
		a = Mikrot.objects.get(id = mikrot_id)
		
	except:
		raise Http404("???????? ???? ????????????")

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

@permission_required('mikronik.index')
def sort_host(request, mikrot_id):

	try:
		a = Mikrot.objects.get(id = mikrot_id)
		
	except:
		raise Http404("???????? ???? ????????????")

	deviceHost = request.POST['device']


	name = api.viewHostName(mikrot_id)
	listDevice = api.changeDevice(deviceHost, api.viewAllDevice(mikrot_id))

	return render(request, 'monitor/detail.html', {'mikrot': a, 'hostname': name, 'listDevice':listDevice})



def all_device(request):

	listDev = api.viewAllHost()
	return render(request, 'monitor/all_device.html', {'listDevice': listDev})


def sort_all_device(request):

	try:
		deviceHost = request.POST['device']

		listDev = api.viewAllHost()

		listDevice = api.changeDevice(deviceHost, listDev)
		

		return render(request, 'monitor/all_device.html', {'listDevice': listDevice})
	except:
		listDev = api.viewAllHost()
		return render(request, 'monitor/all_device.html', {'listDevice': listDev})


def save_device(request):
	deviceHost = request.POST['device']

	listDev = api.viewAllHost()

	listDevice = api.changeDevice(deviceHost, listDev)
	api.saveDevice(listDevice, deviceHost)
	return render(request, 'monitor/all_device.html', {'listDevice': listDevice})





def invent_printers(request):
	try:
		deviceHost = request.POST['device']

		listDev = api.viewAllHost()

		listDevice = api.changeDevice(deviceHost, listDev)

		return render(request, 'monitor/invent.html', {'listDevice': listDevice})

	except:
		listDev = api.viewAllHost()
		return render(request, 'monitor/invent.html', {'listDevice': listDev})

	return render(request, 'monitor/invent.html', {'listDevice': listDevice})



@permission_required('mikronik.index')
def group(request):

	all_mikrot = api.viewListMikrotGroup()

	
	return render(request, 'monitor/group.html', {'all_mikrot': all_mikrot})

@permission_required('mikronik.index')
def group_command(request):
	groupCommand = ''
	allM = Mikrot.objects.all()
	all_mikrot = api.viewListMikrotGroup()

	arrMain = []

	groupCommand =  request.POST['command']
	groupDevice = []
	
	for a in allM:
			
		statusDevice = request.POST.get(str(a.id), False)
			
		arrMain.append(a.id)
		arrMain.append(statusDevice)

		groupDevice.append(arrMain)
		arrMain = []

	api.groupCommand(groupCommand, groupDevice)

	
	return render(request, 'monitor/group.html', {'all_mikrot': all_mikrot})




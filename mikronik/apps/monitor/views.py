from django.shortcuts import render
from .models import Mikrot
from django.http import Http404, HttpResponseRedirect
from ping3 import ping, verbose_ping
from django.http import HttpResponse
from django.urls import reverse
from . import mikropi

api = mikropi.newMikrotApi()
	
def index(request):
	all_mikrot = Mikrot.objects.all()
	res = []

	iterat = []

	j = 1


	while j <= len(all_mikrot):
		iterat.append(j)
		j = j + 1


	for p in all_mikrot:
		try:
			x = ping(str(p.mikrotIP))
			if x:
				res.append('Available')
			else:
				res.append('Not available')
		except:
			res.append('Not available')

	

	return render(request, 'monitor/list.html', {'all_mikrot': all_mikrot, 'ip': res, 'iteration': iterat})


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
	print(resCommand)

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
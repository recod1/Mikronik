
import os, sys
sys.path.append('C:\mikronik\Mikronik')
os.environ['DJANGO_SETTINGS_MODULE'] = 'mikronik.settings'

import django

django.setup()

from monitor.models import *

import mikropi
import subprocess
import datetime
from datetime import date
import wmi
api = mikropi.newMikrotApi()
current_date = date.today()
def wmiParseNote(machine, mikrot):
	
	try:
		user = ''
		proc = ''
		drive = ''
		model = ''
		c = wmi.WMI(machine, user=r"bestnov.local\sysadmin", password="PR)mokashka")

		# username
		for os in c.Win32_ComputerSystem():
			domain = os.UserName.split('\\')
			user = str(domain[1])
			print ('Пользователь: ', user)

		# MotherBand
		# for os in c.Win32_BaseBoard():

		# 	print('Материнская плата:',os.Manufacturer,os.Product, os.Version)

		mem = 0
		# RAM
		for os in c.Win32_PhysicalMemory():
			mem = mem + int(str(os.Capacity)[0])
		print ('RAM: ', mem, 'Gb')

		# Processor
		for os in c.Win32_Processor():
			proc = os.Name
			print('Процессор: ', os.Name)

		# HardDrive
		for os in c.Win32_DiskDrive():
			if str(os.MediaType) == 'Fixed hard disk media':
				drive = 'SSD'
				print('Жесткий диск: SSD')

			else:
				drive = 'HDD'
				print('Жесткий диск: HDD')


		for os in c.Win32_ComputerSystem():
			model = str(os.Manufacturer) + '' + os.Model 
			print(os.Manufacturer, os.Model)

		print(current_date)
		host = InventNote(hostNameNote = machine, 
			userNote = user, 
			modelNote = model, 
			hardDriveNote = drive, 
			ramNote = mem, 
			processorNote = proc, 
			placeNote = mikrot, 
			dateInvent = current_date)
		host.save()

	except:
		
		host = InventNote(hostNameNote = machine, 
			userNote = 'None', 
			modelNote = 'None', 
			hardDriveNote = 'None', 
			ramNote ='None', 
			processorNote = 'None', 
			placeNote = mikrot, 
			dateInvent = current_date)
		host.save()
		print("На компьютере ", machine, "не запущена служба")

def wmiParsePc(machine, mikrot):
	try:
		c = wmi.WMI(machine, user=r"bestnov.local\sysadmin", password="PR)mokashka")
		user = ''
		proc = ''
		drive = ''
		mother = ''

		# username
		for os in c.Win32_ComputerSystem():
			domain = os.UserName.split('\\')
			user = str(domain[1])
			print ('Пользователь: ', user)

		# MotherBand
		# for os in c.Win32_BaseBoard():
		# 	mother = str(os.Manufacturer,os.Product, os.Version)
		# 	print('Материнская плата:',mother)

		mem = 0
		# RAM
		for os in c.Win32_PhysicalMemory():
			mem = mem + int(str(os.Capacity)[0])
		print ('RAM: ', mem, 'Gb')

		# Processor
		for os in c.Win32_Processor():
			proc = os.Name
			print('Процессор: ', proc)

		# HardDrive
		for os in c.Win32_DiskDrive():
			if str(os.MediaType) == 'Fixed hard disk media':
				drive = 'SSD'
				print('Жесткий диск: SSD')

			else:
				drive = 'HDD'
				print('Жесткий диск: HDD')


		
		host = InventPC(hostNamePC = machine, 
			userPC = user, 
			motherBandPC = mother, 
			hardDrivePC = drive, 
			ramPC = mem, 
			processorPC = proc, 
			placePC = mikrot, 
			dateInvent = current_date)
		host.save()
		print(current_date)

	except:
		host = InventPC(hostNamePC = machine, 
			userPC = 'None', 
			motherBandPC = 'None', 
			hardDrivePC = 'None', 
			ramPC = 'None', 
			processorPC = 'None', 
			placePC = mikrot, 
			dateInvent = current_date)
		host.save()
		print("На компьютере ", machine, "не запущена служба")
		
			



def parse():
	all_mikrot = Mikrot.objects.all()

	for mikrot in all_mikrot:
		all_device = api.viewAllDevice(mikrot.id)

		try:
	
			listDevice = api.changeDevice('5', all_device)

			for device in listDevice:
				wmiParsePc(device[2], mikrot)
		except:
			continue

		
	for mikrot in all_mikrot:
		all_device = api.viewAllDevice(mikrot.id)

		try:
			print('Parse Notebook')
			listDevice = api.changeDevice('1', api.viewAllDevice(mikrot.id))
			for device in listDevice:
				wmiParseNote(device[2], mikrot)
		except:
			continue

while True:
	current_date_time = datetime.datetime.now()
	current_time = current_date_time.time()
	nowTime = str(current_time).split(':')
	print('Wait need time')

	if nowTime[0] == '16' and nowTime[1] == '54':
		print('ITS WORKING') 
	parse()

	if nowTime[0] == '18' and nowTime[1] == '00':
		print('ITS WORKING')

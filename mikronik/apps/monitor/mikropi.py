# -*- coding: utf-8 -*-
#!/usr/bin/python3
from monitor import libapi
from monitor.models import Mikrot, InventPrinter
from ping3 import ping, verbose_ping
from sys import getdefaultencoding
import pandas as pd
from datetime import datetime
from puresnmp import get
from puresnmp.api.raw import get as raw_get
from django.http import HttpResponse, Http404
from wsgiref.util import FileWrapper
import os

class newMikrotApi():

	def identityDevice(self, hostname):
		NB = ['BN-NB', 'BNNB', 'BN NB', 'BN_NB']
		SB = ['BN-SB', 'BNSB', 'BN SB', 'BN_SB']
		MN = ['BN-MN', 'BNMN', 'BN MN', 'BN_MN']
		PR = ['BN-PR', 'BNPR', 'BN PR', 'BN_PR']
		for i in NB:
			if i.lower() in hostname.lower():
				return 'Ноутбук'


		for i in SB:
			if i.lower() in hostname.lower():
				return 'Системник'


		for i in MN:
			if i.lower() in hostname.lower():
				return 'Моноблок'

							
		for i in PR:
			if i.lower() in hostname.lower():
				return 'Принтер'

		if  hostname[:2] == 'KM':
			return 'Принтер'

		elif hostname[:1] == 'W':
			return 'Телефонная База'

		else:
			return 'Неизвестно'


	def viewHostName(self, mikrot_id):
		getdefaultencoding()
		data = Mikrot.objects.get(id = mikrot_id)

		s = libapi.socketOpen(str(data.mikrotIP))
		dev_api = libapi.ApiRos(s)

		if not dev_api.login(data.mikrotLogin, data.mikrotPass):
			pass
		

		commandName = ["/system/identity/print"]
		dev_api.writeSentence(commandName)
		resName = libapi.readResponse(dev_api)
		
		name = resName[0][1][6:]

		libapi.socketClose(s)
		return name


	def viewAllDevice(self, mikrot_id):
		objectIdentity = newMikrotApi()
		data = Mikrot.objects.get(id = mikrot_id)

		s = libapi.socketOpen(str(data.mikrotIP))
		dev_api = libapi.ApiRos(s)
	
		if not dev_api.login(data.mikrotLogin, data.mikrotPass):
			pass

		

		command = ["/ip/dhcp-server/lease/print"]
		dev_api.writeSentence(command)
		res = libapi.readResponse(dev_api)
		libapi.socketClose(s)

		
		listDevice = []
		arr = []

		for element in res:
			
			for el in element:
				
				if '=address=' in el:
					ip = el[9:]
					arr.append(ip)
					
				if '=mac-address=' in el:
					mac = el[13:]
					arr.append(mac)
					

				if '=host-name=' in el:
					hostname = el[11:]
					
					
					arr.append(hostname)
					# try:
					# 	#print(ip)
					# 	if get(ip, 'public', '.1.3.6.1.4.1.2699.1.2.1.2.1.1.3.1'):
					# 		arr.append('Принтер')
					# 		#print(arr)
					# except:
					arr.append(objectIdentity.identityDevice(hostname))

					listDevice.append(arr)
				
					arr = []
						
			if len(arr) != 4:
				arr = []
	
		return listDevice

	def cmdExecution(self, cmd, mikrot_id):

		data = Mikrot.objects.get(id = mikrot_id)

		cmd = cmd.split(',')
		s = libapi.socketOpen(str(data.mikrotIP))

		dev_api = libapi.ApiRos(s)

		if not dev_api.login(data.mikrotLogin, data.mikrotPass):
			pass

		
		dev_api.writeSentence(cmd)
		res = libapi.readResponse(dev_api)
		libapi.socketClose(s)

		return res
	
	def parsePrinters(self, deviceNumber, deviceArr):
		community = 'public'
		arr = []
		print('start parse')

		modelPrinter = []
		oids = {
			'model': '.1.3.6.1.4.1.2699.1.2.1.2.1.1.3.1',
			'capacityType': '.1.3.6.1.2.1.43.11.1.1.6.1.1'
		}
		for device in deviceArr:
				
			if 'Принтер' in device:
				try:

					mdl = ''
					mfg = ''
					modelPrinter = list(get(device[0], community, oids['model']).decode('UTF-8').split(';'))

					capacityNow = get(device[0], community, '.1.3.6.1.2.1.43.11.1.1.9.1.1')
					capacityMax = get(device[0], community, '.1.3.6.1.2.1.43.11.1.1.8.1.1')
					capacity = int((100 * int(capacityNow)) / int(capacityMax))

					for printer in modelPrinter:
						if 'MFG' in printer:
							mfg = str(printer[4:])						
								
						if 'MDL' in printer:
							mdl = str(mfg + ' ' + str(printer[4:]))
							

					tonerType = get(device[0], community, '.1.3.6.1.2.1.43.11.1.1.6.1.1').decode('UTF-8')
					if len(tonerType) > 20:
						tonerType = tonerType.split(',')
						tonerType = tonerType[2] 
					device.append(mdl)
					device.append(tonerType)
					device.append(capacity)
				except:
					continue
					
				arr.append(device)
	
			

		return arr

	def changeDevice(self, deviceNumber, deviceArr):

		arr = []
		
		if deviceNumber == '1':
			for device in deviceArr:
				
				if 'Ноутбук' in device:
					arr.append(device)
				

		if deviceNumber == '2':
			for device in deviceArr:
				if 'Принтер' in device:
					arr.append(device)
			

		if deviceNumber == '3':
			for device in deviceArr:
				if 'Телефонная База' in device:
					arr.append(device)
				

		if deviceNumber == '4':
			for device in deviceArr:
				if 'Неизвестно' in device:
					arr.append(device)
		if deviceNumber == '5':
			for device in deviceArr:
				if 'Системник' in device:
					arr.append(device)
			
		if deviceNumber == '0':
			arr = deviceArr
		
		return arr


	def viewAllHost(self):
		objectIdentity = newMikrotApi()

		arrAll = []
		listDev = []
		arrSom = []	
		nout = []
		all_mikrot = Mikrot.objects.all()

		arrAllHost = []
		for mikrot in all_mikrot:
			try:
				s = libapi.socketOpen(str(mikrot.mikrotIP))

			except:
				print(mikrot.mikrotName, ' Не доступен')
				continue

			dev_api = libapi.ApiRos(s)
	
			if not dev_api.login(mikrot.mikrotLogin, mikrot.mikrotPass):
				pass
			
			command = ["/ip/dhcp-server/lease/print"]
			dev_api.writeSentence(command)
			res = libapi.readResponse(dev_api)
			arrAll.append(res)
	
			for element in arrAll:
				for ele in element:	
					for el in ele:			
						if '=address=' in el:
							ip = el[9:]
							arrSom.append(ip)
							
						if '=mac-address=' in el:
							mac = el[13:]
							arrSom.append(mac)

						if '=host-name=' in el:
							hostname = el[11:]
							arrSom.append(hostname)
							arrSom.append(objectIdentity.identityDevice(hostname))
							arrSom.append(mikrot.mikrotName)
							listDev.append(arrSom)
															
							arrSom = []
					if len(arrSom) != 4:
						arrSom = []
			arrAll = []
			libapi.socketClose(s)
	
		return listDev


	def groupCommand(self, groupCommand, arrGroupHost):

		for arr in arrGroupHost:
			if arr[1]:
				#print(arr[0])
				

				data = Mikrot.objects.get(id = arr[0])

				cmd = groupCommand.split(',')
				s = libapi.socketOpen(str(data.mikrotIP))

				dev_api = libapi.ApiRos(s)

				if not dev_api.login(data.mikrotLogin, data.mikrotPass):
					pass

				
				dev_api.writeSentence(cmd)
				res = libapi.readResponse(dev_api)

				libapi.socketClose(s)
				print("------------------")
				print(data.mikrotName)
				for ar in res:
					for r in ar:
						print(r)
				
		return 'Command execute'

	def saveDevice(self, listDevice, fileName):

		df = pd.DataFrame([[' ', ' ', ' ']], columns=['Объект', 'Инвентаризационный номер', 'Устройство'])

		for a in listDevice:
			def2 = pd.DataFrame([[a[4], a[2], a[3]]], columns=['Объект', 'Инвентаризационный номер', 'Устройство'])
			df = df.append(def2, ignore_index=True)

	
		fileName = listDevice[0][3]
		timeNow = datetime.now()
		timeNow = str(timeNow.hour) + '-' + str(timeNow.minute) + '-' + str(timeNow.second)
		path = './gtables/' + str(fileName) + ' ' + str(timeNow) + '.xlsx'
		df.to_excel(path)



	def viewListMikrot(self):

		all_mikrot = Mikrot.objects.all()
		arr = []
		arrM = []
		
		j = 1
		
		for p in all_mikrot:
			
			x = ping(str(p.mikrotIP))
			

			if isinstance(x, float):
				arr.append(j)
				arr.append(p.mikrotName)
				arr.append(p.mikrotIP)
				arr.append('Available')
				arr.append(p.id)
				arrM.append(arr)
				
				arr = []


			else:
				arr.append(j)
				arr.append(p.mikrotName)
				arr.append(p.mikrotIP)
				arr.append('Not available')
				arr.append(p.id)
				arrM.append(arr)
				
				arr = []


			j = j + 1
		
		name = []
		res = []

		for a in arrM:
		    name.append(a[1])

		name = sorted(name)

		i = 0
		while i <= len(name) -1:
		    for a in arrM:
		        if name[i] in a:
		        	a[0] = i+1
		        	res.append(a)
		    i = i + 1

		return res




	def viewListMikrotGroup(self):

		all_mikrot = Mikrot.objects.all()
		arr = []
		arrM = []
			
		j = 1
			
		for p in all_mikrot:
				
			arr.append(j)
			arr.append(p.mikrotName)
			arr.append(p.mikrotIP)

			arr.append(p.id)
			arrM.append(arr)
			arr = []
			

			j = j + 1
			
		name = []
		res = []

		for a in arrM:
			name.append(a[1])

		name = sorted(name)

		i = 0
		while i <= len(name) -1:
			for a in arrM:
				if name[i] in a:
					a[0] = i+1
					res.append(a)
			i = i + 1

		return res

	#def viewListPrinters(self):

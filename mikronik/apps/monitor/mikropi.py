from . import libapi
from .models import Mikrot

class newMikrotApi():

	def identityDevice(self, hostname):
		NB = ['BN-NB', 'BNNB', 'BN NB']
		SB = ['BN-SB', 'BNSB', 'BN SB']
		MN = ['BN-MN', 'BNMN', 'BN MN']
		PR = ['BN-PR', 'BNPR', 'BN PR']
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

		data = Mikrot.objects.get(id = mikrot_id)

		s = libapi.socketOpen(str(data.mikrotIP))
		dev_api = libapi.ApiRos(s)

		if not dev_api.login('admin', str(data.mikrotPass)):
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

		if not dev_api.login('admin', str(data.mikrotPass)):
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
				
				if '=active-mac-address=' in el:
					mac = el[20:]
					arr.append(mac)

				if '=host-name=' in el:
					hostname = el[11:]
					arr.append(hostname)
					arr.append(objectIdentity.identityDevice(hostname))
					listDevice.append(arr)
					arr = []
		return listDevice

	def cmdExecution(self, cmd, mikrot_id):

		data = Mikrot.objects.get(id = mikrot_id)

		cmd = cmd.split(',')
		s = libapi.socketOpen(str(data.mikrotIP))

		dev_api = libapi.ApiRos(s)

		if not dev_api.login('admin', str(data.mikrotPass)):
			pass

		
		dev_api.writeSentence(cmd)
		res = libapi.readResponse(dev_api)
		libapi.socketClose(s)

		return res
		
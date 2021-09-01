import libapi

devices = [

      { 'ip': '192.168.116.1',
      'login': 'admin',
      'pass': '100vfnjkjuVfujvtl'}
      ]
service = 'api'
   
for device in devices:

      print("Connect to {}:".format(device['ip']))

      #Создание сокета и объекта устройства

      s = libapi.socketOpen(device['ip'])

      dev_api = libapi.ApiRos(s)

 
      #Авторизация на устройстве

      if not dev_api.login(device['login'], device['pass']):

            break

 
      #Список команд

      commandName = ['/ip/service/disable', '=numbers=5']
      
      dev_api.writeSentence(commandName)
      resName = libapi.readResponse(dev_api)

      name = resName[0][1][6:]

      command = ["/ip/dhcp-server/lease/print"]

      print(type(commandName))

      #Выполнение команды на устройстве

      dev_api.writeSentence(command)

     

      #Получение результата выполнения команды

      res = libapi.readResponse(dev_api)

     

      #Закрытие сокета

      libapi.socketClose(s)

      

      #Форматированный вывод результата команды
      print(resName)
      #print(name)

      listIP = []
      listHostName = []
      listMac = []
      for element in res:
            for el in element:
                  if '=address=' in el:
                        ip = el[9:]
                        listIP.append(ip)
                        print(ip, end = " ")
                  if '=host-name=' in el:
                        hostname = el[11:]
                        listHostName.append(hostname)
                        print(hostname, end = " ")

                  if '=active-mac-address=' in el:
                        mac = el[20:]
                        listMac.append(mac)
                        print(mac)


      print('')


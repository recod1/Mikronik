from django.db import models


class Mikrot(models.Model):
	mikrotIP = models.CharField("Адрес Микротик", max_length = 20)
	mikrotName = models.CharField("Имя Микротик", max_length =  30)
	mikrotLogin = models.CharField("Логин Микротик", max_length =  30)
	mikrotPass = models.CharField("Пароль Микротик", max_length = 30)

	def __str__(self):
		return self.mikrotName

	class Meta():
		verbose_name = 'Микротик'
		verbose_name_plural = 'Микротики'



class InventPC(models.Model):
	hostNamePC = models.CharField(max_length = 20)
	userPC = models.CharField(max_length = 50)
	motherBandPC = models.CharField(max_length = 50)
	hardDrivePC = models.CharField(max_length = 20)
	ramPC = models.CharField(max_length = 20)
	processorPC = models.CharField(max_length = 50)
	placePC = models.CharField(max_length = 20)
	dateInvent = models.CharField(max_length = 20)

	def __str__(self):
		return self.hostNamePC
	
class InventNote(models.Model):
	hostNameNote = models.CharField(max_length = 20)
	userNote = models.CharField(max_length = 50)
	modelNote = models.CharField(max_length = 50)
	hardDriveNote = models.CharField(max_length = 20)
	ramNote = models.CharField(max_length = 20)
	processorNote = models.CharField(max_length = 50)
	placeNote = models.CharField(max_length = 20)
	dateInvent = models.CharField(max_length = 20)

	def __str__(self):
		return self.hostNameNote

class InventPrinter(models.Model):
	hostNamePrinter = models.CharField(max_length = 20)
	modelPrinter = models.CharField(max_length = 50)
	tonerTypePrinter = models.CharField(max_length = 20)
	placePrinter = models.CharField(max_length = 20)
	dateInvent = models.CharField(max_length = 20)

	def __str__(self):
		return self.hostNamePrinter


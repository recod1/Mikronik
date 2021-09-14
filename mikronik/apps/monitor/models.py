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

		#permissions = (("detail", "User not auth"),) 
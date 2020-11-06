from django.db import models


class StreetTypeModel(models.Model):
    name = models.CharField(max_length=100, null=False)
    short_name = models.CharField(max_length=10, null=False)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тип улицы'
        verbose_name_plural = 'Типы улиц'


class CampaignModel(models.Model):
    date_create = models.DateTimeField(auto_now_add=True)
    date_modify = models.DateTimeField(auto_now_add=True)
    
    name = models.CharField(max_length=255, null=False, verbose_name="Название кампании/обхода")
    fio_candidate = models.CharField(max_length=255, null=False, verbose_name="ФИО кандидата")
    region = models.CharField(max_length=255, null=False, verbose_name="Регион")
    rayon = models.CharField(max_length=255, null=False, verbose_name="Район")
    settlement = models.CharField(max_length=255, null=False, verbose_name="Населённый пункт")


class StreetModel(models.Model):
    date_create = models.DateTimeField(auto_now_add=True)
    date_modify = models.DateTimeField(auto_now_add=True)

    campaign_id = models.ForeignKey(CampaignModel, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=255, null=False, verbose_name='Название улицы')
    type_id = models.ForeignKey(StreetTypeModel, on_delete=models.CASCADE, null=False, verbose_name="Тип улицы")


class HouseModel(models.Model):
    date_create = models.DateTimeField(auto_now_add=True)
    date_modify = models.DateTimeField(auto_now_add=True)

    street_id = models.ForeignKey(StreetModel, on_delete=models.CASCADE, null=False)
    number = models.CharField(max_length=10, null=False, verbose_name="Номер дома")
    # тип здания: 1 - частный дом, 2 - многоквартирный, 3 - квартира
    type = models.IntegerField(null=False, verbose_name="Тип дома")
    group_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True) # ID многоквартирного дома
    is_openned = models.IntegerField(verbose_name="Отрыли", null=True)
    is_interesed = models.IntegerField(verbose_name="Интерес", null=True)
    is_recieved = models.IntegerField(verbose_name="Приняли", null=True)
    problem_description = models.TextField(null=False, default='', verbose_name="Проблемы/наказы избирателя", blank=True)
    comment = models.CharField(max_length=255, null=False, default='', verbose_name="Произвольный комментарий", blank=True)

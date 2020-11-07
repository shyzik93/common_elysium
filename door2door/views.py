from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse

from utils.utils import get_success, get_error, get_absent_fields_list
from door2door.models import CampaignModel, StreetModel, HouseModel
from door2door.forms import CampaignForm, StreetForm, HouseForm, ReactionCommentForm
from door2door.constants import TYPE_HOUSE_MULTIFLAT


def select_campaign(request):
    """ Отображает страницу выбора кампании """
    campaigns = CampaignModel.objects.all().order_by('-date_create')
    context = {
        'page_title':'Кампании',
        'description': 'кампании',
        'keywords': '',
        'campaigns': campaigns,
        'is_admin': True,
    }
    return render(request, 'door2door/campaign_select.html', context)


def edit_campaign(request, pk=''):
    """ Отображает форму для добавления/редактирования кампании """
    campaign = CampaignModel.objects.get(pk=pk) if pk else CampaignModel()
    form_campaign = CampaignForm(instance=campaign)
    context = {
        'campaign': form_campaign,
        'page_title': '{} кампании'.format('Редактирование' if campaign.pk else 'Добавление'),
        'pk': campaign.pk,
        'description': '',
        'keywords': '',
    }
    return render(request, 'door2door/campaign_edit.html', context)


@csrf_protect
@require_POST
def save_campaign(request):
    """ Сохраняет свойства кампании с формы """
    pk = request.POST.get('id')
    try:
        campaign = CampaignModel.objects.get(pk=pk) if pk else None
    except CampaignModel.DoesNotExist as err:
        return HttpResponse(get_error('Кампания не существует!'))
    form_campaign = CampaignForm(request.POST, instance=campaign)

    if form_campaign.is_valid():
        form_campaign.save()
        new_pk = form_campaign.instance.pk
        answer = get_success(
            'Кампания {}'.format('обновлена' if pk else 'добавлена'),
            {'data': {'id': new_pk}}
    )
    else:
        absent_fields, msg_err = get_absent_fields_list(form_campaign)
        answer = get_error('Ошибка: {}'.format(msg_err), {'absent_fields': absent_fields})

    return HttpResponse(answer)


def select_street(request, campaign_pk):
    """ Отображает страницу выбора улицы """
    streets = StreetModel.objects.filter(campaign_id=campaign_pk).order_by('-date_create')
    context = {
        'page_title':'Выберите улицу',
        'description': 'улицы',
        'keywords': '',
        'streets': streets,
        'campaign_pk': campaign_pk,
        'is_admin': True,
    }
    return render(request, 'door2door/street_select.html', context)


def edit_street(request, campaign_pk, pk=''):
    """ Отображает форму для добавления/редактирования улицы """
    street = StreetModel.objects.get(pk=pk, campaign_id=campaign_pk) if pk else StreetModel(campaign_id=CampaignModel(pk=campaign_pk))
    form_street = StreetForm(instance=street)
    context = {
        'street': form_street,
        'page_title': '{} улицы'.format('Редактирование' if street.pk else 'Добавление'),
        'pk': street.pk,
        'description': '',
        'keywords': '',
    }
    return render(request, 'door2door/street_edit.html', context)


@csrf_protect
@require_POST
def save_street(request):
    """ Сохраняет свойства улицы с формы """
    pk = request.POST.get('id')
    campaign_pk = request.POST.get('campaign_id')
    try:
        street = StreetModel.objects.get(pk=pk, campaign_id=CampaignModel(pk=campaign_pk)) if pk else None
    except StreetModel.DoesNotExist as err:
        return HttpResponse(get_error('Улица не существует!'))
    form_street = StreetForm(request.POST, instance=street)

    if form_street.is_valid():
        form_street.save()
        new_pk = form_street.instance.pk
        answer = get_success(
            'Улица {}'.format('обновлена' if pk else 'добавлена'),
            {'data': {'id': new_pk}}
    )
    else:
        absent_fields, msg_err = get_absent_fields_list(form_street)
        answer = get_error('Ошибка: {}'.format(msg_err), {'absent_fields': absent_fields})

    return HttpResponse(answer)


def select_house(request, street_pk, house_pk=None):
    """ Отображает страницу выбора МКД/квартиры/частного дома """
    houses = HouseModel.objects.filter(street_id=street_pk, group_id=house_pk).order_by('-date_create')
    context = {
        'page_title':'Выберите {}'.format('квартиру' if house_pk else 'дом'),
        'description': '',
        'keywords': '',
        'houses': houses,
        'street_pk': street_pk,
        'house_pk': house_pk,
        'is_admin': True,
    }
    return render(request, 'door2door/house_select.html', context)


def edit_house(request, street_pk, **kwargs):
    """ Отображает форму для добавления/редактирования МКД/квартиры/частного дома """
    house_pk = kwargs.get('house_pk')
    pk = kwargs.get('pk')

    house = HouseModel.objects.get(pk=pk, street_id=street_pk, group_id=house_pk) if pk else HouseModel(street_id=StreetModel(pk=street_pk), group_id=HouseModel(pk=house_pk))
    form_house = HouseForm(instance=house)
    context = {
        'house': form_house,
        'page_title': '{} {}'.format(
            'Редактирование' if house.pk else 'Добавление',
            'квартиры' if house_pk else 'дома'
        ),
        'pk': house.pk,
        'description': '',
        'keywords': '',
    }
    return render(request, 'door2door/house_edit.html', context)


@csrf_protect
@require_POST
def save_house(request):
    """ Сохраняет свойства МКД/квартиры/частного дома с формы """
    pk = request.POST.get('id')
    street_pk = request.POST.get('street_id')
    house_pk = request.POST.get('group_id')
    try:
        house = HouseModel.objects.get(pk=pk, street_id=StreetModel(pk=street_pk), group_id=HouseModel(pk=house_pk)) if pk else None
    except StreetModel.DoesNotExist as err:
        return HttpResponse(get_error('Дом не существует!'))
    form_house = HouseForm(request.POST, instance=house)

    if form_house.is_valid():
        form_house.save()
        new_pk = form_house.instance.pk
        answer = get_success(
            '{} {}'.format('Квартира' if house_pk else 'Дом', 'обновлён' if pk else 'добавлен'),
            {'data': {'id': new_pk}}
    )
    else:
        absent_fields, msg_err = get_absent_fields_list(form_house)
        answer = get_error('Ошибка: {}'.format(msg_err), {'absent_fields': absent_fields})

    return HttpResponse(answer)


def reaction(request, pk):
    """ Отображает панель реакции частного дома/квартиры """
    queryset = HouseModel.objects.exclude(type=TYPE_HOUSE_MULTIFLAT)
    house = get_object_or_404(queryset, pk=pk)
    reaction_comment = ReactionCommentForm(instance=house)

    context = {
        'page_title': 'Реакция',
        'pk': pk,
        'house': house,
        'reaction_comment': reaction_comment,
        'description': '',
        'keywords': '',
    }
    return render(request, 'door2door/reaction.html', context)
    

@csrf_protect
@require_POST
def save_reaction_comment(request, pk):
    """ Сохраняет комментарий частного дома/квартиры """
    try:
        house = HouseModel.objects.exclude(type=TYPE_HOUSE_MULTIFLAT).get(pk=pk)
    except HouseModel.DoesNotExist as err:
        return HttpResponse(get_error('Дом не существует!'))

    form_house = ReactionCommentForm(request.POST, instance=house)
    
    if form_house.is_valid():
        form_house.save()
        answer = get_success('Обновлено')
    else:
        absent_fields, msg_err = get_absent_fields_list(form_house)
        answer = get_error('Ошибка: {}'.format(msg_err), {'absent_fields': absent_fields})

    return HttpResponse(answer)


@csrf_protect
@require_POST
def save_reaction(request, pk):
    """
    Сохраняет реакцию:
    открыли ли дверь, как встретили, приняли ли листовку или дали ли подпись
    """
    reaction_values = {
        'unknown': None,
        'no': 0,
        'yes': 1,
    }
    reaction_names = ('is_openned', 'is_interesed', 'is_recieved')
    
    try:
        house = HouseModel.objects.exclude(type=TYPE_HOUSE_MULTIFLAT).get(pk=pk)
    except HouseModel.DoesNotExist as err:
        return HttpResponse(get_error('Дом не существует!'))
    reaction_name = request.POST.get('name')
    reaction_value = request.POST.get('value')
    
    if reaction_name not in reaction_names:
        return HttpResponse(get_error('Неверное название реакции!'))
    if reaction_value not in reaction_values:
        return HttpResponse(get_error('Неверное значение реакции!'))
    
    setattr(house, reaction_name, reaction_values[reaction_value])
    house.save()
    
    return HttpResponse(get_success('Реакция обновлена'))
    
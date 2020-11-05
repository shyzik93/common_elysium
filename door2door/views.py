from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse

from utils.utils import get_success, get_error, get_absent_fields_list
from door2door.models import CampaignModel, StreetModel, HouseModel
from door2door.forms import CampaignForm, StreetForm, HouseForm, ReactionForm
from door2door.constants import TYPE_HOUSE_MULTIFLAT


def select_campaign(request):
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
    queryset = HouseModel.objects.exclude(type=TYPE_HOUSE_MULTIFLAT)
    house = get_object_or_404(queryset, pk=pk)
    reaction = ReactionForm(instance=house)

    context = {
        'page_title': 'Реакция',
        'pk': pk,
        'house': house,
        'reaction': reaction,
        'description': '',
        'keywords': '',
    }
    return render(request, 'door2door/reaction.html', context)
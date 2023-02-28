from django.forms import ModelForm, TextInput, Select, HiddenInput, Textarea

from door2door.models import CampaignModel, StreetModel, HouseModel


class CampaignForm(ModelForm):
    
    class Meta:
        model = CampaignModel
        exclude = ['date_create', 'date_modify']
        widgets = {
            'name': TextInput(attrs={'placeholder': CampaignModel._meta.get_field('name').verbose_name}),
            'fio_candidate': TextInput(attrs={'placeholder': CampaignModel._meta.get_field('fio_candidate').verbose_name}),
            'region': TextInput(attrs={'placeholder': CampaignModel._meta.get_field('region').verbose_name}),
            'rayon': TextInput(attrs={'placeholder': CampaignModel._meta.get_field('rayon').verbose_name}),
            'settlement': TextInput(attrs={'placeholder': CampaignModel._meta.get_field('settlement').verbose_name}),
        }


class StreetForm(ModelForm):
    
    class Meta:
        model = StreetModel
        exclude = ['date_create', 'date_modify']
        widgets = {
            'campaign_id': HiddenInput(),
            'type_id': Select(attrs={'placeholder': StreetModel._meta.get_field('type_id').verbose_name}),
            'name': TextInput(attrs={'placeholder': StreetModel._meta.get_field('name').verbose_name}),
        }


class HouseForm(ModelForm):
    
    class Meta:
        model = HouseModel
        fields = ['street_id', 'group_id', 'number', 'type']

        widgets = {
            'street_id': HiddenInput(),
            'group_id': HiddenInput(),
            'number': TextInput(attrs={'placeholder': HouseModel._meta.get_field('number').verbose_name}),
        }


class ReactionCommentForm(ModelForm):
    
    class Meta:
        model = HouseModel
        fields = ['problem_description', 'comment']
        
        widgets = {
            'problem_description': Textarea(attrs={'placeholder': HouseModel._meta.get_field('problem_description').verbose_name}),
            'comment': Textarea(attrs={'placeholder': HouseModel._meta.get_field('comment').verbose_name}),
        }
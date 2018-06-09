from django import forms
from django.db import models

from myfarog.models import (
    Armor,
    Earring,
    Footwear,
    Glove,
    Helmet,
    Necklace,
    Pants,
    Ring,
    Shield,
    Shirt,
    Skill,
    Spell,
    Trinket,
    Weapon,
)

class ArmorModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArmorModelForm, self).__init__(*args, **kwargs)
        self.initial['type'] = "Armor"
    
    class Meta:
        model = Armor
        fields = '__all__'


class EarringModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EarringModelForm, self).__init__(*args, **kwargs)
        self.initial['type'] = "Earring"
    
    class Meta:
        model = Earring
        fields = '__all__'


class FootwearModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FootwearModelForm, self).__init__(*args, **kwargs)
        self.initial['type'] = "Footwear"
    
    class Meta:
        model = Footwear
        fields = '__all__'


class GloveModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GloveModelForm, self).__init__(*args, **kwargs)
        self.initial['type'] = "Glove"
    
    class Meta:
        model = Glove
        fields = '__all__'


class HelmetModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(HelmetModelForm, self).__init__(*args, **kwargs)
        self.initial['type'] = "Helmet"
    
    class Meta:
        model = Helmet
        fields = '__all__'


class NecklaceModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NecklaceModelForm, self).__init__(*args, **kwargs)
        self.initial['type'] = "Necklace"
    
    class Meta:
        model = Necklace
        fields = '__all__'


class PantsModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PantsModelForm, self).__init__(*args, **kwargs)
        self.initial['type'] = "Pants"
    
    class Meta:
        model = Pants
        fields = '__all__'


class RingModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RingModelForm, self).__init__(*args, **kwargs)
        self.initial['type'] = "Ring"
    
    class Meta:
        model = Ring
        fields = '__all__'


class ShieldModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ShieldModelForm, self).__init__(*args, **kwargs)
        self.initial['type'] = "Shield"
    
    class Meta:
        model = Shield
        fields = '__all__'


class ShirtModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ShirtModelForm, self).__init__(*args, **kwargs)
        self.initial['type'] = "Shirt"
    
    class Meta:
        model = Shirt
        fields = '__all__'


class SkillModelForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)


    class Meta:
        model = Skill
        fields = '__all__'


class SpellModelForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)


    class Meta:
        model = Spell
        fields = '__all__'


class TrinketModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TrinketModelForm, self).__init__(*args, **kwargs)
        self.initial['type'] = "Trinket"
    
    class Meta:
        model = Trinket
        fields = '__all__'


class WeaponModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WeaponModelForm, self).__init__(*args, **kwargs)
        self.initial['type'] = "Weapon"
    
    class Meta:
        model = Weapon
        fields = '__all__'
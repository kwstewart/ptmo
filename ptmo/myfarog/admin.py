# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from myfarog.models import (
    Armor,
    Container,
    Compartment,
    Culture,
    CultureGenderSkill,
    Earring,
    Footwear,
    Glove,
    Helmet,
    Item,
    ItemBonus,
    ItemBonusType,
    ItemMaterial,
    Necklace,
    Pants,
    Ring,
    Role,
    RoleSkill,
    Shield,
    Shirt,
    Skill,
    Species,
    SpeciesGenderMod,
    Spell,
    SpellElement,
    Talent,
    TalentExtra,
    TalentSkill,
    Trinket,
    Weapon,
)
from myfarog.battle import (
    Battle
)

from myfarog.character import (
    Character,
    CharacterCompartmentItem,
    CharacterCut,
    CharacterSkill,
    CharacterTalent,

)


from myfarog.forms import (
    ArmorModelForm,
    EarringModelForm,
    FootwearModelForm,
    GloveModelForm,
    HelmetModelForm,
    NecklaceModelForm,
    PantsModelForm,
    RingModelForm,
    ShieldModelForm,
    ShirtModelForm,
    SkillModelForm,
    SpellModelForm,
    TrinketModelForm,
    WeaponModelForm,
)

class ArmorAdmin(admin.ModelAdmin):
    form            = ArmorModelForm
    list_display    = ('name', 'AV', 'MS_mod', 'weight', 'stealth_mod', 'swimming_mod', 'get_bonuses', )
    search_fields   = ['name']
    readonly_fields = ('type', )
    save_as         = True

admin.site.register(Armor, ArmorAdmin)


class CharacterAdmin(admin.ModelAdmin):
    list_display        = ('name', 'user', 'species', 'role')
    search_fields       = ['name', 'user', 'species', 'role']
    ordering            = ['name']
    readonly_fields     = ['_cha', '_con', '_dex', '_int', '_str', '_wil',
                           'max_HP', 'max_MHP', 'max_SP', 'size', 
                           'encumbrance_mod', 'encumbrance_status',
                           'health_mod', 'health_status', 'mental_health_mod',
                           'mental_health_status', 'stamina_mod', 'stamina_status',
                           'morale_status' ,'morale_rounds', 'morale_check_bonus',
                           'fright_mod', 'initiative_check_bonus',
                           'OV_melee', 'OV_missile', 'DV_melee', 'DV_missile'
                          ]
    save_as             = True

admin.site.register(Character, CharacterAdmin)


class CharacterCompartmentItemAdmin(admin.ModelAdmin):
    list_display    = ('character', 'compartment', 'item')
    search_fields   = ['character', 'compartment', 'item']
    save_as         = True

admin.site.register(CharacterCompartmentItem, CharacterCompartmentItemAdmin)


class CharacterCutAdmin(admin.ModelAdmin):
    list_display = ('character', 'severity')
    search_fields = ['character', 'severity']
    save_as = True

admin.site.register(CharacterCut, CharacterCutAdmin)


class CharacterSkillAdmin(admin.ModelAdmin):
    list_display    = ('character', 'skill', 'trained', 'role_skill')
    search_fields   = ['character', 'skill']
    save_as         = True

admin.site.register(CharacterSkill, CharacterSkillAdmin)


class CharacterTalentAdmin(admin.ModelAdmin):
    list_display = ('character', 'talent',)
    search_fields = ['character', 'talent']
    save_as = True

admin.site.register(CharacterTalent, CharacterTalentAdmin)


class CompartmentAdmin(admin.ModelAdmin):
    list_display    = ('name',)
    search_fields   = ['name']
    save_as         = True

admin.site.register(Compartment, CompartmentAdmin)


class ContainerAdmin(admin.ModelAdmin):
    list_display    = ('name',)
    search_fields   = ['name']
    save_as         = True

admin.site.register(Container, ContainerAdmin)


class CultureAdmin(admin.ModelAdmin):
    list_display    = ('name',)
    search_fields   = ['name']
    save_as         = True

admin.site.register(Culture, CultureAdmin)


class CultureGenderSkillAdmin(admin.ModelAdmin):
    list_display    = ('culture', 'gender', 'skill')
    search_fields   = ['name', 'gender', 'skill']
    save_as         = True

admin.site.register(CultureGenderSkill, CultureGenderSkillAdmin)


class EarringAdmin(admin.ModelAdmin):
    form            = EarringModelForm
    list_display    = ('name', 'get_bonuses', )
    search_fields   = ['name']
    save_as         = True
    readonly_fields = ('type', )

admin.site.register(Earring, EarringAdmin)


class FootwearAdmin(admin.ModelAdmin):
    form            = FootwearModelForm
    list_display    = ('name', 'get_bonuses', )
    search_fields   = ['name']
    save_as         = True
    readonly_fields = ('type', )

admin.site.register(Footwear, FootwearAdmin)


class GloveAdmin(admin.ModelAdmin):
    form            = GloveModelForm
    list_display    = ('name', 'get_bonuses', )
    search_fields   = ['name']
    save_as         = True
    readonly_fields = ('type', )

admin.site.register(Glove, GloveAdmin)


class HelmetAdmin(admin.ModelAdmin):
    form            = HelmetModelForm
    list_display    = ('name', 'get_bonuses', )
    search_fields   = ['name']
    save_as         = True
    readonly_fields = ('type', )

admin.site.register(Helmet, HelmetAdmin)


class ItemMaterialAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']
    ordering = ['name']
    save_as = True

admin.site.register(ItemMaterial, ItemMaterialAdmin)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'description')
    search_fields = ['name', 'type', 'description']
    ordering = ['name']
    save_as = True

admin.site.register(Item, ItemAdmin)

class ItemBonusAdmin(admin.ModelAdmin):
    list_display = ('type', 'value',)
    search_fields = ['type']
    ordering = ['type', 'value']
    save_as = True

admin.site.register(ItemBonus, ItemBonusAdmin)


class ItemBonusTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']
    ordering = ['name']
    save_as = True

admin.site.register(ItemBonusType, ItemBonusTypeAdmin)


class NecklaceAdmin(admin.ModelAdmin):
    form            = NecklaceModelForm
    list_display    = ('name', 'get_bonuses', )
    search_fields   = ['name']
    save_as         = True

admin.site.register(Necklace, NecklaceAdmin)


class PantsAdmin(admin.ModelAdmin):
    form            = PantsModelForm
    list_display    = ('name', 'get_bonuses', )
    search_fields   = ['name']
    save_as         = True
    readonly_fields = ('type', )

admin.site.register(Pants, PantsAdmin)


class RingAdmin(admin.ModelAdmin):
    form            = RingModelForm
    list_display    = ('name', 'get_bonuses', )
    search_fields   = ['name']
    save_as         = True
    readonly_fields = ('type', )

admin.site.register(Ring, RingAdmin)


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']
    ordering = ['name']
    save_as = True

admin.site.register(Role, RoleAdmin)


class RoleSkillAdmin(admin.ModelAdmin):
    list_display = ('role', 'skill',)
    search_fields = ['role', 'skill']
    ordering = ['role', 'skill']
    save_as = True

admin.site.register(RoleSkill, RoleSkillAdmin)


class ShieldAdmin(admin.ModelAdmin):
    form            = ShieldModelForm
    list_display    = ('name', 'get_bonuses', )
    search_fields   = ['name']
    save_as         = True
    readonly_fields = ('type', )

admin.site.register(Shield, ShieldAdmin)


class ShirtAdmin(admin.ModelAdmin):
    form            = ShirtModelForm
    list_display    = ('name', 'get_bonuses', )
    search_fields   = ['name']
    save_as         = True
    readonly_fields = ('type', )

admin.site.register(Shirt, ShirtAdmin)


class SkillAdmin(admin.ModelAdmin):
    form            = SkillModelForm
    list_display    = ('name', 'attribute', 'untrained', 'description')
    search_fields   = ['name']
    ordering        = ['name']
    save_as         = True

admin.site.register(Skill, SkillAdmin)


class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']
    save_as = True

admin.site.register(Species, SpeciesAdmin)


class SpeciesGenderModAdmin(admin.ModelAdmin):
    list_display = ('species', 'gender')
    search_fields = ['species', 'gender']
    save_as = True

admin.site.register(SpeciesGenderMod, SpeciesGenderModAdmin)


class SpellAdmin(admin.ModelAdmin):
    form            = SpellModelForm
    list_display    = ('name', 'get_elements', 'description')
    search_fields   = ['name']
    ordering        = ['name']
    save_as         = True

    def get_elements(self, obj):
        return obj.get_elements()
    get_elements.short_description = "Elements"

admin.site.register(Spell, SpellAdmin)


class SpellElementAdmin(admin.ModelAdmin):
    list_display    = ('name', 'symbol')
    search_fields   = ['name']
    ordering        = ['name']
    save_as         = True

admin.site.register(SpellElement, SpellElementAdmin)


class TalentAdmin(admin.ModelAdmin):
    list_display = ('name', 'prerequisite')
    search_fields = ['name', 'prerequisite']
    ordering = ['name']
    save_as = True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "prerequisite":
            kwargs["queryset"] = Talent.objects.filter().order_by('name')
        return super(TalentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Talent, TalentAdmin)


class TalentSkillAdmin(admin.ModelAdmin):
    list_display = ('talent', 'skill', 'mod')
    search_fields = ['talent', 'skill']
    ordering = ['talent', 'skill']
    save_as = True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "talent":
            kwargs["queryset"] = Talent.objects.filter().order_by('name')
        elif db_field.name == "skill":
            kwargs["queryset"] = Skill.objects.filter().order_by('name')
        return super(TalentSkillAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(TalentSkill, TalentSkillAdmin)


class TalentExtraAdmin(admin.ModelAdmin):
    list_display = ('talent', 'extra', 'mod')
    search_fields = ['talent', 'extra']
    ordering = ['talent', 'extra']
    save_as = True

admin.site.register(TalentExtra, TalentExtraAdmin)


class TrinketAdmin(admin.ModelAdmin):
    form            = TrinketModelForm
    list_display    = ('name', 'get_bonuses', )
    search_fields   = ['name']
    save_as         = True
    readonly_fields = ('type', )

admin.site.register(Trinket, TrinketAdmin)


class WeaponAdmin(admin.ModelAdmin):
    form            = WeaponModelForm
    list_display    = ('name', 'weapon_type', 'material', 'damage', 'cut', 'shock', 'range', 'get_bonuses', 'unique')
    search_fields   = ['name']
    ordering        = ['name']
    readonly_fields = ('type', )
    save_as         = True

    def get_bonuses(self, obj):
        return obj.get_bonuses()
    get_bonuses.short_description = "Bonuses"

admin.site.register(Weapon, WeaponAdmin)

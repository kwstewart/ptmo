
ANIMAL_SPECIES = [
    'Cat'
]

ATTRIBUTES = (
    ('CHA', 'CHA'),
    ('CON', 'CON'),
    ('DEX', 'DEX'),
    ('INT', 'INT'),
    ('STR', 'STR'),
    ('WIL', 'WIL'),
)

BATTLE_ROUND_LOG_ACTIONS = (
    ('attack' , 'Attack'),
    ('cast' , 'Cast'),
    ('use' , 'Use'),
)

COMPARTMENT_TYPES = (
    ('main',    'Main'),
    ('pocket',  'pocket'),
)

CUT_SEVERITIES = (
    ('Light',   'Light'),
    ('Medium',  'Medium'),
    ('Serious', 'Serious'),
)

ENCUMBERANCE_STATUSES = (
    ('Light',   'Light'),
    ('Medium',  'Medium'),
    ('Heavy',   'Heavy'),
)

EQUIPMENT_SLOTS = [
    'shirt_equipment',
    'pants_equipment',
    'jacket_equipment',
    'left_hand_weapon',
    'left_hand_shield',
    'right_hand_weapon',
    'right_hand_shield',
    'armor_equipment',
    'helmet_equipment',
    'left_glove_equipment',
    'right_glove_equipment',
    'footwear_equipment',
    'necklace_equipment',
    'left_earring_equipment',
    'right_earring_equipment',
    'ring_equipment',
    'trinket_equipment',
    'belt_equipment'
]

GENDER = (
    ('male', 'Male'),
    ('female', 'Female'),
)

HANDEDNESS_CHOICES = (
    ('right',   'Right'),
    ('left',    'Left'),
)

HEALTH_STATUSES = (
    ('Normal',              'Normal'),
    ('Seriously Injured',   'Seriously Injured'),
    ('Severely Injured',    'Severely Injured'),
    ('Fatally Injured',     'Fatally Injured'),
)

ITEM_BONUS_TYPES = (
    ('Cha', 'Cha'),
    ('Con', 'Con'),
    ('Dex', 'Dex'),
    ('Int', 'Int'),
    ('Str', 'Str'),
    ('Wil', 'Wil'),
    ('Life Stance', 'Life Stance'),
    ('Social Class', 'Social Class'),
)

ITEM_PREREQ_TYPES = (
    ('CHA', 'CHA'),
    ('CON', 'CON'),
    ('DEX', 'DEX'),
    ('INT', 'INT'),
    ('STR', 'STR'),
    ('WIL', 'WIL'),
    ('Role', 'Role'),
    ('Life Stance', 'Life Stance'),
    ('Social Class', 'Social Class'),
)

ITEM_TYPES = (
    ('shirt',    'Shirt'),
    ('pants',    'Pants'),
    ('weapon',   'Weapon'),
    ('armor',    'Armor'),
    ('helmet',   'Helmet'),
    ('shield',   'Shield'),
    ('gloves',   'Gloves'),
    ('belt',     'Belt'),
    ('footwear', 'Footwear'),
    ('necklace', 'Necklace'),
    ('earring',  'Earring'),
    ('ring',     'Ring'),
    ('trinket',  'Trinket'),
    ('backpack', 'Backpack'),
    ('sack',     'Sack'),
    ('misc',     'Misc'),
)

MENTAL_HEALTH_STATUSES = (
    ('Normal',      'Normal'),
    ('Stressed',    'Stressed'),
    ('Agitated',    'Agitated'),
    ('Deranged',    'Deranged'),
    ('Pyschotic',   'Pyschotic'),
)

MORALE_STATUSES = (
    ('Normal',      'Normal'),
    ('Nervous',     'Nervous'),
    ('Afraid',      'Afraid'),
    ('Fearful',     'Fearful'),
    ('Terrified',   'Terrified'),
    ('Panic',       'Panic'),
)

ROLE_PREREQ_TYPES = (
    ('CHA', 'CHA'),
    ('CON', 'CON'),
    ('DEX', 'DEX'),
    ('INT', 'INT'),
    ('STR', 'STR'),
    ('WIL', 'WIL'),
    ('Talent', 'Talent'),
    ('Life Stance', 'Life Stance'),
    ('Social Class', 'Social Class'),
)

SKILL_TYPES = (
    ('CS', 'Combat Skill'),
    ('MS', 'Movement Skill'),
    ('SS', 'Special Skill'),
)

STAMINA_STATUSES = (
    ('Normal',      'Normal'),
    ('Tired',       'Tired'),
    ('Weary',       'Weary'),
    ('Exhausted',   'Exhausted'),
    ('Unconscious', 'Unconscious'),
)

STUN_STATUSES = (
    ('Normal',          'Normal'),
    ('Stunned',         'Strunned'),
    ('Knocked Down',    'Knocked Down'),
    ('Knocked Out',     'Knocked Out'),
)

TALENT_EXTRAS = (
    ('Cold Toughness',          'Cold Toughness'),
    ('Disease Resistance',      'Disease Resistance'),
    ('Electrical Toughness',    'Electrical Toughness'),
    ('Heat Toughness',          'Heat Toughness'),
    ('Initiative',              'Initiative'),
    ('Morale',                  'Morale'),
    ('Mental Toughness',        'Mental Toughness'),
    ('Physical Toughness',      'Physical Toughness'),
    ('Posion Resistance',       'Posion Resistance'),
)

WEAPON_CLASSES = (
    ('melee',           'Melee'),
    ('missile',         'Missile'),
    ('small Weapon',    'Small_weapon'),
    ('heavy Weapon',    'Heavy_weapon'),
)

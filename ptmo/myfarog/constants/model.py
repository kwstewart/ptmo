GENDER = (
    ('male', 'Male'),
    ('female', 'Female'),
)

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

COMPARTMENT_TYPES = (
    ('main',    'Main'),
    ('pocket',  'pocket'),
)

HANDEDNESS_CHOICES = (
    ('right',   'Right'),
    ('left',    'Left'),
)

TALENT_EXTRAS = (
    ('Cold Toughness',          'Cold Toughness'),
    ('Disease Resistance',      'Disease Resistance'),
    ('Electrical Toughness',    'Electrical Toughness'),
    ('Heat Toughness',          'Heat Toughness'),
    ('Initiative',              'Initiative'),
    ('Morale',                  'Morale'),
    ('Physical Toughness',      'Physical Toughness'),
    ('Posion Resistance',       'Posion Resistance'),
)

SKILL_TYPES = (
    ('CS', 'Combat Skill'),
    ('MS', 'Movement Skill'),
    ('SS', 'Special Skill'),
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

MORALE_STATUSES = (
    ('Normal',      'Normal'),
    ('Nervous',     'Nervous'),
    ('Afraid',      'Afraid'),
    ('Fearful',     'Fearful'),
    ('Terrified',   'Terrified'),
    ('Panic',       'Panic'),
)

ENCUMBERANCE_STATUSES = (
    ('Light',   'Light'),
    ('Medium',  'Medium'),
    ('Heavy',   'Heavy'),
)

HEALTH_STATUSES = (
    ('Normal',              'Normal'),
    ('Seriously Injured',   'Seriously Injured'),
    ('Severely Injured',    'Severely Injured'),
    ('Fatally Injured',     'Fatally Injured'),
)

MENTAL_HEALTH_STATUSES = (
    ('Normal',      'Normal'),
    ('Stressed',    'Stressed'),
    ('Agitated',    'Agitated'),
    ('Deranged',    'Deranged'),
    ('Pyschotic',   'Pyschotic'),
)

STAMINA_STATUSES = (
    ('Normal',      'Normal'),
    ('Tired',       'Tired'),
    ('Exhausted',   'Exhausted'),
    ('Unconscious', 'Unconscious'),
)

STUN_STATUSES = (
    ('Normal',          'Normal'),
    ('Stunned',         'Strunned'),
    ('Knocked Down',    'Knocked Down'),
    ('Knocked Out',     'Knocked Out'),
)

CUT_SEVERITIES = (
    ('Light',   'Light'),
    ('Medium',  'Medium'),
    ('Serious', 'Serious'),
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

WEAPON_CLASSES = (
    ('melee',           'Melee'),
    ('missile',         'Missile'),
    ('small Weapon',    'Small_weapon'),
    ('heavy Weapon',    'Heavy_weapon'),
)

BATTLE_ROUND_LOG_ACTIONS = (
    ('attack' , 'Attack'),
    ('cast' , 'Cast'),
    ('use' , 'Use'),
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
    'helment_equipment',
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
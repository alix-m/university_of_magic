import services
from _sims4_collections import frozendict

from sims.sim_spawner import SimSpawner, Language
from sims.sim_spawner_enums import SimNameType


def spellcaster_names(cls):
    language = Language.ENGLISH
    name_type = SimNameType.Spellcaster
    new_names_language = {}

    base_name_map = dict(SimSpawner.SIM_NAME_TYPE_TO_LOCALE_NAMES)
    base_names = base_name_map[SimNameType.FamiliarOwl][language]

    new_names = base_names.clone_with_overrides(female_first_names=tuple(SpellcasterNames.female_first_names),
                                                male_first_names=tuple(SpellcasterNames.male_first_names),
                                                last_names=tuple(SpellcasterNames.last_names))

    new_names_language[language] = new_names
    base_name_map[name_type] = frozendict(new_names_language)

    SimSpawner.SIM_NAME_TYPE_TO_LOCALE_NAMES = frozendict(base_name_map)


class SpellcasterNames:
    female_first_names = ['Amaltheia', 'Andromeda', 'Ariadne', 'Artemis', 'Astraea', 'Aurora', 'Blossom', 'Calpurnia',
                          'Cassiopeia', 'Circe', 'Clementine', 'Cordelia', 'Cressida', 'Cybele', 'Daphne', 'Demeteria',
                          'Emmeline', 'Eurydice', 'Fern', 'Fleur', 'Hermione', 'Hypatia', 'Isolde', 'Juliette',
                          'Juniper', 'Lavinia', 'Lucretia', 'Luna', 'Magnolia', 'Maxime', 'Melody', 'Minerva', 'Nebula',
                          'Pandora', 'Persephone', 'Poppy', 'Selene', 'Serenity', 'Stella', 'Valentina', 'Xanthia']

    male_first_names = ['Atticus', 'Ares', 'Abraxas', 'Draco', 'Perseus', 'Aslan', 'Felix', 'Achilles', 'Altair',
                        'Aristotle', 'Angus', 'Alasdair', 'Avery', 'Gilderoy', 'Cedric', 'Hermes', 'Casper', 'Silas',
                        'Niall', 'Rufus', 'Endymion', 'Wyatt', 'Edwin', 'Bancroft', 'Herodotus', 'Benedict',
                        'Archibald',
                        'Archimedes', 'Hesiod', 'Erasmus', 'Evander', 'Oberon', 'Octavius', 'Orion', 'Julian',
                        'Barclay', 'Ulysses', 'Edelbert', 'Ignatius', 'Helios']

    last_names = ['Alves', 'Bell', 'Blackwood', 'Bellchant', 'Birch', 'Dedelworth', 'Delacroix', 'Alton', 'Bilberry',
                  'Gardner', 'Batworthy', 'Alderton', 'Fudge', 'Flitwick', 'Cooper', 'Flamel', 'Dawlish', 'Bones',
                  'Bobbin', 'Gaunt', 'Goosewink', 'Green', 'Bagman', 'Flume', 'Cloke', 'Carneirus', 'Foxfig', 'Diggory',
                  'Dodderidge', 'Belby', 'Greyback', 'Bletchley', 'Fox', 'Boffin', 'Creighton', 'Denbright', 'Brown',
                  'Fortescue',
                  'Fenwick', 'Filch', 'Dippet', 'Figg', 'Granger', 'Finch', 'Calderon', 'Farley', 'Fawcett',
                  'Featherstone', 'Fletcher', 'Bagshot', 'Grimblehawk', 'Gray', 'Carlyle', 'Brandybuck', 'Graves',
                  'Flowers', 'Goyle',
                  'Cattermole', 'Grimm', 'Grubbly-Plank', 'Gudgeon', 'Hawkworth', 'Haywood', 'Hedgehopper',
                  'Hifflepepper', 'Hobday', 'Honeyfoam', 'Hooch', 'Horton', 'Izzledoff', 'Jones', 'Kettleburn',
                  'Killick', 'King',
                  'Krum',
                  'Latimer', 'Laufsblad', 'Lestrange', 'Lima', 'Littlepond', 'Longbottom', 'Lovegood', 'Loxias',
                  'Lupin',
                  'MacFusty', 'Macnair', 'Maestro', 'Malfoy', 'McGonagall', 'Midgen', 'Miller', 'Mimsy', 'Montague',
                  'Montgomery', 'Moon', 'Moonsage', 'Morgan', 'Moriarty', 'Murk', 'Nettles', 'Noel', 'Nox', 'Oddpick',
                  'Ogden', 'Ollivander', 'Orpington', 'Peasegood', 'Pendragon', 'Pettigrew', 'Plunkett', 'Podmore',
                  'Poke',
                  'Popswaddle', 'Porpington', 'Poufsouffle', 'Rabnott', 'Ragnor', 'Robins', 'Runcorn', 'Sangrey',
                  'Scamander', 'Scrimbleshank', 'Scrimgeour', 'Skeeter', 'Slinkhard', 'Smethwyck', 'Snyde', 'Spinnet',
                  'Sprout', 'Spudmore', 'Stump', 'Thorne', 'Tinkleton', 'Tinyfoot', 'Tofty', 'Tonks', 'Took',
                  'Trelawney',
                  'Trigg', 'Trimble', 'Tuft', 'Tumblecreek', 'Tuttle', 'Umbridge', 'Vane', 'Vexmoor', 'Vole',
                  'Vulchanov',
                  'Wakefield', 'Weasley', 'Weiss', 'Wendell', 'Whistleton', 'Whitbottom', 'Whittle', 'Wilkinson',
                  'Williams', 'Wolfmoon', 'Wolpert', 'Wood', 'Wright', 'Yaxley', 'Zabini', 'Streudel']


with SimNameType.make_mutable():
    # noinspection PyProtectedMember
    SimNameType._add_new_enum_value('Spellcaster', 687)

services.definition_manager().add_on_load_complete(spellcaster_names)

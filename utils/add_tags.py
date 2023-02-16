from tag import Tag


def add_tags(category, kvp):
    with category.make_mutable():
        for (k, v) in kvp.items():
            category._add_new_enum_value(k, v)


func_tags = { 
    'attractor_charms': 2262496390,
    'attractor_potions': 3858182614,
    'attractor_herbology': 4250065225,
    'attractor_datda': 3706829272
}

add_tags(Tag, func_tags)
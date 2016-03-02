import string
import random
try:
    from slugify import slugify
except ImportError:
    def slugify(words):
        return words.lower().replace(" ", "-")

titles = [
    'captain',
    'lieutenant',
    'leftenant',
    'colonel',
    'general',
    'major',
    'sir',
    'sensei',
    'lord',
    'duke',
    'president',
    'master',
    'mister',
    'miss',
    'lady',
    'queen',
    'king',
    'doctor',
    'monsieur',
    'madame',
    'senor',
    'senorita',
    'lord commander',
    'luchadore',
    'commodore',
    'emperor',
    'super-emperor',
    'madam',
    'dame',
    'professor',
    'father',
    'brother',
    'sister',
    'reverend',
]

adjectives = [
    'heroic',
    'magnificent',
    'mighty',
    'amazing',
    'wonderful',
    'fantastic',
    'incredible',
    'spectacular',
    'tremendous',
    'throbbing',
    'enormous',
    'terrific',
    'wondrous',
    'spectacular',
    'big',
    'tiny',
    'small',
    'mighty',
    'musky',
    'transparent',
    'opaque',
    'light',
    'dark',
    'scary',
    'extraneous',
    'huge',
    'aqua',
    'aquamarine',
    'azure',
    'beige',
    'black',
    'almond',
    'blue',
    'brown',
    'chartreuse',
    'coral',
    'cornflower',
    'crimson',
    'cyan',
    'navy',
    'goldenrod',
    'gray',
    'grey',
    'green',
    'khaki',
    'magenta',
    'olive',
    'salmon',
    'slate',
    'turquoise',
    'violet',
    'pink',
    'skyblue',
    'brick',
    'white',
    'fuchsia',
    'gainsboro',
    'golden',
    'honeydew',
    'hotpink',
    'indigo',
    'ivory',
    'lavender',
    'lemon',
    'chiffon',
    'purple',
    'orchid',
    'linen',
    'rose',
    'orange',
    'pale',
    'sandy',
    'seashell',
    'silver',
    'tan',
    'teal',
    'thistle',
    'violet',
    'plaid',
    'polkadot',
    'paisley',
    'iron',
    'bronze',
    'stone',
    'birch',
    'cedar',
    'cherrywood',
    'sandalwood',
    'pine',
    'fir',
    'yew',
    'hemlock',
    'spruce',
    'chestnut',
    'boxwood',
    'butternut',
    'camphor',
    'elm',
    'oak',
    'mahogany',
    'huckleberry',
    'ironwood',
    'maple',
    'poplar',
    'unpoplar',
    'teak',
    'beech',
    'nutmeg',
    'willow',
    'cinnamon',
    'allspice',
    'basil',
    'cardamom',
    'clove',
    'garlic',
    'juniper',
    'gin-soaked',
    'rum',
    'lime',
    'licorice',
    'capable',
    'trustworthy',
    'heavy',
    'fast',
    'slow',
    'charming',
    'noticeable',
    'sly',
    'slippery',
    'sluggish',
    'casual',
    'cautious',
    'cement',
    'diabolical',
    'evil',
    'metropolitan',
    'banana',
    'good',
    'neutral',
    'apple',
    'pear',
    'winter',
    'spring',
    'fall',
    'autumn',
    'summer',
    'garbage',
    'imposing',
    'correct',
    'underhanded',
    'salty',
    'coffee',
    'cheese',
    'floppy',
    'unpopular',
    'popular',
    'forgettable',
    'misty',
    'soulful',
    'gassy',
    'spectacular',
    'sleepy',
    'laudable',
    'comfortable',
    'soft',
    'dicey',
    'memorable',
    'patterned',
    'greasy',
    'elongated',
    'long',
    'collapsible',
    'mysterious',
    'expandible',
    'delicious',
    'edible',
    'scattered',
    'impenetrable',
    'sexy',
    'curvaceous',
    'intractable',
    'unavoidable',
    'impressive',
    'impeccable',
    'fussy',
    'touchable',
    'intermittent',
    'scandalous',
    'murky',
    'sloshing',
    'damp',
    'chubby',
]

nouns = [
    'apparatus',
    'britches',
    'mystery',
    'secret',
    'butt',
    'hunter',
    'fisher',
    'bean',
    'harvest',
    'mixer',
    'hand',
    'finger',
    'nose',
    'eye',
    'belly',
    'jeans',
    'plan',
    'disk',
    'horse',
    'battery',
    'staple',
    'face',
    'button',
    'byte',
    'cabinet',
    'vehicle',
    'canyon',
    'dance',
    'crayon',
    'sausage',
    'meat',
    'napkin',
    'device',
    'cape',
    'chair',
    'person',
    'character',
    'burger',
    'ham',
    'beef',
    'book',
    'circuit',
    'civilian',
    'clamp',
    'circuitry',
    'calculus',
    'cloud',
    'code',
    'coast',
    'coin',
    'corporation',
    'concern',
    'space',
    'key',
    'object',
    'heart',
    'stapler',
    'mug',
    'bottle',
    'cable',
    'note',
    'lamp',
    'shelf',
    'blanket',
    'dong',
    'board',
    'indicator',
    'injection',
    'investment',
    'issue',
    'job',
    'knife',
    'thing',
    'phone',
    'sweater',
    'pants',
    'boot',
    'sock',
    'socks',
    'hat',
    'ring',
    'dong',
    'wrap',
    'holder',
    'pen',
    'pencil',
    'bag',
    'dispenser',
    'butter',
    'potato',
    'sword',
    'shield',
    'spear',
    'staff',
    'shaft',
    'slab',
    'sandwich',
    'song',
    'glaive',
    'axe',
    'crossbow',
    'armour',
    'lamp',
    'club',
    'cage',
    'typewriter',
    'hole',
    'ass',
    'chump',
    'jerk',
    'feet',
    'spud',
]

firstnames = [
    'carl',
    'tim',
    'mary',
    'peter',
    'wilhelm',
    'kimmy',
    'steve',
    'jennifer',
    'frank',
    'pierre',
    'george',
    'aya',
    'thiago',
    'daniel',
    'liam',
    'jack',
    'agustin',
    'santiago',
    'noah',
    'sofia',
    'olivia',
    'madison',
    'chloe',
    'camilla',
    'carla',
    'hiroto',
    'rasmus',
    'charlie',
    'miguel',
    'alexander',
    'youssef',
    'emma',
    'maya',
    'sara',
    'amelia',
    'tiffany',
    'arnold',
    'ronald',
    'hogan',
    'doug',
    'pete',
    'jim',
    'james',
    'mandy',
    'andy',
    'cole',
    'miloslav',
    'walter',
]



def title():
    return random.choice(titles)


def adjective():
    return random.choice(adjectives)


def noun():
    return random.choice(nouns)


def firstname():
    return random.choice(firstnames)


def name():
    return slugify(proper_name())


def thing():
    return adjective()+" "+noun()


def proper_name():
    slab = random.choice([
        noun(),
        adjective(),
        noun()+noun(),
        noun()+adjective(),
        noun()+adjective(),
        adjective()+noun(),
        adjective()+noun()])
    if random.choice([True, False]):
        slab = firstname() + " " + slab
    else:
        slab = title() + " " + slab

    return slab.title()

def special_thing():
    return random.choice([
        "{}'s {}".format(proper_name(), noun().title()),
        "{}'s {}".format(proper_name(), thing().title()),
        "The {} of {}".format(thing().title(), proper_name()),
        "The {} {} {} of {}".format(adjective().title(), adjective().title(), noun().title(), proper_name()),
        ])

def markdown():
    words = ""
    for i in range(0, 10):
        if random.choice([True, False, False, False, False]):
            words = words + "#### "
        words = words + proper_name() + " "
        for i in range(0, random.randrange(3,30,1)):
            word = random.choice([noun(), adjective()])
            if random.choice([True, False, False]):
                word = "**{}**".format(word)
            elif random.choice([True, False, False]):
                word = "_{}_".format(word)
            words = words + word + " "
        words = words + ".\n\n"
    return words


def int_to_silly_slug(n):
    """
    Converts an integer, via a 2-way mapping, into a silly slug.

    >>> int_to_silly_slug(17)
    'mighty'

    >>> int_to_silly_slug(-17)
    'miss-mighty'

    >>> int_to_silly_slug(300)
    'peter-heroic'

    >>> int_to_silly_slug(2503121232130)
    'mary-violet-almond-light-scary-light-black'

    """
    str_n = str(int(n))
    word_constructor = []
    if str_n[0] == '-':
        word_constructor.append("miss")
        str_n = str_n[1:]

    odd = lambda x: x % 2 == 1
    assert(odd(1))
    assert(not odd(2))

    if odd(len(str_n)):
        word_constructor.append(firstnames[int(str_n[0])])
        str_n = str_n[1:]

    while len(str_n) > 2:
        word_constructor.append(adjectives[int(str_n[:2])])
        str_n = str_n[2:]

    if len(str_n) == 2:
        word_constructor.append(nouns[int(str_n[:2])])
        str_n = str_n[2:]

    return "-".join(word_constructor)


def silly_slug_to_int(silly_slug):
    """
    Converts a silly slug back into an integer.
    """
    words = silly_slug.split("-")
    number_constructor = []
    if words[0] == "miss":
        number_constructor.append("-")
        words = words[1:]

    try:
        indx = firstnames.index(words[0])
        number_constructor.append(str(indx))
        words = words[1:]
    except ValueError:
        pass

    while len(words) > 1:
        indx = adjectives.index(words[0])
        number_constructor.append(str(indx))
        words = words[1:]

    if len(words) == 1:
        indx = nouns.index(words[0])
        number_constructor.append(str(indx))
        words = words[1:]

    return int("".join(number_constructor))

def noop(x):
    """
    A test.
    """
    return silly_slug_to_int(int_to_silly_slug(x))


if __name__ == '__main__':
    print(name())

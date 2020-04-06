""" Color dictionary. [XKCD colors](https://xkcd.com/color/rgb/) are used. """


import imgui
import sys


MAX_COLOR = 256 - sys.float_info.epsilon * 128


def color_to_rgba(c):
    if isinstance(c, int):
        return c
    elif isinstance(c, (tuple, list)) and len(c) == 4:
        return int(MAX_COLOR * c[3]) * 0x1000000 + int(MAX_COLOR * c[2]) * 0x10000 + int(MAX_COLOR * c[1]) * 0x100 + int(MAX_COLOR * c[0])
    elif isinstance(c, (tuple, list)) and len(c) == 3:
        return 0xff000000 + int(MAX_COLOR * c[2]) * 0x10000 + int(MAX_COLOR * c[1]) * 0x100 + int(MAX_COLOR * c[0])
    elif isinstance(c, str):
        return xkcd_colors[c]
    elif isinstance(c, (tuple, list)) and len(c) == 2 and isinstance(c[0], str):
        return xkcd_colors[c[0]] - 0xff000000 + (min(255, max(0, int(MAX_COLOR * c[1]))) << 24)
    else:
        raise ValueError("Color must be RGBA tuple, RGB tuple, string, int, or (str, float) name & alpha tuple")

def color_to_rgba_tuple(c):
    n = color_to_rgba(c)
    return ((n // 0x1) % 0x100) / 255, \
           ((n // 0x100) % 0x100) / 255, \
           ((n // 0x10000) % 0x100) / 255, \
           ((n // 0x1000000) % 0x100) / 255


# License: http://creativecommons.org/publicdomain/zero/1.0/
xkcd_colors = {
"cloudy blue": 0xffd9c2ac,
"dark pastel green": 0xff57ae56,
"dust": 0xff6e99b2,
"electric lime": 0xff04ffa8,
"fresh green": 0xff4fd869,
"light eggplant": 0xff854589,
"nasty green": 0xff3fb270,
"really light blue": 0xffffffd4,
"tea": 0xff7cab65,
"warm purple": 0xff8f2e95,
"yellowish tan": 0xff81fcfc,
"cement": 0xff91a3a5,
"dark grass green": 0xff048038,
"dusty teal": 0xff85904c,
"grey teal": 0xff8a9b5e,
"macaroni and cheese": 0xff35b4ef,
"pinkish tan": 0xff829bd9,
"spruce": 0xff385f0a,
"strong blue": 0xfff7060c,
"toxic green": 0xff2ade61,
"windows blue": 0xffbf7837,
"blue blue": 0xffc74222,
"blue with a hint of purple": 0xffc63c53,
"booger": 0xff3cb59b,
"bright sea green": 0xffa6ff05,
"dark green blue": 0xff57631f,
"deep turquoise": 0xff747301,
"green teal": 0xff77b50c,
"strong pink": 0xff8907ff,
"bland": 0xff8ba8af,
"deep aqua": 0xff7f7808,
"lavender pink": 0xffd785dd,
"light moss green": 0xff75c8a6,
"light seafoam green": 0xffb5ffa7,
"olive yellow": 0xff09b7c2,
"pig pink": 0xffa58ee7,
"deep lilac": 0xffbd6e96,
"desert": 0xff60adcc,
"dusty lavender": 0xffa886ac,
"purpley grey": 0xff947e94,
"purply": 0xffb23f98,
"candy pink": 0xffe963ff,
"light pastel green": 0xffa5fbb2,
"boring green": 0xff65b363,
"kiwi green": 0xff3fe58e,
"light grey green": 0xffa1e1b7,
"orange pink": 0xff526fff,
"tea green": 0xffa3f8bd,
"very light brown": 0xff83b6d3,
"egg shell": 0xffc4fcff,
"eggplant purple": 0xff410543,
"powder pink": 0xffd0b2ff,
"reddish grey": 0xff707599,
"baby shit brown": 0xff0d90ad,
"liliac": 0xfffd8ec4,
"stormy blue": 0xff9c7b50,
"ugly brown": 0xff03717d,
"custard": 0xff78fdff,
"darkish pink": 0xff7d46da,
"deep brown": 0xff000241,
"greenish beige": 0xff79d1c9,
"manilla": 0xff86faff,
"off blue": 0xffae8456,
"battleship grey": 0xff857c6b,
"browny green": 0xff0a6c6f,
"bruise": 0xff71407e,
"kelley green": 0xff379300,
"sickly yellow": 0xff29e4d0,
"sunny yellow": 0xff17f9ff,
"azul": 0xffec5d1d,
"darkgreen": 0xff074905,
"green/yellow": 0xff08ceb5,
"lichen": 0xff7bb68f,
"light light green": 0xffb0ffc8,
"pale gold": 0xff6cdefd,
"sun yellow": 0xff22dfff,
"tan green": 0xff70bea9,
"burple": 0xffe33268,
"butterscotch": 0xff47b1fd,
"toupe": 0xff7dacc7,
"dark cream": 0xff9af3ff,
"indian red": 0xff040e85,
"light lavendar": 0xfffec0ef,
"poison green": 0xff14fd40,
"baby puke green": 0xff06c4b6,
"bright yellow green": 0xff00ff9d,
"charcoal grey": 0xff42413c,
"squash": 0xff15abf2,
"cinnamon": 0xff064fac,
"light pea green": 0xff82fec4,
"radioactive green": 0xff1ffa2c,
"raw sienna": 0xff00629a,
"baby purple": 0xfff79bca,
"cocoa": 0xff425f87,
"light royal blue": 0xfffe2e3a,
"orangeish": 0xff498dfd,
"rust brown": 0xff03318b,
"sand brown": 0xff60a5cb,
"swamp": 0xff398369,
"tealish green": 0xff73dc0c,
"burnt siena": 0xff0352b7,
"camo": 0xff4e8f7f,
"dusk blue": 0xff8d5326,
"fern": 0xff50a963,
"old rose": 0xff897fc8,
"pale light green": 0xff99fcb1,
"peachy pink": 0xff8a9aff,
"rosy pink": 0xff8e68f6,
"light bluish green": 0xffa8fd76,
"light bright green": 0xff5cfe53,
"light neon green": 0xff54fd4e,
"light seafoam": 0xffbffea0,
"tiffany blue": 0xffdaf27b,
"washed out green": 0xffa6f5bc,
"browny orange": 0xff026bca,
"nice blue": 0xffb07a10,
"sapphire": 0xffab3821,
"greyish teal": 0xff919f71,
"orangey yellow": 0xff15b9fd,
"parchment": 0xffaffcfe,
"straw": 0xff79f6fc,
"very dark brown": 0xff00021d,
"terracota": 0xff4368cb,
"ugly blue": 0xff8a6631,
"clear blue": 0xfffd7a24,
"creme": 0xffb6ffff,
"foam green": 0xffa9fd90,
"grey/green": 0xff7da186,
"light gold": 0xff5cdcfd,
"seafoam blue": 0xffb6d178,
"topaz": 0xffafbb13,
"violet pink": 0xfffc5ffb,
"wintergreen": 0xff86f920,
"yellow tan": 0xff6ee3ff,
"dark fuchsia": 0xff59079d,
"indigo blue": 0xffb1183a,
"light yellowish green": 0xff89ffc2,
"pale magenta": 0xffad67d7,
"rich purple": 0xff580072,
"sunflower yellow": 0xff03daff,
"green/blue": 0xff8dc001,
"leather": 0xff3474ac,
"racing green": 0xff004601,
"vivid purple": 0xfffa0099,
"dark royal blue": 0xff6f0602,
"hazel": 0xff18768e,
"muted pink": 0xff8f76d1,
"booger green": 0xff03b496,
"canary": 0xff63fffd,
"cool grey": 0xffa6a395,
"dark taupe": 0xff4e687f,
"darkish purple": 0xff731975,
"true green": 0xff049408,
"coral pink": 0xff6361ff,
"dark sage": 0xff568559,
"dark slate blue": 0xff614721,
"flat blue": 0xffa8733c,
"mushroom": 0xff889eba,
"rich blue": 0xfff91b02,
"dirty purple": 0xff654a73,
"greenblue": 0xff8bc423,
"icky green": 0xff22ae8f,
"light khaki": 0xffa2f2e6,
"warm blue": 0xffdb574b,
"dark hot pink": 0xff6601d9,
"deep sea blue": 0xff825401,
"carmine": 0xff16029d,
"dark yellow green": 0xff028f72,
"pale peach": 0xffade5ff,
"plum purple": 0xff50054e,
"golden rod": 0xff08bcf9,
"neon red": 0xff3a07ff,
"old pink": 0xff8679c7,
"very pale blue": 0xfffeffd6,
"blood orange": 0xff034bfe,
"grapefruit": 0xff5659fd,
"sand yellow": 0xff66e1fc,
"clay brown": 0xff3d71b2,
"dark blue grey": 0xff4d3b1f,
"flat green": 0xff4c9d69,
"light green blue": 0xffa2fc56,
"warm pink": 0xff8155fb,
"dodger blue": 0xfffc823e,
"gross green": 0xff16bfa0,
"ice": 0xfffaffd6,
"metallic blue": 0xff8e734f,
"pale salmon": 0xff9ab1ff,
"sap green": 0xff158b5c,
"algae": 0xff68ac54,
"bluey grey": 0xffb0a089,
"greeny grey": 0xff7aa07e,
"highlighter green": 0xff06fc1b,
"light light blue": 0xfffbffca,
"light mint": 0xffbbffb6,
"raw umber": 0xff095ea7,
"vivid blue": 0xffff2e15,
"deep lavender": 0xffb75e8d,
"dull teal": 0xff8f9e5f,
"light greenish blue": 0xffb4f763,
"mud green": 0xff026660,
"pinky": 0xffaa86fc,
"red wine": 0xff34008c,
"shit green": 0xff008075,
"tan brown": 0xff4c7eab,
"darkblue": 0xff640703,
"rosa": 0xffa486fe,
"lipstick": 0xff4e17d5,
"pale mauve": 0xfffcd0fe,
"claret": 0xff180068,
"dandelion": 0xff08dffe,
"orangered": 0xff0f42fe,
"poop green": 0xff007c6f,
"ruby": 0xff4701ca,
"dark": 0xff31241b,
"greenish turquoise": 0xffb0fb00,
"pastel red": 0xff5658db,
"piss yellow": 0xff18d6dd,
"bright cyan": 0xfffefd41,
"dark coral": 0xff4e52cf,
"algae green": 0xff6fc321,
"darkish red": 0xff0803a9,
"reddy brown": 0xff05106e,
"blush pink": 0xff8c82fe,
"camouflage green": 0xff13614b,
"lawn green": 0xff09a44d,
"putty": 0xff8aaebe,
"vibrant blue": 0xfff83903,
"dark sand": 0xff598fa8,
"purple/blue": 0xffd0215d,
"saffron": 0xff09b2fe,
"twilight": 0xff8b514e,
"warm brown": 0xff024e96,
"bluegrey": 0xffb2a385,
"bubble gum pink": 0xffaf69ff,
"duck egg blue": 0xfff4fbc3,
"greenish cyan": 0xffb7fe2a,
"petrol": 0xff6a5f00,
"royal": 0xff93170c,
"butter": 0xff81ffff,
"dusty orange": 0xff3a83f0,
"off yellow": 0xff3ff3f1,
"pale olive green": 0xff7bd2b1,
"orangish": 0xff4a82fc,
"leaf": 0xff34aa71,
"light blue grey": 0xffe2c9b7,
"dried blood": 0xff01014b,
"lightish purple": 0xffe652a5,
"rusty red": 0xff0d2faf,
"lavender blue": 0xfff8888b,
"light grass green": 0xff64f79a,
"light mint green": 0xffb2fba6,
"sunflower": 0xff12c5ff,
"velvet": 0xff510875,
"brick orange": 0xff094ac1,
"lightish red": 0xff4a2ffe,
"pure blue": 0xffe20302,
"twilight blue": 0xff7a430a,
"violet red": 0xff5500a5,
"yellowy brown": 0xff0c8bae,
"carnation": 0xff8f79fd,
"muddy yellow": 0xff05acbf,
"dark seafoam green": 0xff76af3e,
"deep rose": 0xff6747c7,
"dusty red": 0xff4e48b9,
"grey/blue": 0xff8e7d64,
"lemon lime": 0xff28febf,
"purple/pink": 0xffde25d7,
"brown yellow": 0xff0597b2,
"purple brown": 0xff3f3a67,
"wisteria": 0xffc27da8,
"banana yellow": 0xff4bfefa,
"lipstick red": 0xff2f02c0,
"water blue": 0xffcc870e,
"brown grey": 0xff68848d,
"vibrant purple": 0xffde03ad,
"baby green": 0xff9eff8c,
"barf green": 0xff02ac94,
"eggshell blue": 0xfff7ffc4,
"sandy yellow": 0xff73eefd,
"cool green": 0xff64b833,
"pale": 0xffd0f9ff,
"blue/grey": 0xffa38d75,
"hot magenta": 0xffc904f5,
"greyblue": 0xffb5a177,
"purpley": 0xffe45687,
"baby shit green": 0xff179788,
"brownish pink": 0xff797ec2,
"dark aquamarine": 0xff717301,
"diarrhea": 0xff03839f,
"light mustard": 0xff60d5f7,
"pale sky blue": 0xfffef6bd,
"turtle green": 0xff4fb875,
"bright olive": 0xff04bb9c,
"dark grey blue": 0xff5b4629,
"greeny brown": 0xff066069,
"lemon green": 0xff02f8ad,
"light periwinkle": 0xfffcc6c1,
"seaweed green": 0xff6bad35,
"sunshine yellow": 0xff37fdff,
"ugly purple": 0xffa042a4,
"medium pink": 0xff9661f3,
"puke brown": 0xff067794,
"very light pink": 0xfff2f4ff,
"viridian": 0xff67911e,
"bile": 0xff06c3b5,
"faded yellow": 0xff7ffffe,
"very pale green": 0xffbcfdcf,
"vibrant green": 0xff08dd0a,
"bright lime": 0xff05fd87,
"spearmint": 0xff76f81e,
"light aquamarine": 0xffc7fd7b,
"light sage": 0xffacecbc,
"yellowgreen": 0xff0ff9bb,
"baby poo": 0xff0490ab,
"dark seafoam": 0xff7ab51f,
"deep teal": 0xff5a5500,
"heather": 0xffac84a4,
"rust orange": 0xff0855c4,
"dirty blue": 0xff9d823f,
"fern green": 0xff448d54,
"bright lilac": 0xfffb5ec9,
"weird green": 0xff7fe53a,
"peacock blue": 0xff956701,
"avocado green": 0xff22a987,
"faded orange": 0xff4d94f0,
"grape purple": 0xff51145d,
"hot green": 0xff29ff25,
"lime yellow": 0xff1dfed0,
"mango": 0xff2ba6ff,
"shamrock": 0xff4cb401,
"bubblegum": 0xffb56cff,
"purplish brown": 0xff47426b,
"vomit yellow": 0xff0cc1c7,
"pale cyan": 0xfffaffb7,
"key lime": 0xff6effae,
"tomato red": 0xff012dec,
"lightgreen": 0xff7bff76,
"merlot": 0xff390073,
"night blue": 0xff480304,
"purpleish pink": 0xffc84edf,
"apple": 0xff3ccb6e,
"baby poop green": 0xff05988f,
"green apple": 0xff1fdc5e,
"heliotrope": 0xfff54fd9,
"yellow/green": 0xff3dfdc8,
"almost black": 0xff0d0d07,
"cool blue": 0xffb88449,
"leafy green": 0xff3bb751,
"mustard brown": 0xff047eac,
"dusk": 0xff81544e,
"dull brown": 0xff4b6e87,
"frog green": 0xff08bc58,
"vivid green": 0xff10ef2f,
"bright light green": 0xff54fe2d,
"fluro green": 0xff02ff0a,
"kiwi": 0xff43ef9c,
"seaweed": 0xff7bd118,
"navy green": 0xff0a5335,
"ultramarine blue": 0xffdb0518,
"iris": 0xffc45862,
"pastel orange": 0xff4f96ff,
"yellowish orange": 0xff0fabff,
"perrywinkle": 0xffe78c8f,
"tealish": 0xffa8bc24,
"dark plum": 0xff2c013f,
"pear": 0xff5ff8cb,
"pinkish orange": 0xff4c72ff,
"midnight purple": 0xff370128,
"light urple": 0xfff66fb3,
"dark mint": 0xff72c048,
"greenish tan": 0xff7acbbc,
"light burgundy": 0xff5b41a8,
"turquoise blue": 0xffc4b106,
"ugly pink": 0xff8475cd,
"sandy": 0xff7adaf1,
"electric pink": 0xff9004ff,
"muted purple": 0xff875b80,
"mid green": 0xff47a750,
"greyish": 0xff95a4a8,
"neon yellow": 0xff04ffcf,
"banana": 0xff7effff,
"carnation pink": 0xffa77fff,
"tomato": 0xff2640ef,
"sea": 0xff92993c,
"muddy brown": 0xff066888,
"turquoise green": 0xff89f404,
"buff": 0xff9ef6fe,
"fawn": 0xff7bafcf,
"muted blue": 0xff9f713b,
"pale rose": 0xffc5c1fd,
"dark mint green": 0xff73c020,
"amethyst": 0xffc05f9b,
"blue/green": 0xff8e9b0f,
"chestnut": 0xff022874,
"sick green": 0xff2cb99d,
"pea": 0xff20bfa4,
"rusty orange": 0xff0959cd,
"stone": 0xff87a5ad,
"rose red": 0xff3c01be,
"pale aqua": 0xffebffb8,
"deep orange": 0xff014ddc,
"earth": 0xff3e65a2,
"mossy green": 0xff278b63,
"grassy green": 0xff039c41,
"pale lime green": 0xff65ffb1,
"light grey blue": 0xffd4bc9d,
"pale grey": 0xfffefdfd,
"asparagus": 0xff56ab77,
"blueberry": 0xff964146,
"purple red": 0xff470199,
"pale lime": 0xff73fdbe,
"greenish teal": 0xff84bf32,
"caramel": 0xff096faf,
"deep magenta": 0xff5c02a0,
"light peach": 0xffb1d8ff,
"milk chocolate": 0xff1e4e7f,
"ocher": 0xff0c9bbf,
"off green": 0xff53a36b,
"purply pink": 0xffe675f0,
"lightblue": 0xfff6c87b,
"dusky blue": 0xff945f47,
"golden": 0xff03bff5,
"light beige": 0xffb6feff,
"butter yellow": 0xff74fdff,
"dusky purple": 0xff7b5b89,
"french blue": 0xffad6b43,
"ugly yellow": 0xff01c1d0,
"greeny yellow": 0xff08f8c6,
"orangish red": 0xff0536f4,
"shamrock green": 0xff4dc102,
"orangish brown": 0xff035fb2,
"tree green": 0xff197e2a,
"deep violet": 0xff480649,
"gunmetal": 0xff676253,
"blue/purple": 0xffef065a,
"cherry": 0xff3402cf,
"sandy brown": 0xff61a6c4,
"warm grey": 0xff848a97,
"dark indigo": 0xff54091f,
"midnight": 0xff2d0103,
"bluey green": 0xff79b12b,
"grey pink": 0xff9b90c3,
"soft purple": 0xffb56fa6,
"blood": 0xff010077,
"brown red": 0xff052b92,
"medium grey": 0xff7c7f7d,
"berry": 0xff4b0f99,
"poo": 0xff03738f,
"purpley pink": 0xffb93cc8,
"light salmon": 0xff93a9fe,
"snot": 0xff0dbbac,
"easter purple": 0xfffe71c0,
"light yellow green": 0xff7ffdcc,
"dark navy blue": 0xff2e0200,
"drab": 0xff448382,
"light rose": 0xffcbc5ff,
"rouge": 0xff3912ab,
"purplish red": 0xff4b05b0,
"slime green": 0xff04cc99,
"baby poop": 0xff007c93,
"irish green": 0xff299501,
"pink/purple": 0xffe71def,
"dark navy": 0xff350400,
"greeny blue": 0xff95b342,
"light plum": 0xff83579d,
"pinkish grey": 0xffa9acc8,
"dirty orange": 0xff0676c8,
"rust red": 0xff0427aa,
"pale lilac": 0xffffcbe4,
"orangey red": 0xff2442fa,
"primary blue": 0xfff90408,
"kermit green": 0xff00b25c,
"brownish purple": 0xff4e4276,
"murky green": 0xff0e7a6c,
"wheat": 0xff7eddfb,
"very dark purple": 0xff34012a,
"bottle green": 0xff054a04,
"watermelon": 0xff5946fd,
"deep sky blue": 0xfff8750d,
"fire engine red": 0xff0200fe,
"yellow ochre": 0xff069dcb,
"pumpkin orange": 0xff077dfb,
"pale olive": 0xff81ccb9,
"light lilac": 0xffffc8ed,
"lightish green": 0xff60e161,
"carolina blue": 0xfffeb88a,
"mulberry": 0xff4e0a92,
"shocking pink": 0xffa202fe,
"auburn": 0xff01309a,
"bright lime green": 0xff08fe65,
"celadon": 0xffb7fdbe,
"pinkish brown": 0xff6172b1,
"poo brown": 0xff015f88,
"bright sky blue": 0xfffecc02,
"celery": 0xff95fdc1,
"dirt brown": 0xff396583,
"strawberry": 0xff4329fb,
"dark lime": 0xff01b784,
"copper": 0xff2563b6,
"medium brown": 0xff12517f,
"muted green": 0xff52a05f,
"robin's egg": 0xfffded6d,
"bright aqua": 0xffeaf90b,
"bright lavender": 0xffff60c7,
"ivory": 0xffcbffff,
"very light purple": 0xfffccef6,
"light navy": 0xff845015,
"pink red": 0xff4f05f5,
"olive brown": 0xff035464,
"poop brown": 0xff01597a,
"mustard green": 0xff04b5a8,
"ocean green": 0xff73993d,
"very dark blue": 0xff330100,
"dusty green": 0xff73a976,
"light navy blue": 0xff885a2e,
"minty green": 0xff7df70b,
"adobe": 0xff486cbd,
"barney": 0xffb81dac,
"jade green": 0xff6aaf2b,
"bright light blue": 0xfffdf726,
"light lime": 0xff6cfdae,
"dark khaki": 0xff558f9b,
"orange yellow": 0xff01adff,
"ocre": 0xff049cc6,
"maize": 0xff54d0f4,
"faded pink": 0xffac9dde,
"british racing green": 0xff0d4805,
"sandstone": 0xff74aec9,
"mud brown": 0xff0f4660,
"light sea green": 0xffb0f698,
"robin egg blue": 0xfffef18a,
"aqua marine": 0xffbbe82e,
"dark sea green": 0xff5d8711,
"soft pink": 0xffc0b0fd,
"orangey brown": 0xff0260b1,
"cherry red": 0xff2a02f7,
"burnt yellow": 0xff09abd5,
"brownish grey": 0xff5f7786,
"camel": 0xff599fc6,
"purplish grey": 0xff7f687a,
"marine": 0xff602e04,
"greyish pink": 0xff948dc8,
"pale turquoise": 0xffd5fba5,
"pastel yellow": 0xff71feff,
"bluey purple": 0xffc74162,
"canary yellow": 0xff40feff,
"faded red": 0xff4e49d3,
"sepia": 0xff2b5e98,
"coffee": 0xff4c81a6,
"bright magenta": 0xffe808ff,
"mocha": 0xff51769d,
"ecru": 0xffcafffe,
"purpleish": 0xff8d5698,
"cranberry": 0xff3a009e,
"darkish green": 0xff377c28,
"brown orange": 0xff0269b9,
"dusky rose": 0xff7368ba,
"melon": 0xff5578ff,
"sickly green": 0xff1cb294,
"silver": 0xffc7c9c5,
"purply blue": 0xffee1a66,
"purpleish blue": 0xffef4061,
"hospital green": 0xffaae59b,
"shit brown": 0xff04587b,
"mid blue": 0xffb36a27,
"amber": 0xff08b3fe,
"easter green": 0xff7efd8c,
"soft blue": 0xffea8864,
"cerulean blue": 0xffee6e05,
"golden brown": 0xff017ab2,
"bright turquoise": 0xfff9fe0f,
"red pink": 0xff552afa,
"red purple": 0xff470782,
"greyish brown": 0xff4f6a7a,
"vermillion": 0xff0c32f4,
"russet": 0xff0539a1,
"steel grey": 0xff8a826f,
"lighter purple": 0xfff45aa5,
"bright violet": 0xfffd0aad,
"prussian blue": 0xff774500,
"slate green": 0xff6d8d65,
"dirty pink": 0xff807bca,
"dark blue green": 0xff495200,
"pine": 0xff345d2b,
"yellowy green": 0xff28f1bf,
"dark gold": 0xff1094b5,
"bluish": 0xffbb7629,
"darkish blue": 0xff824101,
"dull red": 0xff3f3fbb,
"pinky red": 0xff4726fc,
"bronze": 0xff0079a8,
"pale teal": 0xffb2cb82,
"military green": 0xff3e7c66,
"barbie pink": 0xffa546fe,
"bubblegum pink": 0xffcc83fe,
"pea soup green": 0xff17a694,
"dark mustard": 0xff0589a8,
"shit": 0xff005f7f,
"medium purple": 0xffa2439e,
"very dark green": 0xff032e06,
"dirt": 0xff456e8a,
"dusky pink": 0xff8b7acc,
"red violet": 0xff68019e,
"lemon yellow": 0xff38fffd,
"pistachio": 0xff8bfac0,
"dull yellow": 0xff5bdcee,
"dark lime green": 0xff01bd7e,
"denim blue": 0xff925b3b,
"teal blue": 0xff9f8801,
"lightish blue": 0xfffd7a3d,
"purpley blue": 0xffe7345f,
"light indigo": 0xffcf5a6d,
"swamp green": 0xff008574,
"brown green": 0xff116c70,
"dark maroon": 0xff08003c,
"hot purple": 0xfff500cb,
"dark forest green": 0xff042d00,
"faded blue": 0xffbb8c65,
"drab green": 0xff519574,
"light lime green": 0xff66ffb9,
"snot green": 0xff00c19d,
"yellowish": 0xff66eefa,
"light blue green": 0xffb3fb7e,
"bordeaux": 0xff2c007b,
"light mauve": 0xffa192c2,
"ocean": 0xff927b01,
"marigold": 0xff06c0fc,
"muddy green": 0xff327465,
"dull orange": 0xff3b86d8,
"steel": 0xff958573,
"electric purple": 0xffff23aa,
"fluorescent green": 0xff08ff08,
"yellowish brown": 0xff017a9b,
"blush": 0xff8e9ef2,
"soft green": 0xff76c26f,
"bright orange": 0xff005bff,
"lemon": 0xff52fffd,
"purple grey": 0xff856f86,
"acid green": 0xff09fe8f,
"pale lavender": 0xfffecfee,
"violet blue": 0xffc90a51,
"light forest green": 0xff53914f,
"burnt red": 0xff05239f,
"khaki green": 0xff398672,
"cerise": 0xff620cde,
"faded purple": 0xff996e91,
"apricot": 0xff6db1ff,
"dark olive green": 0xff034d3c,
"grey brown": 0xff53707f,
"green grey": 0xff6f9277,
"true blue": 0xffcc0f01,
"pale violet": 0xfffaaece,
"periwinkle blue": 0xfffb998f,
"light sky blue": 0xfffffcc6,
"blurple": 0xffcc3955,
"green brown": 0xff034e54,
"bluegreen": 0xff797a01,
"bright teal": 0xffc6f901,
"brownish yellow": 0xff03b0c9,
"pea soup": 0xff019992,
"forest": 0xff09550b,
"barney purple": 0xff9804a0,
"ultramarine": 0xffb10020,
"purplish": 0xff8c5694,
"puke yellow": 0xff0ebec2,
"bluish grey": 0xff978b74,
"dark periwinkle": 0xffd15f66,
"dark lilac": 0xffa56d9c,
"reddish": 0xff4042c4,
"light maroon": 0xff5748a2,
"dusty purple": 0xff875f82,
"terra cotta": 0xff3b64c9,
"avocado": 0xff34b190,
"marine blue": 0xff6a3801,
"teal green": 0xff6fa325,
"slate grey": 0xff6d6559,
"lighter green": 0xff63fd75,
"electric green": 0xff0dfc21,
"dusty blue": 0xffad865a,
"golden yellow": 0xff15c6fe,
"bright yellow": 0xff01fdff,
"light lavender": 0xfffec5df,
"umber": 0xff0064b2,
"poop": 0xff005e7f,
"dark peach": 0xff5d7ede,
"jungle green": 0xff438204,
"eggshell": 0xffd4ffff,
"denim": 0xff8c633b,
"yellow brown": 0xff0094b7,
"dull purple": 0xff7e5984,
"chocolate brown": 0xff001941,
"wine red": 0xff23037b,
"neon blue": 0xffffd904,
"dirty green": 0xff2c7e66,
"light tan": 0xffaceefb,
"ice blue": 0xfffeffd7,
"cadet blue": 0xff96744e,
"dark mauve": 0xff624c87,
"very light blue": 0xffffffd5,
"grey purple": 0xff8c6d82,
"pastel pink": 0xffcdbaff,
"very light green": 0xffbdffd1,
"dark sky blue": 0xffe48e44,
"evergreen": 0xff2a4705,
"dull pink": 0xff9d86d5,
"aubergine": 0xff34073d,
"mahogany": 0xff00014a,
"reddish orange": 0xff1c48f8,
"deep green": 0xff0f5902,
"vomit green": 0xff03a289,
"purple pink": 0xffd83fe0,
"dusty pink": 0xff948ad5,
"faded green": 0xff74b27b,
"camo green": 0xff256552,
"pinky purple": 0xffbe4cc9,
"pink purple": 0xffda4bdb,
"brownish red": 0xff23369e,
"dark rose": 0xff5d48b5,
"mud": 0xff125c73,
"brownish": 0xff576d9c,
"emerald green": 0xff1e8f02,
"pale brown": 0xff6e91b1,
"dull blue": 0xff9c7549,
"burnt umber": 0xff0e45a0,
"medium green": 0xff48ad39,
"clay": 0xff506ab6,
"light aqua": 0xffdbff8c,
"light olive green": 0xff5cbea4,
"brownish orange": 0xff2377cb,
"dark aqua": 0xff6b6905,
"purplish pink": 0xffae5dce,
"dark salmon": 0xff535ac8,
"greenish grey": 0xff8dae96,
"jade": 0xff74a71f,
"ugly green": 0xff03977a,
"dark beige": 0xff6293ac,
"emerald": 0xff49a001,
"pale red": 0xff4d54d9,
"light magenta": 0xfff75ffa,
"sky": 0xfffcca82,
"light cyan": 0xfffcffac,
"yellow orange": 0xff01b0fc,
"reddish purple": 0xff510991,
"reddish pink": 0xff542cfe,
"orchid": 0xffc475c8,
"dirty yellow": 0xff0ac5cd,
"orange red": 0xff1e41fd,
"deep red": 0xff00029a,
"orange brown": 0xff0064be,
"cobalt blue": 0xffa70a03,
"neon pink": 0xff9a01fe,
"rose pink": 0xff9a87f7,
"greyish purple": 0xff917188,
"raspberry": 0xff4901b0,
"aqua green": 0xff93e112,
"salmon pink": 0xff7c7bfe,
"tangerine": 0xff0894ff,
"brownish green": 0xff096e6a,
"red brown": 0xff162e8b,
"greenish brown": 0xff126169,
"pumpkin": 0xff0177e1,
"pine green": 0xff1e480a,
"charcoal": 0xff373834,
"baby pink": 0xffceb7ff,
"cornflower": 0xfff7796a,
"blue violet": 0xffe9065d,
"chocolate": 0xff021c3d,
"greyish green": 0xff7da682,
"scarlet": 0xff1901be,
"green yellow": 0xff27ffc9,
"dark olive": 0xff023e37,
"sienna": 0xff1e56a9,
"pastel purple": 0xffffa0ca,
"terracotta": 0xff4166ca,
"aqua blue": 0xffe9d802,
"sage green": 0xff78b388,
"blood red": 0xff020098,
"deep pink": 0xff6201cb,
"grass": 0xff2dac5c,
"moss": 0xff589976,
"pastel blue": 0xfffebfa2,
"bluish green": 0xff74a610,
"green blue": 0xff8bb406,
"dark tan": 0xff4a88af,
"greenish blue": 0xff878b0b,
"pale orange": 0xff56a7ff,
"vomit": 0xff15a4a2,
"forrest green": 0xff064415,
"dark lavender": 0xff986785,
"dark violet": 0xff3f0134,
"purple blue": 0xffe92d63,
"dark cyan": 0xff8a880a,
"olive drab": 0xff32766f,
"pinkish": 0xff7e6ad4,
"cobalt": 0xff8f481e,
"neon purple": 0xfffe13bc,
"light turquoise": 0xffccf47e,
"apple green": 0xff26cd76,
"dull green": 0xff62a674,
"wine": 0xff3f0180,
"powder blue": 0xfffcd1b1,
"off white": 0xffe4ffff,
"electric blue": 0xffff5206,
"dark turquoise": 0xff5a5c04,
"blue purple": 0xffce2957,
"azure": 0xfff39a06,
"bright red": 0xff0d00ff,
"pinkish red": 0xff450cf1,
"cornflower blue": 0xffd77051,
"light olive": 0xff69bfac,
"grape": 0xff61346c,
"greyish blue": 0xff9d815e,
"purplish blue": 0xfff91e60,
"yellowish green": 0xff16ddb0,
"greenish yellow": 0xff02fdcd,
"medium blue": 0xffbb6f2c,
"dusty rose": 0xff7a73c0,
"light violet": 0xfffcb4d6,
"midnight blue": 0xff350002,
"bluish purple": 0xffe73b70,
"red orange": 0xff063cfd,
"dark magenta": 0xff560096,
"greenish": 0xff68a340,
"ocean blue": 0xff9c7103,
"coral": 0xff505afc,
"cream": 0xffc2ffff,
"reddish brown": 0xff0a2b7f,
"burnt sienna": 0xff0f4eb0,
"brick": 0xff2336a0,
"sage": 0xff73ae87,
"grey green": 0xff739b78,
"white": 0xffffffff,
"robin's egg blue": 0xfff9ef98,
"moss green": 0xff388b65,
"steel blue": 0xff9a7d5a,
"eggplant": 0xff350838,
"light yellow": 0xff7afeff,
"leaf green": 0xff04a95c,
"light grey": 0xffd6dcd8,
"puke": 0xff02a5a5,
"pinkish purple": 0xffd748d6,
"sea blue": 0xff957404,
"pale purple": 0xffd490b7,
"slate blue": 0xff997c5b,
"blue grey": 0xff8e7c60,
"hunter green": 0xff08400b,
"fuchsia": 0xffd90ded,
"crimson": 0xff0f008c,
"pale yellow": 0xff84ffff,
"ochre": 0xff0590bf,
"mustard yellow": 0xff0abdd2,
"light red": 0xff4c47ff,
"cerulean": 0xffd18504,
"pale pink": 0xffdccfff,
"deep blue": 0xff730204,
"rust": 0xff093ca8,
"light teal": 0xffc1e490,
"slate": 0xff726551,
"goldenrod": 0xff05c2fa,
"dark yellow": 0xff0ab6d5,
"dark grey": 0xff373736,
"army green": 0xff165d4b,
"grey blue": 0xffa48b6b,
"seafoam": 0xffadf980,
"puce": 0xff527ea5,
"spring green": 0xff71f9a9,
"dark orange": 0xff0251c6,
"sand": 0xff76cae2,
"pastel green": 0xff9dffb0,
"mint": 0xffb0fe9f,
"light orange": 0xff48aafd,
"bright pink": 0xffb101fe,
"chartreuse": 0xff0af8c1,
"deep purple": 0xff3f0136,
"dark brown": 0xff021c34,
"taupe": 0xff81a2b9,
"pea green": 0xff12ab8e,
"puke green": 0xff07ae9a,
"kelly green": 0xff2eab02,
"seafoam green": 0xffabf97a,
"blue green": 0xff6d7e13,
"khaki": 0xff62a6aa,
"burgundy": 0xff230061,
"dark teal": 0xff4e4d01,
"brick red": 0xff02148f,
"royal purple": 0xff6e004b,
"plum": 0xff410f58,
"mint green": 0xff9fff8f,
"gold": 0xff0cb4db,
"baby blue": 0xfffecfa2,
"yellow green": 0xff2dfbc0,
"bright purple": 0xfffd03be,
"dark red": 0xff000084,
"pale blue": 0xfffefed0,
"grass green": 0xff0b9b3f,
"navy": 0xff3e1501,
"aquamarine": 0xffb2d804,
"burnt orange": 0xff014ec0,
"neon green": 0xff0cff0c,
"bright blue": 0xfffc6501,
"rose": 0xff7562cf,
"light pink": 0xffdfd1ff,
"mustard": 0xff01b3ce,
"indigo": 0xff820238,
"lime": 0xff32ffaa,
"sea green": 0xffa1fc53,
"periwinkle": 0xfffe828e,
"dark pink": 0xff6b41cb,
"olive green": 0xff047a67,
"peach": 0xff7cb0ff,
"pale green": 0xffb5fdc7,
"light brown": 0xff5081ad,
"hot pink": 0xff8d02ff,
"black": 0xff000000,
"lilac": 0xfffda2ce,
"navy blue": 0xff461100,
"royal blue": 0xffaa0405,
"beige": 0xffa6dae6,
"salmon": 0xff6c79ff,
"olive": 0xff0e756e,
"maroon": 0xff210065,
"bright green": 0xff07ff01,
"dark purple": 0xff3e0635,
"mauve": 0xff8171ae,
"forest green": 0xff0c4706,
"aqua": 0xffc9ea13,
"cyan": 0xffffff00,
"tan": 0xff6fb2d1,
"dark blue": 0xff5b0300,
"lavender": 0xffef9fc7,
"turquoise": 0xffacc206,
"dark green": 0xff003503,
"violet": 0xffea0e9a,
"light purple": 0xfff677bf,
"lime green": 0xff05fe89,
"grey": 0xff919592,
"sky blue": 0xfffdbb75,
"yellow": 0xff14ffff,
"magenta": 0xff7800c2,
"light green": 0xff7bf996,
"orange": 0xff0673f9,
"teal": 0xff869302,
"light blue": 0xfffcd095,
"red": 0xff0000e5,
"brown": 0xff003765,
"pink": 0xffc081ff,
"blue": 0xffdf4303,
"green": 0xff1ab015,
"purple": 0xff9c1e7e,
}
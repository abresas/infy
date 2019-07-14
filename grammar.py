from parsimonious.grammar import Grammar

grammar = Grammar(
    r"""
    doc = multiline / line
    multiline = line "\n" doc
    line = (assign eol) / (calculate eol) / (text calculate eol) / eol
    assign = ws? var ws? "=" ws? expr
    text = !calculate (ws / non_ws) text?
    calculate = change_unit / operation / lit
    change_unit = (operation / lit) in_unit
    operation = add / sub / mul / div
    expr = operation / val
    add = factor ws? "+" ws? expr
    sub = factor ws? "-" ws? expr
    factor = mul / div / val
    mul = val ws? "*" ws? factor
    div = val ws? "/" ws? factor
    val = var / lit
    var = ~"[a-zA-Z][a-zA-Z0-9_]+"
    lit = numeric (ws units)?
    numeric = perc / int / float
    number = int / float
    int = ~"[0-9]+"
    float = ~"[0-9]+.[0-9]+"
    perc = number ws? "%"
    in_unit = (ws "in" ws units)
    units = (unit ws units) / per_unit / unit
    per_unit = (unit ws "per" ws units) / (unit ws? "/" ws? units) / (ws? "per" ws units)
    unit = scale? (angle / solid_angle / neper / information / length / mass / time / temperature / area / volume / liquid_volume / other_volume / short_unit) "s"?
    scale = "deci" / "centi" / "milli" / "micro" / "nano" / "pico" / "kilo" / "mega" / "giga" / "tera"
    short_unit = "ml" / "mL" / "m" / "s" / "h" / "g" / "k" / "l" / "L" / "b"
    currency = "dollar" / "usd" / "us dollar" / "euro" / "eur" / "pound sterling" / "pound" / "gbp" / "cad" / "jpy" / "yen" / "btc" / "bitcoin" / "ethereum" / "eth"
    angle = "radian" / turn / degree / arcminute / arcsecond / milliarcsecond / "grade"
    turn = "turn" / "revolution" / "cycle" / "circle"
    degree = "degree" / "deg" / "arcdeg" / "arcdegree" / "angular degree"
    arcminute = "arcminute" / "arcmin" / "arc minute" / "angular minute"
    arcsecond = "arcsecond" / "arcsec" / "arc second" / "angular second"
    milliarcsecond = "milliarcsecond" / "mas"
    solid_angle = steradian / square_degree
    steradian = "steradian" / "sr"
    square_degree = "square degree" / ("sq" ws? "deg")
    information = "bit" / "byte" / "baud" / "bps" / "Bd" / "octet"
    length = meter / angstrom / micron / fermi / light_year / astronomical_unit / parsec / nautical_mile / bohr / planck_length
    meter = "meter"
    angstrom = "angstrom"
    micron = "micron"
    fermi = "fermi"
    light_year = "light year"
    astronomical_unit = "astronomical unit"
    parsec = "parsec"
    nautical_mile = "nautical mile"
    bohr = "bohr"
    planck_length = "planck length"
    mass = gram / metric_ton / dalton / grain / gamma_mass / carat / planck_mass
    gram = "gram"
    metric_ton = "metric_ton"
    dalton = "dalton"
    grain = "grain"
    gamma_mass = "gamma mass"
    carat = "carat"
    planck_mass = "planck mass"
    time = second / minute / hour / day / week / fortnight / year / month/ decade / century / millenium / eon / shake / planck_time
    second = "second" / "sec"
    minute = "minute" / "min"
    hour = "hour"
    day = "day"
    week = "week"
    fortnight = "fortnight"
    year = "year"
    month = "month"
    decade = "decade"
    century = "century"
    millenium = "millenium"
    eon = "eon"
    shake = "shake"
    planck_time = "planck time"
    temperature = (("degree" / "deg") "s"?)? ("celsius" / "fahrenheit" / "kelvin")
    area = "are" / "barn" / "darcy" / "hectare" / "ha"
    volume = "liter" / "litre" / "cubic centimeter" / "lambda" / "λ" / "stere"
    liquid_volume = "pint" / "minim" / "fluid dram" / "fldr" / "fluidram" / "fluid ounce" / "floz" / "gill" / "gi" / "pt" / "fifth" / "quart" / "qt" / "gallon"
    other_volume = "teaspoon" / "tsp" / "tablespoon" / "tbsp" / "shot" / "US shot" / "cup" / "cp" / "liquid cup" / "US liquid cup" / "barrel" / "bbl" / "oil barrel" / "oil bbl" / "beer barrel" / "beer bbl"
    neper = "neper" / "bel"
    eol = ~"[^\n]*"
    non_ws = ~"\S+"
    ws = ~"[ \t]+"
    """
)


def find(node, target_type):
    if node.expr_name == target_type:
        return node
    for c in node.children:
        r = find(c, target_type)
        if r is not None:
            return r
    return None


def find_text(node, target_type):
    r = find(node, target_type)
    if r is None:
        return None
    return r.text

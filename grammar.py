from parsimonious.grammar import Grammar

grammar = Grammar(
    r"""
    doc = multiline / line
    multiline = line "\n" doc
    line = (assign eol) / (calculate eol) / (text calculate eol) / eol
    assign = ws? var ws? "=" ws? expr
    text = !calculate (ws / non_ws) text?
    calculate = operation / numeric
    operation = add / sub / mul / div
    expr = operation / val
    add = factor ws? "+" ws? expr
    sub = factor ws? "-" ws? expr
    factor = mul / div / val
    mul = val ws? "*" ws? factor
    div = val ws? "/" ws? factor
    val = var / numeric
    var = ~"[a-zA-Z][a-zA-Z0-9_]+"
    numeric = perc / int / float
    number = int / float
    int = ~"[0-9]+"
    float = ~"[0-9]+.[0-9]+"
    perc = number ws? "%"
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

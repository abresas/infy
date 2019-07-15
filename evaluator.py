from parsimonious.nodes import NodeVisitor
from grammar import find_text
from pint import UnitRegistry

ureg = UnitRegistry()
Q_ = ureg.Quantity


def same_dimension(l):
    unit = None
    for x in l:
        if x.__class__.__name__ == "Quantity" and str(x.units) != 'dimensionless':
            unit = str(x.units)
            break
    if unit is None:
        return l
    for i, x in enumerate(l):
        if x.__class__.__name__ == "Quantity":
            l[i] = x.to(unit)
        else:
            l[i] = Q_(x, unit)
    return l

class Evaluator(NodeVisitor):
    def __init__(self):
        self.variables = {}

    def eval(self, doc):
        return self.visit(doc)

    def set(self, key, val):
        self.variables[key] = val

    def get(self, key):
        return self.variables[key]

    def reset(self):
        self.variables = {}

    def visit_doc(self, node, visited_children):
        if type(visited_children[0]) == list:
            return visited_children[0]
        return visited_children

    def visit_multiline(self, node, visited_children):
        return [visited_children[0]] + visited_children[2]

    def visit_line(self, node, visited_children):
        return visited_children[0]

    def visit_assign(self, node, visited_children):
        var_name = find_text(node, "var")
        self.variables[var_name] = visited_children[5]
        return visited_children[5]

    def visit_calculate(self, node, visited_children):
        return visited_children[0]

    def visit_change_unit(self, node, visited_children):
        if visited_children[1]:
            return visited_children[0].to(visited_children[1].units)
        else:
            return visited_children[0]

    def visit_expr(self, node, visited_children):
        return visited_children[0]

    def visit_operation(self, node, visited_children):
        return visited_children[0]

    def visit_add(self, node, visited_children):
        visited_children = same_dimension(visited_children)
        return visited_children[0] + visited_children[4]

    def visit_sub(self, node, visited_children):
        visited_children = same_dimension(visited_children)
        return visited_children[0] - visited_children[4]

    def visit_mul(self, node, visited_children):
        visited_children = same_dimension(visited_children)
        return visited_children[0] * visited_children[4]

    def visit_div(self, node, visited_children):
        print('dividing', visited_children)
        visited_children = same_dimension(visited_children)
        print('samed', visited_children)
        res = visited_children[0] / visited_children[4]
        print('res', res)
        return res

    def visit_numeric(self, node, visited_children):
        return visited_children[0]

    def visit_var(self, node, visited_children):
        if node.text in self.variables:
            return self.variables[node.text]
        else:
            try:
                print("trying variable to dimension", node.text)
                return Q_(node.text)
            except Exception as e:
                print("to dimension failed with", e)
                return 0

    def visit_factor(self, node, visited_children):
        return visited_children[0]

    def visit_lit(self, node, visited_children):
        if visited_children[1] != 0:
            return visited_children[1] * visited_children[0]
        else:
            return visited_children[0]

    def visit_units(self, node, visited_children):
        if node.text.strip()[:3] == "per":
            text = "1 " + node.text
        else:
            text = node.text
        return Q_(text)

    def visit_in_unit(self, node, visited_children):
        return visited_children[3]

    def visit_val(self, node, visited_children):
        return visited_children[0]

    def visit_int(self, node, visited_children):
        return int(node.text)

    def visit_float(self, node, visited_children):
        return float(node.text)

    def visit_perc(self, node, visited_children):
        return visited_children[0] / 100.0

    def visit_eol(self, node, visited_children):
        return 0

    def generic_visit(self, node, visited_children):
        # returns the only non-zero value of the children
        value = 0
        for v in visited_children:
            if v != 0:
                if value != 0:
                    raise Exception("generic visit multiple non-zero values")
                value = v
        return value

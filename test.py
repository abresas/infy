from grammar import grammar, find_text, find_all_text
from evaluator import Evaluator, Q_

ev = Evaluator()

ast = grammar.parse("make")
assert(find_text(ast, "var") == "make")
assert(ev.eval(ast)[0] is None)

ast = grammar.parse("5")
assert(find_text(ast, "expr") == "5")
assert(ev.eval(ast)[0] == 5)

ast = grammar.parse("bar + 5")
assert(find_text(ast, "expr") == "bar + 5")
assert(find_text(ast, "add") == "bar + 5")
assert(find_text(ast, "var") == "bar")
assert(find_text(ast, "int") == "5")
ev.set("bar", 10)
assert(ev.eval(ast)[0] == 15)

ast = grammar.parse("foo = bar + 5")
assert(find_text(ast, "assign") == "foo = bar + 5")
assert(find_text(ast, "var") == "foo")
assert(find_text(ast, "expr") == "bar + 5")
ev.set("bar", 10)
assert(ev.eval(ast)[0] == 15)
assert(ev.get("foo") == 15)

ast = grammar.parse("rent = 400 euros per month")
assert(find_text(ast, "assign") == "rent = 400")
assert(find_text(ast, "expr") == "400")
assert(find_text(ast, "eol") == " euros per month")
assert(ev.eval(ast)[0] == 400)
assert(ev.get("rent") == 400)

ast = grammar.parse("bar + 5 per month")
assert(find_text(ast, "expr") == "bar + 5 per month")
ev.set("bar", 5)
assert(ev.eval(ast)[0] == Q_(10, '1 / month'))

ast = grammar.parse("my rent is bar + 5")
assert(find_all_text(ast, "expr")[3] == "bar + 5")
ev.reset()
ev.set("bar", 5)
assert(ev.eval(ast)[0] == 10)

ast = grammar.parse("my rent is bar + 400 euros per month")
assert(find_all_text(ast, "expr")[3] == "bar + 400")
assert(ev.eval(ast)[0] == 405)

ast = grammar.parse("5 + 2 * 10")
assert(find_text(ast, "add") == "5 + 2 * 10")
assert(find_text(ast, "mul") == "2 * 10")
assert(ev.eval(ast)[0] == 25)

ast = grammar.parse("5 - 2")
assert(ev.eval(ast)[0] == 3)

ast = grammar.parse("10 / 2")
assert(ev.eval(ast)[0] == 5)

ast = grammar.parse("5 * 2 + 10")
assert(find_text(ast, "add") == "5 * 2 + 10")
assert(find_text(ast, "mul").strip() == "5 * 2")
assert(ev.eval(ast)[0] == 20)

ast = grammar.parse("5 * 2 * 6 + 4 + 2 + 5 * 3 + 3")
assert(find_text(ast, "add") == "5 * 2 * 6 + 4 + 2 + 5 * 3 + 3")
assert(find_text(ast, "mul").strip() == "5 * 2 * 6")
assert(ev.eval(ast)[0] == 84)

ast = grammar.parse("""rent is 500 per month
    foo = 10
    l
    bar = foo + 5
    x
    sum = bar - foo / 2
    tax = sum*20%""")
ev.reset()
assert(ev.eval(ast) == [Q_(500, '1 / month'), 10, None, 15, None, 10.0, 2.0])
assert(ev.variables == {"foo": 10, "bar": 15, "sum": 10.0, "tax": 2.0})

ast = grammar.parse("5 liters in cubic centimeters")
epsilon = 0.0001
assert(5000 - ev.eval(ast)[0].magnitude < epsilon)

ast = grammar.parse("this year tax_rate = 20% of profits")
assert(find_text(ast, "text") == "this year")
assert(find_text(ast, "assign") == " tax_rate = 20%")
assert(find_text(ast, "eol") == " of profits")
ev.reset()
assert(ev.eval(ast) == [Q_(0.20)])
assert(ev.get('tax_rate') == Q_('0.20'))

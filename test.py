from grammar import grammar, find_text
from evaluator import Evaluator

ev = Evaluator()

ast = grammar.parse("make")
assert(find_text(ast, "eol") == "make")
assert(ev.eval(ast)[0] == 0)

ast = grammar.parse("5")
assert(find_text(ast, "calculate") == "5")
assert(ev.eval(ast)[0] == 5)

ast = grammar.parse("bar + 5")
assert(find_text(ast, "calculate") == "bar + 5")
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

ast = grammar.parse("rent = 400 per month")
assert(find_text(ast, "assign") == "rent = 400")
assert(find_text(ast, "expr") == "400")
assert(find_text(ast, "eol") == " per month")
assert(ev.eval(ast)[0] == 400)
assert(ev.get("rent") == 400)

ast = grammar.parse("bar + 5 per month")
assert(find_text(ast, "calculate") == "bar + 5")
ev.set("bar", 5)
assert(ev.eval(ast)[0] == 10)

ast = grammar.parse("my rent is bar + 5")
assert(find_text(ast, "calculate") == "bar + 5")
ev.set("bar", 5)
assert(ev.eval(ast)[0] == 10)

ast = grammar.parse("my rent is bar + 400 per month")
assert(find_text(ast, "calculate") == "bar + 400")
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
assert(find_text(ast, "mul") == "5 * 2")
assert(ev.eval(ast)[0] == 20)

ast = grammar.parse("5 * 2 * 6 + 4 + 2 + 5 * 3 + 3")
assert(find_text(ast, "add") == "5 * 2 * 6 + 4 + 2 + 5 * 3 + 3")
assert(find_text(ast, "mul") == "5 * 2 * 6")
assert(ev.eval(ast)[0] == 84)

ast = grammar.parse("""rent is 500 per month
    foo = 10
    l
    bar = foo + 5
    x
    sum = bar - foo / 2
    tax = sum*20%""")
ev.reset()
assert(ev.eval(ast) == [500, 10, 0, 15, 0, 10.0, 2.0])
assert(ev.variables == {"foo": 10, "bar": 15, "sum": 10.0, "tax": 2.0})

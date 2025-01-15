from storage import Monads, Dyads, Triads, MonadicAdverbs, DyadicAdverbs, SymbolType

# Extension Monads

evaluate = Monads.evaluate.symbol()
erase = Monads.erase.symbol()
truth = Monads.truth.symbol()

# Extension Dyads

applyMonad = Dyads.applyMonad.symbol()
retype = Dyads.retype.symbol()

# Triads

applyDyad = Triads.applyDyad.symbol()

# Monads

atom = Monads.atom.symbol()
char = Monads.char.symbol()
complementation = Monads.complementation.symbol()
enclose = Monads.enclose.symbol()
enumerate = Monads.enumerate.symbol()
first = Monads.first.symbol()
floor = Monads.floor.symbol()
format = Monads.format.symbol()
gradeUp = Monads.gradeUp.symbol()
gradeDown = Monads.gradeDown.symbol()
group = Monads.group.symbol()
negate = Monads.negate.symbol()
reciprocal = Monads.reciprocal.symbol()
reverse = Monads.reverse.symbol()
shape = Monads.shape.symbol()
size = Monads.size.symbol()
transpose = Monads.transpose.symbol()
unique = Monads.unique.symbol()

# Dyads

amend = Dyads.amend.symbol()
cut = Dyads.cut.symbol()
divide = Dyads.divide.symbol()
drop = Dyads.drop.symbol()
equal = Dyads.equal.symbol()
expand = Dyads.expand.symbol()
find = Dyads.find.symbol()
form = Dyads.form.symbol()
format2 = Dyads.format2.symbol()
index = Dyads.index.symbol()
indexInDepth = Dyads.indexInDepth.symbol()
integerDivide = Dyads.integerDivide.symbol()
join = Dyads.join.symbol()
less = Dyads.less.symbol()
match = Dyads.match.symbol()
max = Dyads.max.symbol()
min = Dyads.min.symbol()
minus = Dyads.minus.symbol()
more = Dyads.more.symbol()
plus = Dyads.plus.symbol()
power = Dyads.power.symbol()
remainder = Dyads.remainder.symbol()
reshape = Dyads.reshape.symbol()
rotate = Dyads.rotate.symbol()
split = Dyads.split.symbol()
take = Dyads.take.symbol()
times = Dyads.times.symbol()

# Monadic Adverbs

converge = MonadicAdverbs.converge.symbol()
each = MonadicAdverbs.each.symbol()
eachPair = MonadicAdverbs.eachPair.symbol()
over = MonadicAdverbs.over.symbol()
scanConverging = MonadicAdverbs.scanConverging.symbol()
scanOver = MonadicAdverbs.scanOver.symbol()

# Dyadic Adverbs

each2 = DyadicAdverbs.each2.symbol()
eachLeft = DyadicAdverbs.eachLeft.symbol()
eachRight = DyadicAdverbs.eachRight.symbol()
overNeutral = DyadicAdverbs.overNeutral.symbol()
iterate = DyadicAdverbs.iterate.symbol()
scanIterating = DyadicAdverbs.scanIterating.symbol()
scanOverNeutral = DyadicAdverbs.scanOverNeutral.symbol()
scanWhileOne = DyadicAdverbs.scanWhileOne.symbol()
whileOne = DyadicAdverbs.whileOne.symbol()

# Builtin Words

i = SymbolType.i.symbol()
x = SymbolType.x.symbol()
y = SymbolType.y.symbol()
z = SymbolType.z.symbol()
f = SymbolType.f.symbol()

true = 1
false = 0

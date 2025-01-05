# iota

iota is a small programming language.

It implements the operations from klong, which is a dialect of APL in the k family.

The klong operations are recreated with faithful attention to detail and most examples from the klong book should work.

However, the goal is not to be 100% identical. Rather, the klong manual is being used as a guide for implementing a  complete programming language design. iota should be mostly capable of doing anything that a klong program can do.

Currently, all of the operations are supported except for anything specific to strings, because the string type has not yet been implemented. There is also a lack of syntact constructions, so there is no way to construct functions, conditionals, projections, etc.

If you are looking for a more practical implementation of klong, check out KlongPy, which is implemented on top of numpy and so should be very fast.

## Motivation

iota is an experiment to explore several ideas:
* a small, but very portable language [Portability.md]
* a single, unified storage type
* unifying Smalltalk and APL design concepts
* word-sized integers and word-sized floating point numbers for all computations
* internal use of UTF-32 strings (in word-sized integers) instead of UTF-8

## Differences from klong

Besides than missing features that have not been implemented yet and accidental deficiencies that can be corrected with more comprehensive tests, there are also a few intentional differences from klong.

One minor difference is that an attempt has been made to extend the available options for compatible types for each function. So functions that would return an error for certain types of arguments in klong will return a valid result in iota. In general, if there is a possible interpretation for a function on a type then it will be implemented. For instance, in klong you can Take an integer number of items from a list, but if you were to try to taking a real number of items, say 0.5, then that would result in an error. In iota, when you Take 0.5 of a list, you get half the first half of the list (rounded down). However, when the official Klong documentation gives a non-error result for a specific operation, every endeavor is made to keep the behavior identical to Klong so that examples will work correctly. This is specifically for the difference operations that you can do on values, such as monads, dyads, and adverbs. Syntactically, the languages diverge.

One major syntactic difference is that evaluation is left-to-right as in Smalltalk instead of right-to-left as in APL. Also, the left argument to a function is known as "i" and the right arguments are "x", "y", and "z" respectively. In klong the direction would be reversed and they would be named "x" (on the right), "y", and "z" (on the left, and no "i" involved). The variable "i" is a reference to the variable "self" in Smalltalk (also in Python).

## Why mimic Klong?

APL is a minimalist language in many ways, but there are many implementations and some of them have a large number of operations. In the APL family tree, the most minimalist is K. There are many variants in the K family, including Klong. Of the K family, Klong has the best documentation and the best license. It is easy to tell if you have implemented an operation correctly just by reading the documentation, and if there is any doubt then there is the free and open source klong reference implementation with which to test out examples. If you were to implement a Lisp, you would start with "Structure and Interpretation of Computer Programs" and if you want to implement a modern APL then you would start with "An Introduction to Array Programming in Klong".

## Why not just use Klong?

The Klong implementation is very nice, as is KlongPy. However, they are not portable to all of the systems on which I desire to write programs. In particular, neither of them will run on embedded hardware. Klong is too large for most microcontrollers and has some fancy implementation details which are better suited to normal computers that have an operating system. KlongPy, similarly, is based on numpy, which is not available on embedded devices. iota, on the other hand, is meant to eventually run top of systems such as CircuitPython, with a possible eventual port to embedded C or C++ in mind. It could also be ported to other languages for other platforms, such as Swift for iOS and Kotlin for Android. Please note that it has not yet been tested with CircuitPython, this just a conceptual motivation.

## What's next for iota?

Currently, only integers, reals, and lists are implemented. The next step is to implement additional types, such as symbols, and working up eventually to functions.

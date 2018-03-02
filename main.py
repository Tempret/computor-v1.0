#!/usr/bin/env python3

from modules.class_Equation import Equation
from collections import Counter

# input = ' +  5 * X^0 - X - 9.3  * 23  * X^12 / X^2 = -1   + 1 * X^32'

input = 'x^2 + 3 * x +3 = 0'

equation = Equation(input)

for index, monomial in enumerate(equation.monomials):
	if not index and monomial.sign == '+':
			print(str(monomial)[2:], end=' ')
	else:
		print(monomial, end=' ')
print('= 0')
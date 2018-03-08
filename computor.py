#!/usr/bin/env python3

from modules.class_Equation import Equation
import sys

# input = '1 = 1'
#1*7.88 mist
#input = '7.88 * x^2 + 3 * x^2 + 3 = 0 '
# input = '+2*x^2  =  -  *x+7 +- + + 0'


if __name__ == "__main__":

	if len(sys.argv) == 2:
		input = sys.argv[1]
	else:
		print('usage: ./computor "EQUATION"')
		sys.exit(0)

	try:
		equation = Equation(input)
	except (ValueError, SyntaxError) as err:
		print(err)
	else:
		print("Reduced form:", equation)
		print("Polinomial degree:", equation.get_max_pow())
		equation.simple_algo()

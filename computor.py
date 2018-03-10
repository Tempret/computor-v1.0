#!/usr/bin/env python3

from modules.class_Equation import Equation
from modules.show_graph import show_graph
import argparse



if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="""Computor V-1.
													The program will display solution(s) of polynomial equation
													""", prog="./computor")
	parser.add_argument('eq', metavar='"Equation"', type=str,
						help='an polynomial equation')
	parser.add_argument('-g', dest='graph', action='store_const',
						const=True, default=False,
						help='show graph of equation function')

	args = parser.parse_args()

	try:
		equation = Equation(args.eq)
	except (ValueError, SyntaxError) as err:
		print("Error:", err)
	else:
		print("Reduced form:", equation)
		print("Polinomial degree:", equation.get_max_pow())
		try:
			results = equation.simple_algo()
		except ValueError as err:
			print('Error while find sollution:', err)
		else:
			if args.graph:
				show_graph(equation, results)
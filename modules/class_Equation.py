#!/usr/bin/env python3

import re
from modules.class_Monomial import Monomial
from collections import Counter
from math import sqrt
from decimal import Decimal

class Equation():

	monomials = None

	def __init__(self, input):
		if '=' not in input:
			raise SyntaxError("Didn't find '=' symbol")
		two_sides = [el.strip() for el in input.split('=')]

		for side in two_sides:
			if not side:
				raise SyntaxError('Empty side of equation')

		if len(two_sides) != 2:
			raise SyntaxError("Equation have more than one '=' symbol")
		if two_sides[0][0] != '-' and two_sides[0][0] != '+':
			two_sides[0] = '+' + two_sides[0]
		if two_sides[1][0] != '-' and two_sides[1][0] != '+':
			two_sides[1] = '+' + two_sides[1]

		two_sides = '='.join(two_sides)

		signes = self._make_signes(two_sides)

		self.monomials = [Monomial(el.strip(), signes[index]) for index, el in enumerate(filter(lambda x: x, re.split('[+\-=]', two_sides)))]

		self._set_variables()

		self._normalize_equasion()

		self.monomials.sort(key=lambda x: x.pow)

		if self.get_max_pow() > 2:
			raise ValueError("Max pow is more than two. Cant't solve this equation")
		else:
			print("I can solve")
			self.simple_algo()


	def _make_signes(self, two_sides):

		signes = list(filter(lambda x: x,
				 list(map(lambda x: x if (x == '-' or x == '+' or x == '=') else None, two_sides.strip()))))

		index = signes.index('=') + 1

		while index < len(signes):
			if signes[index] == '+':
				signes[index] = '-'
			elif signes[index] == '-':
				signes[index] = '+'
			index += 1

		del signes[signes.index('=')]

		return signes

	def _set_variables(self):
		variable = None

		for el in self.monomials:
			if el.variable:
				variable = el.variable
				break

		if variable:
			for el in self.monomials:
				if el.variable == variable:
					continue
				if el.variable == None:
					el.variable = variable
				else:
					raise SyntaxError('Was expected more than one variable type')

		else:
			raise SyntaxError('Was expected at least one variable for solve equation')

	def _normalize_equasion(self):

		new_monomials = []

		pow_counter = Counter(list(map(lambda x: x.pow, self.monomials)))

		for pow in pow_counter:

			if pow_counter[pow] == 1:
				new_monomials.append(list(filter(lambda x: x.pow == pow, self.monomials))[0])
				continue
			else:
				pow_filter = list(filter(lambda x: x.pow == pow, self.monomials))
				i = pow_counter[pow]

				result = pow_filter[0]
				while i - 1:
					i -= 1
					result = result + pow_filter[i]
				new_monomials.append(result)

		self.monomials = new_monomials

	def get_max_pow(self):
		return max(map(lambda x: x.pow, [el for el in self.monomials]))

	def simple_algo(self):

		a_mon = list(filter(lambda x: x.pow == 2, self.monomials))
		b_mon = list(filter(lambda x: x.pow == 1, self.monomials))
		c_mon = list(filter(lambda x: x.pow == 0, self.monomials))

		a = a_mon[0].get_coef() if a_mon else 0
		b = b_mon[0].get_coef() if b_mon else 0
		c = c_mon[0].get_coef() if c_mon else 0

		if not a:
			return [c / b]
		else:
			discriminant = b ** 2 - 4 * a * c

			if discriminant > 0:
				print('Discriminant > 0')
				result_1 = (-1 * b + Decimal(float(discriminant) ** 0.5)) / 2 * a
				result_2 = (-1 * b - Decimal(float(discriminant) ** 0.5)) / 2 * a
				print('Results', result_1, result_2)
				return [result_1, result_2]
			elif discriminant == 0:
				print('Discriminant = 0')
				result = -1 * b / 2 * a
				print('Result', result)
				return [result]
			else:
				print('Discriminant < 0')
				im_part = Decimal(float(abs(discriminant)) ** 0.5) / 2 * a
				re_part = -1 * b / 2 * a
				print('Result', re_part, '+' ,im_part, 'i')
				return [im_part, re_part]
			print('Discriminant', discriminant)

		print('A = %d B = %d C = %d' % (a, b, c))

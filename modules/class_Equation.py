#!/usr/bin/env python3

import re
from modules.class_Monomial import Monomial
from collections import Counter
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

		if re.search('[+\-]\s*=', input) or re.search('[+\-]{2}', input):
			raise SyntaxError('Wrong sequence of signs expected')

		two_sides = '='.join(two_sides)

		signes = self._make_signes(two_sides)

		self.monomials = [Monomial(el.strip(), signes[index]) for index, el in enumerate(filter(lambda x: x, re.split('[+\-=]', two_sides)))]

		self._set_variables()

		self._normalize_equation()

		self.monomials.sort(key=lambda x: x.pow)

		max_pow = self.get_max_pow()

		if not max_pow and self.monomials[0].d_coef:
			raise ValueError("Equation isn\'t identical")

		elif max_pow > 2:
			raise ValueError("Max pow is more than two. Cant't solve this equation")

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
					raise SyntaxError('Expected more than one variable type')

		else:
			raise SyntaxError('Expected at least one variable for solve equation')

	def _normalize_equation(self):

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

		new_monomials = list(filter(lambda x: str(x), new_monomials))

		if not new_monomials:
			new_monomials = [Monomial(0, '+')]

		self.monomials = new_monomials

	def get_max_pow(self):
		return max(map(lambda x: x.pow, [el for el in self.monomials]))

	def get_monomial(self, pow):
		search = list(filter(lambda x: x.pow == pow, self.monomials))
		if search:
			return search[0]
		else:
			return Monomial({'d_koef': 0, 'variable': 'x', 'pow': 0}, '+')

	def simple_algo(self):

		a_mon = list(filter(lambda x: x.pow == 2, self.monomials))
		b_mon = list(filter(lambda x: x.pow == 1, self.monomials))
		c_mon = list(filter(lambda x: x.pow == 0, self.monomials))

		a = a_mon[0].get_coef() if a_mon else 0
		b = b_mon[0].get_coef() if b_mon else 0
		c = c_mon[0].get_coef() if c_mon else 0

		if not a and not b and not c:
			print('All real numbers are solution')
			return []

		if not a:
			if not b:
				raise ValueError('Trying divide by zero')
			result = (c / b) * -1
			result = result if result else int(result)
			print('The solution is:', result, sep="\n")
			return [2, result]
		else:
			discriminant = b ** 2 - 4 * a * c

			if discriminant > 0:
				result_1 = ((-1 * b) + (Decimal(float(discriminant) ** 0.5))) / (2 * a)
				result_2 = ((-1 * b) - (Decimal(float(discriminant) ** 0.5))) / (2 * a)
				result_1 = result_1 if result_1 else int(result_1)
				result_2 = result_2 if result_2 else int(result_2)
				print('Discriminant is strictly positive, the two solutions are:', result_1, result_2, sep="\n")
				return [1, result_1, result_2]
			elif discriminant == 0:
				result = (-1 * b) / (2 * a)
				result = result if result else int(result)
				print('Discriminant equal 0, the only one solution are:', result, sep="\n")
				return [0, result]
			else:
				im_part = Decimal(float(abs(discriminant)) ** 0.5) / (2 * a)
				re_part = Decimal((-1 * b) / (2 * a))
				im_part = im_part if im_part else int(im_part)
				re_part = re_part if re_part else int(re_part)
				print('Discriminant is strictly negative, the two complex solutions are:')
				if b:
					print(re_part, '+' ,im_part, '* i')
					print(re_part, '-' ,im_part, '* i')
				else:
					if im_part != 0:
						print(im_part, 'i')
						print((-1) * im_part, 'i')
					else:
						print('0')
				return [-1, im_part, re_part]

	def __str__(self):
		string = []

		for index, monomial in enumerate(self.monomials):
			if not index and monomial.sign == '+':
				string.append(str(monomial)[2:])
			else:
				string.append(str(monomial))

		if string == ['']:
			string.append('0')

		string.append('= 0')
		return " ".join(string)

#!/usr/bin/env python3
import re
from collections import Counter
from decimal import Decimal, InvalidOperation

class Monomial():

	d_coef = 1
	variable = None
	pow = None
	sign = None
	d_sign = 0

	def __init__(self, arg, sign, var='X'):

		self.sign = sign

		self.d_sign = -1 if sign == '-' else 1

		if type(arg) == type(str('')):

			all_alpha = list(filter(lambda x: x.isalpha(), list(arg)))

			if len(all_alpha):
				self.variable = all_alpha[0]

			if len(list(filter(lambda x: x if x != self.variable else None, all_alpha))):
				raise SyntaxError('More than one variable expected in part [%s]' % arg)

			separate = [el.strip() for el in re.split('[*/]', arg)]

			coefs = list(map(lambda x: x if self._is_number(x.strip()) else '1', separate))

			signes = list(filter(lambda x: x, list(map(lambda x: x if (x == '*' or x == '/') else None, arg.strip()))))

			self.d_coef = self._calculate_coef(coefs, signes)

			self.pow = self._calculate_pow(separate, signes)

		elif type(arg) == type(dict()):
			if 'd_koef' in arg and 'variable' in arg and 'pow' in arg:
				self.d_coef = arg['d_koef']
				self.pow = arg['pow']
				self.variable = arg['variable']
			else:
				raise ValueError('Required fields in initial dictionary is missing')

		elif arg == 0:
				self.d_coef = 0
				self.pow = 0
				self.variable = var
		else:
			raise TypeError('Cant init Monomial with argument type ' + type(arg))

	def _is_number(self, number):
		try:
			float(number)
		except:
			return False
		else:
			return True

	def _is_monomial(self, monom):
		if self.variable and re.match(self.variable + '\s*\^\s*[0-9]+', monom.strip()):
			return True
		else:
			return False

	def _calculate_coef(self, coefs, signes):
		result = Decimal(coefs[0])

		if not signes:
			return result

		for sign, coef in zip(signes, coefs[1:]):

			if sign == '/':
				result /= Decimal(coef)
			elif sign == '*':
				result *= Decimal(coef)
			else:
				raise SyntaxError('Wrong operator')

		return result

	def _calculate_pow(self, all_parts, signes):

		signes.insert(0, '*')

		result = 0
		pows = []

		for elem, sign in zip(all_parts, signes):
			if self._is_number(elem):
				continue
			if self._is_monomial(elem):
				try:
					value = int(elem.split('^')[1])
				except ValueError:
					raise SyntaxError('Wrong pow in part %s. Only integer expected as pow' % ''.join(all_parts))
				if sign == '/':
					value *= -1
				pows.append(value)
			elif str(self.variable) in ''.join(all_parts) and "^" not in ''.join(all_parts):
				return 1
			else:
				raise SyntaxError('Wrong syntax in part %s' % ''.join(all_parts))

		for pow in pows:
			result += pow

		return result

	def __str__(self):

		result = [self.sign]

		if self.d_coef == 0:
			return ''
		elif self.d_coef != 1:
			result.append(str(self.d_coef))
		elif self.d_coef == 1 and self.pow == 0:
			result.append(str(self.d_coef))

		if self.pow > 1:
			if self.d_coef == 1:
				result.append('%s^%d' % (self.variable, self.pow))
			else:
				result.append('* %s^%d' % (self.variable, self.pow))
		elif self.pow == 1:
			if self.d_coef == 1:
				result.append('%s' % self.variable)
			else:
				result.append('* %s' % self.variable)

		return ' '.join(result)

	def __add__(self, other):
		if self.pow == other.pow and self.variable == other.variable:
			self_sign = 1 if self.sign == '+' else -1
			other_sign = 1 if other.sign == '+' else -1

			new = {
				'd_koef': abs(self.d_coef * self_sign + other.d_coef * other_sign),
				'variable': self.variable,
				'pow': self.pow
			}

			return Monomial(new, '-' if self.d_coef * self_sign + other.d_coef * other_sign < 0 else '+')
		else:
			raise ValueError("Can't add two monomial with different pow")

	def get_coef(self):
		return self.d_coef if self.sign == '+' else -1 * self.d_coef
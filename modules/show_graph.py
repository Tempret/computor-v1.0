

import matplotlib.pyplot as plt
import numpy as np



NEGATIVE = -1
ZERO = 0
POSITIVE = 1
LINEAR = 2
RANGE = 20

def show_graph(equation, results):

	pow_2 = equation.get_monomial(2)
	pow_1 = equation.get_monomial(1)
	pow_0 = equation.get_monomial(0)

	if not results:
		return
	if results[0] == NEGATIVE:
		x = np.arange(-100, 100, 0.01)
	elif results[0] == ZERO or results[0] == LINEAR:
		x = np.arange(float(results[1]) - RANGE, float(results[1]) + RANGE, 0.01)
	elif results[0] == POSITIVE:
		x = np.arange(float(min(results[1:])) - RANGE, float(max(results[1:])) + RANGE, 0.01)
	else:
		raise ValueError("Wrong discriminant")

	var = equation.monomials[0].variable

	plt.plot(x, x ** 2 * float(pow_2.d_coef * pow_2.d_sign) + x * float(pow_1.d_coef * pow_1.d_sign) + float(pow_0.d_coef * pow_0.d_sign))  # Построение графика
	plt.xlabel(r'$' + var + '$')
	plt.ylabel(r'$f('+ var +')$')
	plt.title(r'$f('+ var +')='+ str(equation)[:-3] + '$')
	plt.grid(True)
	fig = plt.gcf()
	fig.canvas.set_window_title('Computor V-1')
	plt.show()
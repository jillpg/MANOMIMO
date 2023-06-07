def smooth_values_moving_average(values, window_size):
    smoothed_values = []
    for i in range(len(values)):
        start_index = max(0, i - window_size + 1)
        end_index = i + 1
        subset = values[start_index:end_index]
        smoothed_value = sum(subset) / len(subset)
        smoothed_values.append(smoothed_value)
    return smoothed_values


def smooth_values_exponential(values, alpha):
    smoothed_values = [values[0]]  # Valor inicial
    for i in range(1, len(values)):
        smoothed_value = alpha * values[i] + (1 - alpha) * smoothed_values[i - 1]
        smoothed_values.append(smoothed_value)
    return smoothed_values


# import matplotlib.pyplot as plt

# # Ejemplo de uso con una secuencia de valores
# values = [1, 3, 5, 4, 2, 6, 8, 7, 9, 8, 9, 10]
# window_size = 3
# alpha = 0.5

# smoothed_values_ma = smooth_values_moving_average(values, window_size)
# smoothed_values_exp = smooth_values_exponential(values, alpha)

# # Configuración de la gráfica
# plt.plot(values, label='Valores originales')
# plt.plot(smoothed_values_ma, label='Media Móvil')
# plt.plot(smoothed_values_exp, label='Suavizado Exponencial')
# plt.legend()

# # Mostrar la gráfica
# plt.show()

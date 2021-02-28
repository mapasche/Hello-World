from statistics import mean, stdev

def calcular_carga_escpecifica_lab(n = 1, volts = 1, corriente = 1, radio = 1):
    mu = 1.26*10**(-6)

    resultados = []
    for v, i, r in zip(volts,corriente,radio):
        denominador = (r * mu * n * i) ** 2
        numerador = 2 * v
        division = numerador / denominador
        resultados.append(division)
    return resultados


def error_porcentual (valor_teo, valor_pract):
    return abs(valor_teo - valor_pract) / valor_teo * 100


n = 3586.2069

v = [176.8, 176.6, 176.8, 176.5, 179.9]
i = [0.02, 1.94, 2.795, 2.54, 3.379]
r = [0.0066511, 0.0064872, 0.0047143, 0.0024146, 0.0022262]


resultados = calcular_carga_escpecifica_lab(n, v, i, r)

print("Carga especifica de las mediciones:")
for resultado in resultados:
    print(resultado / 10**11)

print()

print("Errores porcnetuales de las mediciones")
valor_teorico = 1.758820024 * ( 10 ** 11 )
for resultado in resultados:
    print(error_porcentual(valor_teorico, resultado))


print()
print("Promedio: ", mean(resultados) / (10**11))
print("Desviacion estandar: ", stdev(resultados) / (10**11))

print()
del resultados[0]
print(resultados)
print("Promedio 2: ", mean(resultados) / (10**11))
print("Desviacion estandar 2: ", stdev(resultados) / (10**11))
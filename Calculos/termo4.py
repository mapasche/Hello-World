
def integral (m, n, v1, v2):
    valor = (m / 2 * v2**2 + n*v2) - ((m / 2 * v1**2 + n*v1))
    return valor

m = 0
n = 101738.4638
v1 = 4.14788 * 10**(-5)
v2 = 3.318305 * 10**(-5)

print(integral(m, n, v1, v2))




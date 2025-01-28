from cs50 import get_int

# Solicitamos el número de tarjeta
card_number = get_int("card number: ")

# Convertimos el número a una lista de dígitos
digits = [int(d) for d in str(card_number)]

# Variables para las sumas
suma_tot = 0
suma_digits = 0

# Multiplicamos por 2 los dígitos en posiciones impares desde el final
# y sumamos los dígitos en posiciones pares
for d in digits[-2::-2]:  # Tomamos cada segundo dígito desde el final hacia atrás
    producto = d * 2
    suma_digits += sum(int(x) for x in str(producto))

# Sumamos los dígitos que no fueron multiplicados por 2
suma_tot += sum(digits[-1::-2])  # Tomamos cada segundo dígito empezando desde el último hacia atrás

# Calculamos el "magic number"
magic_number = suma_tot + suma_digits

# Verificamos el tipo de tarjeta
if magic_number % 10 == 0:
    if len(digits) == 15 and (digits[0] == 3 and (digits[1] == 4 or digits[1] == 7)):
        print("AMEX")
    elif len(digits) == 16 and (digits[0] == 5 and digits[1] in [1, 2, 3, 4, 5]):
        print("MASTERCARD")
    elif (len(digits) == 13 or len(digits) == 16) and digits[0] == 4:
        print("VISA")
    else:
        print("INVALID")
else:
    print("INVALID")

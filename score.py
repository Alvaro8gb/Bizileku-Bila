def contar_digitos(numero):
    return len(str(abs(numero)))


def calculate_score(numero):

    if numero == 0:
        return 0  # Retornar 0 si el número es 0
    num_digitos = len(str(abs(numero)))  # abs para manejar números negativos

    # Dividir según el número de dígitos
    if num_digitos == 1:
        return numero  # No dividir
    else:
        divisor = 10 ** (num_digitos - 2)  # Divisor: 10^(número de dígitos - 2)
        return numero / divisor


if __name__ == "__main__":
    numeros = [0, 5, 12, 123, 4567, -789, 10000]
    for numero in numeros:
        resultado = calculate_score(numero)
        print(f"Número: {numero}, Resultado: {resultado}")

import math

def calculate_score(kpi):

    if kpi <=0:
        return 0
    else:
        return math.log(kpi)

if __name__ == "__main__":
    kpis = [2, 5, 12, 312, 4567, 789, 1330]
    for kpi in kpis:
        resultado = calculate_score(kpi)
        print(f"Número: {kpi}, Resultado: {resultado}")

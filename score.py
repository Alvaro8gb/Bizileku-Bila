import math

from globals import API_KPI


def calculate_score(kpi):

    if kpi <= 0:
        return 0
    else:
        return math.log(kpi)


def find_best_municipalities(indicators, k):
    data_municipalities = {}

    for i in indicators:
        municipalities = API_KPI.get_municipalities(i.id)

        # st.json(municipalities)

        for m in municipalities["municipalities"]:

            if m["id"] not in data_municipalities:
                data_municipalities[m["id"]] = {}

            last_year = max(m["years"][0].keys())
            last_value = m["years"][0][last_year]
            score = calculate_score(last_value)
            data_municipalities[m["id"]][i.id] = score * i.weight

    # st.json(data_municipalities)

    municipality_sums = [
        (municipality_id, sum(indicators.values()), list(indicators.values()))
        for municipality_id, indicators in data_municipalities.items()
    ]

    municipality_sums.sort(key=lambda x: x[1], reverse=True)
    top_k_municipalities = municipality_sums[:k]

    return top_k_municipalities


if __name__ == "__main__":
    kpis = [2, 5, 12, 312, 4567, 789, 1330]
    for kpi in kpis:
        resultado = calculate_score(kpi)
        print(f"Número: {kpi}, Resultado: {resultado}")

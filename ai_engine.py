def advice_engine(temp, hum, a_hum, b_hum) -> str:
    lines = []
    if temp >= 34:
        lines.append(f"Alerta: stres termic extrem ({temp}C)! Activati irigarea de urgenta.")
    elif temp >= 29:
        if hum < 50:
            lines.append("Caldura + umiditate scazuta - cresteti udarea cu 30%, evitati orele 11-16.")
        else:
            lines.append(f"Temperaturi ridicate ({temp}C). Umiditate acceptabila - monitorizati la 3h.")
    elif temp <= 11:
        lines.append(f"Temperaturi scazute ({temp}C) - reduceti irigarea, risc de inghet.")
    else:
        lines.append(f"Conditii optime ({temp}C, {hum}%). Mentineti programul curent.")
    if hum > 85:
        lines.append("Suprasaturare detectata - suspendati irigarea 24h.")
    elif hum < 38:
        lines.append("Umiditate critica globala - irigare imediata necesara.")
    if abs(a_hum - b_hum) > 20:
        low = "prima planta" if a_hum < b_hum else "a doua planta"
        lines.append(f"Dezechilibru hidric - {low} are nevoie de atentie suplimentara.")
    return "  ".join(lines)
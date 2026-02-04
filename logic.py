# Tento soubor má na starosti: Objednávková logika
# Autor: Adam Diblik
def vypocitat_cenu(cena_jidla, kategorie_stravnika):
    """
    Vypočítá konečnou cenu.
    Pokud je to učitel, platí plnou cenu.
    Pokud žák, má dotaci (např. platí jen 40%).
    """
    if kategorie_stravnika == "ucitel":
        return cena_jidla
    elif kategorie_stravnika == "zak":
        return round(cena_jidla * 0.4, 2) # Platí 40% ceny
    else:
        return cena_jidla

def validovat_objednavku(jidlo_id, stravnik_id):
    """
    Ověří, jestli jsou zadané údaje smysluplné.
    """
    if not jidlo_id or not stravnik_id:
        return False, "Chybí ID jídla nebo strávníka."
    
    if jidlo_id < 0 or stravnik_id < 0:
        return False, "ID nesmí být záporné."

    return True, "Objednávka je validní."

# --- TOTO JE TA ČÁST, KTERÁ UKAZUJE VÝSLEDEK ---
if __name__ == "__main__":
    print("--- ZAČÍNÁM TESTOVAT LOGIKU ---")
    
    # 1. Zkouška ceny pro žáka (měl by platit 40 Kč ze 100)
    cena = vypocitat_cenu(100, "zak")
    print(f"Cena jídla 100 Kč pro žáka je: {cena} Kč (Mělo by být 40.0)")

    # 2. Zkouška ceny pro učitele (měl by platit 100 ze 100)
    cena_ucitel = vypocitat_cenu(100, "ucitel")
    print(f"Cena jídla 100 Kč pro učitele je: {cena_ucitel} Kč (Mělo by být 100)")

    # 3. Zkouška validace (Chyba)
    vysledek, zprava = validovat_objednavku(None, 5)
    print(f"Test chyby: {zprava}")

    # 4. Zkouška validace (Správně)
    vysledek, zprava = validovat_objednavku(1, 5)
    print(f"Test správný: {zprava}")
    
    print("--- TESTOVÁNÍ DOKONČENO ---")
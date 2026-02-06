import database # Musime se spojit s databazi

def vypocitat_cenu(cena_jidla, kategorie_stravnika):
    """
    Pokud je to učitel, platí plnou cenu.
    Pokud žák, má dotaci (platí jen 40%).
    """
    if kategorie_stravnika == "ucitel":
        return cena_jidla
    elif kategorie_stravnika == "zak":
        return round(cena_jidla * 0.4, 2)
    else:
        return cena_jidla

def validovat_objednavku(jidlo_id, stravnik_id):
    """
    Ověří, jestli jsou údaje smysluplné A JESTLI JÍDLO EXISTUJE.
    """
    # 1. Základní kontrola čísel
    if not jidlo_id or not stravnik_id:
        return False, "Chybí ID jídla nebo strávníka."
    
    if jidlo_id < 0 or stravnik_id < 0:
        return False, "ID nesmí být záporné."

    # 2. Kontrola v databázi
    try:
        conn = database.connect_db()
        cursor = conn.cursor()
        # Zeptáme se databáze: Existuje jídlo s tímto ID?
        cursor.execute("SELECT id FROM jidla WHERE id = ?", (jidlo_id,))
        vysledek = cursor.fetchone()
        conn.close()

        if vysledek is None:
            return False, f"Jídlo s ID {jidlo_id} v menu neexistuje!"
            
    except Exception as e:
        return False, f"Chyba databáze: {e}"

    return True, "Objednávka je validní."

if __name__ == "__main__":
    print("Testování logiky...")
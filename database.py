import sqlite3

def connect_db():
    """
    Vytvoří a vrátí připojení k databázi.
    Tuhle funkci volá i main.py, proto tu musí být!
    """
    return sqlite3.connect("jidelna.db")

def create_tables():
    """Vytvoří potřebné tabulky, pokud neexistují."""
    conn = connect_db()
    cursor = conn.cursor()
    
    # 1. Tabulka Jídla
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jidla (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nazev TEXT NOT NULL,
            cena REAL NOT NULL,
            alergeny TEXT
        )
    ''')
    
    # 2. Tabulka Strávníci
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stravnici (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jmeno TEXT NOT NULL,
            trida TEXT NOT NULL
        )
    ''')
    
    # 3. Tabulka Objednávky
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS objednavky (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datum TEXT NOT NULL,
            stravnik_id INTEGER,
            jidlo_id INTEGER,
            FOREIGN KEY (stravnik_id) REFERENCES stravnici (id),
            FOREIGN KEY (jidlo_id) REFERENCES jidla (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("-> Tabulky v databázi byly zkontrolovány/vytvořeny.")

# --- TESTOVACÍ ČÁST  ---
if __name__ == "__main__":
    print("--- ZAČÍNÁM TESTOVAT DATABÁZI ---")
    
    # 1. Zkusíme vytvořit tabulky
    create_tables()
    
    # 2. Zkusíme cvičně vložit strávníka
    conn = connect_db()
    cursor = conn.cursor()
    # Vložíme testovacího žáka, jen abychom viděli, že to zapisuje
    cursor.execute("INSERT INTO stravnici (jmeno, trida) VALUES (?, ?)", ("Testovací Žák", "9.A"))
    conn.commit()
    
    print("-> Testovací strávník vložen.")
    conn.close()
    
    print("--- TESTOVÁNÍ DOKONČENO (Vše OK) ---")
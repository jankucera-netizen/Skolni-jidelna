import sqlite3

def create_tables():
    # Připojení k databázi (vytvoří soubor jidelna.db, pokud neexistuje)
    conn = sqlite3.connect("jidelna.db")
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
    print("Hotovo! Databáze a tabulky vytvořeny.")

if __name__ == "__main__":
    create_tables()
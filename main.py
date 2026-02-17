def vytvorit_objednavku(self):
        jidlo_id_str = self.entry_id_objednavka.get()
        typ_stravnika = self.var_typ_stravnika.get() # Tady zjistíme, co jsi vybral nahoře
        stravnik_id = 1 # ID uživatele zatím natvrdo
        
        try:
            jidlo_id = int(jidlo_id_str)
            
            # 1. Zjistíme cenu jídla z databáze
            conn = database.connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT nazev, cena FROM jidla WHERE id = ?", (jidlo_id,))
            radek = cursor.fetchone()
            
            if radek is None:
                messagebox.showerror("Chyba", "Jídlo s tímto ID neexistuje!")
                conn.close()
                return
            
            nazev_jidla = radek[0]
            plna_cena = radek[1]
            
            # 2. Vypočítáme cenu podle toho, kdo jsi
            if typ_stravnika == "zak":
                konecna_cena = plna_cena * 0.40  # Student platí jen 40%
                text_typu = "Studentská cena"
            else:
                konecna_cena = plna_cena         # Učitel platí vše
                text_typu = "Plná cena"

            # 3. Zobrazíme potvrzovací okno s cenou
            zprava = f"Objednáváš: {nazev_jidla}\n\n{text_typu}: {konecna_cena:.0f} Kč\n(Původní cena: {plna_cena} Kč)"
            potvrzeni = messagebox.askyesno("Potvrzení objednávky", zprava + "\n\nOdeslat objednávku?")
            
            if potvrzeni:
                cursor.execute("INSERT INTO objednavky (datum, stravnik_id, jidlo_id) VALUES (?, ?, ?)", 
                               ("2026-02-17", stravnik_id, jidlo_id))
                conn.commit()
                # Tady je ten text, co jsi chtěl:
                self.lbl_status.config(text=f"✅ Jídlo s ID {jidlo_id} bylo objednáno (cena {konecna_cena:.0f} Kč)", fg="green")
            else:
                self.lbl_status.config(text="❌ Objednávka zrušena", fg="red")

            conn.close()
                
        except ValueError:
             messagebox.showerror("Chyba", "ID jídla musí být číslo.")
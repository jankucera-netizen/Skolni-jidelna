import tkinter as tk
from tkinter import ttk, messagebox
import database
import logic

class JidelnaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Školní jídelna - Skupina 7 (Final Verze + Admin)")
        self.root.geometry("900x600")
        
        # Kontrola/Vytvoření tabulek
        database.create_tables()

        # --- HLAVNÍ ROZCESTNÍK (Záložky) ---
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        #Správa jídel
        self.tab_jidla = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_jidla, text=" 🍕 Správa jídel (Admin) ")
        self.setup_tab_jidla()

        #Objednávky
        self.tab_objednavky = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_objednavky, text=" 🛒 Nová objednávka ")
        self.setup_tab_objednavky()

    # ==========================================
    # SPRÁVA JÍDEL
    # ==========================================
    def setup_tab_objednavky(self):
        lbl = tk.Label(self.tab_objednavky, text="Zadejte ID jídla z nabídky:", font=("Arial", 12))
        lbl.pack(pady=10)

        frame_obj = tk.Frame(self.tab_objednavky)
        frame_obj.pack(pady=5)

        tk.Label(frame_obj, text="ID Jídla:").pack(side="left")
        self.entry_id_objednavka = tk.Entry(frame_obj, font=("Arial", 12), width=5)
        self.entry_id_objednavka.pack(side="left", padx=5)

        # --- TUTO ČÁST JSME PŘIDALI (Výběr strávníka) ---
        tk.Label(self.tab_objednavky, text="Kdo objednává?", font=("Arial", 10, "bold")).pack(pady=(20, 5))

        #Proměnná, která si pamatuje volbu ("zak" nebo "ucitel"),
        self.var_typ_stravnika = tk.StringVar(value="zak") 

        frame_radio = tk.Frame(self.tab_objednavky)
        frame_radio.pack()

        tk.Radiobutton(frame_radio, text="Student (sleva 40%)", variable=self.var_typ_stravnika, value="zak").pack(side="left", padx=10)
        tk.Radiobutton(frame_radio, text="Učitel / Cizí (plná cena)", variable=self.var_typ_stravnika, value="ucitel").pack(side="left", padx=10)
        # ---------------------------------------------------

        btn = tk.Button(self.tab_objednavky, text="OBJEDNAT OBĚD", command=self.vytvorit_objednavku, bg="green", fg="white", font=("Arial", 10, "bold"))
        btn.pack(pady=20)

        self.lbl_status = tk.Label(self.tab_objednavky, text="", fg="blue", font=("Arial", 10))
        self.lbl_status.pack()

    # ==========================================
    # OBJEDNÁVKY
    # ==========================================
    def setup_tab_objednavky(self):
        lbl = tk.Label(self.tab_objednavky, text="Zadejte ID jídla z nabídky:", font=("Arial", 12))
        lbl.pack(pady=20)

        frame_obj = tk.Frame(self.tab_objednavky)
        frame_obj.pack(pady=5)

        tk.Label(frame_obj, text="ID Jídla:").pack(side="left")
        self.entry_id_objednavka = tk.Entry(frame_obj, font=("Arial", 12), width=5)
        self.entry_id_objednavka.pack(side="left", padx=5)

        btn = tk.Button(self.tab_objednavky, text="OBJEDNAT OBĚD", command=self.vytvorit_objednavku, bg="green", fg="white", font=("Arial", 10, "bold"))
        btn.pack(pady=20)
        
        self.lbl_status = tk.Label(self.tab_objednavky, text="", fg="blue", font=("Arial", 10))
        self.lbl_status.pack()

    # --- FUNKCE ---
    def pridat_jidlo(self):
        nazev = self.entry_nazev.get()
        try:
            cena = float(self.entry_cena.get())
            conn = database.connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO jidla (nazev, cena) VALUES (?, ?)", (nazev, cena))
            conn.commit()
            conn.close()
            self.naci_jidla()
            self.entry_nazev.delete(0, tk.END)
            self.entry_cena.delete(0, tk.END)
            messagebox.showinfo("Úspěch", "Jídlo přidáno.")
        except ValueError:
            messagebox.showerror("Chyba", "Cena musí být číslo!")

    def smazat_jidlo(self):
        """NOVÁ FUNKCE: Smaže vybraný řádek z databáze"""
        selected_item = self.tree.selection() # Zjistí, co je označeno myší
        
        if not selected_item:
            messagebox.showwarning("Pozor", "Nejdřív musíš označit jídlo v tabulce!")
            return

        # Získáme ID z označeného řádku
        item_data = self.tree.item(selected_item)
        jidlo_id = item_data['values'][0] # ID je v prvním sloupci

        # Potvrzovací okno
        odpoved = messagebox.askyesno("Smazat?", f"Opravdu chceš smazat jídlo s ID {jidlo_id}?")
        
        if odpoved:
            conn = database.connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM jidla WHERE id = ?", (jidlo_id,))
            conn.commit()
            conn.close()
            
            self.naci_jidla() # Obnovíme tabulku
            messagebox.showinfo("Hotovo", "Jídlo bylo smazáno.")

    def naci_jidla(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = database.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jidla")
        for row in cursor.fetchall():
            self.tree.insert("", tk.END, values=row)
        conn.close()

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

if __name__ == "__main__":
    root = tk.Tk()
    app = JidelnaApp(root)
    root.mainloop()
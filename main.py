import tkinter as tk
from tkinter import ttk, messagebox
import database
import logic

class JidelnaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Školní jídelna - Skupina 7 (Final Verze)")
        self.root.geometry("900x600")
        
        # Kontrola/Vytvoření tabulek v databázi
        database.create_tables()

        # --- HLAVNÍ ROZCESTNÍK (Záložky) ---
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # 1. Záložka - Správa jídel (ADMIN)
        self.tab_jidla = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_jidla, text=" 🍕 Správa jídel (Admin) ")
        self.setup_tab_jidla()

        # 2. Záložka - Objednávky (UŽIVATEL)
        self.tab_objednavky = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_objednavky, text=" 🛒 Nová objednávka ")
        self.setup_tab_objednavky()

    # =======================================================
    # ČÁST 1: SPRÁVA JÍDEL (ADMINISTRACE)
    # =======================================================
    def setup_tab_jidla(self):
        # Formulář pro přidání
        frame_form = tk.LabelFrame(self.tab_jidla, text="Přidat / Odebrat jídlo")
        frame_form.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_form, text="Název:").pack(side="left", padx=5)
        self.entry_nazev = tk.Entry(frame_form)
        self.entry_nazev.pack(side="left", padx=5)

        tk.Label(frame_form, text="Cena:").pack(side="left", padx=5)
        self.entry_cena = tk.Entry(frame_form, width=10)
        self.entry_cena.pack(side="left", padx=5)

        # Tlačítka
        tk.Button(frame_form, text="Uložit jídlo", command=self.pridat_jidlo, bg="#ddd").pack(side="left", padx=10)
        tk.Button(frame_form, text="Smazat označené", command=self.smazat_jidlo, bg="red", fg="white").pack(side="right", padx=10)

        # Tabulka jídel
        self.tree = ttk.Treeview(self.tab_jidla, columns=("ID", "Nazev", "Cena"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nazev", text="Název jídla")
        self.tree.heading("Cena", text="Cena")
        self.tree.column("ID", width=50)
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.naci_jidla()

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
            # Vyčistit políčka
            self.entry_nazev.delete(0, tk.END)
            self.entry_cena.delete(0, tk.END)
            messagebox.showinfo("Úspěch", "Jídlo bylo přidáno.")
        except ValueError:
            messagebox.showerror("Chyba", "Cena musí být číslo!")

    def smazat_jidlo(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Pozor", "Nejdřív musíš označit jídlo v tabulce!")
            return

        item_data = self.tree.item(selected_item)
        jidlo_id = item_data['values'][0]

        odpoved = messagebox.askyesno("Smazat?", f"Opravdu chceš smazat jídlo s ID {jidlo_id}?")
        if odpoved:
            conn = database.connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM jidla WHERE id = ?", (jidlo_id,))
            conn.commit()
            conn.close()
            self.naci_jidla()
            messagebox.showinfo("Hotovo", "Jídlo bylo smazáno.")

    def naci_jidla(self):
        # Smaže staré řádky v tabulce a načte nové z DB
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = database.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jidla")
        for row in cursor.fetchall():
            self.tree.insert("", tk.END, values=row)
        conn.close()

    # =======================================================
    # ČÁST 2: OBJEDNÁVKY (PRO STUDENTY A UČITELE)
    # =======================================================
    def setup_tab_objednavky(self):
        # Nadpis
        lbl = tk.Label(self.tab_objednavky, text="Objednávkový systém", font=("Arial", 14, "bold"))
        lbl.pack(pady=10)

        # Vstup pro ID
        frame_obj = tk.Frame(self.tab_objednavky)
        frame_obj.pack(pady=5)
        tk.Label(frame_obj, text="Zadejte číslo (ID) jídla:").pack(side="left")
        self.entry_id_objednavka = tk.Entry(frame_obj, font=("Arial", 12), width=5)
        self.entry_id_objednavka.pack(side="left", padx=5)

        # --- PŘEPÍNAČ (Student / Učitel) ---
        tk.Label(self.tab_objednavky, text="Kdo jsi?", font=("Arial", 10, "bold")).pack(pady=(20, 5))
        
        self.var_typ_stravnika = tk.StringVar(value="zak") # Výchozí je žák
        
        frame_radio = tk.Frame(self.tab_objednavky)
        frame_radio.pack()
        
        tk.Radiobutton(frame_radio, text="Student (sleva 40%)", variable=self.var_typ_stravnika, value="zak").pack(side="left", padx=10)
        tk.Radiobutton(frame_radio, text="Učitel / Cizí (plná cena)", variable=self.var_typ_stravnika, value="ucitel").pack(side="left", padx=10)
        # ------------------------------------

        # Tlačítko Objednat
        btn = tk.Button(self.tab_objednavky, text="OBJEDNAT OBĚD", command=self.vytvorit_objednavku, bg="green", fg="white", font=("Arial", 12, "bold"))
        btn.pack(pady=20)
        
        # Stavový řádek (dole)
        self.lbl_status = tk.Label(self.tab_objednavky, text="", fg="#333", font=("Arial", 10))
        self.lbl_status.pack()

    def vytvorit_objednavku(self):
        jidlo_id_str = self.entry_id_objednavka.get()
        typ_stravnika = self.var_typ_stravnika.get()
        stravnik_id = 1 
        
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
            
            # 2. Logika ceny (Sleva pro studenta)
            if typ_stravnika == "zak":
                konecna_cena = plna_cena * 0.40
                text_typu = "Studentská cena"
            else:
                konecna_cena = plna_cena
                text_typu = "Plná cena"

            # 3. Potvrzovací okno (Důkaz funkčnosti)
            zprava = f"Jídlo: {nazev_jidla}\n\n{text_typu}: {konecna_cena:.0f} Kč\n(Běžná cena: {plna_cena} Kč)"
            potvrzeni = messagebox.askyesno("Potvrzení objednávky", zprava + "\n\nChcete objednat?")
            
            if potvrzeni:
                cursor.execute("INSERT INTO objednavky (datum, stravnik_id, jidlo_id) VALUES (?, ?, ?)", 
                               ("2026-02-17", stravnik_id, jidlo_id))
                conn.commit()
                self.lbl_status.config(text=f"✅ Objednáno: {nazev_jidla} za {konecna_cena:.0f} Kč", fg="green")
            else:
                self.lbl_status.config(text="❌ Objednávka zrušena", fg="red")

            conn.close()
                
        except ValueError:
             messagebox.showerror("Chyba", "ID jídla musí být číslo.")

# Spuštění aplikace
if __name__ == "__main__":
    root = tk.Tk()
    app = JidelnaApp(root)
    root.mainloop()
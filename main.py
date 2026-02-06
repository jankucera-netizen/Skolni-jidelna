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
    def setup_tab_jidla(self):
        # Formulář
        frame_form = tk.LabelFrame(self.tab_jidla, text="Přidat / Odebrat jídlo")
        frame_form.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_form, text="Název:").pack(side="left", padx=5)
        self.entry_nazev = tk.Entry(frame_form)
        self.entry_nazev.pack(side="left", padx=5)

        tk.Label(frame_form, text="Cena:").pack(side="left", padx=5)
        self.entry_cena = tk.Entry(frame_form, width=10)
        self.entry_cena.pack(side="left", padx=5)

        # Tlačítko PŘIDAT
        tk.Button(frame_form, text="Uložit", command=self.pridat_jidlo, bg="#ddd").pack(side="left", padx=10)

        # --- TLAČÍTKO SMAZAT ---
        # Je červené, aby bylo vidět, že je to destruktivní akce
        tk.Button(frame_form, text="Smazat označené", command=self.smazat_jidlo, bg="red", fg="white").pack(side="right", padx=10)

        # Tabulka
        self.tree = ttk.Treeview(self.tab_jidla, columns=("ID", "Nazev", "Cena"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nazev", text="Název jídla")
        self.tree.heading("Cena", text="Cena")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.naci_jidla()

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
        stravnik_id = 1 
        
        try:
            jidlo_id = int(jidlo_id_str)
            validni, zprava = logic.validovat_objednavku(jidlo_id, stravnik_id)
            
            if validni:
                conn = database.connect_db()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO objednavky (datum, stravnik_id, jidlo_id) VALUES (?, ?, ?)", 
                               ("2026-02-17", stravnik_id, jidlo_id))
                conn.commit()
                conn.close()
                self.lbl_status.config(text=f"✅ Objednáno! (Jídlo ID: {jidlo_id})", fg="green")
            else:
                self.lbl_status.config(text=f"❌ Chyba: {zprava}", fg="red")
                
        except ValueError:
             messagebox.showerror("Chyba", "ID jídla musí být číslo.")

if __name__ == "__main__":
    root = tk.Tk()
    app = JidelnaApp(root)
    root.mainloop()
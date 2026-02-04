import tkinter as tk
from tkinter import ttk, messagebox
import database
# import logic # Bude potreba pozdeji

class JidelnaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Školní jídelna - Skupina 7")
        self.root.geometry("800x600")

        # 1. Propojení s databází
        # Pokud ti to tady spadne, nemáš stáhnutý aktuální database.py! Dej git pull.
        database.create_tables()

        # Nadpis
        lbl_nadpis = tk.Label(root, text="Evidence jídel (Admin)", font=("Arial", 16, "bold"))
        lbl_nadpis.pack(pady=10)

        # --- SEKCE: Formulář pro přidání jídla ---
        frame_form = tk.LabelFrame(root, text="Nové jídlo")
        frame_form.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_form, text="Název jídla:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nazev = tk.Entry(frame_form)
        self.entry_nazev.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Cena (Kč):").grid(row=0, column=2, padx=5, pady=5)
        self.entry_cena = tk.Entry(frame_form)
        self.entry_cena.grid(row=0, column=3, padx=5, pady=5)

        # Tlačítko volá funkci self.pridat_jidlo
        btn_pridat = tk.Button(frame_form, text="Uložit do menu", command=self.pridat_jidlo, bg="#ddd")
        btn_pridat.grid(row=0, column=4, padx=20, pady=5)

        # --- SEKCE: Tabulka (Treeview) ---
        self.tree = ttk.Treeview(root, columns=("ID", "Nazev", "Cena"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nazev", text="Název jídla")
        self.tree.heading("Cena", text="Cena")
        
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nazev", width=400)
        self.tree.column("Cena", width=100, anchor="e")
        
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        # Načtení dat hned po spuštění
        self.naci_data()

    def pridat_jidlo(self):
        """Vezme data z políček a pošle je do databáze."""
        nazev = self.entry_nazev.get()
        cena_str = self.entry_cena.get()

        if not nazev or not cena_str:
            messagebox.showwarning("Chyba", "Vyplň název i cenu!")
            return

        try:
            cena = float(cena_str)
            
            # Práce s databází
            conn = database.connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO jidla (nazev, cena) VALUES (?, ?)", (nazev, cena))
            conn.commit()
            conn.close()
            
            # Vyčištění políček a obnovení tabulky
            self.entry_nazev.delete(0, tk.END)
            self.entry_cena.delete(0, tk.END)
            self.naci_data()
            messagebox.showinfo("OK", "Jídlo bylo úspěšně přidáno.")
            
        except ValueError:
            messagebox.showerror("Chyba", "Cena musí být číslo (např. 150)!")

    def naci_data(self):
        """Načte všechna jídla z databáze a zobrazí je v tabulce."""
        # Nejdřív smažeme staré řádky v tabulce
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        # Teď načteme nové z DB
        conn = database.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nazev, cena FROM jidla")
        rows = cursor.fetchall()
        conn.close()

        # Vložíme je do tabulky
        for row in rows:
            self.tree.insert("", tk.END, values=row)

if __name__ == "__main__":
    root = tk.Tk()
    app = JidelnaApp(root)
    root.mainloop()
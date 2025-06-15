import tkinter as tk
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect("travel_app.db")
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS korisnici (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ime TEXT UNIQUE,
    lozinka TEXT
)''')
cur.execute('''CREATE TABLE IF NOT EXISTS grupe (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    naziv TEXT,
    osnivac_id INTEGER
)''')

cur.execute('''CREATE TABLE IF NOT EXISTS clanovi_grupe (
    korisnik_id INTEGER,
    grupa_id INTEGER,
    PRIMARY KEY (korisnik_id, grupa_id)
)''')
cur.execute('''CREATE TABLE IF NOT EXISTS putovanje (
    grupa_id INTEGER PRIMARY KEY,
    grad TEXT
)''')

cur.execute('''CREATE TABLE IF NOT EXISTS glasanje (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grupa_id INTEGER,
    grad TEXT,
    korisnik_id INTEGER,
    glas TEXT CHECK(glas IN ('da', 'ne')),
    UNIQUE(grupa_id, korisnik_id)
)''')
cur.execute('''CREATE TABLE IF NOT EXISTS budzeti (
    grupa_id INTEGER,
    korisnik_id INTEGER,
    iznos REAL,
    PRIMARY KEY (grupa_id, korisnik_id)
)''')
conn.commit()


class TravelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Travel Planner")
        self.user_id = None
        self.btn_style2 = {
        "font": ("Arial", 10, "bold"),
        "bg": "#3b6ea5",  
        "fg": "white",
        "activebackground": "#5a8bd4",
        "activeforeground": "white",
        "bd": 0,
        "relief": "flat",
        "cursor": "hand2",
        "width": 12,
        "pady": 4,
        "highlightthickness": 0,
    }
        self.btn_style = {
    "font": ("Arial", 10),
    "bg": "#d3d3d3",  
    "fg": "#333333",
    "activebackground": "#bfbfbf",
    "activeforeground": "#222222",
    "bd": 1,
    "relief": "solid",
    "cursor": "hand2",
    "width": 18,
    "pady": 5,
    "highlightthickness": 0,
}
        self.btn_style1 = {
    "font": ("Arial", 10),
    "bg": "#d3d3d3",  
    "fg": "red",
    "activebackground": "#bfbfbf",
    "activeforeground": "#222222",
    "bd": 1,
    "relief": "solid",
    "cursor": "hand2",
    "width": 18,
    "pady": 5,
    "highlightthickness": 0,
}
        
        self.entry_style = {
            "font": ("Arial", 12),
            "bd": 2,
            "relief": "groove",
            "highlightthickness": 1,
        }
        self.init_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def init_login_screen(self):
        self.clear_screen()

        self.root.configure(bg="#f0f4f8")  

        tk.Label(self.root, text="Login", font=("Arial", 24, "bold"), bg="#f0f4f8", fg="#2c3e50").pack(pady=(20, 15))

        tk.Label(self.root, text="Korisničko ime", bg="#f0f4f8", fg="#34495e", font=("Arial", 12)).pack(anchor="w", padx=40)
        self.login_username = tk.Entry(self.root,  **self.entry_style)
        self.login_username.pack(padx=40, pady=(0, 15), fill="x")

        tk.Label(self.root, text="Lozinka", bg="#f0f4f8", fg="#34495e", font=("Arial", 12)).pack(anchor="w", padx=40)
        self.login_password = tk.Entry(self.root, show="*",  **self.entry_style)
        self.login_password.pack(padx=40, pady=(0, 20), fill="x")


        tk.Button(self.root, text="Prijavi se", command=self.login_user, **self.btn_style).pack(pady=(0, 10))
        tk.Button(self.root, text="Kreiranje naloga", command=self.init_register_screen, **self.btn_style).pack()

    def init_register_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Registracija", font=("Arial", 20)).pack(pady=10)

        tk.Label(self.root, text="Korisničko ime").pack()
        self.register_username = tk.Entry(self.root,  **self.entry_style)
        self.register_username.pack()

        tk.Label(self.root, text="Lozinka").pack()
        self.register_password = tk.Entry(self.root, show="*", **self.entry_style)
        self.register_password.pack()

        tk.Button(self.root, text="Registruj", command=self.register_user, **self.btn_style).pack(pady=5)
        tk.Button(self.root, text="Nazad na login", command=self.init_login_screen, **self.btn_style).pack()

    def init_main_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Glavni meni", font=("Arial", 18)).pack(pady=10)

        tk.Button(self.root, text="➕ Kreiraj grupu", command=self.kreiraj_grupu, **self.btn_style).pack(pady=5)
        tk.Button(self.root, text="👥 Pregledaj grupe", command=self.pregledaj_grupe, **self.btn_style).pack(pady=5)
        tk.Button(self.root, text="📨 Pozovi člana u grupu",command=self.pozovi_clana, **self.btn_style).pack(pady=5)
        tk.Button(self.root, text="🚪 Odjava", command=self.logout, **self.btn_style).pack(pady=20)

    def register_user(self):
        username = self.register_username.get()
        password = self.register_password.get()

        try:
            cur.execute("INSERT INTO korisnici (ime, lozinka) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Uspeh", "Registracija uspešna.")
            self.init_login_screen()
        except sqlite3.IntegrityError:
            messagebox.showerror("Greška", "Korisničko ime već postoji.")

    def login_user(self):
        username = self.login_username.get()
        password = self.login_password.get()

        cur.execute("SELECT id FROM korisnici WHERE ime=? AND lozinka=?", (username, password))
        row = cur.fetchone()
        if row:
            self.user_id = row[0]
            self.init_main_screen()
        else:
            messagebox.showerror("Greška", "Pogrešno korisničko ime ili lozinka.")

    def logout(self):
        self.user_id = None
        self.init_login_screen()

    def kreiraj_grupu(self):
        self.clear_screen()

        tk.Label(self.root, text="Unesi naziv grupe").pack()
        naziv_entry = tk.Entry(self.root, **self.entry_style)
        naziv_entry.pack()

        def sacuvaj():
            naziv = naziv_entry.get().strip()

            if not naziv:
                messagebox.showerror("Greška", "Naziv grupe ne može biti prazan.")
                return

            cur.execute("SELECT id FROM grupe WHERE naziv = ?", (naziv,))
            if cur.fetchone():
                messagebox.showerror("Greška", "Grupa sa tim imenom već postoji.")
                return

            cur.execute("INSERT INTO grupe (naziv, osnivac_id) VALUES (?, ?)", (naziv, self.user_id))
            grupa_id = cur.lastrowid
            cur.execute("INSERT INTO clanovi_grupe (korisnik_id, grupa_id) VALUES (?, ?)", (self.user_id, grupa_id))
            conn.commit()
            messagebox.showinfo("Uspeh", f"Grupa '{naziv}' je kreirana.")
            self.init_main_screen()

        tk.Button(self.root, text="Sačuvaj", command=sacuvaj, **self.btn_style).pack(pady=10)
        tk.Button(self.root, text="Nazad", command=self.init_main_screen, **self.btn_style).pack()

    def pregledaj_grupe(self):
        self.clear_screen()
        tk.Label(self.root, text="Tvoje grupe", font=("Arial", 16)).pack(pady=10)

        cur.execute('''SELECT g.id, g.naziv FROM grupe g
                       JOIN clanovi_grupe cg ON g.id = cg.grupa_id
                       WHERE cg.korisnik_id=?''', (self.user_id,))
        grupe = cur.fetchall()

        if not grupe:
            tk.Label(self.root, text="Nisi član nijedne grupe.").pack()
        else:
            for grupa_id, naziv in grupe:
                tk.Button(self.root, text=naziv, command=lambda gid=grupa_id: self.prikazi_grupu(gid), **self.btn_style2).pack(pady=2)

        tk.Button(self.root, text="Nazad", command=self.init_main_screen, **self.btn_style).pack(pady=10)

    def pozovi_clana(self):
        self.clear_screen()
        tk.Label(self.root, text="Pozivanje člana", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Naziv grupe:").pack()
        self.grupa_naziv_entry = tk.Entry(self.root, **self.entry_style)
        self.grupa_naziv_entry.pack()

        tk.Label(self.root, text="Korisničko ime za dodavanje:").pack()
        self.korisnik_entry = tk.Entry(self.root, **self.entry_style)
        self.korisnik_entry.pack()

        tk.Button(self.root, text="Pozovi", command=self.pozovi, **self.btn_style).pack(pady=5)
        tk.Button(self.root, text="Nazad", command=self.init_main_screen, **self.btn_style).pack(pady=10)

    def pozovi(self):
        naziv_grupe = self.grupa_naziv_entry.get()
        korisnicko_ime = self.korisnik_entry.get()

        cur.execute("SELECT id FROM grupe WHERE naziv=?", (naziv_grupe,))
        grupa = cur.fetchone()

        if not grupa:
            messagebox.showerror("Greška", "Grupa sa tim imenom ne postoji.")
            return

        grupa_id = grupa[0]

        cur.execute("SELECT id FROM korisnici WHERE ime=?", (korisnicko_ime,))
        korisnik = cur.fetchone()

        if not korisnik:
            messagebox.showerror("Greška", "Korisnik ne postoji.")
            return

        korisnik_id = korisnik[0]

        try:
            cur.execute("INSERT INTO clanovi_grupe (korisnik_id, grupa_id) VALUES (?, ?)", (korisnik_id, grupa_id))
            conn.commit()
            messagebox.showinfo("Uspeh", "Korisnik je uspešno dodat u grupu.")
        except sqlite3.IntegrityError:
            messagebox.showwarning("Već postoji", "Korisnik je već član te grupe.")
    def prikazi_grupu(self, grupa_id):
        self.clear_screen()

        cur.execute("SELECT naziv, osnivac_id FROM grupe WHERE id=?", (grupa_id,))
        naziv, osnivac_id = cur.fetchone()

        tk.Label(self.root, text=f"Grupa: {naziv}", font=("Arial", 16)).pack(pady=10)

        cur.execute("SELECT grad FROM putovanje WHERE grupa_id=?", (grupa_id,))
        putovanje = cur.fetchone()

        if putovanje:
            tk.Label(self.root, text=f"Potvrđeni grad za putovanje: {putovanje[0]}").pack(pady=5)
        else:
            tk.Label(self.root, text="Još nije potvrđen grad za putovanje.").pack(pady=5)

        if putovanje:
            btn_glasaj = tk.Button(self.root, text="Glasaj za grad", state="disabled", **self.btn_style)
        else:
            btn_glasaj = tk.Button(self.root, text="Glasaj za grad", command=lambda: self.ekran_glasanja(grupa_id, osnivac_id), **self.btn_style)
        tk.Button(self.root, text="💰 Budžet", command=lambda: self.ekran_budzeta(grupa_id), **self.btn_style).pack(pady=5)

        btn_glasaj.pack(pady=5)


        tk.Button(self.root, text="Prikaži sve članove", command=lambda: self.prikazi_sve_clanove(grupa_id), **self.btn_style).pack(pady=10)

        def izadji_iz_grupe():
            potvrda = messagebox.askyesno("Potvrda", "Da li ste sigurni da želite da napustite ovu grupu?")
            if potvrda:
                cur.execute("DELETE FROM clanovi_grupe WHERE korisnik_id=? AND grupa_id=?", (self.user_id, grupa_id))
                conn.commit()
                messagebox.showinfo("Obaveštenje", "Uspešno ste napustili grupu.")
                self.pregledaj_grupe()

        tk.Button(self.root, text="Izađi iz grupe", command=izadji_iz_grupe, **self.btn_style1).pack(pady=5)
        tk.Button(self.root, text="Nazad", command=self.pregledaj_grupe, **self.btn_style).pack(pady=10)
    def ekran_budzeta(self, grupa_id):
        self.clear_screen()
        tk.Label(self.root, text="Budžeti članova", font=("Arial", 16)).pack(pady=10)

        cur.execute('''
            SELECT k.id, k.ime, b.iznos
            FROM clanovi_grupe cg
            JOIN korisnici k ON cg.korisnik_id = k.id
            LEFT JOIN budzeti b ON b.korisnik_id = k.id AND b.grupa_id = cg.grupa_id
            WHERE cg.grupa_id = ?
        ''', (grupa_id,))
        clanovi = cur.fetchall()

        for korisnik_id, ime, iznos in clanovi:
            status = f"Budžet: {iznos:.2f} EUR" if iznos is not None else "❌ Nije unijet budžet"
            label_text = f"{ime}: {status}"
            tk.Label(self.root, text=label_text).pack(anchor="w", padx=20)

        cur.execute("SELECT iznos FROM budzeti WHERE grupa_id=? AND korisnik_id=?", (grupa_id, self.user_id))
        moj_budzet = cur.fetchone()

        if moj_budzet is None:
            tk.Label(self.root, text="Unesite vaš budžet:").pack(pady=10)
            budzet_entry = tk.Entry(self.root, **self.entry_style)
            budzet_entry.pack()

            def sacuvaj_budzet():
                try:
                    iznos = float(budzet_entry.get())
                    if iznos <= 0:
                        raise ValueError
                    cur.execute("INSERT INTO budzeti (grupa_id, korisnik_id, iznos) VALUES (?, ?, ?)", (grupa_id, self.user_id, iznos))
                    conn.commit()
                    messagebox.showinfo("Uspeh", "Budžet je uspješno unijet.")
                    self.ekran_budzeta(grupa_id)
                except ValueError:
                    messagebox.showerror("Greška", "Unesite ispravan pozitivan broj.")

            tk.Button(self.root, text="Sačuvaj budžet", command=sacuvaj_budzet, **self.btn_style).pack(pady=5)

        tk.Button(self.root, text="Nazad", command=lambda: self.prikazi_grupu(grupa_id), **self.btn_style).pack(pady=10)

    def prikazi_sve_clanove(self, grupa_id):
        top = tk.Toplevel(self.root)
        top.title("Članovi grupe")

        cur.execute('''
            SELECT k.ime FROM korisnici k
            JOIN clanovi_grupe cg ON k.id = cg.korisnik_id
            WHERE cg.grupa_id = ?
        ''', (grupa_id,))
        clanovi = cur.fetchall()

        tk.Label(top, text="Članovi grupe:", font=("Arial", 14)).pack(pady=10)

        for (ime,) in clanovi:
            tk.Label(top, text=ime).pack(anchor='w', padx=10)

        tk.Button(top, text="Zatvori", command=top.destroy, **self.btn_style).pack(pady=10)


    def ekran_glasanja(self, grupa_id, osnivac_id):
        self.clear_screen()

        tk.Label(self.root, text="Glasanje za grad", font=("Arial", 16)).pack(pady=10)

        cur.execute("SELECT grad FROM putovanje WHERE grupa_id=?", (grupa_id,))
        putovanje = cur.fetchone()
        if putovanje:
            tk.Label(self.root, text=f"Putovanje je već potvrđeno za grad: {putovanje[0]}").pack(pady=10)
            tk.Button(self.root, text="Nazad", command=lambda: self.prikazi_grupu(grupa_id), **self.btn_style).pack(pady=10)
            return

        cur.execute("SELECT DISTINCT grad FROM glasanje WHERE grupa_id=?", (grupa_id,))
        glasanje_gradovi = cur.fetchall()

        if not glasanje_gradovi:
            if self.user_id == osnivac_id:
                tk.Label(self.root, text="Nema aktivnog glasanja.").pack(pady=5)
                tk.Label(self.root, text="Unesi ime grada za glasanje:").pack()
                self.grad_entry = tk.Entry(self.root, **self.entry_style)
                self.grad_entry.pack()

                def kreiraj_glasanje():
                    grad = self.grad_entry.get().strip()
                    if not grad:
                        messagebox.showerror("Greška", "Unesite ime grada.")
                        return
                    cur.execute("DELETE FROM glasanje WHERE grupa_id=?", (grupa_id,))
                    cur.execute("INSERT INTO glasanje (grupa_id, grad, korisnik_id, glas) VALUES (?, ?, ?, ?)",
                                (grupa_id, grad, self.user_id, 'da'))
                    conn.commit()
                    messagebox.showinfo("Uspeh", f"Glasanje za grad '{grad}' je kreirano i tvoj glas je upisan.")
                    self.ekran_glasanja(grupa_id, osnivac_id)

                tk.Button(self.root, text="Kreiraj glasanje", command=kreiraj_glasanje, **self.btn_style).pack(pady=10)
                tk.Button(self.root, text="Nazad", command=lambda: self.prikazi_grupu(grupa_id), **self.btn_style).pack(pady=10)
            else:
                tk.Label(self.root, text="Nema aktivnog glasanja. Sačekajte da osnivač kreira glasanje.").pack(pady=10)
                tk.Button(self.root, text="Nazad", command=lambda: self.prikazi_grupu(grupa_id), **self.btn_style).pack(pady=10)
            return

        grad = glasanje_gradovi[0][0]

        tk.Label(self.root, text=f"Glasa se za grad: {grad}").pack(pady=5)

        cur.execute("SELECT glas FROM glasanje WHERE grupa_id=? AND korisnik_id=?", (grupa_id, self.user_id))
        moj_glas = cur.fetchone()

        if moj_glas:
            tk.Label(self.root, text=f"Već ste glasali sa odgovorom: {moj_glas[0]}").pack(pady=10)
        else:
            def glasaj_odgovor(odgovor):
                try:
                    cur.execute("INSERT INTO glasanje (grupa_id, grad, korisnik_id, glas) VALUES (?, ?, ?, ?)",
                                (grupa_id, grad, self.user_id, odgovor))
                    conn.commit()
                    messagebox.showinfo("Uspeh", "Vaš glas je upisan.")
                    self.ekran_glasanja(grupa_id, osnivac_id)
                except sqlite3.IntegrityError:
                    messagebox.showwarning("Greška", "Već ste glasali.")

            tk.Button(self.root, text="Da", command=lambda: glasaj_odgovor("da"), **self.btn_style).pack(pady=5)
            tk.Button(self.root, text="Ne", command=lambda: glasaj_odgovor("ne"), **self.btn_style).pack(pady=5)

        if self.user_id == osnivac_id:
            cur.execute("SELECT COUNT(*) FROM glasanje WHERE grupa_id=? AND grad=? AND glas='da'", (grupa_id, grad))
            da_count = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM glasanje WHERE grupa_id=? AND grad=? AND glas='ne'", (grupa_id, grad))
            ne_count = cur.fetchone()[0]

            tk.Label(self.root, text=f"Rezultati glasanja: Da = {da_count}, Ne = {ne_count}").pack(pady=10)

            def potvrdi_putovanje():
                if da_count > ne_count:
                    cur.execute("INSERT OR REPLACE INTO putovanje (grupa_id, grad) VALUES (?, ?)", (grupa_id, grad))
                    cur.execute("DELETE FROM glasanje WHERE grupa_id=?", (grupa_id,))
                    conn.commit()
                    messagebox.showinfo("Uspeh", f"Putovanje za grad '{grad}' je potvrđeno.")
                    self.prikazi_grupu(grupa_id)
                else:
                    messagebox.showwarning("Neuspeh", "Grad nema dovoljnu podršku za potvrdu.")

            tk.Button(self.root, text="Potvrdi putovanje", command=potvrdi_putovanje, **self.btn_style).pack(pady=10)

        tk.Button(self.root, text="Nazad", command=lambda: self.prikazi_grupu(grupa_id), **self.btn_style).pack(pady=10)

root = tk.Tk()
root.geometry("300x300")
app = TravelApp(root)
root.mainloop()

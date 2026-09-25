"""Local card browser from the TradeIt course prototype."""

import tkinter as tk
from tkinter import ttk

from catalog import CardCatalog


BG = "#263241"
PANEL = "#253240"
TEXT = "#ffffff"
ACCENT = "#6593b5"


class TradeItApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.catalog = CardCatalog()
        self.cards = {}
        self.saved = set()
        self.title("TradeIt · Kartenkatalog")
        self.geometry("820x620")
        self.minsize(600, 440)
        self.configure(bg=BG)

        tk.Label(self, text="TradeIt", bg=BG, fg=TEXT, font=("Arial", 24, "bold")).pack(
            anchor="w", padx=20, pady=(18, 2)
        )
        tk.Label(
            self, text="Kartenkatalog · lokaler Unterrichtsprototyp", bg=BG,
            fg="#c9d5df", font=("Arial", 11)
        ).pack(anchor="w", padx=20)

        filters = tk.Frame(self, bg=BG)
        filters.pack(fill="x", padx=20, pady=18)
        self.query = tk.StringVar()
        search_entry = ttk.Entry(filters, textvariable=self.query)
        search_entry.pack(side="left", fill="x", expand=True)
        search_entry.bind("<Return>", lambda _event: self.refresh())
        self.card_type = tk.StringVar(value="Alle Typen")
        types = ttk.Combobox(
            filters, textvariable=self.card_type, state="readonly",
            values=["Alle Typen", *self.catalog.types()], width=18
        )
        types.pack(side="left", padx=(10, 0))
        types.bind("<<ComboboxSelected>>", lambda _event: self.refresh())
        ttk.Button(filters, text="Suchen", command=self.refresh).pack(side="left", padx=(10, 0))

        columns = ("number", "name", "type", "rarity")
        self.table = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse")
        for key, label, width in (
            ("number", "Nr.", 90), ("name", "Karte", 240),
            ("type", "Typ", 120), ("rarity", "Seltenheit", 120)
        ):
            self.table.heading(key, text=label)
            self.table.column(key, width=width, stretch=key == "name")
        self.table.pack(fill="both", expand=True, padx=20)
        self.table.bind("<<TreeviewSelect>>", self.show_selection)

        details = tk.Frame(self, bg=BG)
        details.pack(fill="x", padx=20, pady=12)
        self.detail_text = tk.StringVar(value="Wähle eine Karte aus.")
        tk.Label(
            details, textvariable=self.detail_text, bg=BG, fg=TEXT,
            justify="left", wraplength=560
        ).pack(side="left", fill="x", expand=True)
        ttk.Button(details, text="Merken", command=self.save_selection).pack(side="right")

        self.status = tk.StringVar()
        tk.Label(self, textvariable=self.status, bg=PANEL, fg=TEXT, anchor="w", padx=20).pack(
            fill="x", side="bottom", ipady=8
        )
        self.refresh()

    def refresh(self):
        card_type = self.card_type.get()
        if card_type == "Alle Typen":
            card_type = ""
        try:
            cards = self.catalog.search(self.query.get(), card_type)
        except ValueError as error:
            self.status.set(str(error))
            return
        self.table.delete(*self.table.get_children())
        self.cards = {str(card["id"]): card for card in cards}
        for card in cards:
            self.table.insert(
                "", "end", iid=str(card["id"]),
                values=(card["number"], card["name"], card["card_type"], card["rarity"])
            )
        self.detail_text.set("Wähle eine Karte aus.")
        self.status.set(f"{len(cards)} Karten · {len(self.saved)} lokal gemerkt")

    def show_selection(self, _event=None):
        selected = self.table.selection()
        if not selected:
            return
        card = self.cards[selected[0]]
        note = f" · {card['notes']}" if card["notes"] else ""
        self.detail_text.set(
            f"{card['name']} · {card['number']} · {card['condition']}"
            f"{' · Holo' if card['is_holo'] else ''}{note}"
        )

    def save_selection(self):
        selected = self.table.selection()
        if not selected:
            self.status.set("Wähle zuerst eine Karte aus.")
            return
        self.saved.add(selected[0])
        self.status.set(f"{len(self.saved)} Karten lokal gemerkt (nur für diese Sitzung)")


if __name__ == "__main__":
    TradeItApp().mainloop()

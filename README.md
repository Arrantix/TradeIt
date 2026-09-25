# TradeIt

Ein früher Unterrichtsprototyp zum Durchsuchen eines lokalen Pokémon-Kartenkatalogs. Die Python-Oberfläche bietet eine Suche nach Name oder Nummer, einen Typfilter und eine Merkliste für die laufende Sitzung. Ein echter Handel oder Benutzerkonten sind **nicht** implementiert.

## Starten

```sh
python app.py
```

Benötigt Python 3.10+ mit Tkinter; weitere Pakete sind nicht nötig. Die Oberfläche liest `pokemon_base_set.db` ausschließlich im Lesemodus. Die Datenbank mit 102 Karten wurde **bytegenau unverändert** aus dem Unterrichtsprojekt übernommen. Es werden keine persönlichen Nutzerinformationen gespeichert.

Die größere `cardmarket.db` und ihre CSV-Quelle waren im vorhandenen Oberflächen-Prototyp nicht eingebunden und gehören nicht zu dieser kuratierten Fassung.

Tests: `python -m unittest discover -s tests`.

**Stand:** Lokaler Katalog-Prototyp. Die Merkliste wird beim Schließen verworfen; es gibt keine Verbindung zu einem Marktplatz.

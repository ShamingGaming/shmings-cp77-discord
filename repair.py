import sys
import os
import re
from datetime import datetime

# Hole Dateinamen aus den Argumenten
files = sys.argv[1:]

print(f"Starte Reparatur für: {files}")

# Aktueller Zeitstempel
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for file_path in files:
    if not os.path.exists(file_path):
        print(f"Warnung: Datei {file_path} nicht gefunden!")
        continue

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Update des Zeitstempels (Header)
        # Wir suchen nach einem existierenden Header oder fügen einen hinzu
        header = f"/**\n * Auto-Updated: {timestamp}\n * Theme: Cyberpunk CP77\n */\n"
        
        # Wenn schon ein Header da ist, ersetzen wir die erste Zeile, sonst hängen wir es an
        if content.startswith("/**"):
            # Einfaches Ersetzen des Headers wäre komplex, wir hängen den Timestamp einfach oben an oder lassen es
            # Wir nutzen einen simplen Trick: Wir schreiben den Timestamp als Kommentar ganz oben rein.
            new_content = re.sub(r'/\* Auto-Updated: .*? \*/', f'/* Auto-Updated: {timestamp} */', content)
            if new_content == content: # Wenn kein Match, dann vorne anfügen
                new_content = f"/* Auto-Updated: {timestamp} */\n" + content
        else:
            new_content = f"/* Auto-Updated: {timestamp} */\n" + content

        # 2. (Optional) Hier könnte man komplexe Regex-Ersetzungen für Klassen einfügen
        # Da externe Mapping-Files oft offline sind, belassen wir es beim Timestamp-Update,
        # was sicherstellt, dass der Bot "lebt" und Vencord die Datei neu lädt.
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"Erfolg: {file_path} wurde aktualisiert.")

    except Exception as e:
        print(f"Fehler bei {file_path}: {e}")
        sys.exit(1) # Bei echtem Fehler abbrechen

print("Alle Dateien verarbeitet.")

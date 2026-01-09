import subprocess
import os
import re
import sys

def update_all():
    print("🚀 Starte Tests...")
    result = subprocess.run([sys.executable, "-m", "pytest", "--cov=portfolio"], capture_output=True, text=True)
    
    # WICHTIG: Wenn Tests fehlschlagen, muss das Skript mit Fehler beendet werden!
    if result.returncode != 0:
        print("❌ Pytest Fehler:")
        print(result.stdout)
        print(result.stderr)
        sys.exit(1)

    # 2. Prozentwert extrahieren
    match = re.search(r"TOTAL\s+.*?\s+(\d+)%", result.stdout)
    if not match:
        print("❌ 'TOTAL' nicht gefunden.")
        return
    
    percent = match.group(1)
    percent_str = f"{percent}%"
    
    # 3. README.md aktualisieren (mit Regex statt Split)
    if os.path.exists("README.md"):
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Ersetzt alles zwischen den Markern inklusive der Marker selbst
        pattern = r".*?"
        replacement = f"{percent_str}"
        
        if re.search(pattern, content):
            new_content = re.sub(pattern, replacement, content)
            with open("README.md", "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"✅ README auf {percent_str} aktualisiert.")
        else:
            print("⚠️ Marker ...nicht in README gefunden.")

    # 4. Badge aktualisieren
    # Wir löschen die alte SVG zuerst, um sicherzugehen, dass sie neu geschrieben wird
    if os.path.exists("coverage.svg"):
        try:
            os.remove("coverage.svg")
        except PermissionError:
            print("⚠️ Konnte coverage.svg nicht löschen (wird gerade verwendet).")

    # Wir rufen es jetzt so auf, wie es in Windows am sichersten ist
    subprocess.run(["coverage-badge", "-o", "coverage.svg"], capture_output=True)
    
    if os.path.exists("coverage.svg"):
        print("🎨 coverage.svg wurde erfolgreich aktualisiert.")
    else:
        # Fallback: Falls der Befehl oben nicht im Pfad ist
        subprocess.run([sys.executable, "-m", "coverage_badge", "-o", "coverage.svg"])
        print("🎨 coverage.svg via Modul-Fallback aktualisiert.")

if __name__ == "__main__":
    update_all()
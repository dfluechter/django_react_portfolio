import os
import re
import sys

# Konfiguration
README_PATH = "README.md"
SVG_PATH = "coverage.svg"

def get_coverage_from_svg():
    """Liest die Coverage-Prozentzahl aus der coverage.svg aus."""
    if not os.path.exists(SVG_PATH):
        print(f"⚠️ {SVG_PATH} nicht gefunden. Setze auf 0%.")
        return 0
    
    with open(SVG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        # Sucht nach >94%< oder ähnlichem im SVG XML
        match = re.search(r'>(\d+)%<', content)
        if match:
            return int(match.group(1))
    return 0

def get_badge_color(coverage):
    """Bestimmt die Farbe des Badges basierend auf der Coverage."""
    if coverage >= 90: return "green"
    if coverage >= 75: return "yellow"
    return "red"

def update_readme():
    coverage = get_coverage_from_svg()
    color = get_badge_color(coverage)
    
    # Der neue Badge-String (Shields.io Format)
    # URL-Encoding für % ist %25
    new_badge = f"![Coverage](https://img.shields.io/badge/coverage-{coverage}%25-{color})"
    
    if not os.path.exists(README_PATH):
        print(f"❌ {README_PATH} nicht gefunden!")
        return

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex, um einen existierenden Coverage-Badge zu finden (egal welche % oder Farbe)
    # Matcht z.B.: ![Coverage](https://img.shields.io/badge/coverage-88%25-green)
    badge_pattern = r"!\[Coverage\]\(https:\/\/img\.shields\.io\/badge\/coverage-\d+%25-[a-z]+\)"
    
    if re.search(badge_pattern, content):
        # Update: Vorhandenen Badge ersetzen
        new_content = re.sub(badge_pattern, new_badge, content)
    else:
        # Neu: Wenn kein Badge da ist, fügen wir ihn nach der Überschrift ein
        print("ℹ️ Kein Coverage-Badge gefunden. Erstelle neuen Badge.")
        if "# Portfolio" in content:
            new_content = content.replace("# Portfolio", f"# Portfolio\n\n{new_badge}")
        else:
            # Fallback: Einfach ganz oben einfügen
            new_content = f"{new_badge}\n\n{content}"

    # Nur schreiben, wenn sich was geändert hat
    if new_content != content:
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"✅ README auf {coverage}% aktualisiert.")
    else:
        print("✅ README ist bereits aktuell.")

if __name__ == "__main__":
    update_readme()
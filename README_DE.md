# Babel - Echtzeit-Audio-Übersetzung mit Untertitel-Overlay

**[English](README.md) | [Español](README_ES.md) | [Français](README_FR.md) | Deutsch | [日本語](README_JA.md) | [한국어](README_KO.md) | [中文](README_ZH.md)**

Eine Python-Anwendung, die das interne Audio Ihres PCs erfasst, es in Echtzeit mit Faster-Whisper und Google Translate übersetzt und übersetzte Untertitel als Overlay auf Ihrem Bildschirm anzeigt.

## Funktionen

### 🎵 **Audio-Erfassung**
- **Auto-Erkennung**: Findet automatisch das beste Loopback-Gerät (Stereo Mix, Virtual Audio Cable)
- **Manuelle Auswahl**: Wählen Sie aus verfügbaren Eingabegeräten mit Gerätedetails
- **App-spezifische Erfassung**: Unterstützung für Virtual Audio Cable zur Erfassung einzelner Anwendungen
- **System-Audio**: Erfassung aller PC-Audio oder spezifischer Anwendungsaudio

### 🧠 **KI-gestützte Übersetzung**
- **Spracherkennung**: Verwendet Faster-Whisper-Modelle (tiny, turbo, large-v3, distil-large-v3)
- **Automatische Spracherkennung**: Lassen Sie Whisper automatisch die Quellsprache erkennen
- **90+ Quellsprachen**: Unterstützung für alle Hauptsprachen, die Whisper transkribieren kann
- **100+ Zielsprachen**: Übersetzen in jede von Google Translate unterstützte Sprache
- **Echtzeit-Verarbeitung**: Optimiert für niedrige Latenz und Speicherverbrauch

### 📺 **Professionelle Untertitel**
- **Overlay-Anzeige**: Transparentes, immer im Vordergrund befindliches Untertitel-Overlay
- **Anpassbare Schriftarten**: Wählen Sie aus 10 beliebten Schriftarten und mehreren Größen
- **Neu positionierbar**: Ziehen Sie Untertitel an jede Position auf dem Bildschirm
- **Auto-Löschung**: Untertitel verschwinden automatisch bei Stille
- **Modernes Design**: Halbtransparenter Hintergrund mit Textumrissen für Lesbarkeit

### ⚙️ **Intelligente Einstellungen**
- **Persistente Konfiguration**: Alle Einstellungen automatisch in `babel_settings.json` gespeichert
- **Leistungsmodus**: Wechseln zwischen Geschwindigkeit und Genauigkeit
- **Audio-Empfindlichkeit**: Einstellbarer Schwellenwert zum Filtern von Hintergrundgeräuschen
- **Alphabetische Navigation**: Tippen Sie Buchstaben in Dropdown-Menüs, um Optionen schnell zu finden

## Anforderungen

- **Python**: 3.9 oder höher
- **Betriebssystem**: Windows (für WASAPI Loopback-Audio-Erfassung)
- **Speicher**: Mindestens 4GB RAM (8GB empfohlen für große Modelle)
- **Speicherplatz**: 1-5GB für Whisper-Modelle (automatisch heruntergeladen)

## Installation

1. **Klonen oder herunterladen** Sie dieses Repository
2. **Installieren Sie Abhängigkeiten**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Führen Sie die Anwendung aus**:
   ```bash
   python main.py
   ```

## Schnellstart-Anleitung

### Grundeinrichtung
1. **Starten** Sie die Anwendung: `python main.py`
2. **Audio-Eingang**: Wählen Sie "Auto (Empfohlen)" oder wählen Sie ein spezifisches Gerät
3. **Sprachen**: 
   - **Von**: Wählen Sie Quellsprache oder "Auto-Erkennung"
   - **Nach**: Wählen Sie Zielsprache (Standard Englisch)
4. **Klicken** Sie "▶️ Übersetzung starten"

### Erste Einrichtung Tipps
- **Audio testen**: Sprechen oder spielen Sie Audio ab, um zu überprüfen, ob Mikrofon/System-Audio funktioniert
- **Empfindlichkeit anpassen**: Niedrigere Werte = empfindlicher für leise Audio
- **Untertitel positionieren**: Verwenden Sie "⚙ Untertitel neu positionieren", um sie zu platzieren, wo Sie möchten
- **Modell wählen**: "turbo" wird für ausgewogene Geschwindigkeit/Genauigkeit empfohlen
- **Schnelle Sprachauswahl**: Tippen Sie Buchstaben in Sprachmenüs, um zu Optionen zu springen (z.B. tippen Sie "D" für Deutsch)
- **Alle Einstellungen gespeichert**: Ihre Präferenzen werden automatisch zwischen Sitzungen gespeichert

## Unterstützte Sprachen

### Quellsprachen (Whisper-Erkennung)
**Auto-Erkennung**, Afrikaans, Albanisch, Amharisch, Arabisch, Armenisch, Assamesisch, Aserbaidschanisch, Baschkirisch, Baskisch, Weißrussisch, Bengali, Bosnisch, Bretonisch, Bulgarisch, Birmanisch, Katalanisch, Chinesisch, Kroatisch, Tschechisch, Dänisch, Niederländisch, Englisch, Estnisch, Färöisch, Finnisch, Französisch, Galicisch, Georgisch, Deutsch, Griechisch, Gujarati, Haitianisch, Hausa, Hawaiisch, Hebräisch, Hindi, Ungarisch, Isländisch, Indonesisch, Italienisch, Japanisch, Javanisch, Kannada, Kasachisch, Khmer, Koreanisch, Laotisch, Lateinisch, Lettisch, Litauisch, Luxemburgisch, Mazedonisch, Madagassisch, Malaiisch, Malayalam, Maltesisch, Maori, Marathi, Mongolisch, Nepalesisch, Norwegisch, Okzitanisch, Paschtu, Persisch, Polnisch, Portugiesisch, Punjabi, Rumänisch, Russisch, Sanskrit, Serbisch, Shona, Sindhi, Singhalesisch, Slowakisch, Slowenisch, Somali, Spanisch, Sundanesisch, Suaheli, Schwedisch, Tagalog, Tadschikisch, Tamil, Tatarisch, Telugu, Thailändisch, Tibetisch, Türkisch, Turkmenisch, Ukrainisch, Urdu, Usbekisch, Vietnamesisch, Walisisch, Jiddisch, Yoruba

### Zielsprachen (Google Translate)
**Deutsch** (Standard), Afrikaans, Albanisch, Amharisch, Arabisch, Armenisch, Aserbaidschanisch, Baskisch, Weißrussisch, Bengali, Bosnisch, Bulgarisch, Katalanisch, Cebuano, Chinesisch (Vereinfacht), Chinesisch (Traditionell), Korsisch, Kroatisch, Tschechisch, Dänisch, Niederländisch, Esperanto, Estnisch, Finnisch, Französisch, Friesisch, Galicisch, Georgisch, Deutsch, Griechisch, Gujarati, Haitianisches Kreol, Hausa, Hawaiisch, Hebräisch, Hindi, Hmong, Ungarisch, Isländisch, Igbo, Indonesisch, Irisch, Italienisch, Japanisch, Javanisch, Kannada, Kasachisch, Khmer, Koreanisch, Kurdisch, Kirgisisch, Laotisch, Lateinisch, Lettisch, Litauisch, Luxemburgisch, Mazedonisch, Madagassisch, Malaiisch, Malayalam, Maltesisch, Maori, Marathi, Mongolisch, Myanmar (Birmanisch), Nepalesisch, Norwegisch, Odia (Oriya), Paschtu, Persisch, Polnisch, Portugiesisch, Punjabi, Rumänisch, Russisch, Samoanisch, Schottisch-Gälisch, Serbisch, Sesotho, Shona, Sindhi, Singhalesisch, Slowakisch, Slowenisch, Somali, Spanisch, Sundanesisch, Suaheli, Schwedisch, Tagalog, Tadschikisch, Tamil, Tatarisch, Telugu, Thailändisch, Türkisch, Turkmenisch, Ukrainisch, Urdu, Uigurisch, Usbekisch, Vietnamesisch, Walisisch, Xhosa, Jiddisch, Yoruba, Zulu

## Neueste Funktionen und Updates

### 🆕 **Verbesserte Benutzererfahrung** 
- **Alle Einstellungen automatisch gespeichert**: Jede Konfiguration automatisch in `babel_settings.json` gespeichert
- **Alphabetische Navigation**: Tippen Sie Buchstaben in Dropdown-Menüs, um schnell zu Sprachen zu springen
- **Verbesserte UI**: Modernes dunkles Theme mit besserem Abstand und visueller Rückmeldung
- **Intelligente Standards**: Zielsprache Englisch, Turbo-Modell vorausgewählt

### 🎨 **Erweiterte Untertitel-Anpassung**
- **10 Schriftoptionen**: Segoe UI, Arial, Helvetica, Times New Roman und mehr
- **13 Schriftgrößen**: Von 10px bis 48px für perfekte Sichtbarkeit
- **Ziehen zur Positionierung**: Klicken Sie "⚙ Untertitel neu positionieren" und ziehen Sie an jede Bildschirmposition
- **Auto-Löschung**: Untertitel verschwinden nach 2 Sekunden Stille
- **Modernes Design**: Halbtransparente Hintergründe mit Textumrissen

---

**Babel** - Echtzeit-Übersetzung für alle zugänglich machen! Perfekt für internationale Spiele, das Ansehen fremdsprachiger Inhalte oder das Erlernen neuer Sprachen!

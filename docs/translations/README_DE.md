# Babel - Echtzeit-Audio-Übersetzung mit Untertitel-Overlay

**[English](../../README.md) | [Español](README_ES.md) | [Français](README_FR.md) | Deutsch | [Português](README_PT.md) | [日本語](README_JA.md) | [한국어](README_KO.md) | [中文](README_ZH.md)**

Eine Python-Anwendung, die das interne Audio Ihres PCs erfasst, es in Echtzeit mit Faster-Whisper und Google Translate übersetzt und übersetzte Untertitel als Overlay auf Ihrem Bildschirm anzeigt.

## 🌟 Funktionen

### 🎵 **Audio-Erfassung**
- **Automatische Erkennung**: Findet automatisch das beste Loopback-Gerät (Stereo Mix, Virtual Audio Cable)
- **Manuelle Auswahl**: Wählen Sie aus verfügbaren Eingabegeräten mit Gerätedetails
- **App-spezifische Erfassung**: Unterstützung für Virtual Audio Cable zur Erfassung einzelner Anwendungen
- **System-Audio**: Erfassen Sie das gesamte PC-Audio oder spezifisches Anwendungsaudio

### 🧠 **KI-gestützte Übersetzung**
- **Spracherkennung**: Verwendet Faster-Whisper-Modelle (tiny, turbo, large-v3, distil-large-v3)
- **Automatische Spracherkennung**: Lassen Sie Whisper die Quellsprache automatisch erkennen
- **90+ Quellsprachen**: Unterstützung für alle wichtigen Sprachen, die Whisper transkribieren kann
- **100+ Zielsprachen**: Übersetzt in jede von Google Translate unterstützte Sprache
- **Echtzeit-Verarbeitung**: Optimiert für niedrige Latenz und Speicherverbrauch

### 📺 **Professionelle Untertitel**
- **Overlay-Anzeige**: Transparentes, immer im Vordergrund befindliches Untertitel-Overlay
- **Anpassbare Schriftarten**: Wählen Sie aus 10 beliebten Schriftarten und mehreren Größen (10px-48px)
- **Repositionierbar**: Ziehen Sie Untertitel an jede Position auf dem Bildschirm
- **Automatisches Löschen**: Untertitel verschwinden automatisch bei Stille
- **Modernes Design**: Halbtransparenter Hintergrund mit Textumrissen für Lesbarkeit

### 🌍 **Mehrsprachige Benutzeroberfläche**
- **6 UI-Sprachen**: Englisch, Spanisch, Französisch, Deutsch, Portugiesisch, Koreanisch
- **Vollständige Lokalisierung**: Alle Menüs, Schaltflächen, Beschreibungen und Sprachnamen übersetzt
- **Dynamischer Wechsel**: Ändern Sie die Oberflächensprache und sehen Sie sofortige Updates
- **Sprachspezifische Dropdowns**: Sprachnamen werden in der aktuellen Oberflächensprache angezeigt

### ⚙️ **Intelligente Einstellungen**
- **Persistente Konfiguration**: Alle Einstellungen automatisch in `babel_settings.json` gespeichert
- **Leistungsmodus**: Wechseln Sie zwischen Geschwindigkeit und Genauigkeit
- **Audio-Empfindlichkeit**: Einstellbarer Schwellenwert zum Filtern von Hintergrundgeräuschen
- **Alphabetische Navigation**: Tippen Sie Buchstaben in Dropdowns, um Optionen schnell zu finden

## 📋 Anforderungen

- **Python**: 3.9 oder höher
- **Betriebssystem**: Windows (für WASAPI-Loopback-Audio-Erfassung)
- **Speicher**: Mindestens 4GB RAM (8GB empfohlen für große Modelle)
- **Speicherplatz**: 1-5GB für Whisper-Modelle (automatisch heruntergeladen)
- **Internet**: Erforderlich für Google Translate API

## 🚀 Installation

1. **Klonen oder herunterladen** Sie dieses Repository
2. **Abhängigkeiten installieren**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Anwendung ausführen**:
   ```bash
   python main.py
   ```
   Oder verwenden Sie die bereitgestellte Batch-Datei:
   ```bash
   run.bat
   ```

## 📖 Schnellstart-Anleitung

### Grundkonfiguration
1. **Starten** Sie die Anwendung: `python main.py`
2. **Audio-Eingabe**: Wählen Sie "Auto (Empfohlen)" oder ein spezifisches Gerät
3. **Sprachen**: 
   - **Von**: Wählen Sie Quellsprache oder "Automatisch erkennen"
   - **Zu**: Wählen Sie Zielsprache (Standard: Englisch)
4. **Klicken** Sie "▶️ Übersetzung starten"

### Tipps für die Ersteinrichtung
- **Audio testen**: Sprechen Sie oder spielen Sie Audio ab, um zu überprüfen, ob Mikrofon/System-Audio funktioniert
- **Empfindlichkeit anpassen**: Niedrigere Werte = empfindlicher für leises Audio
- **Untertitel positionieren**: Verwenden Sie "⚙ Untertitel repositionieren", um sie zu platzieren, wo Sie möchten
- **Modell wählen**: "turbo" wird für ausgewogene Geschwindigkeit/Genauigkeit empfohlen
- **Schnelle Sprachauswahl**: Tippen Sie Buchstaben in Sprach-Dropdowns, um zu Optionen zu springen (z.B. tippen Sie "E" für Englisch)
- **Alle Einstellungen gespeichert**: Ihre Präferenzen werden automatisch zwischen Sitzungen gespeichert

## 🌍 Sprachen der Benutzeroberfläche

Babel unterstützt die folgenden Sprachen für die Benutzeroberfläche:
- **Englisch** (Standard)
- **Spanisch** (Español)
- **Französisch** (Français) 
- **Deutsch** (Standard)
- **Portugiesisch** (Português)
- **Koreanisch** (한국어)

Ändern Sie die UI-Sprache auf der "⚙ Einstellungen"-Seite mit dem "UI-Sprache"-Dropdown. Alle Menüs, Schaltflächen, Beschreibungen, Tooltips und Sprachnamen werden in Ihrer gewählten Sprache angezeigt.

## 🗣️ Unterstützte Sprachen

### Quellsprachen (Whisper-Erkennung)
**Automatisch erkennen**, Afrikaans, Albanisch, Amharisch, Arabisch, Armenisch, Assamesisch, Aserbaidschanisch, Baschkirisch, Baskisch, Weißrussisch, Bengali, Bosnisch, Bretonisch, Bulgarisch, Birmanisch, Katalanisch, Chinesisch, Kroatisch, Tschechisch, Dänisch, Niederländisch, Englisch, Estnisch, Färöisch, Finnisch, Französisch, Galicisch, Georgisch, Deutsch, Griechisch, Gujarati, Haitianisch, Hausa, Hawaiianisch, Hebräisch, Hindi, Ungarisch, Isländisch, Indonesisch, Italienisch, Japanisch, Javanisch, Kannada, Kasachisch, Khmer, Koreanisch, Laotisch, Lateinisch, Lettisch, Litauisch, Luxemburgisch, Mazedonisch, Madagassisch, Malaiisch, Malayalam, Maltesisch, Maori, Marathi, Mongolisch, Nepalesisch, Norwegisch, Okzitanisch, Paschtu, Persisch, Polnisch, Portugiesisch, Punjabi, Rumänisch, Russisch, Sanskrit, Serbisch, Shona, Sindhi, Singhalesisch, Slowakisch, Slowenisch, Somali, Spanisch, Sundanesisch, Suaheli, Schwedisch, Tagalog, Tadschikisch, Tamil, Tatarisch, Telugu, Thailändisch, Tibetisch, Türkisch, Turkmenisch, Ukrainisch, Urdu, Usbekisch, Vietnamesisch, Walisisch, Jiddisch, Yoruba

### Zielsprachen (Google Translate)
**Englisch** (Standard), Afrikaans, Albanisch, Amharisch, Arabisch, Armenisch, Aserbaidschanisch, Baskisch, Weißrussisch, Bengali, Bosnisch, Bulgarisch, Katalanisch, Cebuano, Chinesisch (Vereinfacht), Chinesisch (Traditionell), Korsisch, Kroatisch, Tschechisch, Dänisch, Niederländisch, Esperanto, Estnisch, Finnisch, Französisch, Friesisch, Galicisch, Georgisch, Deutsch, Griechisch, Gujarati, Haitianisches Kreol, Hausa, Hawaiianisch, Hebräisch, Hindi, Hmong, Ungarisch, Isländisch, Igbo, Indonesisch, Irisch, Italienisch, Japanisch, Javanisch, Kannada, Kasachisch, Khmer, Koreanisch, Kurdisch, Kirgisisch, Laotisch, Lateinisch, Lettisch, Litauisch, Luxemburgisch, Mazedonisch, Madagassisch, Malaiisch, Malayalam, Maltesisch, Maori, Marathi, Mongolisch, Birmanisch (Birmanisch), Nepalesisch, Norwegisch, Odia (Oriya), Paschtu, Persisch, Polnisch, Portugiesisch, Punjabi, Rumänisch, Russisch, Samoanisch, Schottisches Gälisch, Serbisch, Sesotho, Shona, Sindhi, Singhalesisch, Slowakisch, Slowenisch, Somali, Spanisch, Sundanesisch, Suaheli, Schwedisch, Tagalog, Tadschikisch, Tamil, Tatarisch, Telugu, Thailändisch, Türkisch, Turkmenisch, Ukrainisch, Urdu, Uigurisch, Usbekisch, Vietnamesisch, Walisisch, Xhosa, Jiddisch, Yoruba, Zulu

## ⚙️ Konfigurationsoptionen

### Audio-Einstellungen
- **Geräteauswahl**: Automatische Erkennung oder manuelle Geräteauswahl
- **Audio-Empfindlichkeit**: 0.001-0.100 Schwellenwert für Rauschfilterung
- **Leistungsmodus**: Umschalten für optimierte Geschwindigkeit vs. Genauigkeit

### KI-Modelle
- **tiny**: Schnellstes, grundlegende Genauigkeit (~40MB)
- **turbo**: Ausgewogene Geschwindigkeit/Genauigkeit (~810MB) - **Empfohlen**
- **large-v3**: Höchste Genauigkeit, langsamer (~3GB)
- **distil-large-v3**: Optimiertes großes Modell (~1.5GB)

### Untertitel-Aussehen
- **Schriftfamilie**: Segoe UI, Arial, Helvetica, Times New Roman, Calibri, Trebuchet MS, Verdana, Georgia, Comic Sans MS, Impact
- **Schriftgröße**: 10px bis 48px
- **Position**: Ziehen zum Repositionieren überall auf dem Bildschirm
- **Automatisches Löschen**: Untertitel verschwinden nach 2 Sekunden Stille

## 🎯 Anleitung für App-spezifische Audio-Erfassung

### Für einzelne Anwendungen
1. **Virtual Audio Cable installieren** (VB-Cable oder ähnlich)
2. **Anwendungs-Audio-Ausgabe auf Virtual Cable einstellen**
3. **In Babel**: Virtual Cable-Gerät auswählen (markiert mit 🎯)
4. **Übersetzung starten** - jetzt wird nur das Audio dieser App übersetzt

### Für System-Audio
1. **Stereo Mix aktivieren** in Windows-Soundeinstellungen:
   - Rechtsklick auf Lautsprecher-Symbol → Sounds → Aufnahme-Tab
   - Rechtsklick auf leeren Bereich → Deaktivierte Geräte anzeigen
   - "Stereo Mix" aktivieren
2. **In Babel**: Stereo Mix-Gerät auswählen (markiert mit 🔊) oder automatische Erkennung verwenden

### Virtual Audio Cable Setup
1. **VB-Audio Virtual Cable herunterladen** (kostenlos)
2. **Installieren und Computer neu starten**
3. **Zielanwendung für Ausgabe auf "CABLE Input" einstellen**
4. **In Babel**: "🎯 CABLE Output"-Gerät auswählen
5. **Optional**: "CABLE Input" als Standard-Wiedergabegerät einstellen, um Audio zu hören

## 🛠️ Fehlerbehebung

### Kein Audio erkannt
- **Geräteauswahl überprüfen**: Versuchen Sie zuerst "Auto (Empfohlen)"
- **Audio-Quelle überprüfen**: Stellen Sie sicher, dass Audio tatsächlich abgespielt wird
- **Empfindlichkeit anpassen**: Audio-Empfindlichkeitsschwelle senken
- **Stereo Mix aktivieren**: Befolgen Sie die obige System-Audio-Setup-Anleitung

### Audio-Erfassung funktioniert nicht während Anrufen (Zoom, Teams, Discord, etc.)
**Dies ist ein häufiges Problem bei der Verwendung von Konferenzanwendungen. Hier sind die Lösungen:**

#### **Problem: Exklusivmodus-Konflikt**
- **Problem**: Konferenz-Apps übernehmen oft die exklusive Kontrolle über Audio-Geräte
- **Lösung**: 
  1. Gehen Sie zu Windows-Soundeinstellungen → Geräteeigenschaften → Erweitert
  2. Deaktivieren Sie "Anwendungen die exklusive Kontrolle über dieses Gerät erlauben"
  3. Wenden Sie dies sowohl auf Ihr Mikrofon als auch auf die Lautsprecher an
  4. Starten Sie beide Anwendungen neu

#### **Problem: Audio-Geräte-Routing**
- **Problem**: Anruf-Audio kann virtuelle Geräte oder Echounterdrückung verwenden, die System-Audio umgehen
- **Lösung**: 
  1. **Virtual Audio Cable installieren** (VB-Cable, VoiceMeeter)
  2. **In Ihrer Konferenz-App**: Audio-Ausgabe auf Virtual Cable einstellen
  3. **In Babel**: Virtual Cable als Eingabegerät auswählen
  4. **Optional**: Virtual Cable als Standard-Wiedergabegerät einstellen, um Audio zu hören

#### **Problem: App-spezifische Audio-Isolation**
- **Problem**: Einige Konferenz-Apps verschlüsseln oder isolieren ihre Audio-Streams
- **Lösungen**:
  1. **Windows 11 verwenden**: Versuchen Sie OBS's "Application Audio Capture"-Funktion
  2. **Konferenz-App-Einstellungen ändern**: Suchen Sie nach "System-Audio" oder "Computer-Sound teilen"-Optionen
  3. **Browser-Version verwenden**: Web-basierte Konferenz-Apps sind oft einfacher zu erfassen
  4. **VoiceMeeter versuchen**: Erweiterte virtuelle Audio-Routing-Lösung

#### **Schnelle Fixes für Anruf-Audio-Erfassung**
1. **Vor dem Beitritt zu einem Anruf**: Starten Sie Babel und überprüfen Sie, ob es System-Audio erfasst
2. **"Computer-Audio teilen" verwenden**: Aktivieren Sie diese Option in Ihrer Konferenz-App
3. **Zur Browser-Version wechseln**: Hat oft weniger Audio-Beschränkungen
4. **Kopfhörer verwenden**: Verhindert Rückkopplungsschleifen, die die Erfassung stören können
5. **Windows-Datenschutzeinstellungen überprüfen**: Stellen Sie sicher, dass Mikrofon-Berechtigungen für alle Apps aktiviert sind

### Übersetzung funktioniert nicht
- **Internetverbindung überprüfen**: Google Translate benötigt Internet
- **Sprachen überprüfen**: Stellen Sie sicher, dass die Quellsprache dem tatsächlichen Audio entspricht
- **Automatische Erkennung versuchen**: Lassen Sie Whisper die Quellsprache automatisch erkennen
- **Modelle wechseln**: Versuchen Sie das "turbo"-Modell für bessere Genauigkeit

### Leistungsprobleme
- **Leistungsmodus aktivieren**: Reduziert Speicherverbrauch und verbessert Geschwindigkeit
- **Kleineres Modell verwenden**: Wechseln Sie von "large-v3" zu "turbo" oder "tiny"
- **Andere Anwendungen schließen**: RAM für bessere Leistung freigeben
- **Internetgeschwindigkeit überprüfen**: Langsame Verbindung beeinflusst Übersetzungsgeschwindigkeit

### Untertitel-Probleme
- **Untertitel nicht sichtbar**: Überprüfen Sie, ob das Overlay hinter anderen Fenstern ist
- **Falsche Position**: Verwenden Sie "⚙ Untertitel repositionieren", um sie zu bewegen
- **Schrift zu klein/groß**: Schriftgröße in Einstellungen anpassen
- **Löschen sich nicht**: Audio-Empfindlichkeit überprüfen - könnte Hintergrundgeräusche erkennen

## 🔧 Wie es funktioniert

### Audio-Pipeline
1. **Erfassung**: Nimmt Audio vom ausgewählten Gerät auf (System-Audio oder app-spezifisch)
2. **Verarbeitung**: Konvertiert Stereo zu Mono, wendet Rauschfilterung an
3. **Transkription**: Verwendet Faster-Whisper zur Umwandlung von Sprache in Text
4. **Übersetzung**: Google Translate API übersetzt in Zielsprache
5. **Anzeige**: Zeigt Untertitel als Overlay mit automatischem Löschen

### Technische Details
- **Audio-Format**: 48kHz Stereo, konvertiert zu 16kHz Mono für Whisper
- **Chunk-Größe**: 3-Sekunden-Audio-Segmente für Echtzeit-Verarbeitung
- **Speicherverwaltung**: Warteschlangen-Größenbegrenzungen (max 3 Chunks) und Garbage Collection für Effizienz
- **Latenz-Optimierung**: Beam Size 1, VAD-Filterung, optimiertes Resampling
- **UI-Framework**: PyQt5 mit benutzerdefinierten AlphabetComboBox-Widgets für verbesserte Navigation
- **Einstellungsspeicherung**: JSON-basierte persistente Konfiguration mit automatischem Speichern

### Übersetzungssystem-Architektur
- **Externe JSON-Dateien**: Alle Übersetzungen im `translations/`-Verzeichnis gespeichert
- **Dynamisches Laden**: Übersetzungen beim Start automatisch geladen
- **Spracherkennung**: Hardcodierte Übersetzungen verhindern Rekursionsprobleme
- **Vollständige Lokalisierung**: UI-Text, Sprachnamen, Beschreibungen alle übersetzt
- **Umkehrung Mapping**: Übersetzte Sprachnamen zurück ins Englische für Einstellungsspeicherung konvertiert

### Einstellungspersistenz
Alle Einstellungen werden automatisch in `babel_settings.json` gespeichert:
```json
{
  "subtitle_y_offset": 184,
  "subtitle_x_offset": -5,
  "font_family": "Segoe UI",
  "font_size": 16,
  "source_language": "Korean",
  "target_language": "English",
  "audio_device": "Auto (Recommended)",
  "audio_device_data": -1,
  "whisper_model": "turbo",
  "audio_threshold": 0.001,
  "performance_mode": false,
  "ui_language": "German"
}
```

## 📁 Dateistruktur

```
babel/
├── main.py                    # Hauptanwendungsdatei
├── requirements.txt           # Python-Abhängigkeiten
├── babel_settings.json        # Automatisch gespeicherte Benutzereinstellungen
├── run.bat                   # Windows-Batch-Datei zum Ausführen der App
├── logo.png                  # Anwendungslogo
├── translations/             # UI-Übersetzungsdateien
│   ├── en.json              # Englische Übersetzungen
│   ├── es.json              # Spanische Übersetzungen
│   ├── fr.json              # Französische Übersetzungen
│   ├── de.json              # Deutsche Übersetzungen
│   ├── pt.json              # Portugiesische Übersetzungen
│   └── ko.json              # Koreanische Übersetzungen
└── README.md                 # Diese Dokumentation
```

## 🎮 Erweiterte Nutzung

### Benutzerdefinierte Audio-Geräte
Die Anwendung erkennt automatisch:
- **🎯 Virtual Audio Cables**: Für app-spezifische Erfassung
- **🔊 System-Audio-Geräte**: Für vollständige System-Audio-Erfassung  
- **🎤 Mikrofon-Eingänge**: Für externe Audio-Quellen

### Leistungstuning
- **Für Geschwindigkeit**: "tiny"-Modell + Leistungsmodus aktiviert verwenden
- **Für Genauigkeit**: "large-v3"-Modell + Leistungsmodus deaktiviert verwenden
- **Ausgewogen**: "turbo"-Modell verwenden (empfohlener Standard)

### Speicherverbrauch
- **tiny-Modell**: ~200MB RAM
- **turbo-Modell**: ~1GB RAM  
- **large-v3-Modell**: ~4GB RAM
- **distil-large-v3**: ~2GB RAM

## 📚 Support und Mitwirkung

### Hilfe erhalten
1. **Diese README überprüfen** für häufige Lösungen
2. **Anforderungen überprüfen**: Python 3.9+, Windows OS
3. **Mit einfachem Audio testen**: Versuchen Sie es zuerst mit klarer Sprache
4. **Konsole überprüfen**: Von der Kommandozeile ausführen, um Fehlermeldungen zu sehen

### Bekannte Einschränkungen
- **Nur Windows**: WASAPI-Loopback-Audio-Erfassung erfordert Windows
- **Internet erforderlich**: Google Translate API benötigt Internetverbindung
- **Modell-Downloads**: Erster Lauf lädt Whisper-Modelle herunter (können groß sein)
- **Echtzeit-Verarbeitung**: Einige Verzögerung ist normal (1-3 Sekunden)

### Zukünftige Verbesserungen
- Linux/macOS-Unterstützung
- Offline-Übersetzungsoptionen
- Benutzerdefinierte Untertitel-Themes
- Batch-Datei-Verarbeitung
- API für externe Integrationen

## 🆕 Neueste Funktionen und Updates

### **Verbesserte Benutzererfahrung** 
- **Alle Einstellungen automatisch gespeichert**: Jede Konfiguration automatisch in `babel_settings.json` gespeichert
- **Alphabetische Navigation**: Buchstaben in Dropdowns tippen, um schnell zu Sprachen zu springen
- **Verbesserte UI**: Modernes dunkles Theme mit besserem Abstand und visueller Rückmeldung
- **Intelligente Standards**: Englische Zielsprache, Turbo-Modell vorausgewählt

### **Vollständige Interface-Lokalisierung**
- **6 UI-Sprachen**: Vollständige Unterstützung für Englisch, Spanisch, Französisch, Deutsch, Portugiesisch, Koreanisch
- **Dynamischer Sprachwechsel**: Interface-Sprache ändern und sofortige Updates sehen
- **Hardcodierte Übersetzungen**: Alle Sprachnamen übersetzt, um Rekursion zu verhindern
- **Umfassende Abdeckung**: 70+ Sprachen in jeder Interface-Sprache übersetzt

### **Erweiterte Untertitel-Anpassung**
- **10 Schriftoptionen**: Segoe UI, Arial, Helvetica, Times New Roman und mehr
- **13 Schriftgrößen**: Von 10px bis 48px für perfekte Sichtbarkeit
- **Zieh-Positionierung**: "⚙ Untertitel repositionieren" klicken und an jede Bildschirmposition ziehen
- **Automatisches Löschen**: Untertitel verschwinden nach 2 Sekunden Stille
- **Modernes Design**: Halbtransparente Hintergründe mit Textumrissen

### **Intelligente Audio-Geräte-Erkennung**
- **Auto-Kategorisierung**: Geräte markiert mit 🎯 (Virtual Cable), 🔊 (System-Audio), 🎤 (Mikrofon)
- **Intelligente Priorität**: Wählt automatisch das beste verfügbare Loopback-Gerät
- **Gerätedetails**: Zeigt Kanäle und Abtastrate für jedes Gerät
- **Aktualisierungsfähigkeit**: Geräteliste ohne Neustart aktualisieren

### **Leistungsoptimierungen**
- **Leistungsmodus**: Umschalten für Geschwindigkeit vs. Genauigkeitsoptimierung
- **Speicherverwaltung**: Automatische Garbage Collection und Warteschlangen-Größenbegrenzungen
- **Optimierte Modelle**: Unterstützung für distil-large-v3 (optimiertes großes Modell)
- **VAD-Filterung**: Sprachaktivitätserkennung zur Reduzierung der Stilleverarbeitung

---

**Babel** - Echtzeit-Übersetzung für alle zugänglich machen! Perfekt für internationale Spiele, das Ansehen fremder Inhalte oder das Erlernen neuer Sprachen!

# Babel - Traduction Audio en Temps Réel avec Superposition de Sous-titres

**[English](README.md) | [Español](README_ES.md) | Français | [Deutsch](README_DE.md) | [日本語](README_JA.md) | [한국어](README_KO.md) | [中文](README_ZH.md)**

Une application Python qui capture l'audio interne de votre PC, le traduit en temps réel en utilisant Faster-Whisper et Google Translate, et affiche des sous-titres traduits en superposition sur votre écran.

## Fonctionnalités

### 🎵 **Capture Audio**
- **Auto-détection**: Trouve automatiquement le meilleur périphérique loopback (Stereo Mix, Virtual Audio Cable)
- **Sélection manuelle**: Choisissez parmi les périphériques d'entrée disponibles avec détails du périphérique
- **Capture spécifique d'application**: Support pour Virtual Audio Cable pour capturer des applications individuelles
- **Audio système**: Capture tout l'audio PC ou audio d'application spécifique

### 🧠 **Traduction Alimentée par IA**
- **Reconnaissance Vocale**: Utilise les modèles Faster-Whisper (tiny, turbo, large-v3, distil-large-v3)
- **Détection automatique de langue**: Laissez Whisper détecter automatiquement la langue source
- **90+ langues source**: Support pour toutes les langues principales que Whisper peut transcrire
- **100+ langues cible**: Traduit vers n'importe quelle langue supportée par Google Translate
- **Traitement en temps réel**: Optimisé pour faible latence et utilisation mémoire

### 📺 **Sous-titres Professionnels**
- **Affichage superposé**: Superposition de sous-titres transparente, toujours au premier plan
- **Polices personnalisables**: Choisissez parmi 10 polices populaires et plusieurs tailles
- **Repositionnable**: Glissez les sous-titres vers n'importe quelle position à l'écran
- **Auto-effacement**: Les sous-titres disparaissent automatiquement pendant le silence
- **Design moderne**: Arrière-plan semi-transparent avec contours de texte pour la lisibilité

### ⚙️ **Paramètres Intelligents**
- **Configuration persistante**: Tous les paramètres sauvegardés automatiquement dans `babel_settings.json`
- **Mode performance**: Basculer entre vitesse et précision
- **Sensibilité audio**: Seuil ajustable pour filtrer le bruit de fond
- **Navigation alphabétique**: Tapez des lettres dans les menus déroulants pour trouver rapidement les options

## Exigences

- **Python**: 3.9 ou supérieur
- **Système d'Exploitation**: Windows (pour la capture audio loopback WASAPI)
- **Mémoire**: Au moins 4GB RAM (8GB recommandé pour les grands modèles)
- **Stockage**: 1-5GB pour les modèles Whisper (téléchargés automatiquement)

## Installation

1. **Clonez ou téléchargez** ce dépôt
2. **Installez les dépendances**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Exécutez l'application**:
   ```bash
   python main.py
   ```

## Guide de Démarrage Rapide

### Configuration de Base
1. **Lancez** l'application: `python main.py`
2. **Entrée Audio**: Sélectionnez "Auto (Recommandé)" ou choisissez un périphérique spécifique
3. **Langues**: 
   - **De**: Choisissez la langue source ou "Auto-détection"
   - **Vers**: Choisissez la langue cible (par défaut Anglais)
4. **Cliquez** "▶️ Démarrer la Traduction"

### Conseils de Première Configuration
- **Testez l'audio**: Parlez ou jouez de l'audio pour vérifier que le microphone/audio système fonctionne
- **Ajustez la sensibilité**: Valeurs plus basses = plus sensible à l'audio silencieux
- **Positionnez les sous-titres**: Utilisez "⚙ Repositionner les Sous-titres" pour les placer où vous voulez
- **Choisissez le modèle**: "turbo" est recommandé pour un équilibre vitesse/précision
- **Sélection rapide de langue**: Tapez des lettres dans les menus de langues pour sauter aux options (ex. tapez "F" pour Français)
- **Tous les paramètres sauvegardés**: Vos préférences sont automatiquement mémorisées entre les sessions

## Langues Supportées

### Langues Source (Reconnaissance Whisper)
**Auto-détection**, Afrikaans, Albanais, Amharique, Arabe, Arménien, Assamais, Azerbaïdjanais, Bachkir, Basque, Biélorusse, Bengali, Bosniaque, Breton, Bulgare, Birman, Catalan, Chinois, Croate, Tchèque, Danois, Néerlandais, Anglais, Estonien, Féroïen, Finnois, Français, Galicien, Géorgien, Allemand, Grec, Gujarati, Haïtien, Haoussa, Hawaïen, Hébreu, Hindi, Hongrois, Islandais, Indonésien, Italien, Japonais, Javanais, Kannada, Kazakh, Khmer, Coréen, Lao, Latin, Letton, Lituanien, Luxembourgeois, Macédonien, Malgache, Malais, Malayalam, Maltais, Maori, Marathi, Mongol, Népalais, Norvégien, Occitan, Pachto, Persan, Polonais, Portugais, Punjabi, Roumain, Russe, Sanskrit, Serbe, Shona, Sindhi, Cinghalais, Slovaque, Slovène, Somali, Espagnol, Soundanais, Swahili, Suédois, Tagalog, Tadjik, Tamil, Tatar, Telugu, Thaï, Tibétain, Turc, Turkmène, Ukrainien, Ourdou, Ouzbek, Vietnamien, Gallois, Yiddish, Yoruba

### Langues Cible (Google Translate)
**Français** (par défaut), Afrikaans, Albanais, Amharique, Arabe, Arménien, Azerbaïdjanais, Basque, Biélorusse, Bengali, Bosniaque, Bulgare, Catalan, Cebuano, Chinois (Simplifié), Chinois (Traditionnel), Corse, Croate, Tchèque, Danois, Néerlandais, Espéranto, Estonien, Finnois, Français, Frison, Galicien, Géorgien, Allemand, Grec, Gujarati, Créole Haïtien, Haoussa, Hawaïen, Hébreu, Hindi, Hmong, Hongrois, Islandais, Igbo, Indonésien, Irlandais, Italien, Japonais, Javanais, Kannada, Kazakh, Khmer, Coréen, Kurde, Kirghize, Lao, Latin, Letton, Lituanien, Luxembourgeois, Macédonien, Malgache, Malais, Malayalam, Maltais, Maori, Marathi, Mongol, Myanmar (Birman), Népalais, Norvégien, Odia (Oriya), Pachto, Persan, Polonais, Portugais, Punjabi, Roumain, Russe, Samoan, Gaélique Écossais, Serbe, Sesotho, Shona, Sindhi, Cinghalais, Slovaque, Slovène, Somali, Espagnol, Soundanais, Swahili, Suédois, Tagalog, Tadjik, Tamil, Tatar, Telugu, Thaï, Turc, Turkmène, Ukrainien, Ourdou, Ouïghour, Ouzbek, Vietnamien, Gallois, Xhosa, Yiddish, Yoruba, Zoulou

## Dernières Fonctionnalités et Mises à Jour

### 🆕 **Expérience Utilisateur Améliorée** 
- **Tous les paramètres auto-sauvegardés**: Chaque configuration automatiquement sauvegardée dans `babel_settings.json`
- **Navigation alphabétique**: Tapez des lettres dans les menus déroulants pour sauter rapidement aux langues
- **UI améliorée**: Thème sombre moderne avec meilleur espacement et retour visuel
- **Valeurs par défaut intelligentes**: Langue cible Anglais, modèle turbo pré-sélectionné

### 🎨 **Personnalisation Avancée des Sous-titres**
- **10 options de police**: Segoe UI, Arial, Helvetica, Times New Roman, et plus
- **13 tailles de police**: De 10px à 48px pour une visibilité parfaite
- **Positionnement par glissement**: Cliquez "⚙ Repositionner les Sous-titres" et glissez vers n'importe quelle position d'écran
- **Auto-effacement**: Les sous-titres disparaissent après 2 secondes de silence
- **Design moderne**: Arrière-plans semi-transparents avec contours de texte

---

**Babel** - Rendre la traduction en temps réel accessible à tous ! Parfait pour les jeux internationaux, regarder du contenu étranger, ou apprendre de nouvelles langues !

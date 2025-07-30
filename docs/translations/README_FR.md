# Babel - Traduction Audio en Temps Réel avec Superposition de Sous-titres

**[English](../../README.md) | [Español](README_ES.md) | Français | [Deutsch](README_DE.md) | [Português](README_PT.md) | [日本語](README_JA.md) | [한국어](README_KO.md) | [中文](README_ZH.md)**

Une application Python qui capture l'audio interne de votre PC, le traduit en temps réel en utilisant Faster-Whisper et Google Translate, et affiche des sous-titres traduits en superposition sur votre écran.

## 🌟 Fonctionnalités

### 🎵 **Capture Audio**
- **Détection automatique** : Trouve automatiquement le meilleur dispositif de loopback (Stereo Mix, Virtual Audio Cable)
- **Sélection manuelle** : Choisissez parmi les dispositifs d'entrée disponibles avec détails du dispositif
- **Capture spécifique d'app** : Support pour Virtual Audio Cable pour capturer des applications individuelles
- **Audio système** : Capture tout l'audio PC ou audio d'application spécifique

### 🧠 **Traduction Alimentée par IA**
- **Reconnaissance vocale** : Utilise les modèles Faster-Whisper (tiny, turbo, large-v3, distil-large-v3)
- **Détection automatique de langue** : Laissez Whisper détecter automatiquement la langue source
- **90+ langues sources** : Support pour toutes les principales langues que Whisper peut transcrire
- **100+ langues cibles** : Traduit vers n'importe quelle langue supportée par Google Translate
- **Traitement en temps réel** : Optimisé pour faible latence et utilisation mémoire

### 📺 **Sous-titres Professionnels**
- **Affichage superposé** : Superposition de sous-titres transparente, toujours au-dessus
- **Polices personnalisables** : Choisissez parmi 10 polices populaires et tailles multiples (10px-48px)
- **Repositionnable** : Glissez les sous-titres vers n'importe quelle position à l'écran
- **Nettoyage automatique** : Les sous-titres disparaissent automatiquement pendant le silence
- **Design moderne** : Arrière-plan semi-transparent avec contours de texte pour la lisibilité

### 🌍 **Interface Multilingue**
- **6 Langues d'UI** : Anglais, Espagnol, Français, Allemand, Portugais, Coréen
- **Localisation complète** : Tous les menus, boutons, descriptions et noms de langues traduits
- **Changement dynamique** : Changez la langue de l'interface et voyez les mises à jour immédiates
- **Dropdowns spécifiques à la langue** : Noms de langues affichés dans la langue actuelle de l'interface

### ⚙️ **Paramètres Intelligents**
- **Configuration persistante** : Tous les paramètres sauvegardés automatiquement dans `babel_settings.json`
- **Mode performance** : Basculez entre vitesse et précision
- **Sensibilité audio** : Seuil ajustable pour filtrer le bruit de fond
- **Navigation alphabétique** : Tapez des lettres dans les dropdowns pour trouver rapidement les options

## 📋 Prérequis

- **Python** : 3.9 ou supérieur
- **Système d'exploitation** : Windows (pour capture audio loopback WASAPI)
- **Mémoire** : Au moins 4GB RAM (8GB recommandé pour les grands modèles)
- **Stockage** : 1-5GB pour les modèles Whisper (téléchargés automatiquement)
- **Internet** : Requis pour l'API Google Translate

## 🚀 Installation

1. **Clonez ou téléchargez** ce dépôt
2. **Installez les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```
3. **Exécutez l'application** :
   ```bash
   python main.py
   ```
   Ou utilisez le fichier batch fourni :
   ```bash
   run.bat
   ```

## 📖 Guide de Démarrage Rapide

### Configuration de Base
1. **Lancez** l'application : `python main.py`
2. **Entrée Audio** : Sélectionnez "Auto (Recommandé)" ou choisissez un dispositif spécifique
3. **Langues** : 
   - **De** : Choisissez la langue source ou "Détecter automatiquement"
   - **Vers** : Choisissez la langue cible (par défaut : Anglais)
4. **Cliquez** "▶️ Démarrer la Traduction"

### Conseils de Configuration Initiale
- **Testez l'audio** : Parlez ou jouez de l'audio pour vérifier que le microphone/audio système fonctionne
- **Ajustez la sensibilité** : Valeurs plus basses = plus sensible à l'audio faible
- **Positionnez les sous-titres** : Utilisez "⚙ Repositionner les Sous-titres" pour les placer où vous voulez
- **Choisissez le modèle** : "turbo" est recommandé pour vitesse/précision équilibrée
- **Sélection rapide de langue** : Tapez des lettres dans les dropdowns de langue pour aller aux options (ex : tapez "A" pour Anglais)
- **Tous les paramètres sauvegardés** : Vos préférences sont automatiquement mémorisées entre les sessions

## 🌍 Langues de l'Interface Utilisateur

Babel supporte les langues suivantes pour l'interface utilisateur :
- **Anglais** (par défaut)
- **Espagnol** (Español)
- **Français** (par défaut) 
- **Allemand** (Deutsch)
- **Portugais** (Português)
- **Coréen** (한국어)

Changez la langue de l'UI dans la page "⚙ Paramètres" en utilisant le dropdown "Langue de l'UI". Tous les menus, boutons, descriptions, tooltips et noms de langues seront affichés dans votre langue sélectionnée.

## 🗣️ Langues Supportées

### Langues Sources (Reconnaissance Whisper)
**Détecter automatiquement**, Afrikaans, Albanais, Amharique, Arabe, Arménien, Assamais, Azerbaïdjanais, Bashkir, Basque, Biélorusse, Bengali, Bosniaque, Breton, Bulgare, Birman, Catalan, Chinois, Croate, Tchèque, Danois, Néerlandais, Anglais, Estonien, Féroïen, Finnois, Français, Galicien, Géorgien, Allemand, Grec, Gujarati, Haïtien, Haoussa, Hawaïen, Hébreu, Hindi, Hongrois, Islandais, Indonésien, Italien, Japonais, Javanais, Kannada, Kazakh, Khmer, Coréen, Laotien, Latin, Letton, Lituanien, Luxembourgeois, Macédonien, Malgache, Malais, Malayalam, Maltais, Maori, Marathi, Mongol, Népalais, Norvégien, Occitan, Pachto, Persan, Polonais, Portugais, Punjabi, Roumain, Russe, Sanskrit, Serbe, Shona, Sindhi, Cinghalais, Slovaque, Slovène, Somali, Espagnol, Soundanais, Swahili, Suédois, Tagalog, Tadjik, Tamil, Tatar, Telugu, Thaï, Tibétain, Turc, Turkmène, Ukrainien, Ourdou, Ouzbek, Vietnamien, Gallois, Yiddish, Yoruba

### Langues Cibles (Google Translate)
**Anglais** (par défaut), Afrikaans, Albanais, Amharique, Arabe, Arménien, Azerbaïdjanais, Basque, Biélorusse, Bengali, Bosniaque, Bulgare, Catalan, Cebuano, Chinois (Simplifié), Chinois (Traditionnel), Corse, Croate, Tchèque, Danois, Néerlandais, Espéranto, Estonien, Finnois, Français, Frison, Galicien, Géorgien, Allemand, Grec, Gujarati, Créole Haïtien, Haoussa, Hawaïen, Hébreu, Hindi, Hmong, Hongrois, Islandais, Igbo, Indonésien, Irlandais, Italien, Japonais, Javanais, Kannada, Kazakh, Khmer, Coréen, Kurde, Kirghize, Laotien, Latin, Letton, Lituanien, Luxembourgeois, Macédonien, Malgache, Malais, Malayalam, Maltais, Maori, Marathi, Mongol, Birman (Birman), Népalais, Norvégien, Odia (Oriya), Pachto, Persan, Polonais, Portugais, Punjabi, Roumain, Russe, Samoan, Gaélique Écossais, Serbe, Sesotho, Shona, Sindhi, Cinghalais, Slovaque, Slovène, Somali, Espagnol, Soundanais, Swahili, Suédois, Tagalog, Tadjik, Tamil, Tatar, Telugu, Thaï, Turc, Turkmène, Ukrainien, Ourdou, Ouïghour, Ouzbek, Vietnamien, Gallois, Xhosa, Yiddish, Yoruba, Zoulou

## ⚙️ Options de Configuration

### Paramètres Audio
- **Sélection de Dispositif** : Détection automatique ou sélection manuelle de dispositif
- **Sensibilité Audio** : Seuil 0.001-0.100 pour filtrage du bruit
- **Mode Performance** : Basculez pour vitesse vs. précision optimisée

### Modèles IA
- **tiny** : Plus rapide, précision basique (~40MB)
- **turbo** : Vitesse/précision équilibrée (~810MB) - **Recommandé**
- **large-v3** : Précision la plus élevée, plus lent (~3GB)
- **distil-large-v3** : Modèle large optimisé (~1.5GB)

### Apparence des Sous-titres
- **Famille de Police** : Segoe UI, Arial, Helvetica, Times New Roman, Calibri, Trebuchet MS, Verdana, Georgia, Comic Sans MS, Impact
- **Taille de Police** : 10px à 48px
- **Position** : Glissez pour repositionner n'importe où sur l'écran
- **Nettoyage automatique** : Les sous-titres disparaissent après 2 secondes de silence

## 🎯 Guide de Capture Audio Spécifique d'App

### Pour Applications Individuelles
1. **Installez Virtual Audio Cable** (VB-Cable ou similaire)
2. **Configurez la sortie audio de l'application** vers Virtual Cable
3. **Dans Babel** : Sélectionnez le dispositif Virtual Cable (marqué avec 🎯)
4. **Démarrez la traduction** - maintenant seul l'audio de cette app sera traduit

### Pour Audio Système
1. **Activez Stereo Mix** dans les paramètres Son de Windows :
   - Clic droit sur l'icône haut-parleur → Sons → onglet Enregistrement
   - Clic droit sur l'espace vide → Afficher les Dispositifs Désactivés
   - Activez "Stereo Mix"
2. **Dans Babel** : Sélectionnez le dispositif Stereo Mix (marqué avec 🔊) ou utilisez la détection automatique

### Configuration Virtual Audio Cable
1. **Téléchargez** VB-Audio Virtual Cable (gratuit)
2. **Installez et redémarrez** votre ordinateur
3. **Configurez l'application cible** pour sortie vers "CABLE Input"
4. **Dans Babel** : Sélectionnez le dispositif "🎯 CABLE Output"
5. **Optionnel** : Configurez "CABLE Input" comme votre dispositif de lecture par défaut pour entendre l'audio

## 🛠️ Dépannage

### Aucun Audio Détecté
- **Vérifiez la sélection de dispositif** : Essayez "Auto (Recommandé)" d'abord
- **Vérifiez la source audio** : Assurez-vous que l'audio joue réellement
- **Ajustez la sensibilité** : Baissez le seuil de sensibilité audio
- **Activez Stereo Mix** : Suivez le guide de configuration audio système ci-dessus

### La Capture Audio Ne Fonctionne Pas Pendant les Appels (Zoom, Teams, Discord, etc.)
**C'est un problème courant lors de l'utilisation d'applications de conférence. Voici les solutions :**

#### **Problème : Conflit de Mode Exclusif**
- **Problème** : Les apps de conférence prennent souvent le contrôle exclusif des dispositifs audio
- **Solution** : 
  1. Allez dans Paramètres Son de Windows → Propriétés du Dispositif → Avancé
  2. Décochez "Autoriser les applications à prendre le contrôle exclusif de ce dispositif"
  3. Appliquez cela à la fois à votre microphone et aux haut-parleurs
  4. Redémarrez les deux applications

#### **Problème : Routage de Dispositif Audio**
- **Problème** : L'audio d'appel peut utiliser des dispositifs virtuels ou une annulation d'écho qui contournent l'audio système
- **Solution** : 
  1. **Installez un Virtual Audio Cable** (VB-Cable, VoiceMeeter)
  2. **Dans votre app de conférence** : Configurez la sortie audio vers Virtual Cable
  3. **Dans Babel** : Sélectionnez le Virtual Cable comme dispositif d'entrée
  4. **Optionnel** : Configurez Virtual Cable comme dispositif de lecture par défaut pour entendre l'audio

#### **Problème : Isolation Audio Spécifique d'App**
- **Problème** : Certaines apps de conférence chiffrent ou isolent leurs flux audio
- **Solutions** :
  1. **Utilisez Windows 11** : Essayez la fonctionnalité "Application Audio Capture" d'OBS
  2. **Changez les paramètres de l'app de conférence** : Cherchez les options "Audio système" ou "Partager le son de l'ordinateur"
  3. **Utilisez la version navigateur** : Les apps de conférence basées sur le web sont souvent plus faciles à capturer
  4. **Essayez VoiceMeeter** : Solution de routage audio virtuel plus avancée

#### **Corrections Rapides pour Capture Audio d'Appel**
1. **Avant de rejoindre un appel** : Démarrez Babel et vérifiez qu'il capture l'audio système
2. **Utilisez "Partager l'Audio de l'Ordinateur"** : Activez cette option dans votre app de conférence
3. **Passez à la version navigateur** : A souvent moins de restrictions audio
4. **Utilisez des écouteurs** : Prévient les boucles de rétroaction qui peuvent interférer avec la capture
5. **Vérifiez les Paramètres de Confidentialité Windows** : Assurez-vous que les permissions microphone sont activées pour toutes les apps

### La Traduction Ne Fonctionne Pas
- **Vérifiez la connexion internet** : Google Translate nécessite internet
- **Vérifiez les langues** : Assurez-vous que la langue source correspond à l'audio réel
- **Essayez la détection automatique** : Laissez Whisper détecter automatiquement la langue source
- **Changez de modèles** : Essayez le modèle "turbo" pour une meilleure précision

### Problèmes de Performance
- **Activez le Mode Performance** : Réduit l'utilisation mémoire et améliore la vitesse
- **Utilisez un modèle plus petit** : Passez de "large-v3" à "turbo" ou "tiny"
- **Fermez d'autres applications** : Libérez la RAM pour de meilleures performances
- **Vérifiez la vitesse internet** : Une connexion lente affecte la vitesse de traduction

### Problèmes de Sous-titres
- **Sous-titres non visibles** : Vérifiez si la superposition est derrière d'autres fenêtres
- **Mauvaise position** : Utilisez "⚙ Repositionner les Sous-titres" pour les déplacer
- **Police trop petite/grande** : Ajustez la taille de police dans les paramètres
- **Ne se nettoient pas** : Vérifiez la sensibilité audio - peut détecter du bruit de fond

## 🔧 Comment Ça Fonctionne

### Pipeline Audio
1. **Capture** : Enregistre l'audio du dispositif sélectionné (audio système ou spécifique d'app)
2. **Traitement** : Convertit stéréo en mono, applique le filtrage du bruit
3. **Transcription** : Utilise Faster-Whisper pour convertir la parole en texte
4. **Traduction** : L'API Google Translate traduit vers la langue cible
5. **Affichage** : Montre les sous-titres en superposition avec nettoyage automatique

### Détails Techniques
- **Format Audio** : 48kHz stéréo, converti en 16kHz mono pour Whisper
- **Taille de Chunk** : Segments audio de 3 secondes pour traitement en temps réel
- **Gestion Mémoire** : Limites de taille de file d'attente (max 3 chunks) et ramasse-miettes pour l'efficacité
- **Optimisation Latence** : Beam size 1, filtrage VAD, rééchantillonnage optimisé
- **Framework UI** : PyQt5 avec widgets AlphabetComboBox personnalisés pour navigation améliorée
- **Stockage Paramètres** : Configuration persistante basée JSON avec sauvegarde automatique

### Architecture du Système de Traduction
- **Fichiers JSON Externes** : Toutes les traductions stockées dans le répertoire `translations/`
- **Chargement Dynamique** : Traductions chargées automatiquement au démarrage
- **Détection de Langue** : Traductions hard-codées préviennent les problèmes de récursion
- **Localisation Complète** : Texte UI, noms de langues, descriptions tous traduits
- **Mappage Inverse** : Noms de langues traduits convertis de retour en anglais pour stockage des paramètres

### Persistance des Paramètres
Tous les paramètres sont automatiquement sauvegardés dans `babel_settings.json` :
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
  "ui_language": "French"
}
```

## 📁 Structure des Fichiers

```
babel/
├── main.py                    # Fichier principal de l'application
├── requirements.txt           # Dépendances Python
├── babel_settings.json        # Paramètres utilisateur auto-sauvegardés
├── run.bat                   # Fichier batch Windows pour exécuter l'app
├── logo.png                  # Logo de l'application
├── translations/             # Fichiers de traduction UI
│   ├── en.json              # Traductions anglaises
│   ├── es.json              # Traductions espagnoles
│   ├── fr.json              # Traductions françaises
│   ├── de.json              # Traductions allemandes
│   ├── pt.json              # Traductions portugaises
│   └── ko.json              # Traductions coréennes
└── README.md                 # Cette documentation
```

## 🎮 Utilisation Avancée

### Dispositifs Audio Personnalisés
L'application détecte automatiquement :
- **🎯 Virtual Audio Cables** : Pour capture spécifique d'app
- **🔊 Dispositifs Audio Système** : Pour capture audio système complète  
- **🎤 Entrées Microphone** : Pour sources audio externes

### Réglage de Performance
- **Pour Vitesse** : Utilisez modèle "tiny" + Mode Performance activé
- **Pour Précision** : Utilisez modèle "large-v3" + Mode Performance désactivé
- **Équilibré** : Utilisez modèle "turbo" (par défaut recommandé)

### Utilisation Mémoire
- **modèle tiny** : ~200MB RAM
- **modèle turbo** : ~1GB RAM  
- **modèle large-v3** : ~4GB RAM
- **distil-large-v3** : ~2GB RAM

## 📚 Support et Contribution

### Obtenir de l'Aide
1. **Vérifiez ce README** pour les solutions communes
2. **Vérifiez les prérequis** : Python 3.9+, OS Windows
3. **Testez avec audio simple** : Essayez avec parole claire d'abord
4. **Vérifiez la console** : Exécutez depuis la ligne de commande pour voir les messages d'erreur

### Limitations Connues
- **Windows seulement** : La capture audio loopback WASAPI nécessite Windows
- **Internet requis** : L'API Google Translate nécessite une connexion internet
- **Téléchargements de modèle** : La première exécution télécharge les modèles Whisper (peuvent être volumineux)
- **Traitement temps réel** : Un certain délai est normal (1-3 secondes)

### Améliorations Futures
- Support Linux/macOS
- Options de traduction hors ligne
- Thèmes de sous-titres personnalisés
- Traitement de fichiers par lots
- API pour intégrations externes

## 🆕 Fonctionnalités et Mises à Jour Récentes

### **Expérience Utilisateur Améliorée** 
- **Tous les paramètres auto-sauvegardés** : Chaque configuration automatiquement sauvegardée dans `babel_settings.json`
- **Navigation alphabétique** : Tapez des lettres dans les dropdowns pour aller rapidement aux langues
- **UI améliorée** : Thème sombre moderne avec meilleur espacement et retour visuel
- **Valeurs par défaut intelligentes** : Langue cible anglaise, modèle turbo pré-sélectionné

### **Localisation Complète d'Interface**
- **6 Langues d'UI** : Support complet pour Anglais, Espagnol, Français, Allemand, Portugais, Coréen
- **Changement dynamique de langue** : Changez la langue d'interface et voyez les mises à jour immédiates
- **Traductions hard-codées** : Tous les noms de langues traduits pour prévenir la récursion
- **Couverture complète** : 70+ langues traduites dans chaque langue d'interface

### **Personnalisation Avancée des Sous-titres**
- **10 options de police** : Segoe UI, Arial, Helvetica, Times New Roman et plus
- **13 tailles de police** : De 10px à 48px pour visibilité parfaite
- **Positionnement par glissement** : Cliquez "⚙ Repositionner les Sous-titres" et glissez vers n'importe quelle position d'écran
- **Nettoyage automatique** : Les sous-titres disparaissent après 2 secondes de silence
- **Design moderne** : Arrière-plans semi-transparents avec contours de texte

### **Détection Intelligente de Dispositif Audio**
- **Auto-catégorisation** : Dispositifs marqués avec 🎯 (Virtual Cable), 🔊 (Audio Système), 🎤 (Microphone)
- **Priorité intelligente** : Sélectionne automatiquement le meilleur dispositif loopback disponible
- **Détails du dispositif** : Montre les canaux et le taux d'échantillonnage pour chaque dispositif
- **Capacité de rafraîchissement** : Met à jour la liste des dispositifs sans redémarrer

### **Optimisations de Performance**
- **Mode Performance** : Basculez pour optimisation vitesse vs précision
- **Gestion mémoire** : Ramasse-miettes automatique et limites de taille de file d'attente
- **Modèles optimisés** : Support pour distil-large-v3 (modèle large optimisé)
- **Filtrage VAD** : Détection d'Activité Vocale pour réduire le traitement du silence

---

**Babel** - Rendre la traduction en temps réel accessible à tous ! Parfait pour les jeux internationaux, regarder du contenu étranger ou apprendre de nouvelles langues !

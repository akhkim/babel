# Babel - Traducción de Audio en Tiempo Real con Subtítulos Superpuestos

**[English](README.md) | Español | [Français](README_FR.md) | [Deutsch](README_DE.md) | [日本語](README_JA.md) | [한국어](README_KO.md) | [中文](README_ZH.md)**

Una aplicación de Python que captura el audio interno de tu PC, lo traduce en tiempo real usando Faster-Whisper y Google Translate, y muestra subtítulos traducidos como una superposición en tu pantalla.

## Características

### 🎵 **Captura de Audio**
- **Auto-detección**: Encuentra automáticamente el mejor dispositivo de loopback (Stereo Mix, Virtual Audio Cable)
- **Selección manual**: Elige entre dispositivos de entrada disponibles con detalles del dispositivo
- **Captura específica de aplicaciones**: Soporte para Virtual Audio Cable para capturar aplicaciones individuales
- **Audio del sistema**: Captura todo el audio de la PC o audio específico de aplicaciones

### 🧠 **Traducción Impulsada por IA**
- **Reconocimiento de Voz**: Usa modelos Faster-Whisper (tiny, turbo, large-v3, distil-large-v3)
- **Detección automática de idioma**: Permite que Whisper detecte automáticamente el idioma fuente
- **90+ idiomas fuente**: Soporte para todos los idiomas principales que Whisper puede transcribir
- **100+ idiomas objetivo**: Traduce a cualquier idioma soportado por Google Translate
- **Procesamiento en tiempo real**: Optimizado para baja latencia y uso de memoria

### 📺 **Subtítulos Profesionales**
- **Pantalla superpuesta**: Superposición de subtítulos transparente, siempre en primer plano
- **Fuentes personalizables**: Elige entre 10 fuentes populares y múltiples tamaños
- **Reposicionable**: Arrastra subtítulos a cualquier posición en la pantalla
- **Auto-limpieza**: Los subtítulos desaparecen automáticamente durante el silencio
- **Diseño moderno**: Fondo semi-transparente con contornos de texto para legibilidad

### ⚙️ **Configuraciones Inteligentes**
- **Configuración persistente**: Todas las configuraciones guardadas automáticamente en `babel_settings.json`
- **Modo rendimiento**: Alterna entre velocidad y precisión
- **Sensibilidad de audio**: Umbral ajustable para filtrar ruido de fondo
- **Navegación alfabética**: Escribe letras en menús desplegables para encontrar opciones rápidamente

## Requisitos

- **Python**: 3.9 o superior
- **Sistema Operativo**: Windows (para captura de audio loopback WASAPI)
- **Memoria**: Al menos 4GB RAM (8GB recomendado para modelos grandes)
- **Almacenamiento**: 1-5GB para modelos Whisper (descargados automáticamente)

## Instalación

1. **Clona o descarga** este repositorio
2. **Instala dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Ejecuta la aplicación**:
   ```bash
   python main.py
   ```

## Guía de Inicio Rápido

### Configuración Básica
1. **Inicia** la aplicación: `python main.py`
2. **Entrada de Audio**: Selecciona "Auto (Recomendado)" o elige un dispositivo específico
3. **Idiomas**: 
   - **Desde**: Elige idioma fuente o "Auto-detectar"
   - **Hacia**: Elige idioma objetivo (por defecto Inglés)
4. **Haz clic** "▶️ Iniciar Traducción"

### Consejos de Primera Configuración
- **Prueba audio**: Habla o reproduce audio para verificar que el micrófono/audio del sistema funciona
- **Ajusta sensibilidad**: Valores más bajos = más sensible a audio silencioso
- **Posiciona subtítulos**: Usa "⚙ Reposicionar Subtítulos" para colocarlos donde quieras
- **Elige modelo**: "turbo" es recomendado para velocidad/precisión balanceada
- **Selección rápida de idioma**: Escribe letras en menús de idiomas para saltar a opciones (ej. escribe "E" para Español)
- **Todas las configuraciones guardadas**: Tus preferencias se recuerdan automáticamente entre sesiones

## Idiomas Soportados

### Idiomas Fuente (Reconocimiento Whisper)
**Auto-detectar**, Afrikaans, Albanés, Amárico, Árabe, Armenio, Asamés, Azerbaiyano, Bashkir, Vasco, Bielorruso, Bengalí, Bosnio, Bretón, Búlgaro, Birmano, Catalán, Chino, Croata, Checo, Danés, Holandés, Inglés, Estonio, Feroés, Finlandés, Francés, Gallego, Georgiano, Alemán, Griego, Gujarati, Haitiano, Hausa, Hawaiano, Hebreo, Hindi, Húngaro, Islandés, Indonesio, Italiano, Japonés, Javanés, Canarés, Kazajo, Jemer, Coreano, Lao, Latín, Letón, Lituano, Luxemburgués, Macedonio, Malgache, Malayo, Malayalam, Maltés, Maorí, Marathi, Mongol, Nepalí, Noruego, Occitano, Pastún, Persa, Polaco, Portugués, Punjabi, Rumano, Ruso, Sánscrito, Serbio, Shona, Sindhi, Cingalés, Eslovaco, Esloveno, Somalí, Español, Sundanés, Swahili, Sueco, Tagalo, Tayiko, Tamil, Tártaro, Telugu, Tailandés, Tibetano, Turco, Turkmeno, Ucraniano, Urdu, Uzbeko, Vietnamita, Galés, Yiddish, Yoruba

### Idiomas Objetivo (Google Translate)
**Español** (por defecto), Afrikaans, Albanés, Amárico, Árabe, Armenio, Azerbaiyano, Vasco, Bielorruso, Bengalí, Bosnio, Búlgaro, Catalán, Cebuano, Chino (Simplificado), Chino (Tradicional), Corso, Croata, Checo, Danés, Holandés, Esperanto, Estonio, Finlandés, Francés, Frisón, Gallego, Georgiano, Alemán, Griego, Gujarati, Criollo Haitiano, Hausa, Hawaiano, Hebreo, Hindi, Hmong, Húngaro, Islandés, Igbo, Indonesio, Irlandés, Italiano, Japonés, Javanés, Canarés, Kazajo, Jemer, Coreano, Kurdo, Kirguís, Lao, Latín, Letón, Lituano, Luxemburgués, Macedonio, Malgache, Malayo, Malayalam, Maltés, Maorí, Marathi, Mongol, Myanmar (Birmano), Nepalí, Noruego, Odia (Oriya), Pastún, Persa, Polaco, Portugués, Punjabi, Rumano, Ruso, Samoano, Gaélico Escocés, Serbio, Sesotho, Shona, Sindhi, Cingalés, Eslovaco, Esloveno, Somalí, Español, Sundanés, Swahili, Sueco, Tagalo, Tayiko, Tamil, Tártaro, Telugu, Tailandés, Turco, Turkmeno, Ucraniano, Urdu, Uigur, Uzbeko, Vietnamita, Galés, Xhosa, Yiddish, Yoruba, Zulú

## Opciones de Configuración

### Configuraciones de Audio
- **Selección de Dispositivo**: Auto-detección o selección manual de dispositivo
- **Sensibilidad de Audio**: Umbral 0.001-0.100 para filtrado de ruido
- **Modo Rendimiento**: Alternar para velocidad optimizada vs. precisión

### Modelos de IA
- **tiny**: Más rápido, precisión básica (~40MB)
- **turbo**: Velocidad/precisión balanceada (~810MB) - **Recomendado**
- **large-v3**: Mayor precisión, más lento (~3GB)
- **distil-large-v3**: Modelo grande optimizado (~1.5GB)

### Apariencia de Subtítulos
- **Familia de Fuente**: Segoe UI, Arial, Helvetica, Times New Roman, Calibri, Trebuchet MS, Verdana, Georgia, Comic Sans MS, Impact
- **Tamaño de Fuente**: 10px a 48px
- **Posición**: Arrastra para reposicionar en cualquier lugar de la pantalla
- **Auto-limpieza**: Los subtítulos desaparecen después de 2 segundos de silencio

## Últimas Características y Actualizaciones

### 🆕 **Experiencia de Usuario Mejorada** 
- **Todas las configuraciones auto-guardadas**: Cada configuración guardada automáticamente en `babel_settings.json`
- **Navegación alfabética**: Escribe letras en menús desplegables para saltar rápidamente a idiomas
- **UI mejorada**: Tema oscuro moderno con mejor espaciado y retroalimentación visual
- **Valores predeterminados inteligentes**: Idioma objetivo Inglés, modelo turbo pre-seleccionado

### 🎨 **Personalización Avanzada de Subtítulos**
- **10 opciones de fuente**: Segoe UI, Arial, Helvetica, Times New Roman, y más
- **13 tamaños de fuente**: De 10px a 48px para visibilidad perfecta
- **Posicionamiento arrastrando**: Haz clic "⚙ Reposicionar Subtítulos" y arrastra a cualquier posición de pantalla
- **Auto-limpieza**: Los subtítulos desaparecen después de 2 segundos de silencio
- **Diseño moderno**: Fondos semi-transparentes con contornos de texto

---

**Babel** - ¡Haciendo la traducción en tiempo real accesible para todos! Perfecto para juegos internacionales, ver contenido extranjero, o aprender nuevos idiomas.

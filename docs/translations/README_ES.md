# Babel - Traducción de Audio en Tiempo Real con Superposición de Subtítulos

**[English](../../README.md) | Español | [Français](README_FR.md) | [Deutsch](README_DE.md) | [Português](README_PT.md) | [日本語](README_JA.md) | [한국어](README_KO.md) | [中文](README_ZH.md)**

Una aplicación Python que captura el audio interno de tu PC, lo traduce en tiempo real usando Faster-Whisper y Google Translate, y muestra subtítulos traducidos como superposición en tu pantalla.

## 🌟 Características

### 🎵 **Captura de Audio**
- **Detección automática**: Encuentra automáticamente el mejor dispositivo de loopback (Stereo Mix, Virtual Audio Cable)
- **Selección manual**: Elige entre dispositivos de entrada disponibles con detalles del dispositivo
- **Captura específica de app**: Soporte para Virtual Audio Cable para capturar aplicaciones individuales
- **Audio del sistema**: Captura todo el audio del PC o audio de aplicación específica

### 🧠 **Traducción Impulsada por IA**
- **Reconocimiento de voz**: Usa modelos Faster-Whisper (tiny, turbo, large-v3, distil-large-v3)
- **Detección automática de idioma**: Deja que Whisper detecte automáticamente el idioma de origen
- **90+ idiomas de origen**: Soporte para todos los idiomas principales que Whisper puede transcribir
- **100+ idiomas de destino**: Traduce a cualquier idioma compatible con Google Translate
- **Procesamiento en tiempo real**: Optimizado para baja latencia y uso de memoria

### 📺 **Subtítulos Profesionales**
- **Pantalla superpuesta**: Superposición de subtítulos transparente, siempre en la parte superior
- **Fuentes personalizables**: Elige entre 10 fuentes populares y múltiples tamaños (10px-48px)
- **Reposicionable**: Arrastra subtítulos a cualquier posición en pantalla
- **Limpieza automática**: Los subtítulos desaparecen automáticamente durante el silencio
- **Diseño moderno**: Fondo semi-transparente con contornos de texto para legibilidad

### 🌍 **Interfaz Multiidioma**
- **6 Idiomas de UI**: Inglés, Español, Francés, Alemán, Portugués, Coreano
- **Localización completa**: Todos los menús, botones, descripciones y nombres de idiomas traducidos
- **Cambio dinámico**: Cambia el idioma de la interfaz y ve actualizaciones inmediatas
- **Dropdowns específicos de idioma**: Nombres de idiomas mostrados en el idioma actual de la interfaz

### ⚙️ **Configuraciones Inteligentes**
- **Configuración persistente**: Todas las configuraciones guardadas automáticamente en `babel_settings.json`
- **Modo de rendimiento**: Alterna entre velocidad y precisión
- **Sensibilidad de audio**: Umbral ajustable para filtrar ruido de fondo
- **Navegación alfabética**: Escribe letras en dropdowns para encontrar opciones rápidamente

## 📋 Requisitos

- **Python**: 3.9 o superior
- **Sistema Operativo**: Windows (para captura de audio loopback WASAPI)
- **Memoria**: Al menos 4GB RAM (8GB recomendado para modelos grandes)
- **Almacenamiento**: 1-5GB para modelos Whisper (descargados automáticamente)
- **Internet**: Requerido para API de Google Translate

## 🚀 Instalación

1. **Clona o descarga** este repositorio
2. **Instala dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Ejecuta la aplicación**:
   ```bash
   python main.py
   ```
   O usa el archivo batch proporcionado:
   ```bash
   run.bat
   ```

## 📖 Guía de Inicio Rápido

### Configuración Básica
1. **Inicia** la aplicación: `python main.py`
2. **Entrada de Audio**: Selecciona "Auto (Recomendado)" o elige un dispositivo específico
3. **Idiomas**: 
   - **De**: Elige idioma de origen o "Detectar automáticamente"
   - **A**: Elige idioma de destino (por defecto: Inglés)
4. **Haz clic** "▶️ Iniciar Traducción"

### Consejos de Configuración Inicial
- **Prueba audio**: Habla o reproduce audio para verificar que el micrófono/audio del sistema esté funcionando
- **Ajusta sensibilidad**: Valores más bajos = más sensible a audio bajo
- **Posiciona subtítulos**: Usa "⚙ Reposicionar Subtítulos" para colocarlos donde quieras
- **Elige modelo**: "turbo" es recomendado para velocidad/precisión equilibrada
- **Selección rápida de idioma**: Escribe letras en dropdowns de idioma para saltar a opciones (ej: escribe "I" para Inglés)
- **Todas las configuraciones guardadas**: Tus preferencias se recuerdan automáticamente entre sesiones

## 🌍 Idiomas de la Interfaz de Usuario

Babel soporta los siguientes idiomas para la interfaz de usuario:
- **Inglés** (por defecto)
- **Español** (por defecto)
- **Francés** (Français) 
- **Alemán** (Deutsch)
- **Portugués** (Português)
- **Coreano** (한국어)

Cambia el idioma de la UI en la página "⚙ Configuraciones" usando el dropdown "Idioma de UI". Todos los menús, botones, descripciones, tooltips y nombres de idiomas se mostrarán en tu idioma seleccionado.

## 🗣️ Idiomas Soportados

### Idiomas de Origen (Reconocimiento Whisper)
**Detectar automáticamente**, Afrikáans, Albanés, Amárico, Árabe, Armenio, Asamés, Azerbaiyano, Bashkir, Vasco, Bielorruso, Bengalí, Bosnio, Bretón, Búlgaro, Birmano, Catalán, Chino, Croata, Checo, Danés, Holandés, Inglés, Estonio, Feroés, Finlandés, Francés, Gallego, Georgiano, Alemán, Griego, Gujarati, Haitiano, Hausa, Hawaiano, Hebreo, Hindi, Húngaro, Islandés, Indonesio, Italiano, Japonés, Javanés, Canarés, Kazajo, Jemer, Coreano, Laosiano, Latín, Letón, Lituano, Luxemburgués, Macedonio, Malgache, Malayo, Malayalam, Maltés, Maorí, Maratí, Mongol, Nepalí, Noruego, Occitano, Pastún, Persa, Polaco, Portugués, Punjabí, Rumano, Ruso, Sánscrito, Serbio, Shona, Sindhi, Cingalés, Eslovaco, Esloveno, Somalí, Español, Sundanés, Suajili, Sueco, Tagalo, Tayiko, Tamil, Tártaro, Telugu, Tailandés, Tibetano, Turco, Turcomano, Ucraniano, Urdu, Uzbeko, Vietnamita, Galés, Yídish, Yoruba

### Idiomas de Destino (Google Translate)
**Inglés** (por defecto), Afrikáans, Albanés, Amárico, Árabe, Armenio, Azerbaiyano, Vasco, Bielorruso, Bengalí, Bosnio, Búlgaro, Catalán, Cebuano, Chino (Simplificado), Chino (Tradicional), Corso, Croata, Checo, Danés, Holandés, Esperanto, Estonio, Finlandés, Francés, Frisón, Gallego, Georgiano, Alemán, Griego, Gujarati, Criollo Haitiano, Hausa, Hawaiano, Hebreo, Hindi, Hmong, Húngaro, Islandés, Igbo, Indonesio, Irlandés, Italiano, Japonés, Javanés, Canarés, Kazajo, Jemer, Coreano, Kurdo, Kirguís, Laosiano, Latín, Letón, Lituano, Luxemburgués, Macedonio, Malgache, Malayo, Malayalam, Maltés, Maorí, Maratí, Mongol, Birmano (Birmano), Nepalí, Noruego, Odia (Oriya), Pastún, Persa, Polaco, Portugués, Punjabí, Rumano, Ruso, Samoano, Gaélico Escocés, Serbio, Sesoto, Shona, Sindhi, Cingalés, Eslovaco, Esloveno, Somalí, Español, Sundanés, Suajili, Sueco, Tagalo, Tayiko, Tamil, Tártaro, Telugu, Tailandés, Turco, Turcomano, Ucraniano, Urdu, Uigur, Uzbeko, Vietnamita, Galés, Xhosa, Yídish, Yoruba, Zulú

## ⚙️ Opciones de Configuración

### Configuraciones de Audio
- **Selección de Dispositivo**: Detección automática o selección manual de dispositivo
- **Sensibilidad de Audio**: Umbral 0.001-0.100 para filtrado de ruido
- **Modo de Rendimiento**: Alterna para velocidad vs. precisión optimizada

### Modelos de IA
- **tiny**: Más rápido, precisión básica (~40MB)
- **turbo**: Velocidad/precisión equilibrada (~810MB) - **Recomendado**
- **large-v3**: Mayor precisión, más lento (~3GB)
- **distil-large-v3**: Modelo grande optimizado (~1.5GB)

### Apariencia de Subtítulos
- **Familia de Fuente**: Segoe UI, Arial, Helvetica, Times New Roman, Calibri, Trebuchet MS, Verdana, Georgia, Comic Sans MS, Impact
- **Tamaño de Fuente**: 10px a 48px
- **Posición**: Arrastra para reposicionar en cualquier lugar de la pantalla
- **Limpieza automática**: Los subtítulos desaparecen después de 2 segundos de silencio

## 🎯 Guía de Captura de Audio Específica de App

### Para Aplicaciones Individuales
1. **Instala Virtual Audio Cable** (VB-Cable o similar)
2. **Configura salida de audio de la aplicación** a Virtual Cable
3. **En Babel**: Selecciona el dispositivo Virtual Cable (marcado con 🎯)
4. **Inicia traducción** - ahora solo el audio de esa app será traducido

### Para Audio del Sistema
1. **Habilita Stereo Mix** en configuraciones de Sonido de Windows:
   - Clic derecho en ícono de altavoz → Sonidos → pestaña Grabación
   - Clic derecho en espacio vacío → Mostrar Dispositivos Deshabilitados
   - Habilita "Stereo Mix"
2. **En Babel**: Selecciona dispositivo Stereo Mix (marcado con 🔊) o usa detección automática

### Configuración de Virtual Audio Cable
1. **Descarga** VB-Audio Virtual Cable (gratis)
2. **Instala y reinicia** tu computadora
3. **Configura aplicación objetivo** para salida a "CABLE Input"
4. **En Babel**: Selecciona dispositivo "🎯 CABLE Output"
5. **Opcional**: Configura "CABLE Input" como tu dispositivo de reproducción por defecto para escuchar audio

## 🛠️ Solución de Problemas

### No Se Detecta Audio
- **Verifica selección de dispositivo**: Prueba "Auto (Recomendado)" primero
- **Verifica fuente de audio**: Asegúrate de que el audio esté realmente reproduciéndose
- **Ajusta sensibilidad**: Baja el umbral de sensibilidad de audio
- **Habilita Stereo Mix**: Sigue la guía de configuración de audio del sistema arriba

### La Captura de Audio No Funciona Durante Llamadas (Zoom, Teams, Discord, etc.)
**Este es un problema común al usar aplicaciones de conferencia. Aquí están las soluciones:**

#### **Problema: Conflicto de Modo Exclusivo**
- **Problema**: Las apps de conferencia a menudo toman control exclusivo de dispositivos de audio
- **Solución**: 
  1. Ve a Configuraciones de Sonido de Windows → Propiedades del Dispositivo → Avanzado
  2. Desmarca "Permitir que las aplicaciones tomen control exclusivo de este dispositivo"
  3. Aplica esto tanto a tu micrófono como a los altavoces
  4. Reinicia ambas aplicaciones

#### **Problema: Enrutamiento de Dispositivo de Audio**
- **Problema**: El audio de llamada puede usar dispositivos virtuales o cancelación de eco que evitan el audio del sistema
- **Solución**: 
  1. **Instala un Virtual Audio Cable** (VB-Cable, VoiceMeeter)
  2. **En tu app de conferencia**: Configura salida de audio a Virtual Cable
  3. **En Babel**: Selecciona el Virtual Cable como dispositivo de entrada
  4. **Opcional**: Configura Virtual Cable como dispositivo de reproducción por defecto para escuchar audio

#### **Problema: Aislamiento de Audio Específico de App**
- **Problema**: Algunas apps de conferencia encriptan o aíslan sus streams de audio
- **Soluciones**:
  1. **Usa Windows 11**: Prueba la característica "Application Audio Capture" de OBS
  2. **Cambia configuraciones de app de conferencia**: Busca opciones "Audio del sistema" o "Compartir sonido de computadora"
  3. **Usa versión de navegador**: Las apps de conferencia basadas en web son a menudo más fáciles de capturar
  4. **Prueba VoiceMeeter**: Solución de enrutamiento de audio virtual más avanzada

#### **Arreglos Rápidos para Captura de Audio de Llamada**
1. **Antes de unirse a una llamada**: Inicia Babel y verifica que capture audio del sistema
2. **Usa "Compartir Audio de Computadora"**: Habilita esta opción en tu app de conferencia
3. **Cambia a versión de navegador**: A menudo tiene menos restricciones de audio
4. **Usa auriculares**: Previene bucles de retroalimentación que pueden interferir con captura
5. **Verifica Configuraciones de Privacidad de Windows**: Asegúrate de que los permisos de micrófono estén habilitados para todas las apps

### La Traducción No Funciona
- **Verifica conexión a internet**: Google Translate requiere internet
- **Verifica idiomas**: Asegúrate de que el idioma de origen coincida con el audio real
- **Prueba detección automática**: Deja que Whisper detecte automáticamente el idioma de origen
- **Cambia modelos**: Prueba el modelo "turbo" para mejor precisión

### Problemas de Rendimiento
- **Habilita Modo de Rendimiento**: Reduce uso de memoria y mejora velocidad
- **Usa modelo más pequeño**: Cambia de "large-v3" a "turbo" o "tiny"
- **Cierra otras aplicaciones**: Libera RAM para mejor rendimiento
- **Verifica velocidad de internet**: Conexión lenta afecta velocidad de traducción

### Problemas de Subtítulos
- **Subtítulos no visibles**: Verifica si la superposición está detrás de otras ventanas
- **Posición incorrecta**: Usa "⚙ Reposicionar Subtítulos" para moverlos
- **Fuente muy pequeña/grande**: Ajusta tamaño de fuente en configuraciones
- **No se limpian**: Verifica sensibilidad de audio - puede estar detectando ruido de fondo

## 🔧 Cómo Funciona

### Pipeline de Audio
1. **Captura**: Graba audio del dispositivo seleccionado (audio del sistema o específico de app)
2. **Procesamiento**: Convierte estéreo a mono, aplica filtrado de ruido
3. **Transcripción**: Usa Faster-Whisper para convertir habla a texto
4. **Traducción**: API de Google Translate traduce a idioma de destino
5. **Pantalla**: Muestra subtítulos como superposición con limpieza automática

### Detalles Técnicos
- **Formato de Audio**: 48kHz estéreo, convertido a 16kHz mono para Whisper
- **Tamaño de Chunk**: Segmentos de audio de 3 segundos para procesamiento en tiempo real
- **Gestión de Memoria**: Límites de tamaño de cola (máx 3 chunks) y recolección de basura para eficiencia
- **Optimización de Latencia**: Beam size 1, filtrado VAD, remuestreo optimizado
- **Framework UI**: PyQt5 con widgets AlphabetComboBox personalizados para navegación mejorada
- **Almacenamiento de Configuraciones**: Configuración persistente basada en JSON con guardado automático

### Arquitectura del Sistema de Traducción
- **Archivos JSON Externos**: Todas las traducciones almacenadas en directorio `translations/`
- **Carga Dinámica**: Traducciones cargadas automáticamente al inicio
- **Detección de Idioma**: Traducciones hardcoded previenen problemas de recursión
- **Localización Completa**: Texto de UI, nombres de idiomas, descripciones todos traducidos
- **Mapeo Inverso**: Nombres de idiomas traducidos convertidos de vuelta a inglés para almacenamiento de configuraciones

### Persistencia de Configuraciones
Todas las configuraciones se guardan automáticamente en `babel_settings.json`:
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
  "ui_language": "Spanish"
}
```

## 📁 Estructura de Archivos

```
babel/
├── main.py                    # Archivo principal de la aplicación
├── requirements.txt           # Dependencias de Python
├── babel_settings.json        # Configuraciones de usuario auto-guardadas
├── run.bat                   # Archivo batch de Windows para ejecutar la app
├── logo.png                  # Logo de la aplicación
├── translations/             # Archivos de traducción de UI
│   ├── en.json              # Traducciones en inglés
│   ├── es.json              # Traducciones en español
│   ├── fr.json              # Traducciones en francés
│   ├── de.json              # Traducciones en alemán
│   ├── pt.json              # Traducciones en portugués
│   └── ko.json              # Traducciones en coreano
└── README.md                 # Esta documentación
```

## 🎮 Uso Avanzado

### Dispositivos de Audio Personalizados
La aplicación detecta automáticamente:
- **🎯 Virtual Audio Cables**: Para captura específica de app
- **🔊 Dispositivos de Audio del Sistema**: Para captura de audio completo del sistema  
- **🎤 Entradas de Micrófono**: Para fuentes de audio externas

### Ajuste de Rendimiento
- **Para Velocidad**: Usa modelo "tiny" + Modo de Rendimiento habilitado
- **Para Precisión**: Usa modelo "large-v3" + Modo de Rendimiento deshabilitado
- **Equilibrado**: Usa modelo "turbo" (por defecto recomendado)

### Uso de Memoria
- **modelo tiny**: ~200MB RAM
- **modelo turbo**: ~1GB RAM  
- **modelo large-v3**: ~4GB RAM
- **distil-large-v3**: ~2GB RAM

## 📚 Soporte y Contribución

### Obtener Ayuda
1. **Verifica este README** para soluciones comunes
2. **Verifica requisitos**: Python 3.9+, SO Windows
3. **Prueba con audio simple**: Prueba con habla clara primero
4. **Verifica la consola**: Ejecuta desde línea de comandos para ver mensajes de error

### Limitaciones Conocidas
- **Solo Windows**: La captura de audio loopback WASAPI requiere Windows
- **Internet requerido**: La API de Google Translate necesita conexión a internet
- **Descargas de modelo**: La primera ejecución descarga modelos Whisper (pueden ser grandes)
- **Procesamiento en tiempo real**: Algo de retraso es normal (1-3 segundos)

### Mejoras Futuras
- Soporte para Linux/macOS
- Opciones de traducción offline
- Temas de subtítulos personalizados
- Procesamiento de archivos en lote
- API para integraciones externas

## 🆕 Características y Actualizaciones Más Recientes

### **Experiencia de Usuario Mejorada** 
- **Todas las configuraciones auto-guardadas**: Cada configuración automáticamente guardada en `babel_settings.json`
- **Navegación alfabética**: Escribe letras en dropdowns para saltar rápidamente a idiomas
- **UI mejorada**: Tema oscuro moderno con mejor espaciado y retroalimentación visual
- **Valores por defecto inteligentes**: Idioma de destino inglés, modelo turbo pre-seleccionado

### **Localización Completa de Interfaz**
- **6 Idiomas de UI**: Soporte completo para Inglés, Español, Francés, Alemán, Portugués, Coreano
- **Cambio dinámico de idioma**: Cambia idioma de interfaz y ve actualizaciones inmediatas
- **Traducciones hardcoded**: Todos los nombres de idiomas traducidos para prevenir recursión
- **Cobertura integral**: 70+ idiomas traducidos en cada idioma de interfaz

### **Personalización Avanzada de Subtítulos**
- **10 opciones de fuente**: Segoe UI, Arial, Helvetica, Times New Roman y más
- **13 tamaños de fuente**: De 10px a 48px para visibilidad perfecta
- **Posicionamiento por arrastre**: Haz clic "⚙ Reposicionar Subtítulos" y arrastra a cualquier posición de pantalla
- **Limpieza automática**: Los subtítulos desaparecen después de 2 segundos de silencio
- **Diseño moderno**: Fondos semi-transparentes con contornos de texto

### **Detección Inteligente de Dispositivo de Audio**
- **Auto-categorización**: Dispositivos marcados con 🎯 (Virtual Cable), 🔊 (Audio del Sistema), 🎤 (Micrófono)
- **Prioridad inteligente**: Selecciona automáticamente el mejor dispositivo loopback disponible
- **Detalles del dispositivo**: Muestra canales y tasa de muestreo para cada dispositivo
- **Capacidad de actualización**: Actualiza lista de dispositivos sin reiniciar

### **Optimizaciones de Rendimiento**
- **Modo de Rendimiento**: Alterna para optimización velocidad vs precisión
- **Gestión de memoria**: Recolección de basura automática y límites de tamaño de cola
- **Modelos optimizados**: Soporte para distil-large-v3 (modelo grande optimizado)
- **Filtrado VAD**: Detección de Actividad de Voz para reducir procesamiento de silencio

---

**Babel** - ¡Haciendo la traducción en tiempo real accesible para todos! ¡Perfecto para juegos internacionales, ver contenido extranjero o aprender nuevos idiomas!

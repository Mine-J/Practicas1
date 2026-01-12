# 🔐 Evaluador de Contraseñas Avanzado

Sistema de análisis de seguridad de contraseñas que combina heurísticas personalizadas, detección de patrones comunes, normalización Leet Speak y verificación contra bases de datos de contraseñas filtradas mediante la API de HaveIBeenPwned.

---

## 📋 Descripción

Este proyecto proporciona una herramienta completa para evaluar la fortaleza de contraseñas mediante múltiples criterios de seguridad. Utiliza un enfoque multicapa que incluye:

- **Análisis heurístico configurable** mediante variables de entorno
- **Diccionario de +10,000 contraseñas comunes** con características detalladas
- **Detección inteligente de patrones** (Leet Speak, fechas, palabras comunes)
- **Cálculo de entropía** y estimación de tiempo de crackeo
- **Verificación en tiempo real** contra bases de datos de contraseñas filtradas
- **Interfaz de terminal adaptativa** centrada y responsiva

---

## ✨ Características Principales

### 🎯 Análisis Multicapa

- ✅ **Longitud y Complejidad**: Evalúa caracteres, mayúsculas, minúsculas, números y símbolos especiales
- 🔍 **Detección de Palabras Comunes**: Base de datos con 10,000+ contraseñas débiles incluyendo características (longitud, tipos de caracteres, vocales, sílabas)
- 🎭 **Normalización Leet Speak Avanzada**: Detecta más de 100 sustituciones diferentes (`@`, `3`, `1`, `0`, `$`, `!`, `|_|`, `><`, etc.)
- 📅 **Detección de Fechas**: Identifica años entre 1900-2099 en cualquier posición
- 🌐 **Verificación API HaveIBeenPwned**: Comprueba si la contraseña (o su versión normalizada) ha sido filtrada
- 🧮 **Cálculo de Entropía**: Estima bits de entropía basado en el alfabeto utilizado
- ⏱️ **Estimación de Tiempo de Crackeo**: Calcula tiempo estimado contra GPUs modernas (40 mil millones intentos/s)

### 🎨 Interfaz de Usuario

- 📱 **Diseño Responsivo**: Se adapta automáticamente al tamaño del terminal
- 🎯 **Pantalla de Inicio**: Muestra ejemplos de contraseñas para probar
- 📊 **Resultados Detallados**: Visualización clara con emojis, puntuación, entropía y tiempo de crackeo
- 💡 **Recomendaciones Personalizadas**: Sugerencias específicas basadas en debilidades detectadas
- 🔍 **Palabras Detectadas**: Lista todas las palabras comunes encontradas en la contraseña

### ⚙️ Configuración Avanzada

- 🔧 **Puntuación Personalizable**: Archivo `.env` para ajustar pesos del sistema heurístico
- 📝 **Ejemplo Incluido**: Archivo `.env.example` con configuración predeterminada
- 🔄 **Valores por Defecto**: Funciona sin configuración (fallback automático)

---

## 🚀 Instalación

### Requisitos Previos

- **Python 3.7+** (Recomendado: Python 3.9 o superior)
- **Conexión a Internet** (para verificación API HaveIBeenPwned)

### Instalación Paso a Paso

1. **Clona o descarga el repositorio**

2. **Navega al directorio del proyecto**:

   ```bash
   cd Practicas1
   ```

3. **Instala las dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

4. **(Opcional) Configura las variables de entorno**:

   Copia el archivo de ejemplo y ajusta los valores:

   ```bash
   cp .env.example .env
   ```

   Edita `.env` con tus preferencias:

   ```env
   puntuacionHeuristicoLongitudMayor16 = 3
   puntuacionHeuristicoLongitudMayor12 = 2
   puntuacionHeuristicoLongitudMayor8 = 1
   puntuacionHeuristicoMayusculas = 1
   puntuacionHeuristicoMinusculas = 1
   puntuacionHeuristicoNumeros = 1
   puntuacionHeuristicoSimbolos = 2
   puntuacionHeuristicoCSV = 2
   puntuacionHeuristicoLeetSpeak = 3
   puntuacionHeuristicoFechas = 2
   puntuacionHeuristicoFiltrada = 5
   ```

---

## 📖 Uso

### Ejecutar el Evaluador

```bash
python Memoria.py
```

### Flujo de Uso

1. **Pantalla de Inicio**: El programa muestra ejemplos de contraseñas para probar
2. **Introduce una contraseña**: Escribe cualquier contraseña para evaluar
3. **Revisa los resultados**: Observa la puntuación, nivel, entropía y recomendaciones
4. **Evalúa otra**: Escribe `s` para continuar o `n` para salir

### Ejemplos de Contraseñas para Probar

| Contraseña     | Tipo                      | Resultado Esperado                            |
| -------------- | ------------------------- | --------------------------------------------- |
| `password123`  | Palabra común con números | 🔴 Muy Débil - Detecta "password"             |
| `p@ssw0rd`     | Leet speak                | 🔴 Muy Débil - Normaliza y detecta "password" |
| `abc12345`     | Secuencia + substring     | 🟠 Débil - Detecta "abc"                      |
| `Test2024!`    | Contiene año              | 🟡 Media - Penaliza por año 2024              |
| `qwerty123`    | Patrón de teclado         | 🟠 Débil - Detecta "qwerty"                   |
| `1qaz2wsx`     | Patrón diagonal           | 🟠 Débil - Patrón común de teclado            |
| `K7#mPq9$Lx2w` | Aleatoria fuerte          | 💚 Muy Fuerte - Alta entropía                 |

### Interpretación de Resultados

#### Niveles de Seguridad

| Emoji | Nivel      | Puntuación | Descripción                                                |
| ----- | ---------- | ---------- | ---------------------------------------------------------- |
| 🔴    | Muy Débil  | 0-2 puntos | Contraseña extremadamente insegura, cambiar inmediatamente |
| 🟠    | Débil      | 3-5 puntos | Contraseña vulnerable, requiere mejoras significativas     |
| 🟡    | Media      | 6-7 puntos | Contraseña aceptable pero mejorable                        |
| 🟢    | Fuerte     | 8-9 puntos | Contraseña robusta, buena protección                       |
| 💚    | Muy Fuerte | 10+ puntos | Contraseña excelente, máxima seguridad                     |

#### Métricas Mostradas

- **Puntuación**: De 0 a 10+ según criterios heurísticos
- **Entropía**: Bits de entropía (mayor = mejor)
- **Tiempo de Crackeo**: Estimación contra GPU moderna
- **Palabras Comunes**: Lista de palabras detectadas del diccionario
- **Recomendaciones**: Sugerencias específicas de mejora

---

## 📁 Estructura del Proyecto

```
Practicas1/
├── Memoria.py                     # 🔐 Evaluador principal de contraseñas
├── Psswd_comunes.csv              # 📊 Dataset 10,000+ contraseñas comunes
├── requirements.txt               # 📦 Dependencias del proyecto
├── .env.example                   # 📝 Plantilla de configuración
├── .gitignore                     # 🚫 Archivos excluidos de Git
├── README.md                      # 📖 Este archivo
│
└── backUp/                        # 💾 Respaldos y versiones anteriores
```

---

## 🔧 Dependencias

### Librerías Externas

| Librería          | Versión | Propósito                                                                |
| ----------------- | ------- | ------------------------------------------------------------------------ |
| **requests**      | 2.32.4  | Comunicación con API HaveIBeenPwned para verificar contraseñas filtradas |
| **python-dotenv** | 1.1.1   | Carga de variables de entorno desde archivo `.env`                       |

### Módulos Estándar de Python

`csv`, `hashlib`, `math`, `os`, `re`, `time`

---

## 🎯 Sistema de Puntuación

### Puntos Positivos ✅

| Criterio                     | Puntos | Descripción                               |
| ---------------------------- | ------ | ----------------------------------------- |
| Longitud ≥ 16 caracteres     | +3     | Longitud óptima para seguridad moderna    |
| Longitud ≥ 12 caracteres     | +2     | Longitud recomendada mínima               |
| Longitud ≥ 8 caracteres      | +1     | Longitud mínima aceptable                 |
| Contiene minúsculas (a-z)    | +1     | Aumenta alfabeto disponible               |
| Contiene mayúsculas (A-Z)    | +1     | Aumenta alfabeto disponible               |
| Contiene números (0-9)       | +1     | Aumenta alfabeto disponible               |
| Contiene símbolos (!@#$...)  | +2     | Aumenta significativamente la complejidad |
| No está en diccionario común | +2     | Evita palabras conocidas                  |

**Puntuación máxima sin penalizaciones**: 11 puntos

### Penalizaciones ❌

| Criterio                         | Puntos | Descripción                                 |
| -------------------------------- | ------ | ------------------------------------------- |
| Contiene palabra común           | -2     | Palabra encontrada en dataset de 10,000+    |
| Usa Leet Speak con palabra común | -3     | Detectado tras normalización (ej: p@ssw0rd) |
| Contiene año (1900-2099)         | -2     | Fechas fáciles de adivinar                  |
| Filtrada en HaveIBeenPwned       | -5     | Contraseña comprometida públicamente        |
| Versión normalizada filtrada     | -5     | Contraseña equivalente comprometida         |

**Nota**: La puntuación mínima es 0 (no puede ser negativa)

---

## 🔒 Detalles Técnicos de Seguridad

### Cálculo de Entropía

```
Entropía = log₂(alfabeto^longitud) bits
```

**Tamaños de Alfabeto**:

- Minúsculas: 27 caracteres (incluye ñ)
- Mayúsculas: 27 caracteres (incluye Ñ)
- Números: 10 caracteres (0-9)
- Símbolos especiales: 32 caracteres (!@#$%^&\*()-\_=+[]{}|;:,.<>?/`~"'\)

**Ejemplo**:

- Contraseña: `K7#mPq9$Lx2w` (12 caracteres, 4 tipos)
- Alfabeto total: 27+27+10+32 = 96 caracteres
- Entropía: log₂(96^12) ≈ 79.45 bits

### Estimación de Tiempo de Crackeo

**Asunciones**:

- **Velocidad de ataque**: 40,000,000,000 intentos/segundo (GPU moderna como RTX 4090)
- **Método**: Fuerza bruta completa
- **Cálculo**: Combinaciones totales / Intentos por segundo

**Escalas de Tiempo**:

- < 1 segundo → 🔴 Inmediato
- Minutos/Horas → 🟠 Muy vulnerable
- Días/Semanas → 🟡 Vulnerable
- Años → 🟢 Segura
- Miles/Millones de años → 💚 Muy segura

### Normalización Leet Speak (Muestra)

El sistema detecta **100+ sustituciones**, incluyendo:

| Leet                | Normal | Ejemplos de Uso              |
| ------------------- | ------ | ---------------------------- |
| `@`, `4`, `/\`, `^` | `a`    | `p@ss`, `h4cker`, `/\dmin`   |
| `3`, `€`, `&`       | `e`    | `l33t`, `t€st`, `h&llo`      |
| `1`, `!`, `\|`      | `i`    | `adm1n`, `sh!t`, `w\|n`      |
| `0`, `()`, `[]`     | `o`    | `p@ssw0rd`, `l()ve`, `c[]ol` |
| `$`, `5`            | `s`    | `pa$$`, `5ystem`             |
| `7`, `+`            | `t`    | `7est`, `ge+`                |
| `\|_\|`, `µ`        | `u`    | `\|_\|ser`, `µltra`          |

**Ver código para lista completa** en la función `normalizar_leet_speak()`

### Dataset de Contraseñas Comunes

**Archivo**: [Psswd_comunes.csv](Psswd_comunes.csv)

**Estructura**:

```csv
password,length,num_chars,num_digits,num_upper,num_lower,num_special,num_vowels,num_syllables
123456,6,0,6,0,0,0,0,1
password,8,8,0,0,8,0,2,2
qwerty,6,6,0,0,6,0,1,3
...
```

**Características**:

- **10,000+ contraseñas reales** filtradas de brechas de seguridad
- **Metadatos completos**: longitud, tipos de caracteres, vocales, sílabas
- Incluye: secuencias numéricas, palabras comunes, patrones de teclado, nombres populares

### Integración con HaveIBeenPwned API

**Método**: k-Anonymity (privacidad preservada)

1. Calcula SHA-1 de la contraseña
2. Envía solo los primeros 5 caracteres del hash
3. Recibe lista de sufijos coincidentes
4. Compara localmente el sufijo completo

**Ejemplo**:

```python
password = "password123"
sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
# sha1 = "CBFDAC6008F9CAB4083784CBD1874F76618D2A97"
prefix = sha1[:5]  # "CBFDA"
# API devuelve sufijos que empiezan con "CBFDA"
# Se verifica localmente si "C6008F9CAB4083784CBD1874F76618D2A97" está en la lista
```

**Ventajas**:

- ✅ La contraseña nunca se envía completa
- ✅ Privacidad garantizada mediante k-anonymity
- ✅ Base de datos de +800 millones de contraseñas filtradas

---

## 📊 Formato de Salida

### Pantalla de Inicio

```
═══════════════════════════════════════════════════════════════════════════════
              🔐  EVALUADOR DE CONTRASEÑAS AVANZADO

              Prueba estas contraseñas de ejemplo:
              • password123  (palabra común)
              • p@ssw0rd     (leet speak)
              • abc12345     (secuencia + substring común)
              • Test2024!    (contiene año)
              • qwerty123    (teclado + substring)
              • 1qaz2wsx     (patrón diagonal teclado)
              • K7#mPq9$Lx2w (muy fuerte)
═══════════════════════════════════════════════════════════════════════════════
```

### Pantalla de Resultados

```
═══════════════════════════════════════════════════════════════════════════════
                         Contraseña: password123
═══════════════════════════════════════════════════════════════════════════════
                🔴 Nivel: Muy Débil | Puntuación: 0/10
═══════════════════════════════════════════════════════════════════════════════
                      🔐 Entropía: 35.27 bits
              ⏱️  Tiempo estimado de crackeo: < 1 segundo
═══════════════════════════════════════════════════════════════════════════════
                          RECOMENDACIONES
═══════════════════════════════════════════════════════════════════════════════
          • Incluye letras mayúsculas para mayor complejidad.
            • Incluye símbolos especiales como !, @, #, $...
           • Evita palabras comunes o nombres personales.
═══════════════════════════════════════════════════════════════════════════════
                    PALABRAS COMUNES DETECTADAS
═══════════════════════════════════════════════════════════════════════════════
                             • password
═══════════════════════════════════════════════════════════════════════════════
```

---

## 🛡️ Buenas Prácticas de Contraseñas

### Recomendaciones del Programa

El evaluador genera sugerencias automáticas según las debilidades detectadas:

- 📏 **Longitud insuficiente** → Aumentar a mínimo 12-16 caracteres
- 🔤 **Sin mayúsculas** → Incluir al menos una letra mayúscula
- 🔡 **Sin minúsculas** → Incluir al menos una letra minúscula
- 🔢 **Sin números** → Añadir números no secuenciales
- 🔣 **Sin símbolos** → Incorporar símbolos especiales (!@#$%...)
- 📖 **Palabra común** → Evitar palabras del diccionario
- 🎭 **Leet speak detectado** → No confiar en sustituciones simples
- 📅 **Contiene año** → Evitar fechas personales o actuales
- 🚨 **Contraseña filtrada** → Cambiar inmediatamente y usar gestor de contraseñas

### Consejos Generales

1. ✅ **Usa un gestor de contraseñas** (Bitwarden, 1Password, KeePass)
2. ✅ **Genera contraseñas aleatorias** de 16+ caracteres
3. ✅ **Contraseña única** por servicio
4. ✅ **Activa autenticación de dos factores** (2FA/MFA)
5. ✅ **Cambia contraseñas filtradas** inmediatamente
6. ❌ **Evita información personal** (nombres, fechas, lugares)
7. ❌ **No reutilices contraseñas** entre servicios
8. ❌ **No confíes en patrones simples** (leet speak, secuencias)

---

## ⚠️ Advertencias y Limitaciones

### Seguridad

- 🔒 **NO almacena contraseñas**: Todas las contraseñas se procesan en memoria y se descartan
- 🌐 **Requiere Internet**: Para verificación API (funciona parcialmente sin conexión)
- 🔐 **Hashes seguros**: Usa SHA-1 solo para API (no para almacenamiento de contraseñas)
- 🚨 **Uso educativo**: Herramienta para análisis y aprendizaje, no para auditorías profesionales

### Privacidad

- ✅ **k-Anonymity**: La API nunca recibe la contraseña completa
- ✅ **Sin registro**: No se guardan logs de contraseñas evaluadas
- ✅ **Procesamiento local**: Todas las verificaciones se hacen en tu máquina

### Limitaciones Técnicas

- ⏱️ **Tiempo de crackeo estimado**: Basado en hardware actual, puede variar
- 📊 **Dataset finito**: 10,000 contraseñas comunes (existen más en la realidad)
- 🎯 **Heurística no perfecta**: Una puntuación alta no garantiza seguridad absoluta
- 🔍 **Leet speak**: Detecta patrones comunes pero no todas las variantes posibles

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas para mejorar el evaluador:

### Cómo Contribuir

1. **Fork** el proyecto
2. Crea una **rama** para tu feature:
   ```bash
   git checkout -b feature/MejorDeteccion
   ```
3. **Commit** tus cambios:
   ```bash
   git commit -m 'feat: Añade detección de patrones de teclado AZERTY'
   ```
4. **Push** a la rama:
   ```bash
   git push origin feature/MejorDeteccion
   ```
5. Abre un **Pull Request**

### Ideas para Contribuir

- 🔍 Ampliar diccionario de contraseñas comunes
- 🎭 Añadir más patrones Leet Speak
- 🌍 Soporte multiidioma (diccionarios en otros idiomas)
- 📊 Exportar resultados a JSON/CSV
- 🎨 Mejorar interfaz con colores ANSI
- 🧪 Añadir tests unitarios
- 📈 Métricas adicionales de seguridad

---

## 📝 Licencia

Este proyecto es de **uso educativo** y académico.

Desarrollado como parte del trabajo de **Prácticas** en la **Universidad Antonio de Nebrija**, Curso 2025-2026.

### Uso Permitido

✅ Uso académico y educativo  
✅ Modificación y mejora  
✅ Distribución con atribución

### Uso NO Permitido

❌ Uso comercial sin autorización  
❌ Evaluación de contraseñas de terceros sin consentimiento  
❌ Almacenamiento de contraseñas evaluadas

---

## 👥 Autor

**Proyecto de Prácticas - Universidad Antonio de Nebrija**

📧 Contacto: [A través del repositorio]  
🏫 Universidad: Universidad Antonio de Nebrija  
📅 Curso: 2025-2026  
📚 Asignatura: Prácticas I

---

## 🙏 Agradecimientos

- **HaveIBeenPwned API** - Por proporcionar acceso gratuito a su base de datos de contraseñas filtradas
- **Universidad Antonio de Nebrija** - Por el apoyo académico y recursos
- **Comunidad de Seguridad** - Por las mejores prácticas y recomendaciones

---

## 📚 Referencias

- [HaveIBeenPwned API](https://haveibeenpwned.com/API/v3)

---

<div align="center">

**⭐ Si este proyecto te resulta útil, considera darle una estrella ⭐**

**Última actualización**: 12 de enero de 2026

</div>

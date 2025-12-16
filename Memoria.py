import csv
import hashlib
import math
import os
import re
import requests
import time
from dotenv import load_dotenv

def cargar_csv(ruta_archivo):
    psswd = set()
    try:
        with open(ruta_archivo, newline='', encoding="utf-8") as csvfile:
            lector = csv.reader(csvfile)
            for fila in lector:
                if fila:
                    palabra = fila[0].strip().lower()
                    psswd.add(palabra)
    except FileNotFoundError:
        print(f"No se ha podido encontrar el archivo '{ruta_archivo}'")
        
    return psswd
    
def limpiar_consola():
    os.system("cls" if os.name == "nt" else "clear")

def calcular_heuristico(psswd_introducida, csv_psswd):
    puntuacion = 0
    detalles = []
    
    load_dotenv()
    PUNTOS_LONG_16 = int(os.getenv("puntuacionHeuristicoLongitudMayor16"))
    PUNTOS_LONG_12 = int(os.getenv("puntuacionHeuristicoLongitudMayor12"))
    PUNTOS_LONG_8  = int(os.getenv("puntuacionHeuristicoLongitudMayor8"))
    PUNTOS_MAYUSCULAS = int(os.getenv("puntuacionHeuristicoMayusculas", "1"))
    PUNTOS_MINUSCULAS = int(os.getenv("puntuacionHeuristicoMinusculas", "1"))
    PUNTOS_NUMEROS     = int(os.getenv("puntuacionHeuristicoNumeros", "1"))
    PUNTOS_SIMBOLOS    = int(os.getenv("puntuacionHeuristicoSimbolos", "2"))
    PUNTOS_CSV         = int(os.getenv("puntuacionHeuristicoCSV", "2"))
    PUNTOS_LEET        = int(os.getenv("puntuacionHeuristicoLeetSpeak", "3"))
    PUNTOS_FECHAS      = int(os.getenv("puntuacionHeuristicoFechas", "2"))
    PUNTOS_FILTRADA    = int(os.getenv("puntuacionHeuristicoFiltrada", "5"))

    # Longitud
    if len(psswd_introducida) >= 16:
        puntuacion += PUNTOS_LONG_16
    elif len(psswd_introducida) >= 12:
        puntuacion += PUNTOS_LONG_12
    elif len(psswd_introducida) >= 8:
        puntuacion += PUNTOS_LONG_8
    else:
        detalles.append("Menos de 8 caracteres (0) puntos")
    
    # Tipos de caracteres
    if any(c.islower() for c in psswd_introducida):
        puntuacion += PUNTOS_MINUSCULAS
    else:
        detalles.append("No tiene minúsculas")
        
    if any(c.isupper() for c in psswd_introducida):
        puntuacion += PUNTOS_MAYUSCULAS
    else:
        detalles.append("No tiene mayúsculas")
        
    if any(c.isdigit() for c in psswd_introducida):
        puntuacion += PUNTOS_NUMEROS
    else:
        detalles.append("No tiene números")

    if any(c in '!@#$%^&*()-_=+[]{}|;:,.<>?/' for c in psswd_introducida):
        puntuacion += PUNTOS_SIMBOLOS
    else:
        detalles.append("No tiene símbolos")
    
    # Palabras comunes
    palabras_comunes_detectadas = []
    resultado, palabras = is_csv_psswd(psswd_introducida, csv_psswd)
    # is_csv_psswd devuelve (True/False, [lista_palabras])
    if not resultado:
        puntuacion += PUNTOS_CSV
    else:
        puntuacion -= PUNTOS_CSV
        palabras_comunes_detectadas = palabras
        detalles.append(f"Contiene palabra(s) común(es) ({len(palabras)}) (-2) puntos")

    # Leet speak
    if psswd_refactorizada(psswd_introducida, csv_psswd):
        puntuacion -= PUNTOS_LEET
        detalles.append("Usa leet speak con palabra común (p@ssw0rd) (-3) puntos")
    
    # Años
    if contiene_fecha(psswd_introducida):
        puntuacion -= PUNTOS_FECHAS
        detalles.append("Contiene año (1900-2099) (-2) puntos")
    
    # Comprobar pwnedpasswords para la contraseña tal cual
    encontrado, cantidad = verificar_psswd_en_api(psswd_introducida)
    if encontrado:
        puntuacion -= PUNTOS_FILTRADA
        detalles.append(f"Contraseña encontrada en pwnedpasswords ({cantidad} veces) (-5) puntos")
    else:
        # Si no se encuentra, también comprobar la versión normalizada (por si usa leet speak)
        psswd_normalizada = normalizar_leet_speak(psswd_introducida)
        if psswd_normalizada != psswd_introducida:
            encontrado_norm, cantidad_norm = verificar_psswd_en_api(psswd_normalizada)
            if encontrado_norm:
                puntuacion -= PUNTOS_FILTRADA
                detalles.append(f"Contraseña equivalente tras normalizar leet ('{psswd_normalizada}') encontrada en pwnedpasswords ({cantidad_norm} veces) (-5) puntos")
            


    if puntuacion < 0:
        puntuacion = 0
    # Nivel final
    if puntuacion <= 2:
        nivel = "Muy Débil"
        emoji = "🔴"
    elif puntuacion <= 5:
        nivel = "Débil"
        emoji = "🟠"
    elif puntuacion <= 7:
        nivel = "Media"
        emoji = "🟡"
    elif puntuacion <= 9:
        nivel = "Fuerte"
        emoji = "🟢"
    else:
        nivel = "Muy Fuerte"
        emoji = "💚"
    
    return nivel, puntuacion, emoji, detalles, palabras_comunes_detectadas

def is_csv_psswd(psswd, csv_psswd):
    """Comprueba si la contraseña contiene una palabra común completa (o como substring).
    Devuelve (True, [lista_palabras]) si encuentra coincidencias, (False, []) si no."""
        
    if not csv_psswd:
        return False, []
 
    psswd_lower = psswd.lower()
    palabras_encontradas = []
    for palabra in csv_psswd:
        if palabra and palabra in psswd_lower:
            palabras_encontradas.append(palabra)
    
    if palabras_encontradas:
        return True, palabras_encontradas
    return False, []

def contiene_fecha(psswd):
    """Detecta años entre 1900 y 2099"""
    fecha = re.findall(r'(19\d{2}|20\d{2})', psswd)
    return len(fecha) > 0

def normalizar_leet_speak(texto):
    """Convierte leet speak a texto normal para detectar palabras comunes"""
    reemplazos = {
        # A
        '4': 'a', '@': 'a', '/\\': 'a', '/-\\': 'a', '?': 'a', '^': 'a', 'α': 'a', 'λ': 'a',
        # B
        '8': 'b', '|3': 'b', 'ß': 'b', 'l³': 'b', '13': 'b', 'i3': 'b', 'j3': 'b',
        # C
        '(': 'c', '[': 'c', '<': 'c', '©': 'c', '¢': 'c',
        # D
        '|)': 'd', '|]': 'd', 'ð': 'd', 'đ': 'd', '1)': 'd',
        # E
        '3': 'e', '€': 'e', '&': 'e', '£': 'e', 'ε': 'e',
        # F
        '|=': 'f', '|*|-|': 'f', '|"': 'f', 'ƒ': 'f', 'l²': 'f',
        # G
        '6': 'g', '9': 'g',
        # H
        '#': 'h', '|-|': 'h', '}{': 'h', ']-[': 'h', '/-/': 'h', ')-(': 'h',
        # I
        '!': 'i', '1': 'i', '|': 'i', '][': 'i', 'ỉ': 'i',
        # J
        '_|': 'j', '¿': 'j',
        # K
        '|<': 'k', '|{': 'k', '|(': 'k', 'x': 'k',
        # L
        '|_': 'l', '£': 'l', '][_': 'l',
        # M
        '/\\/\\': 'm', '/v\\': 'm', '|v|': 'm', ']v[': 'm', '|\\/|': 'm', 'aa': 'm', '[]v[]': 'm',
        '|11': 'm', '/|\\': 'm', '^^': 'm', '(v)': 'm', '|y|': 'm', '!\\/!': 'm',
        # N
        '|\\|': 'n', '/\\/': 'n', '/v': 'n', '|v': 'n', '/\\\\/': 'n', '|1': 'n', '2': 'n',
        '(\\)': 'n', '11': 'n', 'r': 'n', '!\\!': 'n',
        # Ñ
        '~': 'ñ',
        # O
        '0': 'o', '()': 'o', '[]': 'o', '*': 'o', '°': 'o', '<>': 'o', 'ø': 'o', '{[]}': 'o',
        # P
        '|°': 'p', 'p': 'p', '|>': 'p', '|*': 'p', '[]d': 'p', '][d': 'p', '|²': 'p', '|?': 'p', '|d': 'p',
        # Q
        '0_': 'q', '0,': 'q',
        # R
        '|2': 'r', '1²': 'r', '®': 'r', 'я': 'r', '12': 'r', '.-': 'r',
        # S
        '5': 's', '$': 's', '§': 's', 'ŝ': 's', 'ş': 's',
        # T
        '7': 't', '+': 't', '†': 't', "']['": 't',
        # U
        '|_|': 'u', 'µ': 'u', '[_]': 'u', 'v': 'u',
        # V
        '\\/': 'v', '|/': 'v', '\\|': 'v', "\\'": 'v',
        # W
        '\\/\\/': 'w', 'vv': 'w', '\\a/': 'w', 'uJ': 'w', 'uu': 'w', '\\^/': 'w', '\\|/': 'w',
        # X
        '><': 'x', ')(': 'x', '}{': 'x', '%': 'x', '×': 'x',
        # Y
        '`/': 'y', '°/': 'y', '¥': 'y',
        # Z
        'z': 'z', '"/_': 'z',
    }
    texto_normalizado = texto.lower()
    for leet, normal in reemplazos.items():
        texto_normalizado = texto_normalizado.replace(leet, normal)
    return texto_normalizado

def psswd_refactorizada(psswd, palabras_comunes):
    if not palabras_comunes:
        return False
    texto_normalizado = normalizar_leet_speak(psswd)
    exists, _ = is_csv_psswd(texto_normalizado, palabras_comunes)
    return exists

def obtener_dimensiones_terminal():
    size = os.get_terminal_size()
    return size.columns, size.lines
    
def mostrar_pantalla_inicio():
    """Muestra la pantalla de inicio centrada"""
    ancho, alto = obtener_dimensiones_terminal()
    
    lineas = [
        "🔐  EVALUADOR DE CONTRASEÑAS AVANZADO",
        "",
        "Prueba estas contraseñas de ejemplo:",
        "• password123  (palabra común)",
        "• p@ssw0rd     (leet speak)",
        "• abc12345     (secuencia + substring común)",
        "• Test2024!    (contiene año)",
        "• qwerty123    (teclado + substring)",
        "• 1qaz2wsx     (patrón diagonal teclado)",
        "• K7#mPq9$Lx2w (muy fuerte)"
    ]
    
    # Calcular espacio vertical
    lineas_contenido = len(lineas) + 4
    espacio_superior = max(0, (alto - lineas_contenido) // 2)
    
    # Limpiar y mostrar
    limpiar_consola()
    print("\n" * espacio_superior)
    
    linea = "═" * ancho
    print(linea)
    for texto in lineas:
        print(texto.center(ancho))
    print(linea)

def calcular_entropia(psswd):
    """Calcula la entropía de la contraseña en bits"""
    
    combinaciones = 0
    if any(c.islower() for c in psswd):
        combinaciones += 27
    if any(c.isupper() for c in psswd):
        combinaciones += 27
    if any(c.isdigit() for c in psswd):
        combinaciones += 10
    if any(c in '!@#$%^&*()-_=+[]{}|;:,.<>?/`~"\\\'' for c in psswd):
        combinaciones += 32

    if combinaciones == 0:
        return 0
    
    # Entropía = log2(alfabeto^longitud) = longitud * log2(alfabeto)
    entropia =  math.log2(pow(combinaciones, len(psswd)))
    return round(entropia, 2)

def estimar_tiempo_crackeo(entropia):
    """Estima el tiempo para crackear basado en la entropía"""
    # Asumiendo 40 mil millones de intentos por segundo (GPU moderna)
    intentos_por_segundo = 40_000_000_000
    
    combinaciones = 2 ** entropia
    segundos = combinaciones / intentos_por_segundo
    
    if segundos < 1:
        return "< 1 segundo"
    elif segundos < 60:
        return f"{int(segundos)} segundos"
    elif segundos < 3600:
        return f"{int(segundos/60)} minutos"
    elif segundos < 86400:
        return f"{int(segundos/3600)} horas"
    elif segundos < 31536000:
        return f"{int(segundos/86400)} días"
    elif segundos < 31536000 * 100:
        return f"{int(segundos/31536000)} años"
    elif segundos < 31536000 * 1000000:
        return f"{int(segundos/(31536000*1000))} mil años"
    else:
        return f"{int(segundos/(31536000*1000000))} millones de años"

def mostrar_resultado(psswd, nivel, score, emoji, detalles, entropia, tiempo_crackeo, palabras_comunes_detectadas):
    ancho, alto = obtener_dimensiones_terminal()
    
    # Calcular espacio vertical necesario
    lineas_palabras = len(palabras_comunes_detectadas) + 2 if palabras_comunes_detectadas else 0
    lineas_contenido = 11 + len(detalles) + lineas_palabras
    espacio_superior = max(0, (alto - lineas_contenido) // 2)
    
    # Limpiar y añadir espacio superior
    limpiar_consola()
    print("\n" * espacio_superior)
    
    # Crear línea completa
    linea = "═" * ancho
    
    # Mostrar contenido centrado
    print(linea)
    print(f"Contraseña: {psswd}".center(ancho))
    print(linea)
    print(f"{emoji} Nivel: {nivel} | Puntuación: {score}/10".center(ancho))
    print(linea)
    print(f"🔐 Entropía: {entropia} bits".center(ancho))
    print(f"⏱️  Tiempo estimado de crackeo: {tiempo_crackeo}".center(ancho))
    print(linea)
    print("RECOMENDACIONES".center(ancho))
    print(linea)
    for r in generar_recomendaciones(detalles):
        print(f"• {r}".center(ancho))
    print(linea)
    
    # Mostrar palabras comunes detectadas si las hay
    if palabras_comunes_detectadas:
        print("PALABRAS COMUNES DETECTADAS".center(ancho))
        print(linea)
        for palabra in palabras_comunes_detectadas:
            print(f"• {palabra}".center(ancho))
        print(linea)

def generar_recomendaciones(detalles):
    recomendaciones = []  
    if "No tiene mayúsculas" in detalles:
        recomendaciones.append("Incluye letras mayúsculas para mayor complejidad.")
    if "No tiene minúsculas" in detalles:
        recomendaciones.append("Incluye letras minúsculas para mayor complejidad.")
    if "No tiene números" in detalles:
        recomendaciones.append("Incluye números no secuenciales para mayor complejidad.")
    if "No tiene símbolos" in detalles:
        recomendaciones.append("Incluye símbolos especiales como !, @, #, $...")
    if any("Contiene palabra común" in d for d in detalles):
        recomendaciones.append("Evita palabras comunes o nombres personales.")
    if "Usa leet speak con palabra común (p@ssw0rd) (-3) puntos" in detalles:
        recomendaciones.append("No confíes en leet-speak; usa una contraseña única y aleatoria.")
    if "Contiene año (1900-2099) (-2) puntos" in detalles:
        recomendaciones.append("Evita incluir años o fechas.")
    if any("pwnedpasswords" in d for d in detalles):
        recomendaciones.append("Contraseña filtrada: cámbiala y usa un gestor de contraseñas para generar y guardar una contraseña única.")  

    
    if any("Menos de 8 caracteres" in d for d in detalles):
        recomendaciones.append("Aumenta la longitud a al menos 12-16 caracteres; 16+ es recomendable para mayor seguridad.")

    if not recomendaciones:
        recomendaciones.append("¡Excelente! Tu contraseña es muy sólida.")
    return recomendaciones

def verificar_psswd_en_api(psswd):
    psswd_encriptada = hashlib.sha1(psswd.encode('utf-8')).hexdigest().upper()
    url = f"https://api.pwnedpasswords.com/range/{psswd_encriptada[:5]}"
    respuesta = requests.get(url)
    if respuesta.status_code != 200:
        raise RuntimeError(f"Error al consultar la API: {respuesta.status_code}")
    for fila in respuesta.text.splitlines():
        hash_sufijo, cantidad = fila.split(':')
        if psswd_encriptada[5:] == hash_sufijo:
            return True, int(cantidad)
    return False, 0

def main():
    csv_psswd = cargar_csv("Psswd_comunes.csv")
    mostrar_pantalla_inicio()
    
    while True:
        psswd = input("\n📝 Introduce la contraseña a evaluar (Enter vacío para salir): ").strip()
        if psswd == "":
            print("\n👋 ¡Hasta luego!")
            time.sleep(3)
            limpiar_consola()
            break

        nivel, score, emoji, detalles, palabras_comunes = calcular_heuristico(psswd, csv_psswd)
        entropia = calcular_entropia(psswd)
        tiempo_crackeo = estimar_tiempo_crackeo(entropia)
        mostrar_resultado(psswd, nivel, score, emoji, detalles, entropia, tiempo_crackeo, palabras_comunes)
        respuesta = input("\n¿Quieres evaluar otra contraseña? (s/n): ").strip().lower()

        if respuesta not in ('s', 'si', 'y', 'yes', ''):
            print("\n👋 ¡Hasta luego!")
            time.sleep(3)
            limpiar_consola()
            break
        
        limpiar_consola()

if __name__ == "__main__":
    main()
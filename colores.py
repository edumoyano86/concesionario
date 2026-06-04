# colores.py
# Módulo de estilos ANSI puros para la terminal de Antigravity.
# Sin librerías externas para evitar que limpien los códigos de color.


# ─── RESET (Restablecer) ─────────────────────────────────
# ¿Qué es? Apaga todos los estilos activos y devuelve la terminal a su color normal.
# ¿Por qué usarlo? Si no lo pones al final de una cadena de color, la terminal se
# quedará pegada en ese color y todo lo que se imprima después saldrá coloreado.
RESET   = "\033[0m"

# ─── ESTILOS DE TEXTO ────────────────────────────────────
# Son modificadores visuales del texto (negrita, atenuado, etc.) que no tienen color.
# Se pueden combinar sumándolos antes del texto.
# Ejemplo: f"{BOLD}{UNDER}Texto en negrita y subrayado{RESET}"
BOLD    = "\033[1m"  # Negrita (resalta el texto)
DIM     = "\033[2m"  # Atenuado/Pálido (baja la intensidad a un gris sutil)
ITALIC  = "\033[3m"  # Cursiva (puede no estar soportado en todas las terminales)
UNDER   = "\033[4m"  # Subrayado

# ─── COLORES DE TEXTO ESTÁNDAR (Foreground) ──────────────
# Colores básicos normales. Úsalos directamente en f-strings si no quieres usar funciones.
# Ejemplo directo: print(f"{ROJO}Texto en Rojo{RESET}")
NEGRO   = "\033[30m"
ROJO    = "\033[31m"
VERDE   = "\033[32m"
AMARILLO= "\033[33m"
AZUL    = "\033[34m"
MAGENTA = "\033[35m"
CYAN    = "\033[36m"
BLANCO  = "\033[37m"

# ─── COLORES DE TEXTO BRILLANTES (True Color 24-bits) ─────
# Versiones ultra brillantes y modernas. Se saltan la paleta de la terminal y obligan
# a Antigravity a pintar el color real exacto sin importar qué tema tengas configurado.
# Ejemplo directo: print(f"{VERDE_B}Texto en Verde Brillante{RESET}")
ROJO_B     = "\033[38;2;255;50;50m"      # Rojo brillante real
VERDE_B    = "\033[38;2;50;255;50m"      # Verde brillante real
AMARILLO_B = "\033[38;2;255;255;50m"    # Amarillo brillante real
AZUL_B     = "\033[38;2;50;150;255m"     # Azul brillante real
MAGENTA_B  = "\033[38;2;255;50;255m"     # Magenta brillante real
CYAN_B     = "\033[38;2;50;255;255m"     # Cyan brillante real
BLANCO_B   = "\033[38;2;255;255;255m"   # Blanco puro brillante



# ─── COLORES DE FONDO (background) ───────────────────────
BG_NEGRO   = "\033[40m"
BG_ROJO    = "\033[41m"
BG_VERDE   = "\033[42m"
BG_AMARILLO= "\033[43m"
BG_AZUL    = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN    = "\033[46m"
BG_BLANCO  = "\033[47m"

# El archivo contiene exclusivamente constantes ANSI listas para usar de forma directa en print() o f-strings.


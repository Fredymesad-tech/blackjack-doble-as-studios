"""
Proyecto 1 - Startup Challenge
Producto: Black Jack (Toma de Decisiones)
Programacion G02

Juego de Black Jack simplificado para dos jugadores (usuario vs maquina).
"""

import random 

# ---------------------------------------------------------
# Constantes del juego
# ---------------------------------------------------------
PALOS = ["Corazones", "Diamantes", "Treboles", "Picas"]
VALORES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

CREDITOS_INICIALES = 50
APUESTA = 5
META_CREDITOS = 100


# ---------------------------------------------------------
# Funciones del mazo
# ---------------------------------------------------------
def crear_mazo():
    """Crea y devuelve un mazo de 52 cartas mezclado.
    Cada carta se representa como una tupla (valor, palo)."""
    mazo = []
    for palo in PALOS:
        for valor in VALORES:
            mazo.append((valor, palo))
    random.shuffle(mazo)
    return mazo


def repartir_carta(mazo, mano):
    """Saca la carta de encima del Mazo y la agrega a la mano indicada.
    Si el mazo se queda sin cartas, se vuelve a crear uno nuevo."""
    if len(mazo) == 0:
        nuevas = crear_mazo()
        mazo.extend(nuevas)
    carta = mazo.pop()
    mano.append(carta)


def valor_carta(carta):
    """Devuelve el valor numerico base de una carta (el As se cuenta como 11)."""
    valor = carta[0]
    if valor in ["J", "Q", "K"]:
        return 10
    elif valor == "A":
        return 11
    else:
        return int(valor)


def calcular_puntaje(mano):
    """Calcula el puntaje total de una mano, ajustando los Ases (11 -> 1)
    cuando sea necesario para no pasarse de 21."""
    puntaje = 0
    cantidad_ases = 0

    for carta in mano:
        puntaje += valor_carta(carta)
        if carta[0] == "A":
            cantidad_ases += 1

    # Mientras el puntaje se pase de 21 y todavia haya un As contado como 11,
    # se baja a 1 (es decir, se resta 10)
    while puntaje > 21 and cantidad_ases > 0:
        puntaje -= 10
        cantidad_ases -= 1

    return puntaje


def mostrar_mano(nombre, mano, ocultar_segunda=False):
    """Muestra por consola las cartas de un jugador y su puntaje.
    Si ocultar_segunda es True, la segunda carta se muestra tapada
    (se usa para la primera carta visible de la maquina)."""
    cartas_texto = []
    for i, carta in enumerate(mano):
        if ocultar_segunda and i == 1:
            cartas_texto.append("[?? oculta]")
        else:
            cartas_texto.append(carta[0] + " de " + carta[1])

    print(f"{nombre}: " + ", ".join(cartas_texto))
    if not ocultar_segunda:
        print(f"  Puntaje de {nombre}: {calcular_puntaje(mano)}")


# ---------------------------------------------------------
# Funciones de validacion de entradas
# ---------------------------------------------------------
def pedir_opcion(mensaje, opciones_validas):
    """Pide al usuario una opcion y valida que sea una de las opciones validas.
    Repite la pregunta hasta que la entrada sea correcta."""
    while True:
        entrada = input(mensaje).strip().lower()
        if entrada in opciones_validas:
            return entrada
        print("Opcion no valida, intenta de nuevo.")


# ---------------------------------------------------------
# Turnos
# ---------------------------------------------------------
def turno_jugador(mazo, mano_jugador):
    """Ejecuta el turno del jugador humano: pedir carta o plantarse.
    Devuelve True si el jugador se paso de 21 (perdio)."""
    while True:
        mostrar_mano("Jugador", mano_jugador)
        puntaje_actual = calcular_puntaje(mano_jugador)

        if puntaje_actual > 21:
            print("Te pasaste de 21. Pierdes la ronda.")
            return True

        opcion = pedir_opcion("Deseas (p)edir carta o (t)e plantas? ", ["p", "t"])

        if opcion == "p":
            repartir_carta(mazo, mano_jugador)
        else:
            print("Te plantaste con", calcular_puntaje(mano_jugador), "puntos.")
            return False


def turno_maquina(mazo, mano_maquina):
    """Ejecuta el turno de la maquina. Estrategia simple: pide carta
    mientras su puntaje sea menor a 17. Devuelve True si se paso de 21."""
    print("\nTurno de la maquina...")
    while calcular_puntaje(mano_maquina) < 17:
        repartir_carta(mazo, mano_maquina)

    mostrar_mano("Maquina", mano_maquina)
    puntaje_maquina = calcular_puntaje(mano_maquina)

    if puntaje_maquina > 21:
        print("La maquina se paso de 21.")
        return True
    return False


# ---------------------------------------------------------
# Logica de una ronda
# ---------------------------------------------------------
def determinar_ganador_ronda(puntaje_jugador, puntaje_maquina):
    """Compara los puntajes de la ronda y devuelve un texto indicando
    el resultado: 'jugador', 'maquina' o 'empate'."""
    if puntaje_jugador > 21:
        return "maquina"
    if puntaje_maquina > 21:
        return "jugador"
    if puntaje_jugador > puntaje_maquina:
        return "jugador"
    elif puntaje_maquina > puntaje_jugador:
        return "maquina"
    else:
        return "empate"


def jugar_ronda(creditos):
    """Juega una ronda completa de Black Jack y devuelve el diccionario
    de creditos actualizado despues de la ronda."""
    mazo = crear_mazo()
    mano_jugador = []
    mano_maquina = []

    # Reparto inicial de 2 cartas para cada uno
    for _ in range(2):
        repartir_carta(mazo, mano_jugador)
        repartir_carta(mazo, mano_maquina)

    print("\n----- NUEVA RONDA -----")
    print(f"Creditos jugador: {creditos['jugador']} | Creditos maquina: {creditos['maquina']}")

    # Se decide aleatoriamente quien empieza (solo informativo en esta version)
    primero = random.choice(["jugador", "maquina"])
    print(f"En esta ronda inicia: {primero}")

    mostrar_mano("Maquina", mano_maquina, ocultar_segunda=True)

    jugador_se_paso = turno_jugador(mazo, mano_jugador)

    if jugador_se_paso:
        maquina_se_paso = False
    else:
        maquina_se_paso = turno_maquina(mazo, mano_maquina)

    puntaje_jugador = calcular_puntaje(mano_jugador)
    puntaje_maquina = calcular_puntaje(mano_maquina)

    ganador = determinar_ganador_ronda(puntaje_jugador, puntaje_maquina)

    print(f"\nResultado: Jugador {puntaje_jugador} - Maquina {puntaje_maquina}")

    if ganador == "jugador":
        print("Ganaste la ronda!")
        creditos["jugador"] += APUESTA
        creditos["maquina"] -= APUESTA
    elif ganador == "maquina":
        print("Gano la maquina esta ronda.")
        creditos["maquina"] += APUESTA
        creditos["jugador"] -= APUESTA
    else:
        print("Empate. Los creditos no cambian.")

    return creditos


# ---------------------------------------------------------
# Partida completa
# ---------------------------------------------------------
def jugar_partida():
    """Controla una partida completa: se juegan rondas hasta que alguien
    llegue a la meta de creditos o se quede sin creditos para apostar."""
    creditos = {"jugador": CREDITOS_INICIALES, "maquina": CREDITOS_INICIALES}

    while True:
        if creditos["jugador"] < APUESTA:
            print("\nNo tienes suficientes creditos para seguir apostando. Pierdes la partida.")
            break
        if creditos["maquina"] < APUESTA:
            print("\nLa maquina no tiene suficientes creditos. Ganaste la partida!")
            break

        creditos = jugar_ronda(creditos)

        if creditos["jugador"] >= META_CREDITOS:
            print(f"\nLlegaste a {creditos['jugador']} creditos. GANASTE LA PARTIDA!")
            break
        if creditos["maquina"] >= META_CREDITOS:
            print(f"\nLa maquina llego a {creditos['maquina']} creditos. Perdiste la partida.")
            break

    print(f"\nCreditos finales -> Jugador: {creditos['jugador']} | Maquina: {creditos['maquina']}")


# ---------------------------------------------------------
# Programa principal
# ---------------------------------------------------------
def main():
    print("=== BIENVENIDO A BLACK JACK ===")
    print("Reglas: el As vale 11 o 1, las figuras valen 10.")
    print("Cada ronda se apuesta", APUESTA, "creditos.")
    print(f"Gana la partida quien llegue primero a {META_CREDITOS} creditos.\n")

    jugar_otra = "s"
    while jugar_otra == "s":
        jugar_partida()
        jugar_otra = pedir_opcion("\nQuieres jugar otra partida? (s/n): ", ["s", "n"])

    print("\nGracias por jugar. Hasta la proxima!")


if __name__ == "__main__":
    main()

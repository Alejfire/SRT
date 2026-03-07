import threading
import time
from collections import deque
from random import uniform

users_db = {
    "Alejfire": {"mmr": 1200},
    "AliceTowers": {"mmr": 1150},
    "Minecrafter100": {"mmr": 1100},
    "ShadowSn1per": {"mmr": 1180},
    "NovaStrike": {"mmr": 1120},
    "PixelWarrior": {"mmr": 1090}
}

matchmaking_queue = deque()
match_history = []

queue_semaphore = threading.Semaphore(1)

def join_matchmaking(player):
    try:
        if player not in users_db:
            raise Exception("Jugador no existe en la base de datos")

        print(f"{player} está intentando acceder a la cola...")
        time.sleep(uniform(0.1, 0.5))

        queue_semaphore.acquire()
        print(f"{player} obtuvo acceso al semáforo.")

        matchmaking_queue.append(player)
        print(f"{player} entró a la cola. Jugadores en cola: {len(matchmaking_queue)}")

        time.sleep(1.5)

    except Exception as e:
        print(f"Error con el jugador {player}: {e}")

    finally:
        if queue_semaphore._value == 0:
            print(f"{player} libera el semáforo.")
            queue_semaphore.release()

def save_match_to_file(match):
    try:
        with open("historial_partidas.txt", "a") as f:
            f.write(f"Partida {match['id']}: {match['players'][0]} vs {match['players'][1]}\n")
    except IOError:
        print("Error al guardar el archivo de historial.")

def create_match():
    try:
        queue_semaphore.acquire()

        if len(matchmaking_queue) >= 2:
            p1 = matchmaking_queue.popleft()
            p2 = matchmaking_queue.popleft()

            match_id = len(match_history) + 1
            match = {"id": match_id, "players": [p1, p2]}

            match_history.append(match)

            save_match_to_file(match)

            print(f"\nPartida creada: {p1} vs {p2}\n")

        else:
            raise Exception("No hay suficientes jugadores para crear partida.")

    except Exception as e:
        print(f"Error creando partida: {e}")

    finally:
        queue_semaphore.release()

def simulate_player(player):
    try:
        join_matchmaking(player)
    except Exception as e:
        print(f"Error en el hilo del jugador {player}: {e}")

if __name__ == "__main__":

    try:
        open("historial_partidas.txt", "w").close()
    except IOError:
        print("No se pudo crear el archivo de historial.")

    threads = []

    for player in users_db.keys():
        t = threading.Thread(target=simulate_player, args=(player,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\nIntentando crear partidas...\n")

    while len(matchmaking_queue) >= 2:
        create_match()
        time.sleep(1)

    print("\nHistorial final de partidas:")
    print(match_history)
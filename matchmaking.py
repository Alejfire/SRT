import hashlib
import time
from collections import deque

users_db = {}
match_history = []
matchmaking_queue = deque()
session_tokens = {}


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token(username):
    token = hashlib.sha256(f"{username}{time.time()}".encode()).hexdigest()
    session_tokens[token] = username
    return token

def log_event(event):
    with open("matchmaking_logs.txt", "a") as f:
        f.write(f"{time.ctime()} - {event}\n")


def register(username, password):
    if username in users_db:
        return "Usuario ya existe"
    users_db[username] = {
        "password": hash_password(password),
        "mmr": 1000
    }
    log_event(f"Nuevo usuario registrado: {username}")
    return "Registro exitoso"

def login(username, password):
    if username not in users_db:
        return None
    if users_db[username]["password"] == hash_password(password):
        token = generate_token(username)
        log_event(f"Inicio de sesión: {username}")
        return token
    return None

def authenticate(token):
    return session_tokens.get(token)


def join_matchmaking(token):
    username = authenticate(token)
    if not username:
        return "No autenticado"
    matchmaking_queue.append(username)
    log_event(f"{username} entró a la cola de matchmaking")
    return "En cola"

def create_match():
    if len(matchmaking_queue) < 2:
        return None

    p1 = matchmaking_queue.popleft()
    p2 = matchmaking_queue.popleft()

    mmr_diff = abs(users_db[p1]["mmr"] - users_db[p2]["mmr"])
    if mmr_diff > 300:
        log_event("Diferencia de MMR muy alta, reinsertando en cola")
        matchmaking_queue.append(p1)
        matchmaking_queue.append(p2)
        return None

    match_id = len(match_history) + 1
    match = {"id": match_id, "players": [p1, p2], "result": None}
    match_history.append(match)
    log_event(f"Partida creada: {p1} vs {p2} (ID {match_id})")
    return match


def report_result(match_id, winner):
    for match in match_history:
        if match["id"] == match_id and match["result"] is None:
            if winner not in match["players"]:
                return "Resultado inválido"

            loser = [p for p in match["players"] if p != winner][0]
            users_db[winner]["mmr"] += 25
            users_db[loser]["mmr"] -= 25
            match["result"] = winner

            log_event(f"Resultado registrado: {winner} ganó partida {match_id}")
            return "Resultado guardado"
    return "Partida no válida o ya cerrada"

if __name__ == "__main__":
    print(register("AliceTowers27", "1234"))
    print(register("Alejfire", "abcd"))

    token1 = login("AliceTowers27", "1234")
    token2 = login("Alejfire", "abcd")

    join_matchmaking(token1)
    join_matchmaking(token2)

    match = create_match()
    if match:
        print("Partida creada:", match)
        print(report_result(match["id"], "AliceTowers27"))

    print("MMR Final:", users_db)

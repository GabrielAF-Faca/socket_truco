import threading
import socket
import pickle
from baralho import Baralho

HOST = "10.121.1.171"
PORT = 8080
rodadas = []
pontosP1 = 0
pontosP2 = 0
quero = False

class Rodada:
    def __init__(self):
        self.turno = turnoInicio()

        self.rodadavalor = 0
        cartasp1 = []
        cartasp2 = []
        self.flor = False
        self.contraflor = False
        self.envido = False
        self.realEnvido = False
        self.faltaEnvido =  False
        self.truco =  False
        self.retruco = False
        self.valeQuatro = False
        self.variavelDePassagem = 0


class Cliente:
    def __init__(self,conn,adrr):
        self.conn = conn
        self.adrr = adrr
    def enviaMenssagem(self,menssagem):
        self.conn.send(menssagem).encode("utf-8")
    def recebeMenssagem(self,menssagem):
        data = self.conn.recv(1024)
        menssagem = data.decode("utf-8")
        return menssagem
        

valores_carta_truco = {
    (1, 'e'): 13,
    (2, 'e'): 8,
    (3, 'e'): 9,
    (4, 'e'): 0,
    (5, 'e'): 1,
    (6, 'e'): 2,
    (7, 'e'): 11,
    (10, 'e'): 4,
    (11, 'e'): 5,
    (12, 'e'): 6,

    (1, 'p'): 12,
    (2, 'p'): 8,
    (3, 'p'): 9,
    (4, 'p'): 0,
    (5, 'p'): 1,
    (6, 'p'): 2,
    (7, 'p'): 3,
    (10, 'p'): 4,
    (11, 'p'): 5,
    (12, 'p'): 6,

    (1, 'o'): 7,
    (2, 'o'): 8,
    (3, 'o'): 9,
    (4, 'o'): 0,
    (5, 'o'): 1,
    (6, 'o'): 2,
    (7, 'o'): 10,
    (10, 'o'): 4,
    (11, 'o'): 5,
    (12, 'o'): 6,

    (1, 'c'): 7,
    (2, 'c'): 8,
    (3, 'c'): 9,
    (4, 'c'): 0,
    (5, 'c'): 1,
    (6, 'c'): 2,
    (7, 'c'): 3,
    (10, 'c'): 4,
    (11, 'c'): 5,
    (12, 'c'): 6,
}

def turnoInicio():
    if len(rodadas)%2 == 0:
        return 0
    else:
        return 1

    
def trocaTurno(turno):
    if turno == 1:
        turno = 0
    else: turno = 1

def verificaMaiorPontuacao(pontos1,pontos2):
    if pontos1>pontos2:
        return 1
    elif pontos2>pontos1:
        return 2
    elif pontos1==pontos2:
        return 3
    else: 
        print("erro na contagem dos pontos")
        return 4

def pedido_envido(conn,rodada):
    if len(rodadas) > 0:
        return False
    rodada.envido = True
    conn.send("envido")


def pedido_realEnvido(conn,rodada):
    if len(rodadas) > 0:
        return False
    rodada.realEnvido = True
    conn.send("real envido")

def pedido_faltaEnvido(conn,rodada):
    if len(rodadas) > 0:
        return False
    rodada.faltaEnvido = True
    conn.send("falta envido")

def pedido_truco(conn,rodada):
    if rodada.truco == True:
        return False
    rodada.truco = True
    conn.send("truco")
def pedido_retruco(conn,rodada):
    if rodada.truco ==  False or rodada.retruco == True:
        return False
    rodada.retruco = True
def pedido_valeQuatro(conn,rodada):
    if rodada.truco == False or rodada.retruco == False or rodada.valeQuatro == True:
        return False
    rodada.valeQuatro = True
    conn.send("vale Quatro")    




def verificaVencedorTurno(carta1,carta2):
    if valores_carta_truco[carta1]> valores_carta_truco[carta2]:
        return 1 
    elif valores_carta_truco[carta1] < valores_carta_truco[carta2]:
        return -1
    elif valores_carta_truco[carta1] == valores_carta_truco[carta2]:
        return 0
    else: 
        return -5

def gerarCartas():
    cartas_maos = Baralho.retorna6()
    cartas_p1 = cartas_maos[:3]
    cartas_p2 = cartas_maos[3:]

    return cartas_p1, cartas_p2

def enviarCartas(conn,adrr,id,cartas_p1,cartas_p2,rodada):
    if id == 0:
        conn.send(pickle.dump(cartas_p1),rodada.turno.encode("utf-8"))
        id = 1
    elif id == 1:
        conn.send(pickle.dump(cartas_p2),rodada.turno.encode("utf-8"))
        id = 0

    else:
        print("erro ao enviar cartas")

def recebeCartas(conn,adrr):
    data  = conn.recv(1024)
    carta =  pickle.loads(data)
    return carta

def jogador1(conn,adrr,id):
    p1 = Cliente(conn,adrr)
    
    while True:
        rodada = Rodada()
        if rodada.turno %2 == 0:
            pontosRodada = 0
            cartas_p1, cartas_p2 = gerarCartas()
            enviarCartas(conn,adrr,id,cartas_p1,cartas_p2,rodada)
            
            escolha  = p1.recebeMenssagem()
            if escolha == 1:
                pedido_envido(p1.conn,rodada)
            elif escolha == 2:
                pedido_realEnvido(p1.conn,rodada)
            elif escolha == 3:
                pedido_faltaEnvido(p1.conn,rodada)
            elif escolha == 4:
                pedido_truco(p1.conn,rodada)
            elif escolha == 5:
                pedido_retruco(p1.conn,rodada)
            elif escolha == 6:
                pedido_valeQuatro(p1.conn,rodada)
            
            
            pontosP1 += pontosRodada
            pontosRodada = 0
            rodadas.append(rodada)
        else:
            if rodada.envido == True:
                conn.send("envido") 
            elif rodada.realenvido == True:
                conn.send("envido")
            elif rodada.faltaEnvido == True:
                conn.send("faltaEnvido")
            elif rodada.truco == True:
                conn.send("truco")
            elif rodada.retruco == True:
                conn.send("retruco")
            elif rodada.valeQuatro == True:
                conn.send("vale Quatro")    
            


def jogador2(conn,adrr,id):
    p2 = Cliente(conn,adrr)
    
    while True:
        rodada = Rodada()
        if not rodada.turno % 2 == 0:
        
            pontosRodada = 0
            cartas_p1, cartas_p2 = gerarCartas()
            enviarCartas(conn,adrr,id,cartas_p1,cartas_p2,rodada)
            
            escolha  = p2.recebeMenssagem()
            if escolha == 1:
                pedido_envido(p2.conn,rodada)
            elif escolha == 2:
                pedido_realEnvido(p2.conn,rodada)
            elif escolha == 3:
                pedido_faltaEnvido(p2.conn,rodada)
            elif escolha == 4:
                pedido_truco(p2.conn,rodada)
            elif escolha == 5:
                pedido_retruco(p2.conn,rodada)
            elif escolha == 6:
                pedido_valeQuatro(p2.conn,rodada)
            pontosP2 += pontosRodada
            pontosRodada = 0
            rodadas.append(rodada)

        else:
            if rodada.envido == True:
                conn.send("envido") 
            elif rodada.realenvido == True:
                conn.send("real envido")
                opcao = p2.recebeMenssagem()
                if opcao == "quero":
                    conn.send("quero e canta")
                    trocaTurno()
                elif opcao == "não quero":


            elif rodada.faltaEnvido == True:
                conn.send("faltaEnvido")
            elif rodada.truco == True:
                conn.send("truco")
            elif rodada.retruco == True:
                conn.send("retruco")
            elif rodada.valeQuatro == True:
                conn.send("vale Quatro")



        



def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()

        conn1, addr1 = server.accept()
        t1 = threading.Thread(target=jogador1,args=(conn1,addr1,id))
        id = 1
        conn2, addr2 = server.accept()
        t2 = threading.Thread(target=jogador2,args=(conn2,addr2,id))
        while True:
            t1.start()
            t2.start()
        
        



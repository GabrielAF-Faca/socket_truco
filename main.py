from baralho import Baralho

estado_do_jogo = {

    "rodada": {
        "quem_joga": 0,
        "pedido_envido": 0,
        # 0 para ainda nao foi pedido, 1 para envido em andamento (analisar nivel do pedido atual), 2 para envido nao pode mais ser pedido
        "turno1_3": 1,
        # começa em 1 e vai ate no maximo 3
        "cartas_p1": [],
        "cartas_p2": [],

        "nivel_pedido_envido": 0,
        # 0 para nao foi pedido, 1 = pediu envido, 2 = pediu real, 3 = pediu falta, 4 = cantou flor
        # preciso repensar

        "pedido_truco": 0,
        # 0 = nao foi pedido, 1 = pediu para aumentar o valor da rodada

        "valor_da_rodada": 1
    },

    "jogo": {
        "rodada": 0,
        # começa em 1 e itera a cada rodada

        "pontosP1": 0,
        "pontosP2": 0,
        # marca os pontos de cada jogador
    }
}

jogada = {
    # prototipo de o que o bot enviará de saída ao decidir o que jogar
    "carta_jogada": 0,  # 0 para nao jogou carta, 1 a 3 para cartas de 1 a 3 do jogador;
    "pedir_envido": 0,  # 0 para nao pedir, 1 para pedir, 2 para pedir real, 3 para pedir falta, 4 para cantar flor
    "pedir_truco": 0,  # 0 para nao pedir, 1 para pedir
    "resposta_pedido_envido": -1,  # -1 para nao recebeu pedido, 0 para rejeitou pedido, 1 para quero, 2 = quero real
    # 3 = quero falta, 4 = contraflor eh proibido
    "responder_truco": -1,  # -1 = nao recebeu pedido, 0 = nao quero, 1 = quero, 2 = quero e aumentar, 3 = pedir antes envido
    "responder_flor": -1,  # -1 = outro player n cantou flor, 0 = nao fazer nada, 1 = cantar contraflor
}


def iniciar_jogo(estado_do_jogo):
    # Criar um objeto de Baralho
    global baralho
    baralho = Baralho()
    # Inicializar o estado do jogo
    # estado_do_jogo["quem_joga"] = 1  # Começa com o jogador 1

def fim_de_jogo():
    if estado_do_jogo["jogo"]["pontosP1"] == 24 or estado_do_jogo["jogo"]["pontosP1"] == 24:
        return True


baralho = Baralho()

cartas_mao = baralho.retorna6()

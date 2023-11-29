from baralho import Baralho
from bot import Bot

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

def lidar_com_a_resposta(jogada):
    pass

#iniciar_jogo()  # Chame a função para iniciar o jogo

# Obter as 6 cartas do baralho embaralhado
# cartas_em_mao_jogadores = baralho.retorna6()
#

bot1 = Bot(1)
bot2 = Bot(2)

baralho = Baralho()

cartas_mao = baralho.retorna6()

bot1.mao = cartas_mao[:3]
bot2.mao = cartas_mao[3:]

bot1.print_mao()
print(bot1.tem_flor())
print(bot1.tem_pontos_de_envido())

rodadaAtual = estado_do_jogo['rodada']
rodadaAtual['quem_joga'] = 1

jogada1 = bot1.jogar(estado_do_jogo)


if jogada1['pedir_envido'] != 0 and jogada1['turno1_3'] == 1:
    rodadaAtual['pedido_envido'] = 1
    # se ocorreu algum tipo de pedido de envido, altero a flag para 1 para avisar que há um envido em andamento
    rodadaAtual['quem_joga'] = 0
    # coloco a flag 'quem_joga' como 0 pra indicar pros bots que ao enviar uma jogada, nao deve jogar carta
    rodadaAtual['nivel_pedido_envido'] = jogada1['pedir_envido']
    acao_bot2 = bot2.jogar(estado_do_jogo)

    if acao_bot2['resposta_envido'] != 0:  # bot2 respondeu "nao quero"

        if acao_bot2['resposta_envido'] == 4:  # bot2 respondeu "contraflor não há envido"
            estado_do_jogo['jogo']['pontosP1'] += 3  # 3 pontos por que o bot2 tinha flor e acaba o envido

        elif acao_bot2['resposta_envido'] == 1:  # bot2 respondeu apenas "quero"
            if bot1.tem_pontos_de_envido() > bot2.tem_pontos_de_envido():
                if rodadaAtual['nivel_pedido_envido'] == 1:
                    estado_do_jogo['jogo']['pontosP2'] += 2 # preciso alterar para aumentar de acordo com o nivel do pedido
                elif rodadaAtual['nivel_pedido_envido'] == 2:
                    estado_do_jogo['jogo']['pontosP2'] += 3 # bot1 ganha 3 pontos pq o bot1 pediu o real envido direto
                elif rodadaAtual['nivel_pedido_envido'] == 3:
                    estado_do_jogo['jogo']['pontosP2'] += 24 - estado_do_jogo['jogo']['pontosP1'] # bot1 ganha quantos pontos faltam pro bot2 ganhar
            elif bot2.tem_pontos_de_envido() > bot1.tem_pontos_de_envido():
                if rodadaAtual['nivel_pedido_envido'] == 1:
                    estado_do_jogo['jogo']['pontosP1'] += 2 # preciso alterar para aumentar de acordo com o nivel do pedido
                elif rodadaAtual['nivel_pedido_envido'] == 2:
                    estado_do_jogo['jogo']['pontosP1'] += 3 # bot2 ganha 3 pontos pq o bot1 pediu o real envido direto
                elif rodadaAtual['nivel_pedido_envido'] == 3:
                    estado_do_jogo['jogo']['pontosP1'] += 24 - estado_do_jogo['jogo']['pontosP2'] # bot2 ganha quantos pontos faltam pro bot1 ganhar

        elif acao_bot2['resposta_envido'] == 2:  # bot2 respondeu real envido pro envido inicial do bot1
            rodadaAtual['nivel_pedido_envido'] = 2
            acao_bot1 = bot1.jogar(estado_do_jogo)
            if acao_bot1['resposta_envido'] == 0:
                estado_do_jogo['jogo']['pontosP1'] += 2  # 2 pontos porque bot1 respondeu nao para o real envido que foi
                # pedido após o envido
            elif acao_bot1['resposta_envido'] == 1: #resposta pro real envido foi apenas "quero"
                # abaixo vou colocar 5 pontos pra quem vencer o real envido
                if bot1.tem_pontos_de_envido() > bot2.tem_pontos_de_envido():
                    estado_do_jogo['jogo']['pontosP2'] += 5
                elif bot2.tem_pontos_de_envido() > bot1.tem_pontos_de_envido():
                    estado_do_jogo['jogo']['pontosP1'] += 5
            elif acao_bot1['resposta_envido'] == 3:  # bot1 respondeu falta envido para o real envido do bot2
                rodadaAtual['nivel_pedido_envido'] = 3
                acao_bot2 = bot2.jogar(estado_do_jogo)
                if acao_bot2 == 0:
                    estado_do_jogo['jogo']['pontosP2'] += 3  # 3 pontos porque bot2 respondeu nao para o falta envido que foi
                    # pedido após o real envido que tinha sido pedido após o envido
                elif acao_bot2 == 1:
                    if bot1.tem_pontos_de_envido() > bot2.tem_pontos_de_envido():
                        estado_do_jogo['jogo']['pontosP2'] += 24 - estado_do_jogo['jogo']['pontosP1'] # bot1 ganha quantos pontos faltam pro bot2 ganhar
                    elif bot2.tem_pontos_de_envido() > bot1.tem_pontos_de_envido():
                        estado_do_jogo['jogo']['pontosP1'] += 24 - estado_do_jogo['jogo']['pontosP2'] # bot2 ganha quantos pontos faltam pro bot1 ganhar

        elif acao_bot2['resposta_envido'] == 3:  # bot2 respondeu falta envido para o envido inicial do bot1
            rodadaAtual['nivel_pedido_envido'] = 3
            acao_bot1 = bot1.jogar(estado_do_jogo)
            if acao_bot1 == 0:
                estado_do_jogo['jogo']['pontosP1'] += 2  # 2 pontos porque bot1 respondeu nao para o falta envido que foi
                # pedido pelo bot2 após o envido inicial do bot1
            elif acao_bot1 == 1:
                if bot1.tem_pontos_de_envido() > bot2.tem_pontos_de_envido():
                    estado_do_jogo['jogo']['pontosP2'] += 24 - estado_do_jogo['jogo']['pontosP1'] # bot1 ganha quantos pontos faltam pro bot2 ganhar
                elif bot2.tem_pontos_de_envido() > bot1.tem_pontos_de_envido():
                    estado_do_jogo['jogo']['pontosP1'] += 24 - estado_do_jogo['jogo']['pontosP2'] # bot2 ganha quantos pontos faltam pro bot1 ganhar
    else:
        # se entrar aqui, quer dizer que o bot2 respondeu nao para o envido logo de cara
        estado_do_jogo['jogo']['pontosP2'] += 1  # nesse caso, o bot1 que pediu o envido recebe 1 ponto
    rodadaAtual['pedido_envido'] = 2  # coloco a flag "2" para determinar que o envido já foi resolvido nesta rodada
    rodadaAtual['quem_joga'] = 1

if jogada1['pedir_truco'] != 0:
    rodadaAtual['pedido_truco'] = 1  # coloquei a flag 'pedido_truco' = 1 para avisar que ocorreu um pedido de aumento
    # do valor do jogo
    acao_bot2 = bot2.jogar(estado_do_jogo)

    if acao_bot2['resposta_pedido_truco'] == 0:  # bot2 respondeu "nao quero" pro bot1
        # todo: dar um jeito de acabar a rodada e dar os devidos pontos pro bot1 de acordo com o valor atual do jogo
        pass

    elif acao_bot2['resposta_pedido_truco'] == 3:  # bot2 respondeu "antes envido" pro truco do bot1
        # todo: aqui fazer o processamento de envido como se o bot2 tivesse pedido envido inicialmente
        pass

    elif acao_bot2['resposta_pedido_truco'] == 1:  # bot2 respondeu apenas "quero"
        rodadaAtual['pedido_truco'] = 0
        rodadaAtual['valor_da_rodada'] += 1

    elif acao_bot2['resposta_pedido_truco'] == 2:  # bot2 respondeu quero e quero aumentar pra bot1
        rodadaAtual['pedido_truco'] = 1
        rodadaAtual['valor_da_rodada'] += 1
        acao_bot1 = bot1.jogar(estado_do_jogo)
        if acao_bot1['resposta_pedido_truco'] == 0:  # bot1 respondeu "nao quero" pra aumentada do bot2
            # todo: dar um jeito de acabar a rodada e dar os devidos pontos pro bot2 de acordo com o valor atual do jogo
            pass
        elif acao_bot1['resposta_pedido_truco'] == 1:  # bot1 apenas aceitou a aumentada de valor do bot2
            rodadaAtual['pedido_truco'] = 0
            rodadaAtual['valor_da_rodada'] += 1
        elif acao_bot1['resposta_pedido_truco'] == 2:  # bot1 respondeu quero e quero aumentar pra bot2
            rodadaAtual['pedido_truco'] = 1
            rodadaAtual['valor_da_rodada'] += 1
            acao_bot2 = bot2.jogar(estado_do_jogo)
            if acao_bot2['resposta_pedido_truco'] == 0:
                # todo: dar um jeito de acabar a rodada e dar os devidos pontos pro bot2 de acordo com o valor atual do jogo
                pass
            else:
                rodadaAtual['pedido_truco'] = 0
                rodadaAtual['valor_da_rodada'] += 1




#  aqui ja foi processado o possível pedido de envido e o possível pedido de truco vindo do bot1
# agora vamos ver qual carta ele jogou e colocá-la na mesa, e passar a vez pro outro bot jogar
if jogada1['carta_jogada'] != -1:
    rodadaAtual['cartas_p1'][0] = bot1.mao[jogada1['carta_jogada']]
rodadaAtual['quem_joga'] = 2
jogada2 = bot2.jogar(estado_do_jogo)




if jogada2['pedir_envido'] != 0 and jogada2['turno1_3'] == 1:
    rodadaAtual['pedido_envido'] = 1
    # se ocorreu algum tipo de pedido de envido, altero a flag para 1 para avisar que há um envido em andamento
    rodadaAtual['quem_joga'] = 0
    # coloco a flag 'quem_joga' como 0 pra indicar pros bots que ao enviar uma jogada, nao deve jogar carta
    rodadaAtual['nivel_pedido_envido'] = jogada2['pedir_envido']
    acao_bot1 = bot1.jogar(estado_do_jogo)

    if acao_bot1['resposta_envido'] != 0:  # bot1 respondeu "nao quero"

        if acao_bot1['resposta_envido'] == 4:  # bot1 respondeu "contraflor não há envido"
            estado_do_jogo['jogo']['pontosP1'] += 3  # 3 pontos por que o bot1 tinha flor e acaba o envido

        elif acao_bot1['resposta_envido'] == 1:  # bot1 respondeu apenas "quero"
            if bot2.tem_pontos_de_envido() > bot1.tem_pontos_de_envido():
                if rodadaAtual['nivel_pedido_envido'] == 1:
                    estado_do_jogo['jogo']['pontosP2'] += 2 # preciso alterar para aumentar de acordo com o nivel do pedido
                elif rodadaAtual['nivel_pedido_envido'] == 2:
                    estado_do_jogo['jogo']['pontosP2'] += 3 # bot2 ganha 3 pontos pq o bot2 pediu o real envido direto
                elif rodadaAtual['nivel_pedido_envido'] == 3:
                    estado_do_jogo['jogo']['pontosP2'] += 24 - estado_do_jogo['jogo']['pontosP1'] # bot2 ganha quantos pontos faltam pro bot1 ganhar
            elif bot1.tem_pontos_de_envido() > bot2.tem_pontos_de_envido():
                if rodadaAtual['nivel_pedido_envido'] == 1:
                    estado_do_jogo['jogo']['pontosP1'] += 2 # preciso alterar para aumentar de acordo com o nivel do pedido
                elif rodadaAtual['nivel_pedido_envido'] == 2:
                    estado_do_jogo['jogo']['pontosP1'] += 3 # bot1 ganha 3 pontos pq o bot2 pediu o real envido direto
                elif rodadaAtual['nivel_pedido_envido'] == 3:
                    estado_do_jogo['jogo']['pontosP1'] += 24 - estado_do_jogo['jogo']['pontosP2'] # bot1 ganha quantos pontos faltam pro bot2 ganhar

        elif acao_bot1['resposta_envido'] == 2:  # bot1 respondeu real envido pro envido inicial do bot2
            rodadaAtual['nivel_pedido_envido'] = 2
            acao_bot2 = bot2.jogar(estado_do_jogo)
            if acao_bot2['resposta_envido'] == 0:
                estado_do_jogo['jogo']['pontosP1'] += 2  # 2 pontos porque bot2 respondeu nao para o real envido que foi
                # pedido após o envido
            elif acao_bot2['resposta_envido'] == 1: #resposta pro real envido foi apenas "quero"
                # abaixo vou colocar 5 pontos pra quem vencer o real envido
                if bot2.tem_pontos_de_envido() > bot1.tem_pontos_de_envido():
                    estado_do_jogo['jogo']['pontosP2'] += 5
                elif bot1.tem_pontos_de_envido() > bot2.tem_pontos_de_envido():
                    estado_do_jogo['jogo']['pontosP1'] += 5
            elif acao_bot2['resposta_envido'] == 3:  # bot2 respondeu falta envido para o real envido do bot1
                rodadaAtual['nivel_pedido_envido'] = 3
                acao_bot1 = bot1.jogar(estado_do_jogo)
                if acao_bot1 == 0:
                    estado_do_jogo['jogo']['pontosP2'] += 3  # 3 pontos porque bot1 respondeu nao para o falta envido que foi
                    # pedido após o real envido que tinha sido pedido após o envido
                elif acao_bot1 == 1:
                    if bot2.tem_pontos_de_envido() > bot1.tem_pontos_de_envido():
                        estado_do_jogo['jogo']['pontosP2'] += 24 - estado_do_jogo['jogo']['pontosP1'] # bot2 ganha quantos pontos faltam pro bot1 ganhar
                    elif bot1.tem_pontos_de_envido() > bot2.tem_pontos_de_envido():
                        estado_do_jogo['jogo']['pontosP1'] += 24 - estado_do_jogo['jogo']['pontosP2'] # bot1 ganha quantos pontos faltam pro bot2 ganhar

        elif acao_bot1['resposta_envido'] == 3:  # bot1 respondeu falta envido para o envido inicial do bot2
            rodadaAtual['nivel_pedido_envido'] = 3
            acao_bot2 = bot2.jogar(estado_do_jogo)
            if acao_bot2 == 0:
                estado_do_jogo['jogo']['pontosP1'] += 2  # 2 pontos porque bot2 respondeu nao para o falta envido que foi
                # pedido pelo bot1 após o envido inicial do bot2
            elif acao_bot2 == 1:
                if bot2.tem_pontos_de_envido() > bot1.tem_pontos_de_envido():
                    estado_do_jogo['jogo']['pontosP2'] += 24 - estado_do_jogo['jogo']['pontosP1'] # bot2 ganha quantos pontos faltam pro bot1 ganhar
                elif bot1.tem_pontos_de_envido() > bot2.tem_pontos_de_envido():
                    estado_do_jogo['jogo']['pontosP1'] += 24 - estado_do_jogo['jogo']['pontosP2'] # bot1 ganha quantos pontos faltam pro bot2 ganhar
    else:
        # se entrar aqui, quer dizer que o bot1 respondeu nao para o envido logo de cara
        estado_do_jogo['jogo']['pontosP2'] += 1  # nesse caso, o bot2 que pediu o envido recebe 1 ponto
    rodadaAtual['pedido_envido'] = 2  # coloco a flag "2" para determinar que o envido já foi resolvido nesta rodada
    rodadaAtual['quem_joga'] = 1

if jogada2['pedir_truco'] != 0:
    rodadaAtual['pedido_truco'] = 1  # coloquei a flag 'pedido_truco' = 1 para avisar que ocorreu um pedido de aumento
    # do valor do jogo
    acao_bot1 = bot1.jogar(estado_do_jogo)

    if acao_bot1['resposta_pedido_truco'] == 0:  # bot1 respondeu "nao quero" pro bot2
        # todo: dar um jeito de acabar a rodada e dar os devidos pontos pro bot2 de acordo com o valor atual do jogo
        pass

    elif acao_bot1['resposta_pedido_truco'] == 3:  # bot1 respondeu "antes envido" pro truco do bot2
        # todo: aqui fazer o processamento de envido como se o bot1 tivesse pedido envido inicialmente
        pass

    elif acao_bot1['resposta_pedido_truco'] == 1:  # bot1 respondeu apenas "quero"
        rodadaAtual['pedido_truco'] = 0
        rodadaAtual['valor_da_rodada'] += 1

    elif acao_bot1['resposta_pedido_truco'] == 2:  # bot1 respondeu quero e quero aumentar pra bot2
        rodadaAtual['pedido_truco'] = 1
        rodadaAtual['valor_da_rodada'] += 1
        acao_bot2 = bot2.jogar(estado_do_jogo)
        if acao_bot2['resposta_pedido_truco'] == 0:  # bot2 respondeu "nao quero" pra aumentada do bot1
            # todo: dar um jeito de acabar a rodada e dar os devidos pontos pro bot1 de acordo com o valor atual do jogo
            pass
        elif acao_bot2['resposta_pedido_truco'] == 1:  # bot2 apenas aceitou a aumentada de valor do bot1
            rodadaAtual['pedido_truco'] = 0
            rodadaAtual['valor_da_rodada'] += 1
        elif acao_bot2['resposta_pedido_truco'] == 2:  # bot2 respondeu quero e quero aumentar pra bot1
            rodadaAtual['pedido_truco'] = 1
            rodadaAtual['valor_da_rodada'] += 1
            acao_bot1 = bot1.jogar(estado_do_jogo)
            if acao_bot1['resposta_pedido_truco'] == 0:
                # todo: dar um jeito de acabar a rodada e dar os devidos pontos pro bot1 de acordo com o valor atual do jogo
                pass
            else:
                rodadaAtual['pedido_truco'] = 0
                rodadaAtual['valor_da_rodada'] += 1


bot1.printa_resposta()

print()

bot2.print_mao()
print(bot2.tem_flor())
print(bot2.tem_pontos_de_envido())
jogada2 = bot2.jogar(estado_do_jogo)
# bot2.printa_resposta()


# while not fim_de_jogo():
#     estado_do_jogo["rodada"] += 1
#
#     if estado_do_jogo["Quem_joga"] == 1:
#         retorno = bot1.jogada(estado_do_jogo)
#         if retorno[carta_jogada] != 0:
#             estado_do_jogo["Quem_joga"] = 2

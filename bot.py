from iqoptionapi.stable_api import IQ_Option
import time
from configobj import ConfigObj
import json, sys
from datetime import datetime, timedelta


### CRIANDO ARQUIVO DE CONFIGURAÇÃO ####
config = ConfigObj('config.txt')
email = config['LOGIN']['email']
senha = config['LOGIN']['senha']
tipo = config['AJUSTES']['tipo']
qnt_velas = int(config['VELAS']['qnt_velas'])
timeframe = int(config['VELAS']['timeframe'])
valor_entrada = float(config['AJUSTES']['valor_entrada'])
stop_win = float(config['AJUSTES']['stop_win'])
stop_loss = float(config['AJUSTES']['stop_loss'])
tempo_de = float(config['MINUTOS']['tempo_de'])
tempo_ate = float(config['MINUTOS']['tempo_ate'])
tempo_fim = float(config['MINUTOS']['tempo_fim'])
lucro_total = 0
stop = True

if config['MARTINGALE']['usar_martingale'].upper() == 'S':
    martingale = int(config['MARTINGALE']['maximo_perda_martingale'])
else:
    martingale = 0
fator_mg = float(config['MARTINGALE']['fator_martingale'])

analise_medias = config['AJUSTES']['analise_medias']
velas_medias = int(config['AJUSTES']['velas_medias'])

print('Iniciando Conexão com a IQOption')
API = IQ_Option(email,senha)

### Função para conectar na IQOPTION ###
check, reason = API.connect()
if check:
    print('\nConectado com sucesso')
else:
    if reason == '{"code":"invalid_credentials","message":"You entered the wrong credentials. Please ensure that your login/password is correct."}':
        print('\nEmail ou senha incorreta')
        sys.exit()
        
    else:    
        print('\nHouve um problema na conexão')

        print(reason)
        sys.exit()

### Função para Selecionar demo ou real ###
while True:
    escolha = input('\nSelecione a conta em que deseja conectar: demo ou real  - ')
    if escolha == 'demo':
        conta = 'PRACTICE'
        print('Conta demo selecionada')
        break
    if escolha == 'real':
        conta = 'REAL'
        print('Conta real selecionada')
        break
    else:
        print('Escolha incorreta! Digite demo ou real')
        
API.change_balance(conta)

### Função para checar stop win e loss
def check_stop():
    global stop,lucro_total
    if lucro_total <= float('-'+str(abs(stop_loss))):
        stop = False
        print('\n#########################')
        print('STOP LOSS BATIDO ',str(cifrao),str(lucro_total))
        print('#########################')
        sys.exit()
        

    if lucro_total >= float(abs(stop_win)):
        stop = False
        print('\n#########################')
        print('STOP WIN BATIDO ',str(cifrao),str(lucro_total))
        print('#########################')
        sys.exit()

def payout(par):
    profit = API.get_all_profit()
    all_asset = API.get_all_open_time()

    try:
        if all_asset['binary'][par]['open']:
            if profit[par]['binary']> 0:
                binary = round(profit[par]['binary'],2) * 100
        else:
            binary  = 0
    except:
        binary = 0

    try:
        if all_asset['turbo'][par]['open']:
            if profit[par]['turbo']> 0:
                turbo = round(profit[par]['turbo'],2) * 100
        else:
            turbo  = 0
    except:
        turbo = 0

    try:
        if all_asset['digital'][par]['open']:
            digital = API.get_digital_payout(par)
        else:
            digital  = 0
    except:
        digital = 0

    return binary, turbo, digital

### Função abrir ordem e checar resultado ###
def compra(ativo,entrada,direcao,exp,tipo):
    global stop,lucro_total

    for i in range(martingale + 1):

        if stop == True:
        
            if tipo == 'digital':
                check, id = API.buy_digital_spot_v2(ativo,entrada,direcao,exp)
            else:
                check, id = API.buy(entrada,ativo,direcao,exp)


            if check:
                if i == 0: 
                    print('\n>> Ordem aberta \n>> Par:',ativo,'\n>> Timeframe:',exp,'\n>> Entrada de:',entrada)
                    print('\nSeu Saldo na conta ',escolha, 'é de', cifrao,float(API.get_balance()))
                   
                

                while True:
                    time.sleep(0.1)
                    resultado = API.check_win_v3(id)
                    lucro_total=float(API.get_balance()) - valorconta
                    
                    if resultado > 0:
                            if i == 0:
                                valor_entrada = float(config['AJUSTES']['valor_entrada'])
                                entrada = valor_entrada
                                i=0
                                print('\n>> Resultado: WIN \n>> Lucro:', round(resultado,2), '\n>> Par:', ativo, '\n>> Lucro total: ', lucro_total)
                                print('\nSeu Saldo na conta ',escolha, 'é de', cifrao,float(API.get_balance()))
                                print('\nPróxima entrada é de: ',cifrao,valor_entrada)
                    elif resultado == 0:
                            if i == 0:
                                print('\n>> Resultado: EMPATE \n>> Lucro:', round(resultado,2), '\n>> Par:', ativo, '\n>> Lucro total: ', lucro_total)
                                print('\nSeu Saldo na conta ',escolha, 'é de', cifrao,float(API.get_balance()))
                                gale = float(entrada) * float(fator_mg)                           
                                entrada = round(abs(gale),2)
                                valor_entrada=entrada
                                print('\nPróxima entrada é de: ',cifrao,valor_entrada)
                                i=i+1
                                
                    else:       
                            if i == 0:
                                print('\n>> Resultado: LOSS \n>> Lucro:', round(resultado,2), '\n>> Par:', ativo, '\n>> Lucro total: ', lucro_total)
                                print('\nSeu Saldo na conta ',escolha, 'é de', cifrao,float(API.get_balance()))
                                gale = float(entrada) * float(fator_mg)                           
                                entrada = round(abs(gale),2)
                                valor_entrada=entrada
                                print('\nPróxima entrada é de: ',cifrao,valor_entrada)
                                i=i+1
       
                    check_stop()

                    break


                if resultado == -9999999999999999999999999999999999:
                    break
                    
                else:
                    if valor_entrada <= martingale:
                        global horario, medias,estrategia_mhi

                        ### Fução que busca hora da corretora ###
                        def horario():
                            x = API.get_server_timestamp()
                            now = datetime.fromtimestamp(API.get_server_timestamp())
    
                            return now

                        def medias(velas):
                            soma = 0
                            for i in velas:
                                soma += i['close']
                            media = soma / velas_medias

                            if media > velas[-1]['close']:
                                tendencia = 'put'
                            else:
                                tendencia = 'call'

                            return tendencia

                        ### Função de análise MHI   
                        def estrategia_mhi():
                            global tipo,timeframe,qnt_velas

                            if tipo == 'automatico':
                                binary, turbo, digital = payout(ativo)
                                print(binary, turbo, digital )
                                if digital > turbo:
                                    print( 'Suas entradas serão realizadas nas digitais')
                                    tipo = 'digital'
                                elif turbo > digital:
                                    print( 'Suas entradas serão realizadas nas binárias')
                                    tipo = 'binary'
                                else:
                                    print(' Par fechado, escolha outro')
                                    sys.exit()


    
                        while True:
                            if i>0:    
                                ### Horario do computador ###
                                #minutos = float(datetime.now().strftime('%M.%S')[1:])

                                ### horario da iqoption ###
                                minutos = float(datetime.fromtimestamp(API.get_server_timestamp()).strftime('%M.%S')[1:])

                                entrar = True if (minutos >= tempo_de and minutos <= tempo_ate) or minutos >= tempo_fim else False

                                print('Aguardando Horário de entrada ' ,minutos, end='\r')
        
                                if resultado>0:
                                    valor_entrada = float(config['AJUSTES']['valor_entrada'])
                                    entrada = valor_entrada
                                   
                                
                                if entrar:
                                    print('\n>> Iniciando análise da estratégia MHI')

                                    direcao = False

                                    if analise_medias == 'S':
                                        velas = API.get_candles(ativo, timeframe, velas_medias, time.time())
                                        vela = API.get_candles(ativo, timeframe, velas_medias, time.time())
                                        tendencia = medias(velas)

                                    else:
                                        velas = API.get_candles(ativo, timeframe, qnt_velas, time.time())
                                        vela = API.get_candles(ativo, timeframe, velas_medias, time.time())


                                    velas[-1] = 'Verde' if velas[-1]['open'] < velas[-1]['close'] else 'Vermelha' if velas[-1]['open'] > velas[-1]['close'] else 'Doji'
                                    velas[-2] = 'Verde' if velas[-2]['open'] < velas[-2]['close'] else 'Vermelha' if velas[-2]['open'] > velas[-2]['close'] else 'Doji'
                                    velas[-3] = 'Verde' if velas[-3]['open'] < velas[-3]['close'] else 'Vermelha' if velas[-3]['open'] > velas[-3]['close'] else 'Doji'


                                    cores = velas[-3] ,velas[-2] ,velas[-1] 

                                    if cores.count('Verde') > cores.count('Vermelha') and cores.count('Doji') == 0: direcao = 'call'
                                    if cores.count('Verde') < cores.count('Vermelha') and cores.count('Doji') == 0: direcao = 'put'
                                    ultimo_preco = vela[-1]['close']
                                    high = max([candle['max'] for candle in vela])
                                    low = min([candle['min'] for candle in vela])
                                    fib_levels = fibonacci_levels(high, low)
                                    if analise_medias =='S':
                                        if direcao == tendencia:
                                            pass
                                        else:
                                            direcao = 'abortar'


                                    if direcao=='put':
                                        direcao='call'
                                        direcao2=direcao
                                    else:
                                        direcao='put'
                                        direcao2=direcao    
                                    if direcao == 'put' or direcao == 'call':
                                        if ultimo_preco < fib_levels[2]:
                                            direcao = 'put'
                                            if direcao2==direcao:
                                                print('Velas: ',velas[-3] ,velas[-2] ,velas[-1] , ' - Entrada para ', direcao)
                                                print('High: ',high ,' - Low: ',low ,' - Último preço: ',ultimo_preco , '- Level1: ', fib_levels[1], '- Level2: ', fib_levels[2], '- Level3: ', fib_levels[3], '- Level4: ', fib_levels[4])
                                                compra(ativo,valor_entrada,direcao,1,tipo)
                                                print('\n')
                                            else:
                                                direcao='call'
                                                print('Velas: ',velas[-3] ,velas[-2] ,velas[-1] , ' - Entrada para ', direcao)
                                                print('High: ',high ,' - Low: ',low ,' - Último preço: ',ultimo_preco , '- Level1: ', fib_levels[1], '- Level2: ', fib_levels[2], '- Level3: ', fib_levels[3], '- Level4: ', fib_levels[4])
                                                compra(ativo,valor_entrada,direcao,1,tipo)
                                                print('\n')        
                                        elif ultimo_preco > fib_levels[2]:
                                            direcao = 'call'
                                            if direcao2==direcao:
                                                print('Velas: ',velas[-3] ,velas[-2] ,velas[-1] , ' - Entrada para ', direcao)
                                                print('High: ',high ,' - Low: ',low ,' - Último preço: ',ultimo_preco , '- Level1: ', fib_levels[1], '- Level2: ', fib_levels[2], '- Level3: ', fib_levels[3], '- Level4: ', fib_levels[4])
                                                compra(ativo,valor_entrada,direcao,1,tipo)
                                                print('\n')
                                            else:
                                                direcao='put'
                                                print('Velas: ',velas[-3] ,velas[-2] ,velas[-1] , ' - Entrada para ', direcao)
                                                print('High: ',high ,' - Low: ',low ,' - Último preço: ',ultimo_preco , '- Level1: ', fib_levels[1], '- Level2: ', fib_levels[2], '- Level3: ', fib_levels[3], '- Level4: ', fib_levels[4])
                                                compra(ativo,valor_entrada,direcao,1,tipo)
                                                print('\n')   

                                    else:
                                        if direcao == 'abortar':
                                            print('Velas: ',velas[-3] ,velas[-2] ,velas[-1] )
                                            print('Entrada abortada - Contra Tendência.')
                                            print('\nSeu Saldo na conta ',escolha, 'é de', cifrao,float(API.get_balance()))

                                        else:
                                            print('Velas: ',velas[-3] ,velas[-2] ,velas[-1] )
                                            print('Entrada abortada - Contra tendência Fibonacci.')
                                            print('\nSeu Saldo na conta ',escolha, 'é de', cifrao,float(API.get_balance()))


                                    print('\n######################################################################\n')
                            else:
                                break
                    else:
                        print('\nMartingale máximo atingido! Recomeçando...')
                        break

            else:
                print('erro na abertura da ordem,', id,ativo)
                print('\nSeu Saldo na conta ',escolha, 'é de', cifrao,float(API.get_balance()))


### Fução que busca hora da corretora ###
def horario():
    x = API.get_server_timestamp()
    now = datetime.fromtimestamp(API.get_server_timestamp())
    
    return now

def medias(velas):
    soma = 0
    for i in velas:
        soma += i['close']
    media = soma / velas_medias

    if media > velas[-1]['close']:
        tendencia = 'put'
    else:
        tendencia = 'call'

    return tendencia

# Função para calcular os níveis de Fibonacci
def fibonacci_levels(high, low):
    diff = high - low
    level_0 = high
    level_1 = high - 0.236 * diff
    level_2 = high - 0.382 * diff
    level_3 = high - 0.618 * diff
    level_4 = low

    return level_0, level_1, level_2, level_3, level_4

# Verifica se o preço está próximo de algum nível de Fibonacci
def is_near_fibonacci(price, levels):
    for i, level in enumerate(levels[:-1]):
        if price >= level and price <= levels[i + 1]:
            return True
    return False


### Função de análise MHI   
def estrategia_mhi():
    global tipo,timeframe,qnt_velas

    if tipo == 'automatico':
        binary, turbo, digital = payout(ativo)
        print(binary, turbo, digital )
        if digital > turbo:
            print( 'Suas entradas serão realizadas nas digitais')
            tipo = 'digital'
        elif turbo > digital:
            print( 'Suas entradas serão realizadas nas binárias')
            tipo = 'binary'
        else:
            print(' Par fechado, escolha outro')
            sys.exit()


    
    while True:

        ### Horario do computador ###
        #minutos = float(datetime.now().strftime('%M.%S')[1:])

        ### horario da iqoption ###
        minutos = float(datetime.fromtimestamp(API.get_server_timestamp()).strftime('%M.%S')[1:])

        entrar = True if (minutos >= tempo_de and minutos <= tempo_ate) or minutos >= tempo_fim else False 
        print('Aguardando Horário de entrada ' ,minutos, end='\r')
        

        if entrar:
            print('\n>> Iniciando análise da estratégia MHI')

            direcao = False

            if analise_medias == 'S':
                velas = API.get_candles(ativo, timeframe, velas_medias, time.time())
                vela = API.get_candles(ativo, timeframe, qnt_velas, time.time())
                tendencia = medias(velas)

            else:
                velas = API.get_candles(ativo, timeframe, qnt_velas, time.time())
                vela = API.get_candles(ativo, timeframe, qnt_velas, time.time())


            velas[-1] = 'Verde' if velas[-1]['open'] < velas[-1]['close'] else 'Vermelha' if velas[-1]['open'] > velas[-1]['close'] else 'Doji'
            velas[-2] = 'Verde' if velas[-2]['open'] < velas[-2]['close'] else 'Vermelha' if velas[-2]['open'] > velas[-2]['close'] else 'Doji'
            velas[-3] = 'Verde' if velas[-3]['open'] < velas[-3]['close'] else 'Vermelha' if velas[-3]['open'] > velas[-3]['close'] else 'Doji'


            cores = velas[-3] ,velas[-2] ,velas[-1] 

            if cores.count('Verde') > cores.count('Vermelha') and cores.count('Doji') == 0: direcao = 'call'
            if cores.count('Verde') < cores.count('Vermelha') and cores.count('Doji') == 0: direcao = 'put'

            ultimo_preco = vela[-1]['close']
            high = max([candle['max'] for candle in vela])
            low = min([candle['min'] for candle in vela])
            fib_levels = fibonacci_levels(high, low)
            if analise_medias =='S':
                if direcao == tendencia:
                    pass
                else:
                    direcao = 'abortar'




            if direcao=='put':
                direcao='call'
                direcao2=direcao
            else:
                direcao='put'
                direcao2=direcao    
            if direcao == 'put' or direcao == 'call':
                if ultimo_preco < fib_levels[2]:
                    direcao = 'put'
                    if direcao2==direcao:
                        print('Velas: ',velas[-3] ,velas[-2] ,velas[-1] , ' - Entrada para ', direcao)
                        print('High: ',high ,' - Low: ',low ,' - Último preço: ',ultimo_preco , '- Level1: ', fib_levels[1], '- Level2: ', fib_levels[2], '- Level3: ', fib_levels[3], '- Level4: ', fib_levels[4])
                        compra(ativo,valor_entrada,direcao,1,tipo)
                        print('\n')
                    else:
                        direcao='call'
                        print('Velas: ',velas[-3] ,velas[-2] ,velas[-1] , ' - Entrada para ', direcao)
                        print('High: ',high ,' - Low: ',low ,' - Último preço: ',ultimo_preco , '- Level1: ', fib_levels[1], '- Level2: ', fib_levels[2], '- Level3: ', fib_levels[3], '- Level4: ', fib_levels[4])
                        compra(ativo,valor_entrada,direcao,1,tipo)
                        print('\n')        
                elif ultimo_preco > fib_levels[2]:
                    direcao = 'call'
                    if direcao2==direcao:
                        print('Velas: ',velas[-3] ,velas[-2] ,velas[-1] , ' - Entrada para ', direcao)
                        print('High: ',high ,' - Low: ',low ,' - Último preço: ',ultimo_preco , '- Level1: ', fib_levels[1], '- Level2: ', fib_levels[2], '- Level3: ', fib_levels[3], '- Level4: ', fib_levels[4])
                        compra(ativo,valor_entrada,direcao,1,tipo)
                        print('\n')
                    else:
                        direcao='put'
                        print('Velas: ',velas[-3] ,velas[-2] ,velas[-1] , ' - Entrada para ', direcao)
                        print('High: ',high ,' - Low: ',low ,' - Último preço: ',ultimo_preco , '- Level1: ', fib_levels[1], '- Level2: ', fib_levels[2], '- Level3: ', fib_levels[3], '- Level4: ', fib_levels[4])
                        compra(ativo,valor_entrada,direcao,1,tipo)
                        print('\n') 
     
                

            else:
                if direcao == 'abortar':
                    print('Velas: ',velas[-3] ,velas[-2] ,velas[-1] )
                    print('Entrada abortada - Contra Tendência.')
                    print('\nSeu Saldo na conta ',escolha, 'é de', cifrao,float(API.get_balance()))

                else:
                    print('Velas: ',velas[-3] ,velas[-2] ,velas[-1] )
                    print('Entrada abortada - Contra tendência Fibonacci.')
                    print('\nSeu Saldo na conta ',escolha, 'é de', cifrao,float(API.get_balance()))

            print('\n######################################################################\n')

### DEFININCãO INPUTS NO INICIO DO ROBÔ ###

ativo = input('\n>> Digite o ativo que você deseja operar: ').upper()

perfil = json.loads(json.dumps(API.get_profile_ansyc()))
cifrao = str(perfil['currency_char'])
nome = str(perfil['name'])

valorconta = float(API.get_balance())

print('\n######################################################################')
print('\nOlá, ',nome, '\nSeja bem vindo')
print('\nSeu Saldo na conta ',escolha, 'é de', cifrao,valorconta)
print('\nSeu valor de entrada é de ',cifrao,valor_entrada)
print('\nStop win:',cifrao,stop_win)
print('\nStop loss:',cifrao,stop_loss)
print('\nTempo: ',timeframe,'segundos - Quantidade de velas: ',qnt_velas)
print('\n######################################################################\n\n')


### chamada da estrategia mhi ###
estrategia_mhi()

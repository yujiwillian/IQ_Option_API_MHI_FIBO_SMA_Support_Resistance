# IQ_Option_API_MHI_FIBO_SMA_Support_Resistance

## Atualização: bot opera com as estratégias médias móveis, Fibonacci, SMA e Suporte/Resistência.
### Ao realizar o Martingale, ele faz a análise novamente das velas.

#### 1. Primeiro, instale o Python [clicando aqui](https://www.python.org/downloads/), e tenha uma conta na [IQ Option](https://iqoption.com/)

### Agora vamos instalar os pacotes e bibliotecas da IQOptionAPI.Stable_API

#### 2. Abra o terminal (CMD) na sua máquina e digite:
  -  pip3 install websocket-client==0.56
      -  OBS: Caso haja outra versão websocket-client instalada, desinstale usando o comando: pip3 uninstall websocket-client
    Após isso, instale a versão websocket-client 0.56

- Baixe a pasta da API do Lu-Yi-Hsun [clicando aqui](https://github.com/Lu-Yi-Hsun/iqoptionapi.git)
- No terminal (CMD) vá até essa pasta baixada, encontre o arquivo setup.py.
- Ao encontrar, digite: python setup.py install
- OBS: Caso você não saiba como achar o arquivo dentro do terminal para executar. Siga os passos:
Se o terminal estiver apontando no diretório raíz, só digitar: 
  -  cd Downloads
  -  cd iqoptionapi
  -  python setup.py install
- Pronto! Instalou os pacotes, bibliotecas e dependências do iqoptionapi.stable_api

### Agora utilize este repositório:

#### 3. Copie ou baixe os arquivos: config.txt, bot.py
  - [Baixe](https://github.com/yujiwillian/IQ_Option_API_MHI/archive/refs/heads/main.zip)

#### 4. Abra o arquivo "config.txt" (Esse arquivo é a configuração que você deseja):
  - No campo LOGIN:
  - Coloque o seu e-mail no campo "INSIRA O SEU E-MAIL"
  - Coloque a sua senha no campo "INSIRA A SUA SENHA"

  - No campo AJUSTES:
  - valor_entrada: É o valor que você deseja que o bot dê em cada aposta;
  - tipo: Pode deixar como automatico para o bot realizar os comandos sozinho;
  - stop_win: Significa o valor da meta que você deseja bater;
  - stop_loss: Significa o valor máximo de perdas;
  - analise_medias: Se quiser que ele analise pela estratégia MHI, deixar como "S", caso contrário "N";
  - velas_medias: Inserir a quantidade de velas médias a serem analisadas pela tendência.

  -  No campo MARTINGALE:
  -  usar_martingale: Se deseja que o bot utilize Martingale, colocar "S", caso contrário "N";
  -  maximo_perda_martingale: Inserir o valor máximo ($) que ele poderá fazer o Martingale;
  -  fator_martingale: É a multiplicação do martingale (Deixei como 2.6, que significa que ele vai multiplicar o valor perdido em 2.6).

  -  No campo VELAS:
  -  qnt_velas: Quantidade de velas a serem analisadas;
  -  timeframe: Tempo da vela (colocar em segundos).

  -  No campo MINUTOS:
  -  tempo_de: Início do tempo para a entrada (Se preferir, pode deixar 4.59);
  -  tempo_ate: Tempo limite para a entrada (Se preferir, pode deixar 5.00);
  -  tempo_fim: Tempo de expiração, e nesse tempo ele não fará mais a entrada. Irá recomeçar o tempo e análise (Se preferir, pode deixar 9.59).


### Execute o bot.py

#### 5. Ainda com o terminal (CMD) aberto, localize a pasta do bot.py digite:
  -  python bot.py

OBS: Caso você não saiba como achar o arquivo dentro do terminal para executar. Siga os passos:
Se o terminal estiver apontando no diretório raíz, só digitar: 
  -  cd Downloads
  -  cd IQ_OPTION_API_MHI-main
  -  python bot.py
Nessa sequência você está apontando que o terminal (CMD) entre na pasta Downloads > IQ_OPTION_API_MHI-main e execute o arquivo bot.py

#### 6. Após executar, o bot pega a sua credencial e conecta com sucesso com a IQ Option de forma automatica. (Caso dê erros na autenticação, verifique se possui a autenticação de dois fatores - se tiver, desative-a), caso ainda apresente erros, verifique se o e-mail e senha digitados está correto.
  -  Ele vai perguntar qual conta você gostaria de testar. Escolha entre a "demo" ou "real";
  -  Após, ele vai perguntar qual ativo você deseja escolher. Caso seja EUR/USD, digite: EURUSD (Caso esteja em OTC, digitar: EURUSD-OTC);
  -  Ele vai verificar se o ativo está disponível, se estiver, o bot irá funcionar.

###### Códigos e passos baseados na documentação da API: [Lu-Yi-Hsun](https://lu-yi-hsun.github.io/iqoptionapi/) e no robô de análise MHI [Luke Feix](https://github.com/lukefeix/Rob-de-MHI-para-IQoption-Aulas-Completas/tree/main/Aula%2012-%20M%C3%A9dias%20M%C3%B3veis)

##Imagem do bot funcionando:
![Captura de Tela 2023-08-28 às 21 53 33](https://github.com/yujiwillian/IQ_Option_API_MHI/assets/93338593/460abbd2-0dce-48cc-9c5c-7df14e32228c)

# Não deixe a ganância corromper você, utilize com sabedoria.

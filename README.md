# 🌐 Trabalho 2 de Redes de Computadores II

Repositório contendo implementações práticas de protocolos de rede TCP, UDP e WebSocket em Python.

## 👤 Alunos

- Caio Bruno Gonzaga Liboreiro
- Kayky Nery Alcântara Vieira
- Marcus Vinícius de Oliveira Pinto

## 📋 Índice

- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Repositório](#estrutura-do-repositório)
- [Instalação](#instalação)
- [Exercícios](#exercícios)
  - [Exercício 1: Cliente-Servidor TCP](#exercício-1-cliente-servidor-tcp)
  - [Exercício 2: Servidor Echo UDP](#exercício-2-servidor-echo-udp)
  - [Exercício 3: Chat em Rede TCP](#exercício-3-chat-em-rede-tcp)
  - [Exercício 4: Servidor de Hora com Threads](#exercício-4-servidor-de-hora-com-threads)
  - [Exercício 10: Chat WebSocket](#exercício-10-chat-websocket)

## 🛠️ Tecnologias Utilizadas

- **Python 3.7+**
- **Bibliotecas:**
  - `socket` - Comunicação TCP/UDP
  - `threading` - Programação concorrente
  - `asyncio` - Programação assíncrona
  - `websockets` - Protocolo WebSocket
  - `aioconsole` - Console assíncrono
  - `datetime` - Manipulação de data/hora
  - `logging` - Sistema de logs

## 📦 Instalação

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Instalando Dependências

```bash
# Clone o repositório
git clone https://github.com/oliveira-marcus/Trabalho2_Redes2.git
cd tp2-redes2

# Instale as dependências necessárias
pip install websockets aioconsole
```

## 🚀 Exercícios

---

## Exercício 1: Cliente-Servidor TCP

**Objetivo:** Criar um cliente e servidor TCP que permite envio e recebimento de mensagens com suporte a múltiplos clientes.

### Como Executar

**Terminal 1 - Servidor:**
```bash
cd exercicio01
python servidor.py
```

**Terminal 2 - Cliente:**
```bash
cd exercicio01
python cliente.py
```

### Uso

1. O servidor inicia na porta **5000**
2. Execute quantos clientes desejar em terminais diferentes
3. Digite mensagens no cliente
4. Digite `sair` para encerrar a conexão
5. Use `Ctrl+C` para parar o servidor

---

## Exercício 2: Servidor Echo UDP

**Objetivo:** Implementar um serviço de eco usando UDP, onde mensagens são enviadas de volta ao cliente.

### Como Executar

**Terminal 1 - Servidor:**
```bash
cd exercicio02
python servidor_udp.py
```

**Terminal 2 - Cliente:**
```bash
cd exercicio02
python cliente_udp.py
```

### Uso

1. O servidor inicia na porta **6000**
2. Digite mensagens no cliente
3. O servidor retorna a mesma mensagem (eco)
4. Digite `sair` para encerrar
5. Timeout de 5 segundos para detectar perda de pacotes

---

## Exercício 3: Chat em Rede TCP

**Objetivo:** Sistema de chat em tempo real permitindo comunicação entre dois usuários.

### Como Executar

**Terminal 1 - Servidor:**
```bash
cd exercicio03
python servidor_chat.py
```

**Terminal 2 - Cliente 1:**
```bash
cd exercicio03
python cliente_chat.py
```

**Terminal 3 - Cliente 2:**
```bash
cd exercicio03
python cliente_chat.py
```

### Uso

1. O servidor inicia na porta **7000**
2. Conecte exatamente 2 clientes
3. Os clientes podem conversar em tempo real
4. Digite `sair` para encerrar
5. Mensagens são transmitidas instantaneamente

---

## Exercício 4: Servidor de Hora com Threads

**Objetivo:** Servidor multithread que fornece hora atual para múltiplos clientes simultaneamente.

### Como Executar

**Terminal 1 - Servidor:**
```bash
cd exercicio04
python servidor_hora.py
```

**Terminal 2+ - Clientes:**
```bash
cd exercicio04
python cliente_hora.py
```

### Uso

#### Servidor

1. Inicia na porta **8000**
2. Aguarda conexões
3. Gera logs em `servidor_hora.log`
4. Use `Ctrl+C` para parar

#### Cliente

**Modo Interativo:**
- Digite `hora` para obter a hora atual
- Digite `sair` para encerrar

**Modo Simples:**
- Solicita hora uma vez e encerra

---

## Exercício 10: Chat WebSocket

**Objetivo:** Chat moderno usando WebSocket com interface web e terminal.

### Como Executar

**Terminal 1 - Servidor:**
```bash
cd exercicio10
python servidor_websocket.py
```

**Opção 1 - Cliente Terminal:**
```bash
cd exercicio10
python cliente_websocket.py
```

**Opção 2 - Cliente Web:**
```bash
cd exercicio10
# Abra o arquivo no navegador
xdg-open chat_web.html

# Ou
firefox chat_web.html
google-chrome chat_web.html
```

### Uso

1. Servidor inicia na porta **9000**
2. Escolha cliente terminal ou web
3. Digite seu nome de usuário
4. Converse em tempo real com outros usuários
5. Veja indicador quando alguém está digitando
6. Digite `sair`, `exit` ou `quit` para encerrar

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

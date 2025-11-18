"""
Participantes: 
    Caio Bruno Gonzaga Liboreiro
    Kayky Nery Alcantara Vieira
    Marcus Vinícius de Oliveira Pinto
"""

import asyncio
import websockets
import json
import aioconsole

class WebSocketChatClient:
    def __init__(self, server_url='ws://localhost:9000'):
        self.server_url = server_url
        self.websocket = None
        self.username = None
        self.running = False
        self.disconnecting = False
        
    async def receive_messages(self):
        """Recebe e exibe mensagens do servidor"""
        try:
            async for message in self.websocket:
                data = json.loads(message)
                msg_type = data.get('type')
                
                if msg_type == 'message':
                    # Mensagem de chat
                    username = data.get('username')
                    content = data.get('message')
                    timestamp = data.get('timestamp')
                    
                    print(f"\r[{timestamp}] {username}: {content}")
                    if not self.disconnecting:
                        print(f"{self.username}> ", end='', flush=True)
                
                elif msg_type == 'system':
                    # Mensagem do sistema
                    content = data.get('message')
                    timestamp = data.get('timestamp')
                    
                    print(f"\r*** [{timestamp}] {content} ***")
                    
                    # Se é mensagem de confirmação de desconexão, pode encerrar
                    if self.disconnecting and "confirmada" in content.lower():
                        self.running = False
                        break
                    
                    if not self.disconnecting:
                        print(f"{self.username}> ", end='', flush=True)
                
                elif msg_type == 'user_list':
                    # Lista de usuários conectados
                    users = data.get('users', [])
                    count = data.get('count', 0)
                    
                    print(f"\r*** Usuários online ({count}): {', '.join(users)} ***")
                    if not self.disconnecting:
                        print(f"{self.username}> ", end='', flush=True)
                
                elif msg_type == 'typing':
                    # Notificação de digitação
                    username = data.get('username')
                    print(f"\r*** {username} está digitando... ***")
                    if not self.disconnecting:
                        print(f"{self.username}> ", end='', flush=True)
                
                elif msg_type == 'error':
                    # Mensagem de erro
                    error = data.get('message')
                    print(f"\r[ERRO] {error}")
                    if not self.disconnecting:
                        print(f"{self.username}> ", end='', flush=True)
                    
        except websockets.exceptions.ConnectionClosed:
            if not self.disconnecting:
                print("\n[DESCONECTADO] Conexão com o servidor encerrada.")
            self.running = False
        except Exception as e:
            if not self.disconnecting:
                print(f"\n[ERRO] Erro ao receber mensagem: {e}")
            self.running = False
    
    async def send_messages(self):
        """Envia mensagens para o servidor"""
        print(f"{self.username}> ", end='', flush=True)
        
        try:
            while self.running:
                # Lê entrada do usuário de forma assíncrona
                message = await aioconsole.ainput()
                
                if not self.running:
                    break
                
                # Verifica comando de saída
                if message.strip().lower() in ['sair', 'exit', 'quit']:
                    print("[SAINDO] Encerrando conexão...")
                    self.disconnecting = True
                    
                    # Envia notificação de saída ao servidor
                    try:
                        disconnect_msg = json.dumps({
                            'type': 'disconnect',
                            'message': 'sair'
                        })
                        await self.websocket.send(disconnect_msg)
                        
                        # Aguarda um pouco para receber confirmação via receive_messages
                        await asyncio.sleep(1.0)
                        
                    except Exception as e:
                        print(f"[INFO] Erro ao notificar servidor: {e}")
                    
                    self.running = False
                    break
                
                # Valida mensagem vazia
                if message.strip() == "":
                    print(f"{self.username}> ", end='', flush=True)
                    continue
                
                # Envia mensagem
                msg_data = json.dumps({
                    'type': 'message',
                    'message': message.strip()
                })
                
                await self.websocket.send(msg_data)
                print(f"{self.username}> ", end='', flush=True)
                
        except Exception as e:
            if self.running and not self.disconnecting:
                print(f"\n[ERRO] Erro ao enviar mensagem: {e}")
            self.running = False
    
    async def connect(self):
        """Conecta ao servidor WebSocket"""
        try:
            # Solicita username
            print("=" * 60)
            print("CHAT WEBSOCKET - CLIENTE")
            print("=" * 60)
            self.username = input("Digite seu nome de usuário: ").strip()
            
            if not self.username:
                self.username = f"User{asyncio.get_event_loop().time():.0f}"
            
            print(f"\nConectando a {self.server_url}...")
            
            # Conecta ao servidor
            self.websocket = await websockets.connect(self.server_url)
            self.running = True
            
            print("[CONECTADO] Conectado ao servidor!")
            print("Digite 'sair', 'exit' ou 'quit' para encerrar.\n")
            
            # Registra username
            register_msg = json.dumps({
                'type': 'register',
                'username': self.username
            })
            await self.websocket.send(register_msg)
            
            # Cria tasks para recebimento e envio
            receive_task = asyncio.create_task(self.receive_messages())
            send_task = asyncio.create_task(self.send_messages())
            
            # Aguarda até que uma das tasks termine
            done, pending = await asyncio.wait(
                [receive_task, send_task],
                return_when=asyncio.FIRST_COMPLETED
            )
            
            # Cancela a task pendente
            for task in pending:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            
        except ConnectionRefusedError:
            print("[ERRO] Não foi possível conectar ao servidor.")
            print("[INFO] Verifique se o servidor está rodando.")
        except Exception as e:
            print(f"[ERRO] Erro na conexão: {e}")
        finally:
            self.running = False
            if self.websocket:
                try:
                    await self.websocket.close()
                except:
                    pass
            print("\n[DESCONECTADO] Cliente encerrado.")

def main():
    client = WebSocketChatClient()
    
    try:
        asyncio.run(client.connect())
    except KeyboardInterrupt:
        print("\n[ENCERRANDO] Cliente encerrado pelo usuário (Ctrl+C)")

if __name__ == "__main__":
    main()
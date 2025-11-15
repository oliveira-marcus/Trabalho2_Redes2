"""
Participantes: 
    Caio Bruno Gonzaga Liboreiro
    Kayky Nery Alcantara Vieira
    Marcus Vinícius de Oliveira Pinto
"""

import asyncio
import websockets
import json
import datetime
from typing import Set

class WebSocketChatServer:
    def __init__(self, host='localhost', port=9000):
        self.host = host
        self.port = port
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.usernames = {}  # Mapeia conexão -> username
        
    def get_timestamp(self):
        """Retorna timestamp formatado"""
        return datetime.datetime.now().strftime("%H:%M:%S")
    
    async def broadcast(self, message, exclude=None):
        """Envia mensagem para todos os clientes conectados"""
        if self.clients:
            tasks = []
            for client in self.clients:
                if client != exclude:
                    tasks.append(client.send(message))
            
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
    
    async def send_user_list(self):
        """Envia lista de usuários conectados para todos"""
        users = list(self.usernames.values())
        message = json.dumps({
            'type': 'user_list',
            'users': users,
            'count': len(users)
        })
        await self.broadcast(message)
    
    async def handle_client(self, websocket):
        """Gerencia conexão de um cliente"""
        client_address = websocket.remote_address
        username = None
        
        try:
            # Adiciona cliente ao conjunto
            self.clients.add(websocket)
            print(f"[{self.get_timestamp()}] Nova conexão de {client_address}")
            
            # Aguarda mensagem de registro com username
            register_msg = await websocket.recv()
            register_data = json.loads(register_msg)
            
            if register_data.get('type') == 'register':
                username = register_data.get('username', f'User{len(self.clients)}')
                self.usernames[websocket] = username
                
                print(f"[{self.get_timestamp()}] {username} entrou no chat")
                
                # Mensagem de boas-vindas
                welcome = json.dumps({
                    'type': 'system',
                    'message': f'Bem-vindo ao chat, {username}!',
                    'timestamp': self.get_timestamp()
                })
                await websocket.send(welcome)
                
                # Notifica todos sobre novo usuário
                notification = json.dumps({
                    'type': 'system',
                    'message': f'{username} entrou no chat',
                    'timestamp': self.get_timestamp()
                })
                await self.broadcast(notification, exclude=websocket)
                
                # Envia lista de usuários atualizada
                await self.send_user_list()
                
                # Loop principal de mensagens
                async for message in websocket:
                    try:
                        data = json.loads(message)
                        msg_type = data.get('type')
                        
                        if msg_type == 'message':
                            # Mensagem de chat normal
                            content = data.get('message', '').strip()
                            
                            if content:
                                chat_message = json.dumps({
                                    'type': 'message',
                                    'username': username,
                                    'message': content,
                                    'timestamp': self.get_timestamp()
                                })
                                
                                print(f"[{self.get_timestamp()}] {username}: {content}")
                                await self.broadcast(chat_message)
                        
                        elif msg_type == 'disconnect':
                            # Cliente solicitou desconexão
                            print(f"[{self.get_timestamp()}] {username} solicitou desconexão")
                            
                            # Envia confirmação
                            goodbye = json.dumps({
                                'type': 'system',
                                'message': 'Desconexão confirmada. Até logo!',
                                'timestamp': self.get_timestamp()
                            })
                            await websocket.send(goodbye)
                            break
                        
                        elif msg_type == 'typing':
                            # Notificação de digitação
                            typing_msg = json.dumps({
                                'type': 'typing',
                                'username': username
                            })
                            await self.broadcast(typing_msg, exclude=websocket)
                    
                    except json.JSONDecodeError:
                        error = json.dumps({
                            'type': 'error',
                            'message': 'Formato de mensagem inválido'
                        })
                        await websocket.send(error)
                    
        except websockets.exceptions.ConnectionClosedOK:
            print(f"[{self.get_timestamp()}] {username or client_address} desconectou normalmente")
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"[{self.get_timestamp()}] {username or client_address} desconectou com erro: {e}")
        except Exception as e:
            print(f"[{self.get_timestamp()}] Erro com {username or client_address}: {e}")
        finally:
            # Remove cliente
            self.clients.discard(websocket)
            
            if websocket in self.usernames:
                username = self.usernames[websocket]
                del self.usernames[websocket]
                
                # Notifica saída do usuário
                notification = json.dumps({
                    'type': 'system',
                    'message': f'{username} saiu do chat',
                    'timestamp': self.get_timestamp()
                })
                await self.broadcast(notification)
                
                # Atualiza lista de usuários
                await self.send_user_list()
                
                print(f"[{self.get_timestamp()}] {username} removido. Total de clientes: {len(self.clients)}")
    
    async def start(self):
        """Inicia o servidor WebSocket"""
        print("=" * 60)
        print(f"Servidor de Chat WebSocket iniciado")
        print(f"Host: {self.host}")
        print(f"Porta: {self.port}")
        print(f"URL: ws://{self.host}:{self.port}")
        print("=" * 60)
        print()
        
        async with websockets.serve(self.handle_client, self.host, self.port):
            await asyncio.Future()  # Roda para sempre

def main():
    server = WebSocketChatServer()
    
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("Servidor encerrado pelo usuário (Ctrl+C)")
        print("=" * 60)

if __name__ == "__main__":
    main()
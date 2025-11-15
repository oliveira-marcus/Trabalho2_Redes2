"""
Participantes: 
    Caio Bruno Gonzaga Liboreiro
    Kayky Nery Alcantara Vieira
    Marcus Vinícius de Oliveira Pinto
"""

import socket
import threading

class ChatServer:
    def __init__(self, host='localhost', port=7000):
        self.host = host
        self.port = port
        self.clients = []
        self.clients_lock = threading.Lock()
        self.max_clients = 2
        
    def broadcast(self, message, sender_socket):
        """Envia mensagem para todos os clientes exceto o remetente"""
        with self.clients_lock:
            for client in self.clients:
                if client != sender_socket:
                    try:
                        client.send(message.encode('utf-8'))
                    except:
                        # Remove cliente se houver erro ao enviar
                        self.remove_client(client)
    
    def remove_client(self, client_socket):
        """Remove cliente da lista"""
        with self.clients_lock:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
                print(f"[INFO] Cliente removido. Total de clientes: {len(self.clients)}")
    
    def handle_client(self, client_socket, client_address, client_number):
        """Gerencia comunicação com um cliente específico"""
        print(f"[CONECTADO] Cliente {client_number} ({client_address}) entrou no chat.")
        
        try:
            # Envia mensagem de boas-vindas
            welcome_msg = f"Bem-vindo ao chat! Você é o Cliente {client_number}.\n"
            client_socket.send(welcome_msg.encode('utf-8'))
            
            # Notifica outros clientes
            notification = f"[SISTEMA] Cliente {client_number} entrou no chat.\n"
            self.broadcast(notification, client_socket)
            
            while True:
                # Recebe mensagem do cliente
                message = client_socket.recv(1024).decode('utf-8')
                
                if not message:
                    break
                
                # Verifica comando de saída
                if message.strip().lower() == "sair":
                    goodbye_msg = "[SISTEMA] Você saiu do chat. Até logo!\n"
                    client_socket.send(goodbye_msg.encode('utf-8'))
                    
                    # Notifica outros clientes
                    notification = f"[SISTEMA] Cliente {client_number} saiu do chat.\n"
                    self.broadcast(notification, client_socket)
                    break
                
                # Valida mensagem vazia
                if message.strip() == "":
                    continue
                
                # Formata e transmite mensagem
                formatted_msg = f"[Cliente {client_number}] {message}"
                print(f"[MENSAGEM] {formatted_msg.strip()}")
                
                self.broadcast(formatted_msg, client_socket)
                
        except Exception as e:
            print(f"[ERRO] Erro ao processar Cliente {client_number}: {e}")
        finally:
            self.remove_client(client_socket)
            client_socket.close()
            print(f"[DESCONECTADO] Cliente {client_number} ({client_address}) saiu.")
    
    def start(self):
        """Inicia o servidor de chat"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen(self.max_clients)
            
            print(f"[INICIADO] Servidor de Chat rodando em {self.host}:{self.port}")
            print(f"[INFO] Aguardando {self.max_clients} clientes para iniciar o chat...\n")
            
            client_number = 0
            
            while True:
                client_socket, client_address = server_socket.accept()
                
                with self.clients_lock:
                    if len(self.clients) >= self.max_clients:
                        # Rejeita conexão se já houver 2 clientes
                        reject_msg = "Servidor cheio. Tente novamente mais tarde.\n"
                        client_socket.send(reject_msg.encode('utf-8'))
                        client_socket.close()
                        print(f"[REJEITADO] Conexão rejeitada de {client_address} (servidor cheio)")
                        continue
                    
                    self.clients.append(client_socket)
                    client_number += 1
                
                # Cria thread para cada cliente
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address, client_number)
                )
                client_thread.daemon = True
                client_thread.start()
                
                print(f"[INFO] Total de clientes conectados: {len(self.clients)}/{self.max_clients}\n")
                
        except KeyboardInterrupt:
            print("\n[ENCERRANDO] Servidor encerrado pelo usuário.")
        except Exception as e:
            print(f"[ERRO] Erro no servidor: {e}")
        finally:
            server_socket.close()
            print("[FECHADO] Servidor encerrado.")

if __name__ == "__main__":
    server = ChatServer()
    server.start()
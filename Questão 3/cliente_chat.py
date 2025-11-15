"""
Participantes: 
    Caio Bruno Gonzaga Liboreiro
    Kayky Nery Alcantara Vieira
    Marcus Vinícius de Oliveira Pinto
"""

import socket
import threading

class ChatClient:
    def __init__(self, host='localhost', port=7000):
        self.host = host
        self.port = port
        self.client_socket = None
        self.running = False
        
    def receive_messages(self):
        """Thread para receber mensagens do servidor"""
        while self.running:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                
                if not message:
                    print("\n[DESCONECTADO] Conexão com o servidor perdida.")
                    self.running = False
                    break
                
                # Limpa a linha atual e imprime a mensagem
                print(f"\r{message}", end='')
                print("\nVocê: ", end='', flush=True)
                
            except Exception as e:
                if self.running:
                    print(f"\n[ERRO] Erro ao receber mensagem: {e}")
                break
    
    def send_messages(self):
        """Thread para enviar mensagens ao servidor"""
        
        while self.running:
            try:
                message = input()
                
                if not self.running:
                    break
                
                # Valida mensagem vazia
                if message.strip() == "":
                    print("Você: ", end='', flush=True)
                    continue
                
                # Envia mensagem ao servidor
                self.client_socket.send(message.encode('utf-8'))
                
                # Verifica comando de saída
                if message.strip().lower() == "sair":
                    self.running = False
                    break
                
                print("Você: ", end='', flush=True)
                
            except EOFError:
                # Ctrl+D pressionado
                self.running = False
                break
            except KeyboardInterrupt:
                # Ctrl+C pressionado
                print("\n[ENCERRANDO] Saindo do chat...")
                self.running = False
                break
            except Exception as e:
                if self.running:
                    print(f"\n[ERRO] Erro ao enviar mensagem: {e}")
                break
    
    def start(self):
        """Inicia o cliente de chat"""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            # Conecta ao servidor
            self.client_socket.connect((self.host, self.port))
            self.running = True
            
            print(f"[CONECTADO] Conectado ao servidor de chat em {self.host}:{self.port}")
            print("Digite 'sair' para encerrar o chat.\n")
            
            # Cria threads para envio e recebimento simultâneo
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            send_thread = threading.Thread(target=self.send_messages)
            send_thread.daemon = True
            send_thread.start()
            
            # Aguarda threads finalizarem
            send_thread.join()
            
            # Pequeno delay para receber mensagem final do servidor
            receive_thread.join(timeout=1)
            
        except ConnectionRefusedError:
            print("[ERRO] Não foi possível conectar ao servidor.")
            print("[INFO] Verifique se o servidor está rodando.")
        except Exception as e:
            print(f"[ERRO] Erro na conexão: {e}")
        finally:
            self.running = False
            if self.client_socket:
                self.client_socket.close()
            print("\n[DESCONECTADO] Cliente encerrado.")

if __name__ == "__main__":
    client = ChatClient()
    client.start()
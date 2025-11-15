"""
Participantes: 
    Caio Bruno Gonzaga Liboreiro
    Kayky Nery Alcantara Vieira
    Marcus Vinícius de Oliveira Pinto
"""

import socket

class TimeClient:
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.client_socket = None
        
    def connect(self):
        """Conecta ao servidor de hora"""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.client_socket.connect((self.host, self.port))
            print(f"[CONECTADO] Conectado ao servidor de hora em {self.host}:{self.port}\n")
            return True
        except ConnectionRefusedError:
            print("[ERRO] Não foi possível conectar ao servidor.")
            print("[INFO] Verifique se o servidor está rodando.")
            return False
        except Exception as e:
            print(f"[ERRO] Erro ao conectar: {e}")
            return False
    
    def request_time(self):
        """Solicita hora ao servidor"""
        try:
            # Envia solicitação
            self.client_socket.send("hora".encode('utf-8'))
            
            # Recebe resposta
            response = self.client_socket.recv(1024).decode('utf-8')
            
            if response:
                print(f"[RESPOSTA] {response}")
                return True
            else:
                print("[ERRO] Servidor não respondeu.")
                return False
                
        except Exception as e:
            print(f"[ERRO] Erro ao solicitar hora: {e}")
            return False
    
    def interactive_mode(self):
        """Modo interativo - permite múltiplas solicitações"""
        print("=" * 60)
        print("CLIENTE DE HORA - MODO INTERATIVO")
        print("=" * 60)
        print("Comandos disponíveis:")
        print("  'hora'  - Solicitar hora atual")
        print("  'sair'  - Encerrar conexão")
        print("=" * 60)
        print()
        
        try:
            while True:
                command = input("Digite um comando: ").strip()
                
                if command == "":
                    continue
                
                # Envia comando ao servidor
                self.client_socket.send(command.encode('utf-8'))
                
                # Verifica se é comando de saída
                if command.lower() == "sair":
                    response = self.client_socket.recv(1024).decode('utf-8')
                    print(f"\n[SERVIDOR] {response}")
                    break
                
                # Recebe resposta
                response = self.client_socket.recv(1024).decode('utf-8')
                print(f"[SERVIDOR] {response}\n")
                
        except KeyboardInterrupt:
            print("\n\n[ENCERRANDO] Cliente encerrado pelo usuário (Ctrl+C)")
        except Exception as e:
            print(f"\n[ERRO] Erro durante comunicação: {e}")
    
    def simple_mode(self):
        """Modo simples - solicita hora uma vez e encerra"""
        print("=" * 60)
        print("CLIENTE DE HORA - MODO SIMPLES")
        print("=" * 60)
        print()
        
        if self.request_time():
            print("\n[SUCESSO] Hora obtida com sucesso!")
        else:
            print("\n[FALHA] Não foi possível obter a hora.")
    
    def close(self):
        """Encerra conexão"""
        if self.client_socket:
            self.client_socket.close()
            print("[DESCONECTADO] Conexão encerrada.\n")
    
    def run(self, mode='interactive'):
        """Executa o cliente"""
        if not self.connect():
            return
        
        try:
            if mode == 'simple':
                self.simple_mode()
            else:
                self.interactive_mode()
        finally:
            self.close()

def main():
    """Função principal com menu de escolha"""
    print("\n" + "=" * 60)
    print("CLIENTE DE HORA TCP")
    print("=" * 60)
    print("\nEscolha o modo de operação:")
    print("  1 - Modo Interativo (múltiplas solicitações)")
    print("  2 - Modo Simples (solicita hora e encerra)")
    print("=" * 60)
    
    choice = input("\nDigite sua escolha (1 ou 2): ").strip()
    print()
    
    client = TimeClient()
    
    if choice == '1':
        client.run(mode='interactive')
    elif choice == '2':
        client.run(mode='simple')
    else:
        print("[ERRO] Opção inválida. Use 1 ou 2.")

if __name__ == "__main__":
    main()
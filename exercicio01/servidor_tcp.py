"""
Participantes: 
    Caio Bruno Gonzaga Liboreiro
    Kayky Nery Alcantara Vieira
    Marcus Vinícius de Oliveira Pinto
"""

import socket
import threading

def handle_client(client_socket, client_address):
    """Função para lidar com cada cliente conectado"""
    print(f"[NOVA CONEXÃO] Cliente conectado: {client_address}")
    
    try:
        while True:
            # Recebe mensagem do cliente
            message = client_socket.recv(1024).decode('utf-8')
            
            # Verifica se a conexão foi encerrada
            if not message:
                print(f"[DESCONEXÃO] Cliente {client_address} desconectou.")
                break
            
            # Validação de mensagem vazia
            if message.strip() == "":
                response = "ERRO: Mensagem vazia não é permitida."
                client_socket.send(response.encode('utf-8'))
                continue
            
            # Verifica se cliente quer encerrar
            if message.lower() == "sair":
                print(f"[ENCERRAMENTO] Cliente {client_address} solicitou desconexão.")
                response = "Conexão encerrada. Até logo!"
                client_socket.send(response.encode('utf-8'))
                break
            
            # Imprime mensagem recebida
            print(f"[{client_address}] Mensagem recebida: {message}")
            
            # Envia confirmação ao cliente
            response = "Mensagem recebida"
            client_socket.send(response.encode('utf-8'))
            
    except Exception as e:
        print(f"[ERRO] Erro ao processar cliente {client_address}: {e}")
    
    finally:
        # Encerramento seguro da conexão
        client_socket.close()
        print(f"[FECHADO] Conexão com {client_address} encerrada.")

def start_server(host='localhost', port=5000):
    """Inicializa o servidor TCP"""
    # Cria socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Permite reutilização do endereço
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # Bind e Listen
        server_socket.bind((host, port))
        server_socket.listen(5)
        
        print(f"[INICIADO] Servidor rodando em {host}:{port}")
        print("[AGUARDANDO] Aguardando conexões...")
        
        while True:
            # Aceita conexão do cliente
            client_socket, client_address = server_socket.accept()
            
            # Cria thread para cada cliente
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address)
            )
            client_thread.start()
            
            print(f"[CONEXÕES ATIVAS] {threading.active_count() - 1} cliente(s) conectado(s)")
            
    except KeyboardInterrupt:
        print("\n[ENCERRANDO] Servidor encerrado pelo usuário.")
    except Exception as e:
        print(f"[ERRO] Erro no servidor: {e}")
    finally:
        server_socket.close()
        print("[FECHADO] Servidor encerrado.")

if __name__ == "__main__":
    start_server()
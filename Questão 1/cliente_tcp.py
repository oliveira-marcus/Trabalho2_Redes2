"""
Participantes: 
    Caio Bruno Gonzaga Liboreiro
    Kayky Nery Alcantara Vieira
    Marcus Vinícius de Oliveira Pinto
"""

import socket

def start_client(host='localhost', port=5000):
    """Inicializa o cliente TCP e se conecta ao servidor"""
    # Cria socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Conecta ao servidor
        client_socket.connect((host, port))
        print(f"[CONECTADO] Conectado ao servidor {host}:{port}")
        print("Digite 'sair' para encerrar a conexão.\n")
        
        while True:
            # Solicita mensagem do usuário
            message = input("Digite sua mensagem: ")
            
            # Validação de mensagem vazia
            if message.strip() == "":
                print("[ERRO] Mensagem vazia não é permitida. Tente novamente.\n")
                continue
            
            # Envia mensagem ao servidor
            client_socket.send(message.encode('utf-8'))
            
            # Recebe resposta do servidor
            response = client_socket.recv(1024).decode('utf-8')
            print(f"[SERVIDOR] {response}\n")
            
            # Verifica se deve encerrar
            if message.lower() == "sair":
                break
                
    except ConnectionRefusedError:
        print("[ERRO] Não foi possível conectar ao servidor. Verifique se o servidor está rodando.")
    except Exception as e:
        print(f"[ERRO] Erro na comunicação: {e}")
    finally:
        # Encerramento seguro da conexão
        client_socket.close()
        print("[DESCONECTADO] Conexão encerrada.")

if __name__ == "__main__":
    start_client()
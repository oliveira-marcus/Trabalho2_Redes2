"""
Participantes: 
    Caio Bruno Gonzaga Liboreiro
    Kayky Nery Alcantara Vieira
    Marcus Vinícius de Oliveira Pinto
"""

import socket

# Constante para tamanho máximo de mensagem UDP
MAX_UDP_SIZE = 65535  # 65535 - 8 (UDP header) - 20 (IP header)
TIMEOUT = 5  # Timeout em segundos para resposta do servidor

def start_echo_client(host='localhost', port=6000):
    """Inicializa o cliente Echo UDP"""
    # Cria socket UDP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Define timeout para evitar bloqueio indefinido
    client_socket.settimeout(TIMEOUT)
    
    try:
        print(f"[CONECTADO] Cliente Echo UDP conectado a {host}:{port}")
        print(f"[INFO] Tamanho máximo de mensagem: {MAX_UDP_SIZE} bytes")
        print(f"[INFO] Timeout de resposta: {TIMEOUT} segundos")
        print("Digite 'sair' para encerrar.\n")
        
        while True:
            try:
                # Solicita mensagem do usuário
                message = input("Digite sua mensagem: ")
                
                # Validação de mensagem vazia
                if message.strip() == "":
                    print("[ERRO] Mensagem vazia não é permitida. Tente novamente.\n")
                    continue
                
                # Validação de tamanho máximo
                message_bytes = message.encode('utf-8')
                message_size = len(message_bytes)
                
                if message_size > MAX_UDP_SIZE:
                    print(f"[ERRO] Mensagem muito grande ({message_size} bytes).")
                    print(f"[ERRO] Tamanho máximo permitido: {MAX_UDP_SIZE} bytes.\n")
                    continue
                
                # Envia mensagem ao servidor
                client_socket.sendto(message_bytes, (host, port))
                print(f"[ENVIADO] Mensagem enviada ({message_size} bytes)")
                
                # Recebe eco do servidor
                try:
                    data, server_address = client_socket.recvfrom(MAX_UDP_SIZE)
                    echo_message = data.decode('utf-8')
                    echo_size = len(data)
                    
                    print(f"[ECO RECEBIDO] ({echo_size} bytes): {echo_message}\n")
                    
                    # Verifica se deve encerrar
                    if message.lower() == "sair":
                        break
                        
                except socket.timeout:
                    print(f"[TIMEOUT] Servidor não respondeu em {TIMEOUT} segundos.")
                    print("[INFO] Possível perda de pacote. Tente novamente.\n")
                    
                except UnicodeDecodeError:
                    print("[ERRO] Não foi possível decodificar a resposta do servidor.\n")
                    
            except KeyboardInterrupt:
                print("\n[ENCERRANDO] Cliente encerrado pelo usuário.")
                break
                
    except Exception as e:
        print(f"[ERRO] Erro na comunicação: {e}")
    finally:
        # Encerramento do socket
        client_socket.close()
        print("[DESCONECTADO] Cliente encerrado.")

if __name__ == "__main__":
    start_echo_client()
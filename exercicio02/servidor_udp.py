"""
Participantes: 
    Caio Bruno Gonzaga Liboreiro
    Kayky Nery Alcantara Vieira
    Marcus Vinícius de Oliveira Pinto
"""

import socket

# Constante para tamanho máximo de mensagem UDP
MAX_UDP_SIZE = 4  # 65535 - 8 (UDP header) - 20 (IP header)

def start_echo_server(host='localhost', port=6000):
    """Inicializa o servidor Echo UDP"""
    # Cria socket UDP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        # Bind na porta especificada
        server_socket.bind((host, port))
        
        print(f"[INICIADO] Servidor Echo UDP rodando em {host}:{port}")
        print(f"[INFO] Tamanho máximo de mensagem: {MAX_UDP_SIZE} bytes")
        print("[AGUARDANDO] Aguardando mensagens...\n")
        
        while True:
            try:
                # Recebe mensagem do cliente (non-blocking após receber dados)
                data, client_address = server_socket.recvfrom(MAX_UDP_SIZE)
                message = data.decode('utf-8')
                
                # Validação de tamanho
                message_size = len(data)
                
                print(f"[{client_address}] Mensagem recebida ({message_size} bytes): {message}")
                
                # Verifica se é mensagem de encerramento
                if message.lower() == "sair":
                    response = "Servidor recebeu comando de saída. Até logo!"
                    server_socket.sendto(response.encode('utf-8'), client_address)
                    print(f"[INFO] Cliente {client_address} encerrou comunicação.\n")
                    continue
                
                # Validação de mensagem vazia
                if message.strip() == "":
                    response = "ERRO: Mensagem vazia"
                    server_socket.sendto(response.encode('utf-8'), client_address)
                    continue
                
                # Envia eco da mensagem de volta ao cliente
                server_socket.sendto(data, client_address)
                print(f"[ECO] Mensagem enviada de volta para {client_address}\n")
                
            except UnicodeDecodeError:
                print("[ERRO] Não foi possível decodificar a mensagem recebida.\n")
                error_msg = "ERRO: Mensagem inválida"
                server_socket.sendto(error_msg.encode('utf-8'), client_address)
                
            except Exception as e:
                print(f"[ERRO] Erro ao processar mensagem: {e}\n")
                
    except KeyboardInterrupt:
        print("\n[ENCERRANDO] Servidor encerrado pelo usuário.")
    except Exception as e:
        print(f"[ERRO] Erro no servidor: {e}")
    finally:
        server_socket.close()
        print("[FECHADO] Servidor encerrado.")

if __name__ == "__main__":
    start_echo_server()
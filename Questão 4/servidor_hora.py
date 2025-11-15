"""
Participantes: 
    Caio Bruno Gonzaga Liboreiro
    Kayky Nery Alcantara Vieira
    Marcus Vinícius de Oliveira Pinto
"""

import socket
import threading
import datetime
import logging

class TimeServer:
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.active_clients = 0
        self.clients_lock = threading.Lock()
        self.request_counter = 0
        self.setup_logging()
        
    def setup_logging(self):
        """Configura sistema de logs"""
        # Configura formato do log
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'
        
        # Configura logging para arquivo e console
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            datefmt=date_format,
            handlers=[
                logging.FileHandler('servidor_hora.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def get_current_time(self):
        """Retorna hora atual no formato HH:MM:SS"""
        now = datetime.datetime.now()
        return now.strftime("%H:%M:%S")
    
    def handle_client(self, client_socket, client_address):
        """Gerencia solicitações de um cliente específico"""
        with self.clients_lock:
            self.active_clients += 1
            active = self.active_clients
        
        self.logger.info(f"Nova conexão de {client_address} - Clientes ativos: {active}")
        
        try:
            while True:
                # Recebe solicitação do cliente
                data = client_socket.recv(1024).decode('utf-8')
                
                if not data:
                    self.logger.info(f"Cliente {client_address} desconectou")
                    break
                
                request = data.strip()
                
                # Incrementa contador de requisições
                with self.clients_lock:
                    self.request_counter += 1
                    request_id = self.request_counter
                
                self.logger.info(f"[REQ #{request_id}] Solicitação de {client_address}: '{request}'")
                
                # Verifica comando de encerramento
                if request.lower() == "sair":
                    response = "Conexão encerrada. Até logo!"
                    client_socket.send(response.encode('utf-8'))
                    self.logger.info(f"[REQ #{request_id}] Cliente {client_address} solicitou desconexão")
                    break
                
                # Verifica se é solicitação de hora
                if request.lower() in ["hora", "time", "horario", "horário"]:
                    current_time = self.get_current_time()
                    response = f"Hora atual: {current_time}"
                    client_socket.send(response.encode('utf-8'))
                    self.logger.info(f"[REQ #{request_id}] Hora enviada para {client_address}: {current_time}")
                
                elif request.strip() == "":
                    # Ignora mensagens vazias
                    continue
                
                else:
                    # Comando não reconhecido
                    response = "Comando inválido. Use 'hora' para obter a hora atual ou 'sair' para encerrar."
                    client_socket.send(response.encode('utf-8'))
                    self.logger.warning(f"[REQ #{request_id}] Comando inválido de {client_address}: '{request}'")
                
        except ConnectionResetError:
            self.logger.warning(f"Conexão perdida com {client_address} (reset)")
        except BrokenPipeError:
            self.logger.warning(f"Conexão quebrada com {client_address} (broken pipe)")
        except Exception as e:
            self.logger.error(f"Erro ao processar cliente {client_address}: {e}", exc_info=True)
        finally:
            # Garante que a conexão seja encerrada e contador atualizado
            try:
                client_socket.close()
            except:
                pass
            
            with self.clients_lock:
                self.active_clients -= 1
                active = self.active_clients
            
            self.logger.info(f"Conexão encerrada com {client_address} - Clientes ativos: {active}")
    
    def start(self):
        """Inicia o servidor de hora"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen(10)
            
            self.logger.info(f"=" * 60)
            self.logger.info(f"Servidor de Hora iniciado em {self.host}:{self.port}")
            self.logger.info(f"Aguardando conexões...")
            self.logger.info(f"=" * 60)
            
            while True:
                # Aceita conexão do cliente
                client_socket, client_address = server_socket.accept()
                
                # Cria thread para atender o cliente
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address),
                    daemon=True
                )
                client_thread.start()
                
        except KeyboardInterrupt:
            self.logger.info("\n" + "=" * 60)
            self.logger.info("Servidor encerrado pelo usuário (Ctrl+C)")
            self.logger.info(f"Total de requisições atendidas: {self.request_counter}")
            self.logger.info("=" * 60)
        except Exception as e:
            self.logger.error(f"Erro crítico no servidor: {e}", exc_info=True)
        finally:
            server_socket.close()
            self.logger.info("Servidor encerrado")

if __name__ == "__main__":
    server = TimeServer()
    server.start()
import socket
import threading

# Banco de dados em memória para registrar a localização dos serviços
REGISTRY = {}

def handle_client(conn, addr):
    try:
        data = conn.recv(1024).decode('utf-8').strip()
        if not data:
            return
        
        # Protocolo: REGISTRO;nome_servico;ip;porta  OU  BUSCA;nome_servico
        parts = data.split(';')
        command = parts[0]
        
        if command == "REGISTRO":
            nome, ip, porta = parts[1], parts[2], parts[3]
            REGISTRY[nome] = (ip, int(porta))
            conn.sendall(b"200 OK - Servico Registrado")
            print(f"[REGISTRO] {nome} mapeado para {ip}:{porta}")
            
        elif command == "BUSCA":
            nome = parts[1]
            if nome in REGISTRY:
                ip, porta = REGISTRY[nome]
                conn.sendall(f"{ip};{porta}".encode('utf-8'))
            else:
                conn.sendall(b"404 NOT FOUND")
    except Exception as e:
        print(f"Erro no manuseio: {e}")
    finally:
        conn.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5000))
    server.listen()
    print("[SERVIÇO DE NOMES] Rodando na porta 5000...")
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()

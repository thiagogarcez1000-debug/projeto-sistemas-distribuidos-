import socket
import threading
import time

def registrar_no_servico_de_nomes():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 5000))
        # Registra o serviço 'ProcessadorPedidos' rodando na porta 6000
        s.sendall(b"REGISTRO;ProcessadorPedidos;127.0.0.1;6000")
        resposta = s.recv(1024).decode('utf-8')
        print(f"[WORKER] Resposta do Registry: {resposta}")
        s.close()
    except Exception as e:
        print(f"[WORKER] Erro ao registrar serviço: {e}")

def processar_tarefa_assincrona(dados_pedido):
    # Simula computação/sincronização assíncrona pesada
    print(f"[ASSÍNCRONO] Iniciando processamento do {dados_pedido}...")
    time.sleep(4)  # Simula delay de processamento (I/O bound)
    print(f"[ASSÍNCRONO] {dados_pedido} processado e persistido com sucesso!")

def gerenciar_requisicao(conn, addr):
    data = conn.recv(1024).decode('utf-8')
    if data:
        # Responde imediatamente ao cliente (Comunicação Assíncrona / Non-blocking feel)
        conn.sendall(b"ACK - Pedido recebido e na fila de processamento.")
        conn.close() # Libera o cliente
        
        # Dispara thread em background para concluir a tarefa de forma assíncrona
        async_worker = threading.Thread(target=processar_tarefa_assincrona, args=(data,))
        async_worker.start()

def main():
    registrar_no_servico_de_nomes()
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 6000))
    server.listen()
    print("[WORKER SERVIDOR] Aguardando requisições na porta 6000...")
    
    while True:
        conn, addr = server.accept()
        threading.Thread(target=gerenciar_requisicao, args=(conn, addr)).start()

if __name__ == "__main__":
    main()

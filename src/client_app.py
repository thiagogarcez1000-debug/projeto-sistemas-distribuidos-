import socket

def buscar_servico(nome_servico):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 5000))
    s.sendall(f"BUSCA;{nome_servico}".encode('utf-8'))
    resposta = s.recv(1024).decode('utf-8')
    s.close()
    return resposta

def enviar_pedido(ip, porta, pedido):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, int(porta)))
    s.sendall(pedido.encode('utf-8'))
    resposta = s.recv(1024).decode('utf-8')
    s.close()
    print(f"[CLIENTE] Resposta do Servidor: {resposta}")

if __name__ == "__main__":
    print("[CLIENTE] Consultando Serviço de Nomes...")
    localizacao = buscar_servico("ProcessadorPedidos")
    
    if localizacao != "404 NOT FOUND":
        ip, porta = localizacao.split(';')
        print(f"[CLIENTE] Serviço encontrado em {ip}:{porta}. Enviando requisição...")
        enviar_pedido(ip, porta, "Pedido #10293 - Notebook Pro")
    else:
        print("[CLIENTE] Erro: Serviço não encontrado.")

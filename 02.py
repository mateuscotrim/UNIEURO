import hashlib
import threading
import time

# Variáveis Globais
hash_alvo = "ca6ae33116b93e57b87810a27296fc36"
encontrado = False
evento_parada = threading.Event()

def buscar_intervalo(inicio, fim, id_thread):
    """Função executada por cada thread"""
    global encontrado
    md5_func = hashlib.md5
    
    print(f"[Thread {id_thread}] Iniciando busca de {inicio:09} até {fim:09}")

    for i in range(inicio, fim):
        # Verifica se outra thread já encontrou a senha
        if evento_parada.is_set():
            return

        # Gera tentativa e compara
        tentativa = f"{i:09}"
        if md5_func(tentativa.encode('utf-8')).hexdigest() == hash_alvo:
            print(f"\n========================================")
            print(f"!!! SUCESSO PELA THREAD {id_thread} !!!")
            print(f"Senha: {tentativa}")
            print(f"========================================\n")
            
            encontrado = True
            evento_parada.set() # Avisa as outras threads para pararem
            return

def executar_paralelo_threads(num_threads):
    total_combinacoes = 1000000000 # 1 bilhão
    chunk = total_combinacoes // num_threads
    threads = []

    print(f"Configurando {num_threads} Threads...")
    tempo_inicio = time.time()

    # Criar e disparar as threads
    for t in range(num_threads):
        v_inicio = t * chunk
        v_fim = (t + 1) * chunk if t < num_threads - 1 else total_combinacoes
        
        thread = threading.Thread(target=buscar_intervalo, args=(v_inicio, v_fim, t))
        threads.append(thread)
        thread.start()

    # Aguardar todas terminarem
    for thread in threads:
        thread.join()

    tempo_final = time.time() - tempo_inicio
    print(f"Busca finalizada em: {tempo_final:.4f} segundos")

if __name__ == "__main__":
    # Defina aqui a quantidade de threads (ex: 4, 8, 16)
    NUM_THREADS = 4
    executar_paralelo_threads(NUM_THREADS)

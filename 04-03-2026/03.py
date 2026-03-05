import hashlib
import threading
import time

def buscar_intervalo(inicio, fim, hash_alvo, evento_parada):
    """Função executada por cada thread."""
    md5_func = hashlib.md5
    
    for i in range(inicio, fim):
        if evento_parada.is_set():
            return

        # Otimização: f-string e encode direto
        tentativa = f"{i:09}".encode('utf-8')
        
        if md5_func(tentativa).hexdigest() == hash_alvo:
            evento_parada.set()
            return

def executar_teste(n_threads, hash_alvo):
    """Configura e dispara a quantidade específica de threads."""
    total = 1000000000
    chunk = total // n_threads
    evento_parada = threading.Event()
    threads = []

    inicio_cronometro = time.time()

    for t in range(n_threads):
        v_inicio = t * chunk
        v_fim = (t + 1) * chunk if t < n_threads - 1 else total
        
        thread = threading.Thread(
            target=buscar_intervalo, 
            args=(v_inicio, v_fim, hash_alvo, evento_parada)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    tempo_total = time.time() - inicio_cronometro
    return tempo_total

if __name__ == "__main__":
    HASH_ALVO = "ca6ae33116b93e57b87810a27296fc36"
    LISTA_THREADS = [2, 4, 8, 12, 16, 20]
    resultados = {}

    print("=== INICIANDO EXPERIMENTO DE DESEMPENHO ===")
    print(f"Alvo: {HASH_ALVO} (Senha: 314159265)\n")

    for qtd in LISTA_THREADS:
        print(f"Testando com {qtd:02} threads...", end=" ", flush=True)
        
        tempo = executar_teste(qtd, HASH_ALVO)
        resultados[qtd] = tempo
        
        print(f"Concluído em {tempo:.2f}s")

    # Relatório Final
    print("\n" + "="*40)
    print(f"{'Threads':<10} | {'Tempo (s)':<15}")
    print("-" * 40)
    for qtd, tempo in resultados.items():
        print(f"{qtd:<10} | {tempo:<15.4f}")
    print("="*40)

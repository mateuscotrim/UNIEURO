import hashlib
import threading
import time

# Configurações Globais
HASH_ALVO = "ca6ae33116b93e57b87810a27296fc36"
EVENTO_PARADA = threading.Event()

def buscar_intervalo(inicio, fim, id_thread):
    """Função executada por cada thread com feedback de progresso."""
    md5_func = hashlib.md5
    contador_local = 0
    intervalo_feedback = 10000000  # Mostrar mensagem a cada 10 milhões
    
    for i in range(inicio, fim):
        # Verifica se alguma thread já encontrou a senha
        if EVENTO_PARADA.is_set():
            return

        # Processamento do Hash
        tentativa = f"{i:09}"
        if md5_func(tentativa.encode('utf-8')).hexdigest() == HASH_ALVO:
            print(f"\n[!!!] SUCESSO PELA THREAD {id_thread:02} [!!!]")
            print(f"Senha encontrada: {tentativa}")
            EVENTO_PARADA.set()
            return

        # Sistema de "Heartbeat" (Sinal de Vida)
        contador_local += 1
        if contador_local % intervalo_feedback == 0:
            progresso = (contador_local / (fim - inicio)) * 100
            print(f"[Thread {id_thread:02}] Ainda processando... ({progresso:.1f}% do meu bloco)")

def realizar_experimento(n_threads):
    """Prepara o ambiente para um número específico de threads."""
    EVENTO_PARADA.clear()
    total_combinacoes = 1000000000
    chunk = total_combinacoes // n_threads
    threads = []

    print(f"\n>>> TESTANDO COM {n_threads} THREADS <<<")
    inicio_tempo = time.time()

    for t in range(n_threads):
        v_inicio = t * chunk
        v_fim = (t + 1) * chunk if t < n_threads - 1 else total_combinacoes
        
        thread = threading.Thread(
            target=buscar_intervalo, 
            args=(v_inicio, v_fim, t)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    tempo_final = time.time() - inicio_tempo
    return tempo_final

if __name__ == "__main__":
    lista_testes = [2, 4, 8, 12, 16, 20]
    relatorio_tempos = {}

    print("INICIANDO BATERIA DE TESTES")
    print("Cada thread informará o progresso do seu próprio intervalo.")

    for qtd in lista_testes:
        tempo = realizar_experimento(qtd)
        relatorio_tempos[qtd] = tempo
        print(f"Concluído {qtd} threads em: {tempo:.2f}s")
        print("-" * 40)

    # Tabela Final de Comparação
    print("\n" + "="*35)
    print(f"{'Nº Threads':<12} | {'Tempo Total (s)':<15}")
    print("-" * 35)
    for q, t in relatorio_tempos.items():
        print(f"{q:<12} | {t:<15.4f}")
    print("="*35)

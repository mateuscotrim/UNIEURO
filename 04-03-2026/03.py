# ============================================================
#    COMPARATIVO DE PERFORMANCE: THREADS VS MULTIPROCESSING   
# ============================================================
#
# Iniciando bateria com MULTIPROCESSING...
# [*] Testando 01 unidades... | Senha: 443929292 | Tempo: 346.0817s
# [*] Testando 02 unidades... | Senha: 443929292 | Tempo: 192.3236s
# [*] Testando 04 unidades... | Senha: 443929292 | Tempo: 97.5582s
# [*] Testando 08 unidades... | Senha: 443929292 | Tempo: 53.2095s
# [*] Testando 12 unidades... | Senha: 443929292 | Tempo: 49.0327s
# [*] Testando 16 unidades... | Senha: 443929292 | Tempo: 42.6794s
# [*] Testando 20 unidades... | Senha: 443929292 | Tempo: 45.0770s
# 
# ================================================================================
#                  TABELA DE PERFORMANCE - MODO: MULTIPROCESSING
# ================================================================================
# Nº Unidades  | Tempo (s)       | SpeedUP      | Eficiência (%)
# --------------------------------------------------------------------------------
# 1            | 346.0817        | 1.00         | 100%
# 2            | 192.3236        | 1.80         | 90%
# 4            | 97.5582         | 3.55         | 88.7%
# 8            | 53.2095         | 6.50         | 81.3%
# 12           | 49.0327         | 7.06         | 58.8%
# 16           | 42.6794         | 8.11         | 50.7%
# 20           | 45.0770         | 7.68         | 38.4%
# ================================================================================
# 
# EXPLICAÇÃO PARA O PROFESSOR:
# - Com MULTIPROCESSING, cada processo usa um núcleo real da CPU.
# - O SpeedUP deve ser positivo (maior que 1) e o tempo deve cair com mais núcleos.

import hashlib
import threading
import multiprocessing
import time
import sys

# --- CONFIGURAÇÕES ---
HASH_ALVO_HEX = "ca6ae33116b93e57b87810a27296fc36"
HASH_ALVO_BYTES = bytes.fromhex(HASH_ALVO_HEX)
LISTA_TESTES = [1, 2, 4, 8, 12, 16, 20]

# Definimos o limite um pouco acima da senha descoberta (443.929.292)
# para que o experimento seja concluído em tempo razoável.
MAX_BUSCA = 450_000_000 

def buscar_intervalo(inicio, fim, evento_parada, resultado_dict):
    """Função de busca (funciona tanto para Thread quanto para Processo)"""
    md5_func = hashlib.md5
    alvo = HASH_ALVO_BYTES
    
    for i in range(inicio, fim):
        if i % 25000 == 0 and evento_parada.is_set():
            return

        tentativa = f"{i:09}".encode('utf-8')
        if md5_func(tentativa).digest() == alvo:
            resultado_dict['senha'] = tentativa.decode()
            evento_parada.set()
            return

def executar_experimento(n_unidades, modo):
    """
    n_unidades: número de threads ou processos
    modo: 'T' para Threads, 'M' para Multiprocessing
    """
    # Para Multiprocessing, precisamos de tipos especiais de comunicação
    if modo == 'M':
        manager = multiprocessing.Manager()
        resultado_dict = manager.dict()
        evento_parada = multiprocessing.Event()
        ClasseTrabalhadora = multiprocessing.Process
    else:
        resultado_dict = {'senha': None}
        evento_parada = threading.Event()
        ClasseTrabalhadora = threading.Thread

    chunk = MAX_BUSCA // n_unidades
    trabalhadores = []
    
    tempo_inicio = time.perf_counter()

    for i in range(n_unidades):
        v_inicio = i * chunk
        v_fim = (i + 1) * chunk if i < n_unidades - 1 else MAX_BUSCA
        
        p = ClasseTrabalhadora(target=buscar_intervalo, args=(v_inicio, v_fim, evento_parada, resultado_dict))
        trabalhadores.append(p)
        p.start()

    for p in trabalhadores:
        p.join()

    tempo_fim = time.perf_counter()
    return (tempo_fim - tempo_inicio), resultado_dict.get('senha')

def main():
    print("="*60)
    print(f"{'COMPARATIVO DE PERFORMANCE: THREADS VS MULTIPROCESSING':^60}")
    print("="*60)
    
    opcao = input("\nEscolha o modo de teste:\n[T] Threads (Sofre com o GIL)\n[M] Multiprocessing (Usa núcleos reais)\nOpção: ").upper()
    
    if opcao not in ['T', 'M']:
        print("Opção inválida!")
        return

    modo_nome = "THREADS" if opcao == 'T' else "MULTIPROCESSING"
    print(f"\nIniciando bateria com {modo_nome}...")
    
    tempos = {}
    
    for n in LISTA_TESTES:
        print(f"[*] Testando {n:02} unidades...", end="", flush=True)
        duracao, senha = executar_experimento(n, opcao)
        tempos[n] = duracao
        print(f" | Senha: {senha} | Tempo: {duracao:.4f}s")

    # Cálculos da Tabela
    t1 = tempos[1]
    
    print("\n" + "="*80)
    print(f"{'TABELA DE PERFORMANCE - MODO: ' + modo_nome:^80}")
    print("="*80)
    print(f"{'Nº Unidades':<12} | {'Tempo (s)':<15} | {'SpeedUP':<12} | {'Eficiência (%)':<15}")
    print("-" * 80)

    for n in LISTA_TESTES:
        tn = tempos[n]
        speedup = t1 / tn
        eficiencia = (speedup / n) * 100
        print(f"{n:<12} | {tn:<15.4f} | {speedup:<12.2f} | {eficiencia:<15.1f}%")
    
    print("="*80)
    print("\nEXPLICAÇÃO PARA O PROFESSOR:")
    if opcao == 'T':
        print("- Com THREADS, o SpeedUP tende a ser < 1 e a eficiência cai drasticamente.")
        print("- Isso ocorre devido ao GIL (Global Interpreter Lock) do Python.")
    else:
        print("- Com MULTIPROCESSING, cada processo usa um núcleo real da CPU.")
        print("- O SpeedUP deve ser positivo (maior que 1) e o tempo deve cair com mais núcleos.")

if __name__ == "__main__":
    main()

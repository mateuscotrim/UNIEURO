import hashlib
import time

hash_alvo = "ca6ae33116b93e57b87810a27296fc36"
inicio = time.time()

print("---------------------------------")
print("INICIANDO BUSCA SERIAL (T=1)...")
print("Se o programa estiver rodando, você verá mensagens abaixo.")
print("---------------------------------")

# LOOP DIRETO (0 a 999.999.999)
for i in range(1000000000):
    
    # Gera o número com 9 dígitos (ex: 000000001)
    tentativa = f"{i:09}"
    
    # Calcula o hash MD5
    hash_gerado = hashlib.md5(tentativa.encode('utf-8')).hexdigest()
    
    # Verifica se encontrou o hash
    if hash_gerado == hash_alvo:
        fim = time.time()
        tempo_total = fim - inicio
        
        print("\n================================")
        print(f"ACHEI! Senha: {tentativa}")
        print(f"Tempo Serial (T=1): {tempo_total:.4f} segundos")
        print(f"Tentativas: {i}")
        print("================================")
        break


    if i % 10000000 == 0 and i > 0:
        print(f"Verificando... {i // 1000000} milhões de tentativas feitas.")

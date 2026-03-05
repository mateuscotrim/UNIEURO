import hashlib
import threading
import time

def md5_string(texto):
    return hashlib.md5(texto.encode('utf-8')).hexdigest()

def buscahash(hashbuscado):
    for d1 in range(10):
        for d2 in range(10):
            for d3 in range(10):
                for d4 in range(10):
                    for d5 in range(10):
                        for d6 in range(10):
                            for d7 in range(10):
                                for d8 in range(10):
                                    for d9 in range(10):
                                        combinacao = f"{d1}{d2}{d3}{d4}{d5}{d6}{d7}{d8}{d9}"
                                        if hashbuscado == md5_string(combinacao):
                                            print(f"Achei! {combinacao}")
                                            return combinacao
    print("Não encontrado.")
    return None

inicio = time.time()
t = threading.Thread(target=buscahash, args=("ca6ae33116b93e57b87810a27296fc36",))
t.start()
t.join()
print(f"Tempo (T=1): {time.time() - inicio:.4f}s")

import csv
import gc
import os
import platform
import sys
import time


# ============================================================
# CONFIGURAÇÕES OFICIAIS DO EXPERIMENTO
# ============================================================

BLOCOS_MB = list(range(100, 1001, 100))
REPETICOES = 100

# Operações realizadas na ordem definida pelo professor:
# ALLOC -> WRITE -> READ -> FREE


# ============================================================
# IDENTIFICAÇÃO DO SISTEMA
# ============================================================

sistema = platform.system()

if sistema == "Windows":
    nome_sistema = "Windows"

elif sistema == "Linux":
    nome_sistema = "Linux"

else:
    print("ERRO: sistema operacional não suportado.")
    print(f"Sistema detectado: {sistema}")
    sys.exit(1)


# ============================================================
# INFORMAÇÕES DO AMBIENTE
# ============================================================

print()
print("=" * 60)
print("       MICROBENCHMARK - WINDOWS x LINUX")
print("=" * 60)

print(f"Sistema operacional : {nome_sistema}")
print(f"Python              : {platform.python_version()}")
print(f"Arquitetura         : {platform.machine()}")
print(f"Processador         : {platform.processor()}")
print(f"Blocos              : 100 MB até 1000 MB")
print(f"Repetições          : {REPETICOES} por tamanho")
print("=" * 60)
print()


# ============================================================
# ARQUIVO DE SAÍDA
# ============================================================

arquivo_saida = (
    f"resultados_{nome_sistema.lower()}.csv"
)


# ============================================================
# FUNÇÃO DO MICROBENCHMARK
# ============================================================

def executar_benchmark(tamanho_mb):

    tamanho_bytes = tamanho_mb * 1024 * 1024


    # --------------------------------------------------------
    # 1. ALOCAÇÃO
    # --------------------------------------------------------

    inicio = time.perf_counter()

    memoria = bytearray(tamanho_bytes)

    fim = time.perf_counter()

    alloc_ms = (fim - inicio) * 1000


    # --------------------------------------------------------
    # 2. ESCRITA
    # --------------------------------------------------------

    inicio = time.perf_counter()

    # Escreve em toda a área de memória
    memoria[:] = b"\x01" * tamanho_bytes

    fim = time.perf_counter()

    write_ms = (fim - inicio) * 1000


    # --------------------------------------------------------
    # 3. LEITURA
    # --------------------------------------------------------

    inicio = time.perf_counter()

    soma = 0

    # Percorre a memória em intervalos de 4096 bytes.
    # Isso evita que a operação seja excessivamente lenta.
    for posicao in range(0, tamanho_bytes, 4096):
        soma += memoria[posicao]

    fim = time.perf_counter()

    read_ms = (fim - inicio) * 1000


    # --------------------------------------------------------
    # 4. LIBERAÇÃO
    # --------------------------------------------------------

    inicio = time.perf_counter()

    del memoria

    # Solicita ao Python a coleta de objetos que possam
    # estar aguardando liberação.
    gc.collect()

    fim = time.perf_counter()

    free_ms = (fim - inicio) * 1000


    return (
        alloc_ms,
        write_ms,
        read_ms,
        free_ms
    )


# ============================================================
# EXECUÇÃO
# ============================================================

print(f"Arquivo de saída: {arquivo_saida}")
print()

inicio_total = time.perf_counter()


with open(
    arquivo_saida,
    "w",
    newline="",
    encoding="utf-8"
) as arquivo:

    escritor = csv.writer(arquivo)

    # Cabeçalho
    escritor.writerow([
        "sistema",
        "bloco_MB",
        "teste",
        "alloc_ms",
        "write_ms",
        "read_ms",
        "free_ms"
    ])


    # --------------------------------------------------------
    # CADA TAMANHO DE BLOCO
    # --------------------------------------------------------

    for bloco in BLOCOS_MB:

        print(
            f"[{nome_sistema}] "
            f"Executando bloco de {bloco} MB..."
        )


        # ----------------------------------------------------
        # 100 REPETIÇÕES
        # ----------------------------------------------------

        for teste in range(1, REPETICOES + 1):

            (
                alloc_ms,
                write_ms,
                read_ms,
                free_ms
            ) = executar_benchmark(bloco)


            escritor.writerow([
                nome_sistema,
                bloco,
                teste,
                f"{alloc_ms:.6f}",
                f"{write_ms:.6f}",
                f"{read_ms:.6f}",
                f"{free_ms:.6f}"
            ])


        print(
            f"    -> {REPETICOES} testes concluídos"
        )


fim_total = time.perf_counter()

tempo_total = fim_total - inicio_total


# ============================================================
# FINAL
# ============================================================

print()
print("=" * 60)
print("              EXPERIMENTO CONCLUÍDO")
print("=" * 60)

print(f"Sistema : {nome_sistema}")
print(f"Arquivo : {arquivo_saida}")
print(f"Registros: {len(BLOCOS_MB) * REPETICOES}")
print(f"Tempo total: {tempo_total:.2f} segundos")

print()
print("CSV gerado com sucesso!")
print("=" * 60)
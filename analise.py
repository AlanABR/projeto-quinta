import os
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# ARQUIVOS
# ============================================================

ARQUIVO_WINDOWS = "resultados_windows.csv"
ARQUIVO_LINUX = "resultados_linux.csv"


# ============================================================
# VERIFICAÇÃO DOS ARQUIVOS
# ============================================================

if not os.path.exists(ARQUIVO_WINDOWS):

    print(
        f"ERRO: {ARQUIVO_WINDOWS} não encontrado."
    )

    exit()


if not os.path.exists(ARQUIVO_LINUX):

    print(
        f"ERRO: {ARQUIVO_LINUX} não encontrado."
    )

    exit()


# ============================================================
# LEITURA
# ============================================================

windows = pd.read_csv(ARQUIVO_WINDOWS)

linux = pd.read_csv(ARQUIVO_LINUX)


# ============================================================
# COMBINA OS DOIS SISTEMAS
# ============================================================

dados = pd.concat(
    [windows, linux],
    ignore_index=True
)


# ============================================================
# OPERAÇÕES
# ============================================================

operacoes = [
    "alloc_ms",
    "write_ms",
    "read_ms",
    "free_ms"
]


nomes = {

    "alloc_ms": "Alocação",

    "write_ms": "Escrita",

    "read_ms": "Leitura",

    "free_ms": "Liberação"
}


# ============================================================
# MÉDIAS POR BLOCO
# ============================================================

medias = (

    dados

    .groupby(
        ["sistema", "bloco_MB"]
    )[operacoes]

    .mean()

    .reset_index()
)


medias.to_csv(
    "medias_por_bloco.csv",
    index=False
)


# ============================================================
# MEDIANA POR BLOCO
# ============================================================

medianas = (

    dados

    .groupby(
        ["sistema", "bloco_MB"]
    )[operacoes]

    .median()

    .reset_index()
)


medianas.to_csv(
    "medianas_por_bloco.csv",
    index=False
)


# ============================================================
# DESVIO PADRÃO
# ============================================================

desvios = (

    dados

    .groupby(
        ["sistema", "bloco_MB"]
    )[operacoes]

    .std()

    .reset_index()
)


desvios.to_csv(
    "desvio_padrao_por_bloco.csv",
    index=False
)


# ============================================================
# MÉDIA GERAL
# ============================================================

media_geral = (

    dados

    .groupby("sistema")[operacoes]

    .mean()
)


media_geral.to_csv(
    "media_geral.csv"
)


# ============================================================
# MEDIANA GERAL
# ============================================================

mediana_geral = (

    dados

    .groupby("sistema")[operacoes]

    .median()
)


mediana_geral.to_csv(
    "mediana_geral.csv"
)


# ============================================================
# DESVIO PADRÃO GERAL
# ============================================================

desvio_geral = (

    dados

    .groupby("sistema")[operacoes]

    .std()
)


desvio_geral.to_csv(
    "desvio_padrao_geral.csv"
)


# ============================================================
# IMPRESSÃO
# ============================================================

print()
print("=" * 70)
print("             ANÁLISE WINDOWS x LINUX")
print("=" * 70)


print()
print("QUANTIDADE DE REGISTROS")
print("-" * 70)

print(
    f"Windows: {len(windows)}"
)

print(
    f"Linux:   {len(linux)}"
)


print()
print("MÉDIA GERAL DOS TEMPOS")
print("-" * 70)

print(
    media_geral.to_string()
)


# ============================================================
# COMPARAÇÃO DAS OPERAÇÕES
# ============================================================

print()
print("=" * 70)
print("             COMPARAÇÃO POR OPERAÇÃO")
print("=" * 70)


vitorias_windows = 0
vitorias_linux = 0


for operacao in operacoes:

    tempo_windows = media_geral.loc[
        "Windows",
        operacao
    ]

    tempo_linux = media_geral.loc[
        "Linux",
        operacao
    ]


    print()
    print(
        f"OPERAÇÃO: {nomes[operacao]}"
    )

    print(
        f"Windows: {tempo_windows:.6f} ms"
    )

    print(
        f"Linux:   {tempo_linux:.6f} ms"
    )


    if tempo_windows < tempo_linux:

        vencedor = "Windows"

        vitorias_windows += 1

    elif tempo_linux < tempo_windows:

        vencedor = "Linux"

        vitorias_linux += 1

    else:

        vencedor = "Empate"


    print(
        f"Melhor desempenho: {vencedor}"
    )


# ============================================================
# RESULTADO GERAL
# ============================================================

print()
print("=" * 70)
print("                    RESULTADO")
print("=" * 70)

print()
print(
    f"Operações vencidas pelo Windows: "
    f"{vitorias_windows}"
)

print(
    f"Operações vencidas pelo Linux:   "
    f"{vitorias_linux}"
)


if vitorias_windows > vitorias_linux:

    print()
    print("RESULTADO GERAL: WINDOWS")

elif vitorias_linux > vitorias_windows:

    print()
    print("RESULTADO GERAL: LINUX")

else:

    print()
    print("RESULTADO GERAL: EMPATE")


# ============================================================
# GRÁFICOS
# ============================================================

print()
print("Gerando gráficos...")


for operacao in operacoes:

    plt.figure(
        figsize=(10, 6)
    )


    for sistema in [
        "Windows",
        "Linux"
    ]:

        dados_sistema = medias[
            medias["sistema"] == sistema
        ]


        plt.plot(
            dados_sistema["bloco_MB"],
            dados_sistema[operacao],
            marker="o",
            label=sistema
        )


    plt.title(
        f"{nomes[operacao]} - Windows x Linux"
    )

    plt.xlabel(
        "Tamanho do bloco (MB)"
    )

    plt.ylabel(
        "Tempo (ms)"
    )

    plt.xticks(
        range(100, 1001, 100)
    )

    plt.legend()

    plt.grid(True)

    plt.tight_layout()


    nome_grafico = (
        f"grafico_{operacao}.png"
    )


    plt.savefig(
        nome_grafico,
        dpi=300
    )

    plt.close()


# ============================================================
# FINAL
# ============================================================

print()
print("=" * 70)
print("ANÁLISE CONCLUÍDA!")
print("=" * 70)

print()
print("Arquivos gerados:")

print(" - medias_por_bloco.csv")
print(" - medianas_por_bloco.csv")
print(" - desvio_padrao_por_bloco.csv")
print(" - media_geral.csv")
print(" - mediana_geral.csv")
print(" - desvio_padrao_geral.csv")
print(" - grafico_alloc_ms.png")
print(" - grafico_write_ms.png")
print(" - grafico_read_ms.png")
print(" - grafico_free_ms.png")
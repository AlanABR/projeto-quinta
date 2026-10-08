import csv
import sys


BLOCOS_ESPERADOS = list(range(100, 1001, 100))
TESTES_ESPERADOS = list(range(1, 101))


def validar(nome_arquivo):

    erros = []

    with open(
        nome_arquivo,
        "r",
        newline="",
        encoding="utf-8"
    ) as arquivo:

        leitor = csv.DictReader(arquivo)

        linhas = list(leitor)


    # ========================================================
    # QUANTIDADE
    # ========================================================

    if len(linhas) != 1000:

        erros.append(
            f"Quantidade de registros: {len(linhas)} "
            f"(esperado: 1000)"
        )


    combinacoes = set()


    # ========================================================
    # VERIFICA CADA LINHA
    # ========================================================

    for numero, linha in enumerate(linhas, start=2):

        campos = [
            "sistema",
            "bloco_MB",
            "teste",
            "alloc_ms",
            "write_ms",
            "read_ms",
            "free_ms"
        ]


        # ----------------------------------------------------
        # CAMPOS VAZIOS
        # ----------------------------------------------------

        for campo in campos:

            if campo not in linha:

                erros.append(
                    f"Linha {numero}: "
                    f"campo '{campo}' inexistente."
                )

            elif linha[campo] == "":

                erros.append(
                    f"Linha {numero}: "
                    f"campo '{campo}' vazio."
                )


        try:

            bloco = int(linha["bloco_MB"])
            teste = int(linha["teste"])

            tempos = [
                float(linha["alloc_ms"]),
                float(linha["write_ms"]),
                float(linha["read_ms"]),
                float(linha["free_ms"])
            ]

        except (ValueError, KeyError):

            erros.append(
                f"Linha {numero}: "
                "valor numérico inválido."
            )

            continue


        # ----------------------------------------------------
        # BLOCO
        # ----------------------------------------------------

        if bloco not in BLOCOS_ESPERADOS:

            erros.append(
                f"Linha {numero}: "
                f"bloco inválido: {bloco}"
            )


        # ----------------------------------------------------
        # TESTE
        # ----------------------------------------------------

        if teste not in TESTES_ESPERADOS:

            erros.append(
                f"Linha {numero}: "
                f"teste inválido: {teste}"
            )


        # ----------------------------------------------------
        # TEMPOS
        # ----------------------------------------------------

        for tempo in tempos:

            if tempo < 0:

                erros.append(
                    f"Linha {numero}: "
                    "tempo negativo."
                )


        # ----------------------------------------------------
        # DUPLICIDADE
        # ----------------------------------------------------

        sistema = linha["sistema"]

        chave = (
            sistema,
            bloco,
            teste
        )

        if chave in combinacoes:

            erros.append(
                f"Linha {numero}: "
                f"registro duplicado: {chave}"
            )

        combinacoes.add(chave)


    # ========================================================
    # RESULTADO
    # ========================================================

    print()
    print("=" * 60)
    print(f"VALIDAÇÃO: {nome_arquivo}")
    print("=" * 60)

    if erros:

        print()
        print("ERROS ENCONTRADOS:")
        print()

        for erro in erros:

            print(" -", erro)

        print()
        return False


    print()
    print("ARQUIVO VÁLIDO!")
    print()
    print("Registros: 1000")
    print("Blocos: 100 a 1000 MB")
    print("Repetições: 100 por bloco")
    print("Sem erros encontrados.")
    print()

    return True


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

if __name__ == "__main__":

    if len(sys.argv) != 2:

        print(
            "Uso:"
        )

        print(
            "python validar_csv.py "
            "resultados_windows.csv"
        )

        sys.exit(1)


    sucesso = validar(sys.argv[1])


    if not sucesso:

        sys.exit(1)
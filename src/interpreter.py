def interpretar_copa(tree):
    match tree.data:
        case "start":
            for filho in tree.children:
                interpretar_copa(filho)
            return

        case "grupo":
            nome_grupo = str(tree.children[0])
            classificacao = {}

            for comando in tree.children[1:]:
                if comando.data == "selecao":
                    nome_sel = str(comando.children[0])
                    classificacao[nome_sel] = {"pontos": 0, "gols_pro": 0, "gols_contra": 0, "saldo": 0}

            for comando in tree.children[1:]:
                if comando.data == "confronto":
                    sel1 = str(comando.children[0])
                    placar1 = int(comando.children[1])
                    placar2 = int(comando.children[2])
                    sel2 = str(comando.children[3])

                    classificacao[sel1]["gols_pro"] += placar1
                    classificacao[sel1]["gols_contra"] += placar2
                    classificacao[sel2]["gols_pro"] += placar2
                    classificacao[sel2]["gols_contra"] += placar1

                    if placar1 > placar2:
                        classificacao[sel1]["pontos"] += 3
                    elif placar2 > placar1:
                        classificacao[sel2]["pontos"] += 3
                    else:
                        classificacao[sel1]["pontos"] += 1
                        classificacao[sel2]["pontos"] += 1

            for sel in classificacao:
                classificacao[sel]["saldo"] = classificacao[sel]["gols_pro"] - classificacao[sel]["gols_contra"]

            ranking = sorted(
                classificacao.items(),
                key=lambda x: (x[1]["pontos"], x[1]["saldo"], x[1]["gols_pro"]),
                reverse=True
            )

            print(f"\n=== CLASSIFICAÇÃO FINAL: GRUPO {nome_grupo} ===")
            for i, (time, dados) in enumerate(ranking, 1):
                status = "Classificado" if i <= 2 else "Eliminado"
                print(f"{i}. {time} - {dados['pontos']} pts | Saldo: {dados['saldo']} | GP: {dados['gols_pro']} ({status})")
            return

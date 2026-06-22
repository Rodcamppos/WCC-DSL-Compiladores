def interpretar_copa(tree, memoria_global=None):
    if memoria_global is None:
        memoria_global = {}

    match tree.data:
        case "start":
            for child in tree.children:
                interpretar_copa(child, memoria_global)
            
            terceiros_colocados = []
            for nome_grupo, ranking in memoria_global.items():
                if len(ranking) >= 3:
                    time, dados = ranking[2]
                    terceiros_colocados.append((time, dados, nome_grupo))
            
            melhores_terceiros = sorted(
                terceiros_colocados,
                key=lambda x: (x[1]["pontos"], x[1]["saldo"], x[1]["gols_pro"]),
                reverse=True
            )
            
            print("\n=== RANKING GLOBAL DOS TERCEIROS COLOCADOS ===")
            for i, (time, dados, grupo) in enumerate(melhores_terceiros, 1):
                status = "AVANÇA (Top 8)" if i <= 8 else "ELIMINADO"
                print(f"{i}. {time} (Grupo {grupo}) - {dados['pontos']} pts | Saldo: {dados['saldo']} | GP: {dados['gols_pro']} -> {status}")
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

            memoria_global[nome_grupo] = ranking

            print(f"\n=== CLASSIFICAÇÃO FINAL: GRUPO {nome_grupo} ===")
            for i, (time, dados) in enumerate(ranking, 1):
                if i <= 2:
                    status = "Classificado"
                elif i == 3:
                    status = "Aguardando Repescagem"
                else:
                    status = "Eliminado"
                print(f"{i}. {time} - {dados['pontos']} pts | Saldo: {dados['saldo']} | GP: {dados['gols_pro']} ({status})")
            return
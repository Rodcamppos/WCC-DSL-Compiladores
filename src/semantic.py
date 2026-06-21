def avalie_copa(tree):
    match tree.data:
        case "start":
            for filho in tree.children:
                avalie_copa(filho)
            return

        case "grupo":
            nome_grupo = str(tree.children[0])
            
            selecoes_declaradas = set()
            potes_preenchidos = set()
            continentes_contagem = {}
            jogos_por_selecao = {}
            
            for comando in tree.children[1:]:
                if comando.data == "selecao":
                    nome_sel = str(comando.children[0])
                    pote = int(comando.children[1])
                    continente = str(comando.children[2])
                    
                    if nome_sel in selecoes_declaradas:
                        raise Exception(f"Erro Semântico [{nome_grupo}]: A seleção '{nome_sel}' já foi declarada.")
                    
                    if pote in potes_preenchidos:
                        raise Exception(f"Erro Semântico [{nome_grupo}]: O Pote {pote} já possui uma seleção cadastrada.")
                    
                    qtd_continente = continentes_contagem.get(continente, 0)
                    if continente == "Europa":
                        if qtd_continente >= 2:
                            raise Exception(f"Erro Semântico [{nome_grupo}]: O grupo não pode ter mais de 2 seleções da Europa.")
                    else:
                        if qtd_continente >= 1:
                            raise Exception(f"Erro Semântico [{nome_grupo}]: O grupo não pode ter mais de 1 seleção da confederação '{continente}'.")
                    
                    selecoes_declaradas.add(nome_sel)
                    potes_preenchidos.add(pote)
                    continentes_contagem[continente] = qtd_continente + 1
                    jogos_por_selecao[nome_sel] = 0

            if len(potes_preenchidos) != 4:
                raise Exception(f"Erro Semântico [{nome_grupo}]: O grupo precisa ter exatamente 4 seleções (uma de cada pote de 1 a 4).")

            for comando in tree.children[1:]:
                if comando.data == "confronto":
                    sel1 = str(comando.children[0])
                    placar1 = int(comando.children[1])
                    placar2 = int(comando.children[2])
                    sel2 = str(comando.children[3])
                    
                    if sel1 not in selecoes_declaradas:
                        raise Exception(f"Erro Semântico [{nome_grupo}]: A seleção '{sel1}' no confronto não foi declarada no grupo.")
                    if sel2 not in selecoes_declaradas:
                        raise Exception(f"Erro Semântico [{nome_grupo}]: A seleção '{sel2}' no confronto não foi declarada no grupo.")
                    
                    if sel1 == sel2:
                        raise Exception(f"Erro Semântico [{nome_grupo}]: Uma seleção não pode jogar contra ela mesma ({sel1}).")
                    
                    jogos_por_selecao[sel1] += 1
                    jogos_por_selecao[sel2] += 1
                    
                    if jogos_por_selecao[sel1] > 3:
                        raise Exception(f"Erro Semântico [{nome_grupo}]: A seleção '{sel1}' ultrapassou o limite máximo de 3 jogos.")
                    if jogos_por_selecao[sel2] > 3:
                        raise Exception(f"Erro Semântico [{nome_grupo}]: A seleção '{sel2}' ultrapassou o limite máximo de 3 jogos.")
            return

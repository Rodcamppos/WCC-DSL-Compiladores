from lark import Lark

# Definição da gramática livre de contexto para a Copa do Mundo
analisador_copa = Lark(r"""
    ?start : grupo*

    grupo : "Grupo" ID "{" comando* "}"

    ?comando : selecao | confronto

    selecao : "Selecao" ID "(" "pote" ":" POTE "," "continente" ":" ID ")"
    
    confronto : "Confronto" ID PLACAR "x" PLACAR ID

    # Terminais (Léxico)
    POTE    : /[1-4]/
    PLACAR  : /[0-9]+/
    ID      : /[A-Za-zÀ-ÿ_]+/

    %ignore /[ \t\n\r]+/
    %ignore /#[^\n]*/
""", start='start')

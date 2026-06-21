import sys
from src.grammar import analisador_copa
from src.semantic import avalie_copa
from src.interpreter import interpretar_copa

def rodar_compilador(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        arvore = analisador_copa.parse(conteudo)
        
        avalie_copa(arvore)
        
        interpretar_copa(arvore)
        
    except Exception as e:
        print(f"❌ {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        rodar_compilador(sys.argv[1])
    else:
        print("Por favor, informe o caminho do arquivo .wcc")

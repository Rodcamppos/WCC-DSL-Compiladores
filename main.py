import sys
from src.grammar import analisador_copa
from src.semantic import avalie_copa

def rodar_compilador(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()

        arvore = analisador_copa.parse(conteudo)
        avalie_copa(arvore)
        print("🎉 Compilação e validação concluídas com sucesso!")
    except Exception as e:
        print(f"❌ Erro detectado: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        rodar_compilador(sys.argv[1])
    else:
        print("Por favor, informe o caminho do arquivo .wcc")
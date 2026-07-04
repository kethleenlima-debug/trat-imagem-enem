"""
Propósito: Renomear as imagens do padrão parte_0xx.png para questao-xx.png
Autor: Alexandre Nassar de Peder
Criação: 02/10/2025
Atualização: 03/06/2026

OBS1: puxe todas as pastas do passo 8 para este passo 9

OBS2: você vai atualizar o nome das imagens para seguir um padrão, mas você vai fazer isso pasta por pasta.

OBS3: você pode observar que você separou as questões por intervalos ininterruptos, crescendo de 1 em 1. Isso é importante porque as páginas inteiras foram tratadas de maneira diferente do que as páginas que contém colunas. Por isso teve um gap no meio das questões concatenadas das colunas.

OBS4: no passo 7, você recortou as partes da imagem, por isso as imagens se chama parte_AlgumaCoisa.png. E no passo 8 você separou as imagens em pastas, cada pasta com um intervalo ininterrupto de questões.

OBS5: o objetivo deste passo é renomear as imagens de cada pasta para seguir um padrão.

OBS6: dentro de cada pasta, você tem as partes recortadas em sequência, com o nome parte_AlgumaCoisa.png, crescendo de 1 em 1. Você pode observar também que a imagem parte_AlgumaCoisa é a questao-OutraCoisa. Desse modo, o nome do arquivo parte_AlgumaCoisa.png vai virar questao-OutraCoisa.png, tudo crescendo de 1 em 1.

OBS7: para cada vez que executar esse código, faça:
- atualize a linha 29 com o nome da pasta que você vai arrumar
- atualize o for da linha 40 com o número da primeira imagem "parte_AlgumaCoisa.png" até o número da última imagem "parte_AlgumaCoisa.png" mais 1
- escolha qual padrão novo de nome você vai usar nas linhas 46 a 48. Deixe apenas uma linha descomentada de cada vez. Se são as questões de ingles, use o padrão com sufixo de ingles; se são questões de espanhol, use o padrão com sufixo de espanhol; se são as outras questões, use o padrão sem sufixo de idioma.
- dentro do padrão novo de nome, faça a conta para transformar o número do antigo no número do novo. Você pode ler o comentário antes dos padrões para saber qual conta fazer
- execute o código
"""
import os

def renomear_questoes_simples():
    pasta = "80-90" # ATUALIZE O NOME DA PASTA QUE VOCÊ VAI ARRUMAR AQUI
    
    if not os.path.exists(pasta):
        print(f"Pasta {pasta} não encontrada!")
        return
    
    # Mapeamento direto dos nomes antigos para os novos
    mapeamento = {}
        
    # Aqui você vai renomear seguindo o padrão: parte_00x.png a parte_00y.png -> questao-a.png a questao-b.png
    # atualize seu for com o número da primeira imagem "parte_AlgumaCoisa.png" até o número da última imagem "parte_AlgumaCoisa.png" mais 1 da pasta
    for i in range(81, 91+1):
        # f-string do nome antigo
        antigo = f"parte_{i:03d}.png"

        # f-string dos novos nomes. Faça a conta para transformar o número do antigo no número do novo
        # faça uma conta: se o i do teu for está em 2, e precisa virar questão 35, como você transforma 2 em 35? faça a conta e coloque dentro da concatenação
        novo = f"questao-{i+78}.png"  # faça uma conta: se a primeira pagina for 
        #novo = f"questao-{i+78}-ingles.png"
        #novo = f"questao-{i-1}.png" 
        
        mapeamento[antigo] = novo
    
    # Aplicar o renomeamento
    for antigo, novo in mapeamento.items():
        caminho_antigo = os.path.join(pasta, antigo)
        caminho_novo = os.path.join(pasta, novo)
        
        if os.path.exists(caminho_antigo):
            os.rename(caminho_antigo, caminho_novo)
            print(f"Renomeado: {antigo} -> {novo}")
        else:
            print(f"Arquivo não encontrado: {antigo}")
    
    print("Renomeação concluída!")

# Executar
if __name__ == "__main__":
    renomear_questoes_simples()
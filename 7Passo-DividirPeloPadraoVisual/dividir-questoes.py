from pathlib import Path
import re

import cv2
import easyocr
import numpy as np
from PIL import Image


class DivisorQuestoes:

    def __init__(
        self,
        idioma="pt",
        usar_gpu=False,
        altura_janela=3500,
        sobreposicao=500
    ):

        print("Inicializando OCR...")

        self.reader = easyocr.Reader(
            [idioma],
            gpu=usar_gpu
        )

        self.altura_janela = altura_janela
        self.sobreposicao = sobreposicao

        self.padrao = re.compile(
            r"QUEST[ÃA]O\s*\d+",
            re.IGNORECASE
        )

        print("OCR pronto!")

    def executar_ocr(self, imagem):

        imagem = np.array(imagem)
        imagem = cv2.cvtColor(imagem, cv2.COLOR_RGB2BGR)

        return self.reader.readtext(
            imagem,
            detail=1,
            paragraph=False
        )

    def localizar_inicio_questoes(self, caminho):

        imagem = Image.open(caminho)

        largura, altura = imagem.size

        posicoes = []

        inicio = 0

        while inicio < altura:

            fim = min(
                inicio + self.altura_janela,
                altura
            )

            print(f"Analisando faixa {inicio} -> {fim}")

            trecho = imagem.crop(
                (
                    0,
                    inicio,
                    largura,
                    fim
                )
            )

            resultados = self.executar_ocr(trecho)

            for bbox, texto, _ in resultados:

                texto = texto.upper()

                if not self.padrao.search(texto):
                    continue

                y = min(p[1] for p in bbox)

                posicao = inicio + int(y)

                posicoes.append(posicao)

                print(f"Encontrada: {texto}")

            inicio += (
                self.altura_janela
                - self.sobreposicao
            )

        return sorted(set(posicoes))

    def salvar_partes(
        self,
        imagem,
        cortes,
        pasta
    ):

        Path(pasta).mkdir(
            parents=True,
            exist_ok=True
        )

        largura, altura = imagem.size

        ultimo = 0

        contador = 1

        for corte in cortes:

            if corte - ultimo < 100:
                continue

            imagem.crop(
                (
                    0,
                    ultimo,
                    largura,
                    corte
                )
            ).save(
                Path(pasta) /
                f"parte_{contador:03}.png"
            )

            print(f"parte_{contador:03}.png")

            ultimo = corte

            contador += 1

        imagem.crop(
            (
                0,
                ultimo,
                largura,
                altura
            )
        ).save(
            Path(pasta) /
            f"parte_{contador:03}.png"
        )

        print(f"parte_{contador:03}.png")

        print(f"\nTotal: {contador} imagens.")

    def cortar(self, caminho_imagem, pasta_saida):

        imagem = Image.open(caminho_imagem)

        cortes = self.localizar_inicio_questoes(
            caminho_imagem
        )

        if not cortes:

            print("Nenhuma questão encontrada.")

            return

        print(f"\n{len(cortes)} inícios encontrados.\n")

        self.salvar_partes(
            imagem,
            cortes,
            pasta_saida
        )


if __name__ == "__main__":

    arquivo = "colunas_concatenadas_verticalmente.png"

    pasta = "questoes_colunas"

    divisor = DivisorQuestoes()

    divisor.cortar(
        arquivo,
        pasta
    )
from PIL import Image
import easyocr
import numpy as np
import cv2
import os
import re


class DivisorQuestoesOCR:

    def __init__(self):
        print("Carregando OCR...")
        self.reader = easyocr.Reader(['pt'], gpu=False)
        print("OCR carregado!")

    def encontrar_questoes(self, caminho_imagem):

        imagem = Image.open(caminho_imagem)

        largura, altura = imagem.size

        janela = 3500
        sobreposicao = 500

        cortes = []

        y_inicio = 0

        while y_inicio < altura:

            y_fim = min(y_inicio + janela, altura)

            print(f"Analisando {y_inicio} -> {y_fim}")

            pedaco = imagem.crop((0, y_inicio, largura, y_fim))

            # PIL -> NumPy
            pedaco = np.array(pedaco)

            # RGB -> BGR
            pedaco = cv2.cvtColor(pedaco, cv2.COLOR_RGB2BGR)

            resultado = self.reader.readtext(
                pedaco,
                detail=1,
                paragraph=False
            )

            for item in resultado:

                bbox = item[0]
                texto = item[1].upper()

                if re.search(r"QUEST[ÃA]O\s*\d+", texto):

                    y_local = int(min(p[1] for p in bbox))

                    y_real = y_inicio + y_local - 3

                    cortes.append(y_real)

                    print(f"{texto} encontrada em y={y_real}")

            y_inicio += janela - sobreposicao

        cortes = sorted(set(cortes))

        return cortes

    def cortar(self, caminho_imagem, pasta_saida):

        os.makedirs(pasta_saida, exist_ok=True)

        imagem = Image.open(caminho_imagem)

        largura, altura = imagem.size

        cortes = self.encontrar_questoes(caminho_imagem)

        if len(cortes) == 0:
            print("Nenhuma questão encontrada.")
            return

        print(f"Foram encontradas {len(cortes)} questões.")

        inicio = 0

        contador = 1

        for corte in cortes:

            if corte <= inicio + 100:
                continue

            parte = imagem.crop((0, inicio, largura, corte))

            parte.save(
                os.path.join(
                    pasta_saida,
                    f"parte_{contador:03d}.png"
                )
            )

            print(f"Salvo parte_{contador:03d}.png")

            contador += 1

            inicio = corte

        parte = imagem.crop((0, inicio, largura, altura))

        parte.save(
            os.path.join(
                pasta_saida,
                f"parte_{contador:03d}.png"
            )
        )

        print(f"Salvo parte_{contador:03d}.png")
        print(f"{contador} imagens geradas.")


if __name__ == "__main__":

    caminho = "colunas_concatenadas_verticalmente.png"

    pasta = "questoes_colunas"

    divisor = DivisorQuestoesOCR()

    divisor.cortar(caminho, pasta)
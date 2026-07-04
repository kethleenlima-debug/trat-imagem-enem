from pathlib import Path
from PIL import Image


class AparadorDeImagens:

    def __init__(
        self,
        pasta_entrada="questoes",
        pasta_saida="finalizadas",
        limite_branco=245,
        porcentagem_branca=0.995,
        margem=8
    ):

        self.pasta_entrada = Path(pasta_entrada)
        self.pasta_saida = Path(pasta_saida)

        self.limite_branco = limite_branco
        self.porcentagem_branca = porcentagem_branca
        self.margem = margem

        self.pasta_saida.mkdir(parents=True, exist_ok=True)

    def listar_imagens(self):

        return sorted(
            self.pasta_entrada.glob("*.png")
        )

    def linha_eh_branca(self, pixels, largura, y):

        quantidade = 0

        for x in range(largura):

            r, g, b = pixels[x, y][:3]

            if (
                r >= self.limite_branco
                and g >= self.limite_branco
                and b >= self.limite_branco
            ):
                quantidade += 1

        return (
            quantidade / largura
        ) >= self.porcentagem_branca

    def encontrar_limite(self, imagem):

        largura, altura = imagem.size

        pixels = imagem.load()

        for y in range(altura - 1, -1, -1):

            if not self.linha_eh_branca(
                pixels,
                largura,
                y
            ):
                return min(
                    y + self.margem,
                    altura
                )

        return altura

    def aparar_imagem(self, caminho):

        imagem = Image.open(caminho)

        limite = self.encontrar_limite(imagem)

        imagem = imagem.crop(
            (
                0,
                0,
                imagem.width,
                limite
            )
        )

        destino = self.pasta_saida / caminho.name

        imagem.save(destino)

        print(f"✓ {caminho.name}")

    def executar(self):

        imagens = self.listar_imagens()

        if not imagens:
            print("Nenhuma imagem encontrada.")
            return

        print(f"{len(imagens)} imagens encontradas.\n")

        for imagem in imagens:
            self.aparar_imagem(imagem)

        print("\nProcessamento concluído.")


if __name__ == "__main__":

    aparador = AparadorDeImagens(
        pasta_entrada="questoes",
        pasta_saida="finalizadas"
    )

    aparador.executar()
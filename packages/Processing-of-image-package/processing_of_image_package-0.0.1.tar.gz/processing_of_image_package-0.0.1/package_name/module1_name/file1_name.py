from PIL import Image, ImageFilter

def aplicar_filtro_blur(caminho_imagem, caminho_salvar):
    # Abrir uma imagem
    imagem = Image.open(caminho_imagem)

    # Aplicar um filtro
    imagem_filtrada = imagem.filter(ImageFilter.BLUR)

    # Salvar a imagem processada
    imagem_filtrada.save(caminho_salvar)


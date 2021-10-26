#===============================================================================
# Autores: Eduarda Simonis Gavião (RA: 1879472), Willian Rodrigo Huber(RA: 1992910)
# Universidade Tecnológica Federal do Paraná
#===============================================================================

#importando bibliotecas
import numpy as np
import cv2
from PIL import Image

#importando a imagem
INPUT_IMAGE =  'cafe.jpg'

#passando os parametros da janela
ALTURA= 5
LARGURA= 5

#===================================================================
#===================Algoritmo Ingenuo===============================
#===================================================================
#Filtro da média ingenuo 
def ingenuo (img,h,w):
    #pega as dimensões da imagem (linhas, colunas)
    row,col,_= img.shape
    #cria uma cópia de img
    copia = img.copy()

    # primeiro e segundo laço pra percorrer a imagem 
    for y in range (row):
            for x in range (col):
                soma=0;
                #verifica se é a borda da imagem
                if (y - h//2) < 0 or (y + h//2 + 1) >= row or (x - w//2) < 0 or (x + w//2 + 1)  >= col:
                    copia[y][x] = img[y][x]
                else:
                    # laços para percorrer janela deslizante de altura h e largura w
                    for i in range ((y - h//2),(y + h//2) +1 ):
                        for j in range ((x - w//2),(x + w//2) +1 ):
                            soma+=img[i][j]
                        
                    copia[y][x]= soma/(w*h)
    
    return copia

#===================================================================
#===================Algoritmo Separavel=============================
#===================================================================
#Filtro da Média separavel sem reaproveitar somas 
def separavel(img,h,w):
    #pega as dimensões da imagem (linhas, colunas)
    row,col,_= img.shape
    #cria uma cópia de img
    copia = img.copy()
#borra horizontal 
# primeiro e segundo laço pra percorrer a imagem 
    for y in range (row):
            for x in range (col):
                soma=0;
                #verifica se é a borda da imagem
                if(y-h//2)<=0 or (y+ h//2+1)>= row:
                    copia[y][x]= img[y][x]
                else:
                     #segundo laço pra percorrer a janela
                    for i in range((y - (h//2)), (y + (h//2) + 1)):
                        soma = soma + img[i][x]
                    copia[y][x] = soma/h

    #cria um buffer pra fazer as médias das médias horizontais 
    buffer = copia.copy()
   
   #borra vertical
   # primeiro e segundo laço pra percorrer a imagem 
    for y in range (row):
            for x in range (col):
                soma=0;
                #verifica se é a borda da imagem
                if(x-w//2)<=0 or (x+ w//2+1)>= col:
                    copia[y][x]= buffer[y][x]
                else:
                    #segundo laço pra percorrer a janela
                    for j in range((x - (w//2)), (x + (w//2) + 1)):
                     soma = soma + buffer[y][j]
                    copia[y][x] = soma/w
    
    
    return copia

#===================================================================
#===================Algoritmo Imagens Integrais=====================
#===================================================================
#Filtro da Média utilizando de imagens integrais
def integral (img,h,w):
    #pega as dimensões da imagem (linhas, colunas)
    row, col, _ = img.shape
    #cria uma cópia de img
    img_copy = img.copy()

 #processo de criação da imagem integral
    for y in range(0,row):
        soma=0
        for x in range(1, col):
            soma+=img[y][x]
            img_copy[y][x] = soma

            if y> 0:
                img_copy[y][x]+=img_copy[y-1][x]

    #cria imagem de saída
    saida = img_copy.copy() 
    alt=h
    lag=w
    #processo para realização das somas
    for y in range(row):
            for x in range(col):
                #verifica se é a borda da imagem
                if (y - h//2) < 0 or (y + h//2 + 1) > row or (x - w//2) < 0 or (x + w//2 + 1)  > col:
                    #diminui o tamanho da janela
                    alt= alt - 2
                    lag= lag - 2
                    #verifica se o tamanho da janela é igual a (1x1)
                    if alt <=3 or lag <=3:
                        alt= alt + 2
                        lag= lag + 2
                    min_row, max_row = max( 0, y-alt//2), min( row-1, y+alt//2)
                    min_col, max_col = max( 0, x-lag//2), min( col-1, x+lag//2)
                #definições de minimos e máximos para cálculo das somas
                else:
                    min_row, max_row = max( 0, y-h//2), min( row-1, y+h//2)
                    min_col, max_col = max( 0, x-w//2), min( col-1, x+w//2)
                
                #soma das regiões
                saida[y][x] = img_copy[max_row][max_col]
                if min_row > 0:
                    saida[y][x] -= img_copy[min_row-1][max_col]

                if min_col > 0:
                    saida[y][x] -= img_copy[max_row][min_col-1]
                            
                if min_col > 0 and min_row > 0:
                    saida[y][x] += img_copy[min_row-1][min_col-1]

    return saida/(h*w) #dividindo a soma pelo tamanho da janela 

   

    

#------------------------------------------------------------------
def main ():

    img = cv2.imread (INPUT_IMAGE, cv2.IMREAD_COLOR) #abre a imagem

    img = img.astype(np.float32) / 255

    #faz o teste utilizando o comando do openCV para verificar
    ksize=(LARGURA,ALTURA)
    cv2_img = cv2.blur(img,ksize)
    cv2.imshow('01_OPENCV_MEDIA', cv2_img)
    cv2.imwrite('01_OPENCV_MEDIA.png', cv2_img*255)

    #chamada da função que executa o filtro da média ingenuo
    ingenuo_img= ingenuo(img,ALTURA,LARGURA)
    cv2.imshow('01_INGENUO', ingenuo_img)
    cv2.imwrite('01_INGENUO.png', ingenuo_img*255)

    #chamada da função que executa o filtro da média separável sem reaproveitar somas
    sep_img=separavel(img,ALTURA,LARGURA)
    cv2.imshow('01_SEPARAVEL', sep_img)
    cv2.imwrite('01_SEPARAVEL.png', sep_img*255)
    
    #chamada da função que executa o filtro da média com imagens integrais
    integra_img= integral(img,ALTURA,LARGURA)
    cv2.imshow('01_INTEGRAL', integra_img)
    cv2.imwrite('01_INTEGRAL.png', integra_img*255)

    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

#------------------------------------------------------------------
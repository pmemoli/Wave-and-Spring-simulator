import pygame

# TODO: agarrar la casilla verdadera sin aproximar la aproximacion lol

def punto_mas_proximo(valor, lista):  # Variacion de binary search
    # Sortea la lista de menor a mayor de ser necesario
    if lista[0][0] > lista[-1][0]:
        lista.sort()

    i = 0
    j = len(lista) - 1

    encontrado = False
    while i <= j and not encontrado:
        mid = (i + j) // 2

        if lista[mid][0] == valor:
            encontrado = True

        elif lista[mid][0] < valor:
            i = mid + 1

        else:
            j = mid - 1

    return lista[mid]  # lista[mid] esta como mucho a una casilla del valor real

def draw_line(screen, start, end, color):
    pygame.draw.line(screen, color, start, end, 4)

def block_selection(block_list):  # Returns first_block, last_block
    if block_list[0].center[0] > block_list[-1].center[0]:
        return block_list[-1], block_list[0]
    else:
        return block_list[0], block_list[-1]

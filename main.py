import pygame
import random


def main() :
    pygame.init()

    # création de la map
    map = generateMap()

    # création de la fenetre
    fenetre = pygame.display.set_mode((800, 600))

    # import cow/ grass
    cow = pygame.image.load("src/cow.png")
    grass = pygame.image.load("src/grass.png")

    en_cours = True
    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    # pause
                    pause = True
                    while pause:
                        for event_pause in pygame.event.get():
                            if event_pause.type == pygame.KEYDOWN:
                                if event_pause.key == pygame.K_p:
                                    pause = False
                if event.key == pygame.K_n:
                    # new
                    map = generateMap()
        
        # affiche map
        displayMap(map, fenetre, cow, grass)

        # avance de 1 l'itération
        nextIter(map)

        # vérifie si on a que de l'herbe
        if(checkIfOnlyGrass(map)) :
            # on regenere la map
            map = generateMap()
        
    pygame.quit()

def checkIfOnlyGrass(map) :
    """
    Vérifie si il n'y a que de l'herbe
    """

    for y in range(len(map)) :
        for x in range(len(map[0])) :
            if map[y][x] != 1 :
                return False
    return True

def nextIter(map) :
    """
    Fait un pas dans l iteration
    """
    for y in range(len(map)) :
        for x in range(len(map[0])) :
            freePlace = checkFreePlace(map, y, x)
            direction = random.randint(0, 3)

            if(freePlace[direction]) :
                # si libre
                if(isinstance(map[y][x], Cow)) :
                    # si vache
                    currentCow = map[y][x]

                     # si peut faire un enfant on fait un enfant
                    if(currentCow.canMakeBaby()) :
                        freePlaceBaby = checkFreePlace(map, y, x)
                        directionBaby = random.randint(0, 3)
                        if(freePlaceBaby[directionBaby]) : 
                            chanegMap(True, map, y, x, directionBaby, Cow())

                    currentCow.reduceEnergie()

                    if(currentCow.noEnergie()) :
                        # si plus d energie
                        map[y][x] = 0
                    else :
                        chanegMap(True, map, y, x, direction, currentCow)

                if map[y][x] == 1 :
                    # si herbe proba 1/4 de faire de l'herbe
                    change = random.randint(0, 3)
                    if (change == 0) :
                        chanegMap(False, map, y, x, direction, None)

def chanegMap(cow, map, y, x, direction, currentCow) :
    """
    Change la map pour la direction et l'item
    """
    if(cow == False) :
        if(direction == 0) :
            # haut
            map[y-1][x] = 1
        
        if(direction == 1) :
            # droite
            map[y][x+1] = 1

        if(direction == 2) :
            # bas
            map[y+1][x] = 1
        
        if(direction == 3) :
            # gauche
            map[y][x-1] = 1
    
    if(cow == True) :
        if(direction == 0) :
            # haut
            if(map[y-1][x] == 1) :
                currentCow.increaseEnergie()
            map[y-1][x] = currentCow
        
        if(direction == 1) :
            # droite
            if(map[y][x+1] == 1) :
                currentCow.increaseEnergie()
            map[y][x+1] = currentCow

        if(direction == 2) :
            # bas
            if(map[y+1][x] == 1) :
                currentCow.increaseEnergie()
            map[y+1][x] = currentCow
        
        if(direction == 3) :
            # gauche
            if(map[y][x-1] == 1) :
                currentCow.increaseEnergie()
            map[y][x-1] = currentCow

        map[y][x] = 0

def checkFreePlace(map, y, x) :
    """
    Renvoie une liste nous disant si on a une place de libre autour
    la liste serra de ce style : [Haut, Droite, Bas, Gauche]
    """
    
    checkedList = [False, False, False, False]

    # haut
    if(y != 0) :
        if(map[y-1][x] == 0 or map[y-1][x] == 1) :
            checkedList[0] = True
    
    # droite
    if(x != len(map[0])-1) :
        if(map[y][x+1] == 0 or map[y][x+1] == 1) :
            checkedList[1] = True
    
    # bas
    if(y != len(map)-1) :
        if(map[y+1][x] == 0 or map[y+1][x] == 1) :
            checkedList[2] = True
    
    # gauche
    if(x != 0) :
        if(map[y][x-1] == 0 or map[y][x-1] == 1) :
            checkedList[3] = True

    return checkedList

def displayMap(map, fenetre, cow, grass) :
    """
    Affiche la map
    """

    # efface
    fenetre.fill((0, 0, 0))

    for y in range(len(map)) :
        for x in range(len(map[0])) :
            if isinstance(map[y][x], Cow) :
                fenetre.blit(cow, (x*5, y*5))
            if map[y][x] == 1 :
                fenetre.blit(grass, (x*5, y*5)) 

    pygame.display.flip()

def generateMap() :
    """
    Genere la map
    """

    map = []
    for i in range(120) :
        subMap = []
        for j in range(160) :
            subMap.append(generateItem())
        map.append(subMap)

    return map

def generateItem() :
    """
    Genere un item à mettre : une vache, de l'herbe ou rien
    """

    randNum = random.randint(1, 100)
    
    if (randNum == 1) :
        # 1 % vaches
        return Cow()
    
    if (randNum > 10 and randNum <= 40) :
        # 30 % herbes
        return 1
    
    return 0


class Cow:
    def __init__(self):
        self.energie = 2

    def canMakeBaby(self):
        if(self.energie >= 2) :
            return True
        return False
    
    def reduceEnergie(self):
        self.energie = self.energie - 1
    
    def noEnergie(self) : 
        if(self.energie <= 0) :
            return True
        else :
            return False

    def increaseEnergie(self):
        self.energie = self.energie + 2

main()
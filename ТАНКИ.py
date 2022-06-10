from tkinter import *

# Загрузка данных карты
def getMap(lvl):
    global dataMap, bulletMap
    print("Метод getMap()")

    bulletMap = []
    dataMap = []
    tmp = []

    idx = str(lvl)
    if (lvl < 10):
        idx = f"0{lvl}"
    try:
        f = open(f"levels/level{idx}.dat", "r", encoding="utf-8")
        for i in f.readlines():
            tmp.append(i.replace("\n", ""))
            f.close()
            
        for i in range(len(tmp)):
            dataMap.append([])
            bulletMap.append([])
            for j in tmp[i]:                
                dataMap[i].append(int(j))
                bulletMap[i].append(0)
                # bulletMap заполняем 0-ми чтоб потом отметить 1-ми только стены,
                # вода и лес будут 0-ми для снаряда
    except:
        print("Ненайден файл с данными.")
        quit(0)
            
    

# Залить фон
def clear_setBG():
    print("Метод clear_setBG()")
    cnv.delete(ALL)
    for i in range(WIDTH_M):
        for j in range(HEIGHT):
            cnv.create_image(TILE // 2 + i * TILE,
                             TILE // 2 + j * TILE, image=img[0][2])
    

# Создание обьектов Canvas и списков
def createMap():
    print("Метод createMap()")
    global dataMap, bulletMap, forest, wall, players

    getMap(level)
    
    forest = []
    wall = []
    players = []

    # Танк игрока
    players.append([24, 9,
                    cnv.create_image((WIDTH_M // 2 - 3) * TILE,
                                     HEIGHT * TILE - TILE, image=img[6][0])])

    # Орёл верхний
    players.append([0, 12,
                    cnv.create_image((WIDTH_M // 2) * TILE, TILE, image=img[5][0])])
    # Орёл нижний
    players.append([24, 12,
                    cnv.create_image((WIDTH_M // 2) * TILE,
                                     (HEIGHT * TILE) - TILE, image=img[5][0])])
    

    for i in range(len(dataMap)):
        for j in range(len(dataMap[i])):

            # Пусто, добавляем в dataMap параметр проверки на лес
            if (dataMap[i][j] == 0):
                dataMap[i][j] = [0, 0]
                
            # Кирпич, добавляем параметр проверки на сталь ("жизни" кирпича)
            if (dataMap[i][j] == 1):
                bulletMap[i][j] = 1
                dataMap[i][j] = [1, 0, cnv.create_image(TILE // 2 + j * TILE,
                                                        TILE // 2 + i * TILE, image=img[1][2])] 
                # Список: Стены
                #wall.append([i, j, cnv.create_image(TILE // 2 + j * TILE, TILE // 2 + i * TILE, image=img[1][2])])
            # Сталь, добавляем "жизни"
            elif (dataMap[i][j] == 3):
                bulletMap[i][j] = 1
                dataMap[i][j] = [1, 2, cnv.create_image(TILE // 2 + j * TILE,
                                                        TILE // 2 + i * TILE, image=img[3][2])]
                # Список: Стены
                #wall.append([i, j, cnv.create_image(TILE // 2 + j * TILE, TILE // 2 + i * TILE, image=img[3][3])])
            # Лес : прорисовывается НАД ТАНКАМИ И СНАРЯЛАМИ !!!!
            elif (dataMap[i][j] == 2):
                dataMap[i][j] = [0, 1]
                # Список: Лес
                forest.append([i, j, cnv.create_image(TILE // 2 + j * TILE,
                                                      TILE // 2 + i * TILE,
                                                      image=img[2][0])])
            # Вода
            elif (dataMap[i][j] == 4):
                # Неуничтожаемое препятствие НО ПРОПУСКАЕТ СНАРЯДЫ !!!!
                dataMap[i][j] = [1, 5]
                cnv.create_image(TILE // 2 + j * TILE,
                                 TILE // 2 + i * TILE,
                                 image=img[4][2])

    print(wall)
    #lookMap()
                
# Вывод карты в консоль
def lookMap():
    for i in range(len(dataMap)):
        print(dataMap[i])
                              

    #test()
# Проба текстур
def test():
    for i in range(3):
        for j in range(10):
            cnv.create_image((TILE // 2) + (TILE * 4) + j * TILE,
                             (TILE // 2) + (TILE * 5) + i * TILE,
                             image=img[1][0])
    for i in range(3):
        for j in range(10):
            cnv.create_image((TILE // 2) + (TILE * 4) + j * TILE,
                             (TILE // 2) + (TILE * 10) + i * TILE,
                             image=img[1][1])

    for i in range(3):
        for j in range(10):
            cnv.create_image((TILE // 2) + (TILE * 4) + j * TILE,
                             (TILE // 2) + (TILE * 15) + i * TILE,
                             image=img[1][2])

    for i in range(3):
        for j in range(10):
            cnv.create_image((TILE // 2) + (TILE * 4) + j * TILE,
                             (TILE // 2) + (TILE * 20) + i * TILE,
                             image=img[1][3])

# Метод перерисовывающий лес после перерисовки танка или выстрела
# чтобы обьекты двигались под лесом
def makeForest(x):
    global inForest
    print("Метод makeForest()")
    
    for i in range(len(forest)):
        x = forest[i][1]
        y = forest[i][0]
        cnv.delete(forest[i][2])
        forest[i][2] = cnv.create_image(TILE // 2 + x * TILE,
                                        TILE // 2 + y * TILE, image=img[2][0])
    if (x > 0):
        inForest = True


# Футкция принимает последовательность нажатия клавиш и возвращающает:
# True, если направление танка меняется и False если нет
def changeVector(v):
    global keyList
    keyList[0] = keyList[1]
    keyList[1] = v

    if (keyList[0] != keyList[1]):
        return True
    else:
        return False
# ========================= УПРАВЛЕНИЕ И ДВИЖЕНИЕ ==============================
# Анимация танка
def moveTankTo(x, y, count):
    global moving
    count -= 1
    cnv.move(players[0][2], x, y)

    if (count > 0):
        moving = True
        cnv.after(20, lambda x=x, y=y, c=count: moveTankTo(x, y, c))
    else:
        print("Метод moveTankTo() выполнился")

        moving = False
        
    
# Движение танка
def move(v):
    check0 = changeVector(v)
    
    global vector, inForest

    x = players[0][0]
    y = players[0][1]    

    # Проверяем находится ли танк все ещё в лесу, если нет: inForest = False
    if (inForest):
        if (dataMap[x][y][1] + dataMap[x][y + 1][1] +
            dataMap[x + 1][y][1] + dataMap[x + 1][y + 1][1] == 0):
            inForest = False
    
    if (moving):
        return 0
    print("Метод move(x)")

    if (check0):
        cnv.delete(players[0][2])   
        players[0][2] = cnv.create_image((players[0][1] * TILE) + TILE,
                                     (players[0][0] * TILE) + TILE, image=img[6][v])
    
        if (inForest):
            makeForest(1)
    # Перерисовываем лес
    #makeForest()
    

    if (v == UPKEY):
        vector = UPKEY
        check = getNumber(x - 1, y, v)
        if (check == 1):
            print("up")
            moveTankTo(0, -speed, step)
            players[0][0] -= 1
    if (v == DOWNKEY):
        vector = DOWNKEY
        check = getNumber(x + 1, y, v)
        if (check == 1):
            print("down")
            moveTankTo(0, speed, step)
            players[0][0] += 1
    if (v == LEFTKEY):
        vector = LEFTKEY
        check = getNumber(x, y - 1, v)
        if (check == 1):
            print("left")
            moveTankTo(-speed, 0, step)
            players[0][1] -= 1
    if (v == RIGHTKEY):
        vector = RIGHTKEY
        check = getNumber(x, y + 1, v)
        if (check == 1):
            print("right")
            moveTankTo(speed, 0, step)
            players[0][1] += 1

# Проверка места для движения
def getNumber(x, y, v):
    print("Метод getNumber")
    print(x, y)
    
    if (v == UPKEY and x >= 0):
        if ((dataMap[x][y][0] + dataMap[x][y + 1][0]) == 0):
            if (dataMap[x][y][1] + dataMap[x][y + 1][1] != 0):
                makeForest(1)
            return 1
        else:
            return 0
    elif (v == DOWNKEY and x < 25):
        if ((dataMap[x + 1][y][0] + dataMap[x + 1][y + 1][0]) == 0):
            if (dataMap[x + 1][y][1] + dataMap[x + 1][y + 1][1] != 0):
                makeForest(1)
            return 1
        else:
            return 0
    elif (v == LEFTKEY and y >= 0):
        #print(f"data[x][y]: {dataMap[x][y]} data[x + 1][y]: {dataMap[x + 1][y]}")
        if ((dataMap[x][y][0] + dataMap[x + 1][y][0]) == 0):
            if (dataMap[x][y][1] + dataMap[x + 1][y][1] != 0):
                makeForest(1)
            return 1
        else:
            return 0
    elif (v == RIGHTKEY and y < 25):
        #print(f"data[x][y]: {dataMap[x][y]} data[x + 1][y]: {dataMap[x + 1][y]}") 
        if ((dataMap[x][y][0] + dataMap[x + 1][y + 1][0]) == 0):
            if (dataMap[x][y][1] + dataMap[x + 1][y + 1][1] != 0):
                makeForest(1)
            return 1
        else:
            return 0
            
# Создание выстрела
def shot(event):
    global sh, bullet, ex
    ex = cnv.create_image(10 * TILE, 10 * TILE, image=explode[0])
    
    print("Метод shot()")
    if (shoo):
        return 0
    
    # ВЫКЛЮЧЕНИЕ КЛАВИШИ ВЫСТРЕЛА
    cnv.unbind("<space>")
    x = players[0][0]
    y = players[0][1]
    
    # Координаты анимации относительно танка
    xSh = 0
    ySh = 0
    n = 0          # Направление анимации

    if (vector == UPKEY):
        xSh = x
        ySh = y + 1
        n = 0
    elif (vector == DOWNKEY):
        xSh = x + 2
        ySh = y + 1
        n = 1
    elif (vector == LEFTKEY):
        xSh = x + 1
        ySh = y
        n = 2
    elif (vector == RIGHTKEY):
        xSh = x + 1
        ySh = y + 2
        n = 3
        
    sh = cnv.create_image(y * TILE, x * TILE, image=anim[0][0])

    # Создание снаряда
    bullet = cnv.create_image(ySh * TILE, xSh * TILE, image=bull)

    # Расчёт полёта снаряда
    calculatBullet(xSh, ySh)
    #print(xSh, ySh)

    
    # Анимация выстрела
    shotAnime(xSh, ySh, n, 0)
  

# Тест-------------------------------------------------
def explodeAnime(x, y, a):
    global ex
    cnv.delete(ex)
    a += 1
    ex = cnv.create_image(x, y, image=explode[a])

    if (a < 6):
        cnv.after(50, lambda x=x, y=y, a=a: explodeAnime(x, y, a))
    else:
        cnv.after_cancel(explodeAnime)
        cnv.delete(ex)

        
        # Включаем клавишу выстрела
        cnv.bind("<space>", shot)
        destroyWall(destroy)
    
    
    
# Анимация выстрела
def shotAnime(x, y, n, a):
    global sh  
    shoo = True
    cnv.delete(sh) 
    
        
    a += 1
    sh = cnv.create_image(y * TILE, x * TILE, image=anim[n][a])
    
    if (a < 3):
        cnv.after(30, lambda x=x, y=y, n=n, a=a: shotAnime(x, y, n, a))
    else:
        cnv.after_cancel(shotAnime)
        cnv.delete(sh)
        
        


# Расчёт полёта снаряда
def calculatBullet(x, y):
    global destroy
    
    print("Метод calculateBullet()")
    print(x, y)

    # Координаты начала выстрела (нулевая точка для отсчёта места взрыва)
    xExp = x
    yExp = y

    # Индикатор наличия леса на пути снаряда
    l = False
    
    count = 0
    y -= 1
    if (vector == UPKEY):
        while (sum(bulletMap[x][y:y + 2]) == 0 and x >= 0):
            # Проверяем лес
            if ((dataMap[x][y][1] or dataMap[x][y + 1][1]) == 1):
                l = True
                
            x -= 1
            count += 1
        count -= 1
        
        print()
        print()
        print(x, y, bulletMap[x][y])
        print()
        print()
        print(x, y + 1, bulletMap[x][y + 1])
        print()
        print()
        print(count)
        ex = cnv.create_image(yExp * TILE, (xExp - count) * TILE, image=explode[0])
        # Забиваем координаты в destroy список
        destroy = [[x, y], [x, y + 1]]
        
    elif (vector == DOWNKEY):
        
        while (x < 25 and sum(bulletMap[x][y:y + 2]) == 0): 

            if ((dataMap[x][y][1] or dataMap[x][y + 1][1]) == 1):
                l = True
            
            x += 1
            count += 1
        
        if (x == 25 and (bulletMap[x][y] and bulletMap[x][y]) == 0):   # Компенсируем низ карты
            count += 1
            
        if (x <= 25):
            print()
            print(x, y, bulletMap[x][y])
            print()
            print()
            print(x, y + 1, bulletMap[x][y + 1])
            print()
            print()
            print(count)

        ex = cnv.create_image(yExp * TILE, (xExp + count) * TILE, image=explode[0])
        destroy = [[x, y], [x, y + 1]]

    elif (vector == LEFTKEY):
        while (y >= 0 and (bulletMap[x][y] + bulletMap[x - 1][y]) == 0):
            if ((dataMap[x][y][1] or dataMap[x - 1][y][1]) == 1):
                l = True
            y -= 1
            count += 1
        print()
        print()
        print(x, y, bulletMap[x][y])
        print()
        print()
        print(x - 1, y, bulletMap[x - 1][y])
        print()
        print()
        print(count)
        
        ex = cnv.create_image((yExp - count) * TILE, xExp * TILE, image=explode[0])
        destroy = [[x, y], [x - 1, y]]

    elif (vector == RIGHTKEY):
        while (y < 25 and (bulletMap[x][y] + bulletMap[x - 1][y]) == 0):
            if ((dataMap[x][y][1] or dataMap[x - 1][y][1]) == 1):
                l == True
            y += 1
            count += 1
        count -= 1
        
        if (y == 25 and (bulletMap[x][y] and bulletMap[x - 1][y]) == 0):      # Компенсируем правую сторону
            count += 1
        print()
        print()
        print(x, y, bulletMap[x][y])
        print()
        print()
        print(x - 1, y, bulletMap[x - 1][y])
        print()
        print()
        print(count)
        ex = cnv.create_image((yExp + count) * TILE, xExp * TILE, image=explode[0])
        destroy = [[x, y], [x - 1, y]]
        


    #print(destroy)
    if (l):               # Если по траектории лес, перерисовываем
        makeForest(0)

    v = vector
    count *= 5
    bulletAnime(v, count)

    

# Анимация полёта снаряда
def bulletAnime(v, count):
    global bull, shoo
    
    #print("count", count)
    if (v == UPKEY):        
        cnv.move(bullet, 0, -bullSpeed)
    elif (v == DOWNKEY):
        cnv.move(bullet, 0, bullSpeed)
    elif (v == LEFTKEY):
        cnv.move(bullet, -bullSpeed, 0)
    elif (v == RIGHTKEY):
        cnv.move(bullet, bullSpeed, 0)
        
    if (count > 0):
        count -= 1
        cnv.after(20, lambda v=v, c=count: bulletAnime(v, c))    
        
    else:
        cnv.after_cancel(bulletAnime)

        #print(cnv.coords(bullet))

        

        # Передаём координаты финиша снаряда и счётчик в
        # метод анимации взрыва снаряда
        x = cnv.coords(bullet)[0]
        y = cnv.coords(bullet)[1]
        explodeAnime(x, y, 0)

        cnv.delete(bullet)

        # Включаем возможность выстрела
        shoo = False

# Метод разрушения стен
def destroyWall(d):
    global dataMap, bulletMap
    x = d[0][0]
    y = d[0][1]
    x1 = d[1][0]
    y1 = d[1][1]
    if (x > 25):
        x = 25
    destroyCount(x, y)
    destroyCount(x1, y1)
        
# Дестрой
def destroyCount(x, y):
    global dataMap, bulletMap
    
    if (dataMap[x][y][0] == 1):
        if (dataMap[x][y][1] == 0):
            cnv.delete(dataMap[x][y][2])
            dataMap[x][y][0] = 0
            bulletMap[x][y] = 0
        elif (dataMap[x][y][1] == 2):
            dataMap[x][y][1] -= 1
            cnv.delete(dataMap[x][y][2])
            dataMap[x][y][2] = cnv.create_image(TILE // 2 + y * TILE,
                                                TILE // 2 + x * TILE, image=img[3][3])
            
            
        elif (dataMap[x][y][1] == 1):
            dataMap[x][y][1] = 0
            cnv.delete(dataMap[x][y][2])
            dataMap[x][y][2] = cnv.create_image(TILE // 2 + y * TILE,
                                                TILE // 2 + x * TILE, image=img[1][2])
                                                
      
   

            
    cnv.update()
            
    
        
    
# ================================== ПОЛЕ ==========================================
root = Tk()
root.resizable(False, False)
root.title("Танки 0.1 (beta)")
root.iconbitmap("icon/ico.ico")

WIDTH = 30
HEIGHT = 26
TILE = 40

#Ширина игрового поля в тайлах
WIDTH_M = 26

POS_X = root.winfo_screenwidth() // 2 - (WIDTH * TILE) // 2
POS_Y = (root.winfo_screenheight() // 2 - (HEIGHT * TILE) // 2) - 20
root.geometry(f"{WIDTH * TILE}x{HEIGHT * TILE}+{POS_X}+{POS_Y}")

# КАНВАС
cnv = Canvas(root, width=WIDTH_M * TILE, height=HEIGHT * TILE, bg="#373737")
cnv.config(highlightthickness=0)
cnv.place(x=0, y=0)
cnv.focus_set()

# =============================== ПЕРЕМЕННЫЕ ===================================
# Карта для расчаёта полёта пули
bulletMap = None

# Анимация выстрела идёт?
shoo = False

# Скорость снаряда
bullSpeed = 8


# Математическая модель карты
dataMap = None

# Танки и орлы
players = []

# Карта леса
forest = None

# Танк в лесу?
inForest = False

# Список хранящий последовательность нажатий клавиш
keyList = [5, 0]

# Карта разрушаемых стен (кирпича и стали)
wall = None

# Список с координатами 2-х тайлов попавших под взрыв
destroy = [0, 0, 0, 0]


# Уровень
level = 2

# коды клавиш
UPKEY = 0
DOWNKEY = 1
LEFTKEY = 2
RIGHTKEY = 3

# Танк едет?
moving = False

# В какую сторону смотрит танк?
vector = UPKEY

# Скорость танка
speed = 5

# Шаг танка
step = 8                       
                      

# =============================== КНОПКИ =======================================
cnv.bind("<Up>", lambda e, x=UPKEY: move(x))
cnv.bind("<Down>", lambda e, x=DOWNKEY: move(x))
cnv.bind("<Left>", lambda e, x=LEFTKEY: move(x))
cnv.bind("<Right>", lambda e, x=RIGHTKEY: move(x))
cnv.bind("<space>", shot)

# =============================== ТЕКСТУРЫ =====================================

# Список обьектов карты
img = []

# Земля 2
img.append([])
img[0].append(PhotoImage(file="image/earth/er.png"))
img[0].append(PhotoImage(file="image/earth/er1.png"))
img[0].append(PhotoImage(file="image/earth/er2.png"))
img[0].append(PhotoImage(file="image/earth/er3.png"))
img[0].append(PhotoImage(file="image/earth/er5.png"))

# Стены 2
img.append([])
img[1].append(PhotoImage(file="image/wall/wall.png"))
img[1].append(PhotoImage(file="image/wall/wall1.png"))
img[1].append(PhotoImage(file="image/wall/wall2.png"))
img[1].append(PhotoImage(file="image/wall/wall3.png"))

# Лес 3
img.append([])
img[2].append(PhotoImage(file="image/forest/forest.png"))
img[2].append(PhotoImage(file="image/forest/forest1.png"))
img[2].append(PhotoImage(file="image/forest/forest2.png"))
img[2].append(PhotoImage(file="image/forest/forest3.png"))
img[2].append(PhotoImage(file="image/forest/forest4.png"))

# Сталь 3
img.append([])
img[3].append(PhotoImage(file="image/stell/stell.png"))
img[3].append(PhotoImage(file="image/stell/stell1.png"))
img[3].append(PhotoImage(file="image/stell/stell2.png"))
img[3].append(PhotoImage(file="image/stell/stell3.png"))

# Вода 1
img.append([])
img[4].append(PhotoImage(file="image/water/wat.png"))
img[4].append(PhotoImage(file="image/water/wat1.png"))
img[4].append(PhotoImage(file="image/water/wat2.png"))
img[4].append(PhotoImage(file="image/water/wat3.png"))

# Орлы
img.append([])
img[5].append(PhotoImage(file="image/eagle/eag.png"))
img[5].append(PhotoImage(file="image/eagle/eag1.png"))
img[5].append(PhotoImage(file="image/eagle/eag2.png"))

# Танки
img.append([])
img[6].append(PhotoImage(file="image/tanks/tU.png"))
img[6].append(PhotoImage(file="image/tanks/tD.png"))
img[6].append(PhotoImage(file="image/tanks/tL.png"))
img[6].append(PhotoImage(file="image/tanks/tR.png"))

# Анимация эффектов
anim = []

# Выстрел
for i in range(4):
    anim.append([])
    for j in range(4):
        anim[i].append(PhotoImage(file=f"image/shot/{i}/sh{j}.png"))

# Взрыв
explode = []
for i in range(7):
    explode.append(PhotoImage(file=f"image/explode/{i}.png"))
    

# Пуля
bull = PhotoImage(file="image/bull/bullet.png")




clear_setBG()

createMap()

root.mainloop()

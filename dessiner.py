# authors: Tian Cheng Liu 20050130
#          Flora Kang     20239294
# November 1st 2022
# Travail Pratique 1

#TO BE REMOVED BEFORE HANDING IN --------------------------------------------

# codeBoot functions 

def setScreenMode():
    pass

def getScreenWidth():
    pass

def getScreenHeight():
    pass

def setPixel(x,y,color):
    pass

def fillRectangle(x,y,width,height,color):
    pass

def getPixel(x,y):
    pass

def getMouse():
    pass

def exportScreen():
    pass

def sleep(second):
    pass

# class struct allows for python to have structs like in CodeBoot

class struct:
 def __init__(self, **fields):
    self.__dict__.update(fields)
 def __repr__(self):
    return 'struct('+(', '.join(list(map(lambda f:f+'='+repr(self.__dict__[f]),
                                         self.__dict__))))+')'

# ----------------------------------------------------------------------------

# createButtons will create a list of buttons with "erase" as the first button
# the following buttons will be the colors in the list "colors".
# parameters:   list colors (the button colors that you want), 
#               value size of the width each square button 
#               value spacing between the buttons 
#               value colorErase is the color to paint over when using "erase"
# output:       list of buttons (structures with corner1, corner2, color, bool)

def createButtons(colors, size, space, colorErase):

    # distance between one corner of one button to the same corner of the next
    corn2corn = space + size  
             
    buttons = []
    buttons.append(struct(corner1 = struct(x = space, y = space), 
                          corner2 = struct(x = corn2corn, y = corn2corn), 
                          color = colorErase, erase = True))
    lengthColors = len(colors)                      
    for i in range(lengthColors):  # from 0 to lengthColors-1
            buttons.append(struct(corner1 = struct(x = buttons[i].corner1.x 
                                                   + corn2corn, y = space), 
                                  corner2 = struct(x = buttons[i].corner2.x + 
                                                   corn2corn, y = corn2corn), 
                                  color = colors[i], erase = False))
    return buttons

# testing createButtons
# print(createButtons(["#f00"], 12, 6, "#fff"))

# the function findButtons will check whether there is a button at the location
# of position
# parameters: list buttons is a list containing struct for each button color
#                          this list is usually created using createButtons
#             position is a struct containing x and y of the position to search
# output: returns the struct of the button at position position.
#         if no button is present, return None

def findButtons(buttons, position):
    for currentButton in buttons:
        if ((currentButton.corner1.x <= position.x <= currentButton.corner2.x) 
            and 
           (currentButton.corner1.y <= position.y <= currentButton.corner2.y)):
            return currentButton
    return None

# testing findButtons
# print(findButtons(createButtons(["#f00"], 12, 6, "#fff"), struct(x=7, y=7)))
# print(findButtons(createButtons(["#f00"], 12, 6, "#fff"), struct(x=5, y=5)))

# the function drawFloatingRectangle loops at every 0.1s to get the position 
# and state of the cursor. As long as the mouse pointer is being held down, a
# floating rectangle is drawn over the start position and the current position.
# If the floating rectangle shrinks, the original image over the shrunken part
# should be restored.
# parameters: originalImage is a list of lists containing the color value of 
#                           each pixel
#             start is a struct with x and y value where the floating rectangle
#                   should start being drawn
#             color is the value of the color the rectangle should take
# output: None, the originalImage value will get changed.

def drawFloatingRectangle(originalImage, start, color):
    imageCopy = originalImage[:][:]

    # position of the previous iteration
    iniPos = struct(x = start.x, y = start.y)
    
    while getMouse().button:           # continue loop while mouse button held
        currentPos = struct(x = getMouse().x, y = getMouse().y)
        if currentPos.y <24:
            currentPos.y = 24
        
        if (iniPos.x == start.x and iniPos.y == start.y):
            rectX = struct(corner1 = struct(x = min(currentPos.x, start.x), 
                                            y = min(currentPos.y,start.y)), 
                           corner2 = struct(x = max(currentPos.x, start.x), 
                                            y = max(currentPos.y, start.y)))
            addRectangle(imageCopy, rectX, color)

        if iniPos.x > start.x and iniPos.y > start.y:
            if currentPos.x == iniPos.x and currentPos.y == iniPos.y:
                pass
            elif currentPos.x <= start.x or currentPos.y <= start.y:
                rectX = struct(corner1 = struct(x = start.x, y = start.y), 
                               corner2 = struct(x = iniPos.x, 
                                                y = iniPos.y))
                restoreImage(originalImage, rectX)
                rectY = struct(corner1 = struct(x = min(currentPos.x, start.x), 
                                                y = min(currentPos.y, 
                                                        start.y)), 
                               corner2 = struct(x = max(currentPos.x, start.x), 
                                                y = max(currentPos.y, 
                                                        start.y)))
                addRectangle(imageCopy, rectY, color)
            elif currentPos.x >= iniPos.x and currentPos.y >= iniPos.y:
                rectX = struct(corner1 = struct(x = iniPos.x, y = start.y), 
                               corner2 = struct(x = currentPos.x, 
                                                y = iniPos.y))
                addRectangle(imageCopy, rectX, color)
                rectY = struct(corner1 = struct(x = start.x, y = iniPos.y), 
                               corner2 = struct(x = currentPos.x, 
                                                y = currentPos.y))
                addRectangle(imageCopy, rectY, color)
            elif currentPos.x >=iniPos.x and currentPos.y <= iniPos.y:
                rectX = struct(corner1 = struct(x = iniPos.x, y = start.y), 
                               corner2 = struct(x = currentPos.x, 
                                                y = currentPos.y))
                addRectangle(imageCopy, rectX, color)
                rectY = struct(corner1 = struct(x = start.x, y = currentPos.y), 
                               corner2 = struct(x = currentPos.x, 
                                                y = iniPos.y))
                restoreImage(imageCopy, rectY)
            elif currentPos.x <= iniPos.x and currentPos.y >= iniPos.y:
                rectX = struct(corner1 = struct(x = currentPos.x, y = start.y), 
                               corner2 = struct(x = iniPos.x, 
                                                y = iniPos.y))
                restoreImage(originalImage, rectX)
                rectY = struct(corner1 = struct(x = start.x, y = iniPos.y), 
                               corner2 = struct(x = currentPos.x, 
                                                y = currentPos.y))
                addRectangle(imageCopy, rectY, color)
            elif currentPos.x <=iniPos.x and currentPos.y <= iniPos.y:
                rectX = struct(corner1 = struct(x = currentPos.x, y = start.y), 
                               corner2 = struct(x = iniPos.x, 
                                                y = currentPos.y))
                restoreImage(originalImage, rectX)  
                rectY = struct(corner1 = struct(x = start.x, y = currentPos.y), 
                               corner2 = struct(x = iniPos.x, 
                                                y = iniPos.y))
                restoreImage(imageCopy, rectY)


        if iniPos.x > start.x and iniPos.y < start.y:
            if currentPos.x == iniPos.x and currentPos.y == iniPos.y:
                pass
            elif currentPos.x <= start.x or currentPos.y >= start.y:
                rectX = struct(corner1 = struct(x = start.x, y = iniPos.y), 
                               corner2 = struct(x = iniPos.x, 
                                                y = start.y))
                restoreImage(originalImage, rectX)
                rectY = struct(corner1 = struct(x = min(currentPos.x, start.x), 
                                                y = min(currentPos.y, 
                                                        start.y)), 
                               corner2 = struct(x = max(currentPos.x, start.x), 
                                                y = max(currentPos.y, 
                                                        start.y)))
                addRectangle(imageCopy, rectY, color)
            elif currentPos.x >= iniPos.x and currentPos.y <= iniPos.y:
                rectX = struct(corner1 = struct(x = iniPos.x, 
                                                y = iniPos.y), 
                               corner2 = struct(x = currentPos.x, y = start.y))
                addRectangle(imageCopy, rectX, color)
                rectY = struct(corner1 = struct(x = start.x, 
                                                y = currentPos.y), 
                               corner2 = struct(x = currentPos.x, 
                                                y = iniPos.y))
                addRectangle(imageCopy, rectY, color)
            elif currentPos.x >= iniPos.x and currentPos.y >= iniPos.y:
                rectX = struct(corner1 = struct(x = iniPos.x, 
                                                y = currentPos.y), 
                               corner2 = struct(x = currentPos.x, y = start.y))
                addRectangle(imageCopy, rectX, color)
                rectY = struct(corner1 = struct(x = start.x, 
                                                y = iniPos.y), 
                               corner2 = struct(x = currentPos.x, 
                                                y = currentPos.y))
                restoreImage(originalImage, rectY)
            elif currentPos.x <= iniPos.x and currentPos.y <= iniPos.y:
                rectX = struct(corner1 = struct(x = currentPos.x, 
                                                y = iniPos.y), 
                               corner2 = struct(x = iniPos.x, y = start.y))
                restoreImage(originalImage, rectX)
                rectY = struct(corner1 = struct(x = start.x, 
                                                y = currentPos.y), 
                               corner2 = struct(x = currentPos.x, 
                                                y = iniPos.y))
                addRectangle(imageCopy, rectY, color)
            elif currentPos.x <= iniPos.x and currentPos.y >= iniPos.y:
                rectX = struct(corner1 = struct(x = currentPos.x, 
                                                y = currentPos.y), 
                               corner2 = struct(x = iniPos.x, y = start.y))
                restoreImage(originalImage, rectX)
                rectY = struct(corner1 = struct(x = start.x, 
                                                y = iniPos.y), 
                               corner2 = struct(x = iniPos.x, 
                                                y = currentPos.y))
                restoreImage(originalImage, rectY)
                
        if iniPos.x < start.x and iniPos.y < start.y:
            if currentPos.x == iniPos.x and currentPos.y == iniPos.y:
                pass
            elif currentPos.x >= start.x or currentPos.y >= start.y:
                rectX = struct(corner1 = struct(x = iniPos.x, y = iniPos.y), 
                               corner2 = struct(x = start.x, 
                                                y = start.y))
                restoreImage(originalImage, rectX)
                rectY = struct(corner1 = struct(x = min(currentPos.x, start.x), 
                                                y = min(currentPos.y, 
                                                        start.y)), 
                               corner2 = struct(x = max(currentPos.x, start.x), 
                                                y = max(currentPos.y, 
                                                        start.y)))
                addRectangle(imageCopy, rectY, color)
            elif currentPos.x <= iniPos.x and currentPos.y <= iniPos.y:
                rectX = struct(corner1 = struct(x = currentPos.x, 
                                                y = iniPos.y), 
                               corner2 = struct(x = iniPos.x, y = start.y))
                addRectangle(imageCopy, rectX, color)
                rectY = struct(corner1 = struct(x = currentPos.x, 
                                                y = currentPos.y), 
                               corner2 = struct(x = start.x, 
                                                y = iniPos.y))
                addRectangle(imageCopy, rectY, color)
            elif currentPos.x <= iniPos.x and currentPos.y >= iniPos.y:
                rectX = struct(corner1 = struct(x = currentPos.x, 
                                                y = currentPos.y), 
                               corner2 = struct(x = iniPos.x, y = start.y))
                addRectangle(imageCopy, rectX, color)
                rectY = struct(corner1 = struct(x = iniPos.x, 
                                                y = iniPos.y), 
                               corner2 = struct(x = start.x, 
                                                y = currentPos.y))
                restoreImage(originalImage, rectY)
            elif currentPos.x >= iniPos.x and currentPos.y <= iniPos.y:
                rectX = struct(corner1 = struct(x = iniPos.x, 
                                                y = iniPos.y), 
                               corner2 = struct(x = currentPos.x, y = start.y))
                restoreImage(originalImage, rectX)
                rectY = struct(corner1 = struct(x = currentPos.x, 
                                                y = currentPos.y), 
                               corner2 = struct(x = start.x, 
                                                y = iniPos.y))
                addRectangle(imageCopy, rectY, color)
            elif currentPos.x >= iniPos.x and currentPos.y >= iniPos.y:
                rectX = struct(corner1 = struct(x = iniPos.x, 
                                                y = currentPos.y), 
                               corner2 = struct(x = currentPos.x, y = start.y))
                restoreImage(originalImage, rectX)
                rectY = struct(corner1 = struct(x = iniPos.x, 
                                                y = iniPos.y), 
                               corner2 = struct(x = start.x, 
                                                y = currentPos.y))
                restoreImage(originalImage, rectY)

        if iniPos.x < start.x and iniPos.y > start.y:
            if currentPos.x == iniPos.x and currentPos.y == iniPos.y:
                pass
            elif currentPos.x >= start.x or currentPos.y <= start.y:
                rectX = struct(corner1 = struct(x = iniPos.x, y = start.y), 
                               corner2 = struct(x = start.x, 
                                                y = iniPos.y))
                restoreImage(originalImage, rectX)
                rectY = struct(corner1 = struct(x = min(currentPos.x, start.x), 
                                                y = min(currentPos.y, 
                                                        start.y)), 
                               corner2 = struct(x = max(currentPos.x, start.x), 
                                                y = max(currentPos.y, 
                                                        start.y)))
                addRectangle(imageCopy, rectY, color)
            elif currentPos.x <= iniPos.x and currentPos.y >= iniPos.y:
                rectX = struct(corner1 = struct(x = currentPos.x, 
                                                y = start.y), 
                               corner2 = struct(x = iniPos.x, y = iniPos.y))
                addRectangle(imageCopy, rectX, color)
                rectY = struct(corner1 = struct(x = currentPos.x, 
                                                y = iniPos.y), 
                               corner2 = struct(x = start.x, 
                                                y = currentPos.y))
                addRectangle(imageCopy, rectY, color)
            elif currentPos.x <= iniPos.x and currentPos.y <= iniPos.y:
                rectX = struct(corner1 = struct(x = currentPos.x, 
                                                y = start.y), 
                               corner2 = struct(x = iniPos.x, 
                                                y = currentPos.y))
                addRectangle(imageCopy, rectX, color)
                rectY = struct(corner1 = struct(x = iniPos.x, 
                                                y = currentPos.y), 
                               corner2 = struct(x = start.x, 
                                                y = iniPos.y))
                restoreImage(originalImage, rectY)
            elif currentPos.x >= iniPos.x and currentPos.y >= iniPos.y:
                rectX = struct(corner1 = struct(x = iniPos.x, 
                                                y = start.y), 
                               corner2 = struct(x = currentPos.x, 
                                                y = iniPos.y))
                restoreImage(originalImage, rectX)
                rectY = struct(corner1 = struct(x = currentPos.x, 
                                                y = iniPos.y), 
                               corner2 = struct(x = start.x, 
                                                y = currentPos.y))
                addRectangle(imageCopy, rectY, color)
            elif currentPos.x >= iniPos.x and currentPos.y <= iniPos.y:
                rectX = struct(corner1 = struct(x = iniPos.x, 
                                                y = start.y), 
                               corner2 = struct(x = currentPos.x, 
                                                y = currentPos.y))
                restoreImage(originalImage, rectX)
                rectY = struct(corner1 = struct(x = iniPos.x, 
                                                y = currentPos.y), 
                               corner2 = struct(x = start.x, 
                                                y = iniPos.y))
                restoreImage(originalImage, rectY)

        iniPos = currentPos            # update previous position for next loop
        sleep(0.01)
    originalImage = imageCopy

                        

# restoreImage restores the image when the user drags the cursor to make a 
#              smaller selection
# parameters: originalImage is a list of lists containing the original colors
#                           of each pixel
#             rectangle is a struct containing corner1 and corner2 of the area
#                       to restore.
# output: None, image is a list of lists with the restored values

def restoreImage(originalImage, rectangle):
    minX = rectangle.corner1.x
    maxX = rectangle.corner2.x
    minY = rectangle.corner1.y
    maxY = rectangle.corner2.y
    if minY < 24:
        minY = 24
    for x in range(minX, maxX):
        for y in range(minY, maxY):
            setPixel(x, y, originalImage[y][x])

    return originalImage[minY:maxY][minX:maxX]
    # for yVal in range(rectangle.corner1.y, rectangle.corner2.y):
    #     for xVal in range(rectangle.corner1.x, rectangle.corner2.x):
    #         setPixel(xVal, yVal, originalImage[xVal][yVal])
    

# addRectangle draws a rectangle onto the same image given as parameter
# parameters: image is a list of pixels displaying which color each pixel is
#                      this list is usually created using exportScreen()
#             rectangle is a struct containing corner1 and corner2
#             color is a string with a hex color value of template '#fff'
# output: None, this function changes the values of parameter image and screen

def addRectangle(image, rectangle, color):
    width = rectangle.corner2.x - rectangle.corner1.x
    height = rectangle.corner2.y - rectangle.corner1.y
    print(width)
    fillRectangle(rectangle.corner1.x, rectangle.corner1.y, width, height, 
                  color)
    image[rectangle.corner1.x:rectangle.corner2.x][rectangle.corner1.y:
          rectangle.corner2.y] = height * [width * [color]]  # potential bug

# handleNextClick 
currentColor = '#fff'
def handleNextClick(buttons):

    while True:
        position = struct(x = getMouse().x, y = getMouse().y)             
        if getMouse().button == 1:            
            menuHeight = 24       # to correct later
            global currentColor   # to correct later
            if (findButtons(buttons, position) is None and 
                position.y <= menuHeight):
                pass
            elif (getScreenHeight() > position.y > 24 and 
                    0 < position.x < getScreenWidth()):
                return True
            elif findButtons(buttons, position).erase:
                rect = struct(corner1 = struct(x = 0, y = menuHeight), 
                                corner2 = struct(x = getScreenWidth(), 
                                                y = getScreenHeight()))
                # do not draw in the menu
                if rect.corner1.y < 24:
                    rect.corner1.y = 24
                if rect.corner2.y < 24:
                    rect.corner2.y = 24  
                addRectangle(convertImage(exportScreen()), rect, 
                                buttons[0].color)
            elif (findButtons(buttons, position) is not None):
                return (findButtons(buttons, position).color)
     
        sleep(0.01)

    

# the function convertImage takes an exportScreen() output and returns a list 
# of lists where image[x][y] returns the color of pixel at x,y
# parameter: screen is a string from exportScreen() 
# output: list of lists where each element is a color of form '#fff'

def convertImage(screen):
    rows = screen.split('\n')
    n=len(rows)
    image=[]
    for i in range(n):
        image.append(rows[i].strip('#').split("#"))
    xLength = len(image)
    ylength = len(image[0])
    for xVal in range(xLength):
        for yVal in range(ylength):
            image[xVal][yVal] = '#'+ image[xVal][yVal]
    return image

def draw():
    screenWidth = 180
    screenHeight = 120
    menuHeight = 24
    spacing = 6
    size = 12
    white = "#fff"
    black =  "#000"
    red = "#f00"
    yellow = "#ff0"
    lime = "#0f0"
    blue =  "#00f"
    fuchsia = "#f0f"
    colors = [white, black, red, yellow, lime, blue, fuchsia]
    setScreenMode(screenWidth, screenHeight)
    screen = struct(corner1 = struct(x = 0, y = 0), 
                    corner2 = struct(x = screenWidth, y = screenHeight))
    menu = struct(corner1 = struct(x = 0, y = 0), 
                  corner2 = struct(x = screenWidth, y = menuHeight))
    currentScreen = convertImage(exportScreen())

    # starting color value
    currentColor = '#fff'                           

    # make screen white
    addRectangle(currentScreen, screen, "#fff")

    # draw menu
    addRectangle(currentScreen, menu, "#888")

    # draw buttons in menu
    buttonList = createButtons(colors, size, spacing, '#fff')
    for currentButton in buttonList:
        insideButton = struct(corner1 = struct(x = currentButton.corner1.x+1,
                                               y = currentButton.corner1.y+1),
                              corner2 = struct(x = currentButton.corner2.x-1,
                                               y = currentButton.corner2.y-1))
        addRectangle(currentScreen, currentButton, '#000') # black border
        addRectangle(currentScreen, insideButton, currentButton.color)
    
    # draw red x on first erase button
    for i in range(1, size - 1):
        setPixel(spacing + i, spacing + i, "#f00")
        setPixel(buttonList[0].corner2.x - 1 - i, spacing + i, '#f00')
    
    while True:
        position = struct(x = getMouse().x, y = getMouse().y)  
        if handleNextClick(buttonList) == True:
            image = convertImage(exportScreen())
            position = struct(x = getMouse().x, y = getMouse().y)  
            drawFloatingRectangle(image, position, currentColor)
        else:
            currentColor = handleNextClick(buttonList)
        sleep(0.01)

# REMOVE BEFORE HANDING IN ------------------------------------------------
draw()
# -------------------------------------------------------------------------
def testDraw():
    assert (1 == 1)     # 5 to 10 asserts

testDraw()

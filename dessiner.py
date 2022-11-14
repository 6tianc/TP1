# authors: Tian Cheng Liu 20050130
#          Flora Kang     20239294
# November 1st 2022
# Travail Pratique 1


# declaration of global variables

screenWidth = 180
screenHeight = 120
menuHeight = 24
spacing = 6
size = 12

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
# output: No output, the originalImage value will get changed.

def drawFloatingRectangle(originalImage, start, color):
    # creates imageCopy, a deep copy of the originalImage
    imageCopy = []
    for i in originalImage:
        imageCopy.append(i[:])
    global menuHeight
    global screenHeight
    global screenWidth
    # position of the previous iteration (0.01s ago)
    iniPos = struct(x = start.x, y = start.y)
    
    while getMouse().button:           # continue loop while mouse button held

        # current position of the mouse
        currentPos = struct(x = getMouse().x + 1, y = getMouse().y + 1)

        # do not go over the drawing screen
        if currentPos.x > screenWidth:
            currentPos.x = screenWidth
        if currentPos.y > screenHeight:
            currentPos.y = screenHeight
        
        # do not go over the menu
        if currentPos.y < menuHeight:
            currentPos.y = menuHeight
        
        # if mouse is in quadrant 1 (bottom right from the start position)
        if iniPos.x >= start.x and iniPos.y >= start.y:

            # if the mouse has not moved since the last iteration
            if currentPos.x == iniPos.x and currentPos.y == iniPos.y:
                pass

            # if the mouse moved to another quadrant
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

            # if the mouse has moved towards the bottom right
            elif currentPos.x >= iniPos.x and currentPos.y >= iniPos.y:
                rectX = struct(corner1 = struct(x = iniPos.x, y = start.y), 
                               corner2 = struct(x = currentPos.x, 
                                                y = iniPos.y))
                addRectangle(imageCopy, rectX, color)
                rectY = struct(corner1 = struct(x = start.x, y = iniPos.y), 
                               corner2 = struct(x = currentPos.x, 
                                                y = currentPos.y))
                addRectangle(imageCopy, rectY, color)
            
            # if the mouse has moved towards the top right
            elif currentPos.x >=iniPos.x and currentPos.y <= iniPos.y:
                rectX = struct(corner1 = struct(x = iniPos.x, y = start.y), 
                               corner2 = struct(x = currentPos.x, 
                                                y = currentPos.y))
                addRectangle(imageCopy, rectX, color)
                rectY = struct(corner1 = struct(x = start.x, y = currentPos.y), 
                               corner2 = struct(x = currentPos.x, 
                                                y = iniPos.y))
                restoreImage(originalImage, rectY)
            
            # if the mouse has moved towards the bottom left
            elif currentPos.x <= iniPos.x and currentPos.y >= iniPos.y:
                rectX = struct(corner1 = struct(x = currentPos.x, y = start.y), 
                               corner2 = struct(x = iniPos.x, 
                                                y = iniPos.y))
                restoreImage(originalImage, rectX)
                rectY = struct(corner1 = struct(x = start.x, y = iniPos.y), 
                               corner2 = struct(x = currentPos.x, 
                                                y = currentPos.y))
                addRectangle(imageCopy, rectY, color)
            
            # if the mouse has moved towards the top left
            elif currentPos.x <=iniPos.x and currentPos.y <= iniPos.y:
                rectX = struct(corner1 = struct(x = currentPos.x, y = start.y), 
                               corner2 = struct(x = iniPos.x, 
                                                y = currentPos.y))
                restoreImage(originalImage, rectX)  
                rectY = struct(corner1 = struct(x = start.x, y = currentPos.y), 
                               corner2 = struct(x = iniPos.x, 
                                                y = iniPos.y))
                restoreImage(originalImage, rectY)

        # if mouse is in quadrant 2 (top right from the start position)
        if iniPos.x >= start.x and iniPos.y <= start.y:

            # if the mouse has not moved
            if currentPos.x == iniPos.x and currentPos.y == iniPos.y:
                pass

            # if the mouse has moved to another quadrant
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
            
            # if the mouse has moved towards the top right
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
            
            # if the mouse has moved towards the bottom right
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

            # if the mouse has moved towards the top left
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

            # if the mouse has moved towards the bottom left
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

        # if mouse is in quadrant 3 (top left from the start position)        
        if iniPos.x <= start.x and iniPos.y <= start.y:

            # if the mouse has not moved
            if currentPos.x == iniPos.x and currentPos.y == iniPos.y:
                pass

            # if the mouse has moved to another quadrant
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
            
            # if the mouse has moved towards the top left
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

            # if the mouse has moved towards the bottom left
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

            # if the mouse has moved towards the top right
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

            # if the mouse has moved towards the bottom right
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

        # if mouse is in quadrant 4 (bottom left from the start position)
        if iniPos.x <= start.x and iniPos.y >= start.y:

            # if the mouse has not moved
            if currentPos.x == iniPos.x and currentPos.y == iniPos.y:
                pass

            # if the mouse has moved to another quadrant
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

            # if the mouse has moved towards the bottom left
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

            # if the mouse has moved towards the top left
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
            
            # if the mouse has moved towards the bottom right
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
            
            # if the mouse has moved towards the top right
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

    # updates the original image after lifting the finger
    minX = min(iniPos.x, start.x)
    maxX = max(iniPos.x, start.x)
    minY = min(iniPos.y, start.y)
    maxY = max(iniPos.y, start.y)
    for x in range(minX, maxX):
        for y in range(minY, maxY):
            originalImage[y][x] = color

                        

# restoreImage restores the image when the user drags the cursor to make a 
#              smaller selection
# parameters: originalImage is a list of lists containing the original colors
#                           of each pixel
#             rectangle is a struct containing corner1 and corner2 of the area
#                       to restore.
# output: No output, image is a list of lists with the restored values

def restoreImage(originalImage, rectangle):
    global menuHeight
    minX = rectangle.corner1.x
    maxX = rectangle.corner2.x
    minY = rectangle.corner1.y
    maxY = rectangle.corner2.y
    # do not draw on the menu
    if minY < menuHeight:
        minY = menuHeight
    for x in range(minX, maxX):
        for y in range(minY, maxY):
            setPixel(x, y, originalImage[y][x])
    

# addRectangle draws a rectangle onto the same image given as parameter
# parameters: image is a list of pixels displaying which color each pixel is
#                      this list is usually created using exportScreen()
#             rectangle is a struct containing corner1 and corner2
#             color is a string with a hex color value of template '#fff'
# output: No output, this function changes the values of parameter image and 
#         screen

def addRectangle(image, rectangle, color):
    width = rectangle.corner2.x - rectangle.corner1.x
    height = rectangle.corner2.y - rectangle.corner1.y
    fillRectangle(rectangle.corner1.x, rectangle.corner1.y, width, height, 
                  color)
    for x in range(rectangle.corner1.x, rectangle.corner2.x):
        for y in range(rectangle.corner1.y, rectangle.corner2.y):
            image[y][x] = color

# handleNextClick starts a loop that waits for a click every 0.01s. When a 
# click is found, it will check whether it is on a button or in the drawing
# space. If the click is on the reset button, the drawing is reset. If the 
# click is on a color button, the color of the next rectangle is changed to the
# selected color. If the click is on the drawing area, it will begin the 
# drawing process.
# parameters: buttons is a list of buttons created using the createButtons() 
#             function
# output: No output.
def handleNextClick(buttons):
    image = convertImage(exportScreen())
    color = "#fff"
    global menuHeight        
    while True:
        position = struct(x = getMouse().x, y = getMouse().y)             
        if getMouse().button == 1:            

            if (findButtons(buttons, position) is not None and findButtons(
                buttons, position).erase):
                rect = struct(corner1 = struct(x = 0, y = menuHeight), 
                                corner2 = struct(x = getScreenWidth(), 
                                                y = getScreenHeight()))
                addRectangle(image, rect, buttons[0].color)
            elif (findButtons(buttons, position) is not None):
                color = findButtons(buttons, position).color
            elif (getScreenHeight() > position.y > menuHeight and 
                    0 < position.x < getScreenWidth()):
                drawFloatingRectangle(image, position, color)
            else:
                pass
     
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

# draw will start the procedure that allows users to draw on the screen in
# codeBoot using in-built functions.
# parameters: none
# outputs: none, changes will be reflected on the screen in Code Boot

def draw():
    global screenWidth 
    global screenHeight 
    global menuHeight 
    global spacing
    global size 
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

    handleNextClick(buttonList)

def testDraw():
    # 5 to 10 asserts
    
    # assert for the function createButtons
    assert (createButtons(["#f00"], 12, 6, "#fff") == 
            [struct(corner1=struct(x=6, y=6), 
            corner2=struct(x=18, y=18), color='#fff', erase=True), 
            struct(corner1=struct(x=24, y=6), corner2=struct(x=36, y=18),
            color='#f00', erase=False)])
    
    # assert for the function findButons if the position is in the button
    assert (findButtons(createButtons(["#f00"], 12, 6, "#fff"), 
            struct(x=7, y=7)) 
            == 
            struct(corner1=struct(x=6, y=6), corner2=struct(x=18, y=18), 
            color='#fff', erase=True))
    
    # assert for the function findButons if the position is not in the button
    assert (findButtons(createButtons(["#f00"], 12, 6, "#fff"),
            struct(x=5, y=5))
            ==
            None)
    
    # assert for the function convertImage off a 3 by 3 black screen
    setScreenMode(3,3)
    assert (convertImage(exportScreen()) == [['#000', '#000', '#000'], 
                                             ['#000', '#000', '#000'], 
                                             ['#000', '#000', '#000']])
    
    # assert for the function addRectangle off a 3 by 3 black screen with a
    # 1 by 2 green rectangle in the top left
    addRectangle(convertImage(exportScreen()),
                 struct(corner1 = struct(x =0, y =0),
                       corner2 = struct(x = 2, y = 1)), "#0f0")
    assert(exportScreen() == '#0f0#0f0#000\n#000#000#000\n#000#000#000')

testDraw()
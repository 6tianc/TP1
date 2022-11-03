# authors: Tian Cheng Liu 20050130
#          Flora Kang     20239294
# November 1st 2022
# Travail Pratique 1

# codeBoot functions: setScreenMode(width, height), getScreenWidth(),
# getScreenHeight(), setPixel(x, y, color), 
# fillRectangle(x, y, width, height, color), getPixel(x, y), getMouse(),
# exportScreen()

# class struct allows for python to have structs like in CodeBoot

class struct:
 def __init__(self, **fields):
    self.__dict__.update(fields)
 def __repr__(self):
    return 'struct('+(', '.join(list(map(lambda f:f+'='+repr(self.__dict__[f]),
                                         self.__dict__))))+')'

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
                          color = colorErase, effacer = True))
    lengthColors = len(colors)                      
    for i in range(lengthColors):  # from 0 to lengthColors-1
            buttons.append(struct(corner1 = struct(x = buttons[i].corner1.x 
                                                   + corn2corn, y = space), 
                                  corner2 = struct(x = buttons[i].corner2.x + 
                                                   corn2corn, y = corn2corn), 
                                  color = colors[i], effacer = False))
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
# and state of the cursor. 

def drawFloatingRectangle(originalImage, start, color):
    pass

# restoreImage restores the image when the user drags the cursor to make a 
#              smaller selection
# parameters: originalImage is a list of lists containing the original colors
#                           of each pixel
#             rectangle is a struct containing corner1 and corner2 of the area
#                       to restore.
# output: image is a list of lists with the restored values

def restoreImage(originalImage, rectangle):
    for yVal in range(rectangle.corner1.y, rectangle.corner2.y):
        for xVal in range(rectangle.corner1.x, rectangle.corner2.x):
            setPixel(xVal, yVal, originalImage[xVal][yVal])
    

# addRectangle draws a rectangle onto the same image given as parameter
# parameters: image is a list of pixels displaying which color each pixel is
#                      this list is usually created using exportScreen()
#             rectangle is a struct containing corner1 and corner2
#             color is a string with a hex color value of template '#fff'
# output: None, this function changes the values of parameter image and screen

def addRectangle(image, rectangle, color):
    width = rectangle.corner2.x - rectangle.corner1.x
    height = rectangle.corner2.y - rectangle.corner1.y
    fillRectangle(rectangle.corner1.x, rectangle.corner1.y, width, height, 
                  color)
    image[rectangle.corner1.x:rectangle.corner2.x][rectangle.corner1.y:
          rectangle.corner2.y] = height * [width * [color]]  # potential bug

def handleNextClick(buttons):
    pass

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
    
    # handleNextClick(buttonList)

# REMOVE BEFORE HANDING IN ------------------------------------------------
draw()
# -------------------------------------------------------------------------
def testDraw():
    assert (1 == 1)     # 5 to 10 asserts

testDraw()

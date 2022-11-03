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

    # distance between one corner of one button to the same corner of the next button
    corn2corn = space + size  
             
    buttons = []
    buttons.append(struct(corner1 = struct(x = space, y = space), 
                          corner2 = struct(x = corn2corn, y = corn2corn), 
                          couleur = colorErase, effacer = True))
    lengthColors = len(colors)                      
    for i in range(lengthColors):  # from 0 to lengthColors-1
            buttons.append(struct(corner1 = struct(x = buttons[i].corner1.x 
                                                   + corn2corn, y = space), 
                                  corner2 = struct(x = buttons[i].corner2.x + 
                                                   corn2corn, y = corn2corn), 
                                  couleur = colors[i], effacer = False))
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

def drawFloatingRectangle(originalImage, start, color):
    pass

def restoreImage(originalImage, rectangle):
    pass

def addRectangle(image, rectangle, color):
    pass

def handleNextClick(buttons):
    pass

def draw():
    width = 180
    height = 120
    white = "#fff"
    black =  "#000"
    red = "#f00"
    yellow = "#ff0"
    lime = "#0f0"
    blue =  "#00f"
    fuchsia = "#f0f"
    colors = [white, black, red, yellow, lime, blue, fuchsia]

def testDraw():
    assert (1 == 1)

testDraw()

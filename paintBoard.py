import pyglet
from pyglet import app
from pyglet import shapes
from pyglet import image
from pathlib import Path
import os
import pygetwindow as gw
import PIL.ImageGrab

drawingClickAt = [(0, 0)]
pixels = []
drawingColor = [(0, 0, 0)]
penThickness = [4]
eraserActivity = False
penActivity = True
imgCount = 0

# WINDOW
window = pyglet.window.Window(500, 400)
batch = pyglet.graphics.Batch()


canvasBackground = shapes.Rectangle(100, 0, 400, 400, color=(255, 255, 255), batch=batch)
toolLine = shapes.Line(100, 0, 100, 400, width=3, color=(255,20,147), batch=batch)
toolBackground = shapes.Rectangle(0, 0, 100, 400, color=(255, 255, 255), batch=batch)


# COLOR SHAPES
backRect = shapes.Rectangle(5, 170, 40, 40, color=(0, 0, 0), batch=batch)
redRect = shapes.Rectangle(55, 170, 40, 40, color=(255, 20, 20), batch=batch)

blueRect = shapes.Rectangle(5, 120, 40, 40, color=(0,191,255), batch=batch)
greenRect = shapes.Rectangle(55, 120, 40, 40, color=(50,205,50), batch=batch)

yellowRect = shapes.Rectangle(5, 70, 40, 40, color=(255,255,0), batch=batch)
orangeRect = shapes.Rectangle(55, 70, 40, 40, color=(255, 117, 24), batch=batch)

greyRect = shapes.Rectangle(5, 20, 40, 40, color=(192,192,192), batch=batch)
brownRect = shapes.Rectangle(55, 20, 40, 40, color=(160,82,45), batch=batch)

borderCurrentColor = shapes.Rectangle(28, 218, 44, 44, color=(255,20,147), batch=batch)
currentColor = shapes.Rectangle(30, 220, 40, 40, color=drawingColor[-1], batch=batch)

# IMAGES AND BORDERS
px2Border = shapes.Rectangle(20, 345, 59, 25, color=(255,20,147), batch=batch)
px2 = image.load("icons\size2px.png")
px4Border = shapes.Rectangle(20, 314, 60, 25, color=(255,20,147), batch=batch)
px4 = image.load("icons\size4px.png")
eraserBorder = shapes.Rectangle(9, 274, 30, 30, color=(255, 255, 255), batch=batch)
eraser = image.load("icons\eraser.png")
penBorder = shapes.Rectangle(61, 274, 30, 30, color=(255,20,147), batch=batch)
pen = image.load("icons\pen2.png")
saveIconBorder = shapes.Rectangle(9, 375, 30, 23, color=(255,20,147), batch=batch)
saveIcon = image.load("icons\saveImg.png")
newIconBorder = shapes.Rectangle(61, 375, 30, 23, color=(255,20,147), batch=batch)
newIcon = image.load("icons\\newImg.png")

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == 1:
        if y > 374 and x < 50:
            wasSaveImgClicked(x, y)
        elif y > 374 and x < 100:
            wasNewClicked(x, y)
        elif x < 100 and y > 305:
            whichPenThickness(x, y)
        elif x < 45 and y > 265:
            wasEraserClicked(x, y)
        elif x < 90 and y > 265:
            wasPenClicked(x, y)
        elif x > 100:
            drawingClickAt.append((x, y))
            drawCircles()
        elif x < 100:
            if y < 270:
                whichColorClick(x, y)

def wasSaveImgClicked(x, y):
    global imgCount
    if x in range(9, 38):
        if y in range(375, 397):
            imgCount += 1
            saveImg()

def wasNewClicked(x, y):
    global drawingClickAt, pixels, drawingColor, penThickness, eraserActivity, penActivity
    if x in range(61, 89):
        if y in range(375, 397):
            drawingClickAt = [(0, 0)]
            pixels = []
            drawingColor = [(0, 0, 0)]
            penThickness = [4]
            eraserActivity = False
            penActivity = True

def saveImg():
    """
    Saves image to root folder.
    """
    global imgCount
    while True:
        myFileName = f"drawing{imgCount}.png"
        namedFile = Path(f"{myFileName}")
        absolutePath = os.path.abspath("paintBoard.py")

        if namedFile.exists():
            imgCount += 1
        else:
            paintingBoard = gw.getWindowsWithTitle(absolutePath)[0]
            screenshot = PIL.ImageGrab.grab(bbox=(paintingBoard.topleft[0] + 109, paintingBoard.topleft[1] + 31, paintingBoard.bottomright[0] - 8, paintingBoard.bottomright[1] - 9))
            screenshot.save(myFileName)
            return

def whichPenThickness(x, y):
    if y in range(350, 369):
        if x in range(21, 79):
            penThickness[0] = 2
    elif y in range(315, 338):
        if x in range(21,79):
            penThickness[0] = 4

def wasEraserClicked(x, y):
    global eraserActivity
    if x in range(10, 38):
        if y in range(275, 303):
            if eraserActivity == False:
                eraserActivity = True
                drawingColor.append((255, 255, 255))
            elif eraserActivity == True:
                eraserActivity = False
                lastActiveColor = drawingColor[-2]
                drawingColor.append(lastActiveColor)

def wasPenClicked(x, y): 
    global penActivity
    global eraserActivity
    if x in range(62, 90):
        if y in range(275, 303):
            if penActivity == True:
                return
            penActivity = True
            eraserActivity = False
            if drawingColor[-2] != (255, 255, 255): 
                drawingColor[-1] = drawingColor[-2]

def drawCircles():
    if penThickness[0] == 4:
        if drawingClickAt[-1][0] > 104:
            pixel = shapes.Circle(drawingClickAt[-1][0], drawingClickAt[-1][1], penThickness[0], color=drawingColor[-1])
            pixels.append(pixel)
    elif drawingClickAt[-1][0] > 102:
        pixel = shapes.Circle(drawingClickAt[-1][0], drawingClickAt[-1][1], penThickness[0], color=drawingColor[-1])
        pixels.append(pixel)      

def whichColorClick(x, y):
    global penActivity, eraserActivity
    if x in range(5, 45):
        if y in range(170, 201):
            drawingColor.append((0, 0, 0))
            penActivity = True
            eraserActivity = False
        elif y in range(120, 160):
            drawingColor.append((0,191,255))
            penActivity = True
            eraserActivity = False
        elif y in range(70, 110):
            drawingColor.append((255,255,0))
            penActivity = True
            eraserActivity = False
        elif y in range(20, 60):
            drawingColor.append((192,192,192))
            penActivity = True
            eraserActivity = False
    elif x in range(55, 95):
        if y in range(170, 201):
            drawingColor.append((255, 20, 20))
            penActivity = True
            eraserActivity = False
        elif y in range(120, 160):
            drawingColor.append((50,205,50))
            penActivity = True
            eraserActivity = False
        elif y in range(70, 110):
            drawingColor.append((255, 117, 24))
            penActivity = True
            eraserActivity = False
        elif y in range(20, 60):
            drawingColor.append((160,82,45))
            penActivity = True
            eraserActivity = False

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    xNew= x + dx
    if penThickness[0] == 4:
        if xNew > 104:
            yNew = y + dy
            newPixel = shapes.Circle(xNew, yNew, penThickness[0], color=drawingColor[-1])
            pixels.append(newPixel)
    elif xNew > 102:
        yNew = y + dy
        newPixel = shapes.Circle(xNew, yNew, penThickness[0], color=drawingColor[-1])
        pixels.append(newPixel)

def changeCurrentColor():
    color = drawingColor[-1]
    currentColor.color = color

def activePenThickness():
    if penThickness[0] == 2:
        active = (255,20,147)
        px2Border.color = active
        unactive = (255, 255, 255)
        px4Border.color = unactive
    elif penThickness[0] == 4:
        active = (255,20,147)
        px4Border.color = active
        unactive = (255, 255, 255)
        px2Border.color = unactive
    
def eraserStatus():
    global penActivity
    if eraserActivity == False:
        unactiveColor = (255, 255, 255)
        eraserBorder.color = unactiveColor
        penActivity = True
    else:
        activeColor = (255,20,147)
        eraserBorder.color = activeColor
        penActivity = False

def penStatus():
    if penActivity == False:
        unactiveColor = (255, 255, 255)
        penBorder.color = unactiveColor
    else:
        activeColor = (255,20,147)
        penBorder.color = activeColor

@ window.event
def on_draw():
    window.clear()
    batch.draw()
    px2.blit(21, 346)
    px4.blit(21, 315)
    eraser.blit(10, 275)
    pen.blit(62, 275)
    saveIcon.blit(10, 376)
    newIcon.blit(62, 376)
    changeCurrentColor()
    activePenThickness()
    eraserStatus()
    penStatus()
    if pixels:
        for onePixel in pixels:
            onePixel.draw()

if __name__=="__main__":
    app.run()

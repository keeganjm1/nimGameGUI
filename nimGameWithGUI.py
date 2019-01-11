# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 14:00:49 2018

@author: Keegs
"""

# Note: if you want to use additional tkinter widgets, you will need to add their names to
# the import list below
from tkinter import Tk, Toplevel, Canvas, Frame, Button, Label, PhotoImage, Entry, END, LEFT, RIGHT, SUNKEN
from time import sleep
import random

# To run this code, load into Python, and execute runNim(listOfInitialHeaps),
# where listOfInitialHeaps is a list of the form expected by the
# NimGame __init__ function. 
# Note: because of the fixed canvas/gui size, the maximum number of heaps is 10
# and the maximum number of balls in any heap is also 10.
#

# This class is just like the solution to HW 6 Q2 except with small changes related to GUI.
# See comments starting with # ##.
class NimGame():

    def __init__(self, initialHeaps):
        self.heaps = initialHeaps
        print("Nim game initialized with {} heaps.".format(len(self.heaps)))
        statusLabel.configure(text="Nim game initialized with {} heaps.".format(len(self.heaps)))
    def gameOver(self):
        return sum(self.heaps) == 0
    
    playerWins = 0
    computerWins = 0

    def doComputerTurn(self):
        availableHeaps = [i for i in range(len(self.heaps)) if self.heaps[i] != 0]
        chosenHeap = random.choice(availableHeaps)
        compBallsTaken = random.randint(1, self.heaps[chosenHeap])
        self.heaps[chosenHeap] = self.heaps[chosenHeap] - compBallsTaken
        updateGraphics()
        print("Computer took {} balls from heap {}".format(compBallsTaken, chosenHeap))
        statusLabel.configure(text="Computer took {} balls from heap {}".format(compBallsTaken, chosenHeap))
        if self.gameOver():
            print("Computer wins!")
            statusLabel.configure(text='Computer Wins!')
            NimGame.computerWins += 1
            compWinLabel.configure(text = "Computer wins: {}".format(NimGame.computerWins))
            
    def remove(self, numberOfBalls, heapNumber):
        if (heapNumber < 0) or (heapNumber >= len(self.heaps)):
            print("Heap {} does not exist. Try again.".format(heapNumber))
            statusLabel.configure(text="Heap {} does not exist. Try again.".format(heapNumber))
            return
        if (numberOfBalls < 1) or (numberOfBalls > self.heaps[heapNumber]):
             print("You can't take that many balls from heap {}. Try again.".format(heapNumber))
             statusLabel.configure(text="You can't take that many balls from heap {}. Try again.".format(heapNumber))
             return
        self.heaps[heapNumber] = self.heaps[heapNumber] - numberOfBalls
        print("You took {} balls from heap {}.".format(numberOfBalls, heapNumber))
        statusLabel.configure(text="You took {} balls from heap {}.".format(numberOfBalls, heapNumber))
        
        if self.gameOver():
            print("You win!")
            statusLabel.configure(text='You win!')
            NimGame.playerWins += 1
            playerWinLabel.configure(text = "Player wins: {}".format(NimGame.playerWins))
        else:
            # ## After removing player-chosen balls, update graphics and
            # use tkinter's 'after' method to schedule the computer
            # move to occur 2 second later.  This way the player can "see" the
            # intermediate status.  Perhaps think about a nicer way of showing this.
            updateGraphics()
            rootWindow.after(2000, self.doComputerTurn)
                
# global variables used for placement of balls
canvasHeight = 620
canvasWidth = 620
canvasBorderBuffer = 10
maxBallSize = 50
# the values of global variables below are computed and set in initializeNimAndGUI
# ballSize
# halfBallSize 
# spaceBetweenBalls 
# leftmostHeapX
# bottomHeapY

# 1. clear the canvas
# 2. draw the heaps on the canvas
def updateGraphics():
    canvas.delete('all')   
    
    currentX = leftmostHeapX
    for heapnum in range(len(nimGame.heaps)):
        currentY = heapBottomY
        canvas.create_text(currentX, currentY, text="Heap {}".format(heapnum))
        currentY = currentY - (spaceBetweenBalls + (ballSize//2))
        for ballInHeap in range(nimGame.heaps[heapnum]):
            canvas.create_oval(currentX - halfBallSize,
                               currentY - halfBallSize,
                               currentX + halfBallSize,
                               currentY + halfBallSize,
                               fill="#ffdf00")
            currentY = currentY - (spaceBetweenBalls + ballSize)
        currentX = currentX + spaceBetweenBalls + ballSize


# Callback functions invoked by GUI buttons

def executePlayerMove():
    whichHeap = int(whichHeapEntry.get())
    numBalls = int(numBallsEntry.get())
    nimGame.remove(numBalls, whichHeap)
    
def initializeNewGame():
    newGameHeaps = str(placeholder.get())
    newHeaps = newGameHeaps.split() 
    if newHeaps == []:
        initialHeaps = [1,2,3] # change this to read from Entry widget you add to GUI
        initializeNimAndGUI(initialHeaps)
    else:
        currentHeaps = []
        for char in newHeaps:
            currentHeaps.append(int(char))# change this to read from Entry widget you add to GUI
        initializeNimAndGUI(currentHeaps)  
    

#####

# 1. create a NimGame object with specified heaps
# 2. clear the graphics canvas
# 3. set some global variables for balls spacing and positioning 
# 
def initializeNimAndGUI(initialHeaps):
    global nimGame
    global ballSize, halfBallSize, spaceBetweenBalls, leftmostHeapX, heapBottomY

    # Based on the hardcoded canvas dimensions and ball size, the maximum
    # number of heaps is 10, and the maximum number of balls in a heap is also 10
    if (len(initialHeaps) > 10) or (max(initialHeaps) > 10):
        statusLabel.configure(text="Max number heaps: 10. Max balls in a heap:10. Try again.")
    else:
        nimGame = NimGame(initialHeaps)

        canvas.delete('all') 
        ballSize = maxBallSize
        halfBallSize = ballSize // 2
        spaceBetweenBalls = int(0.2 * ballSize)
    
        leftmostHeapX = (canvasBorderBuffer//2) + (spaceBetweenBalls//2) + halfBallSize
        heapBottomY = canvasHeight - (canvasBorderBuffer//2) 
                                
        updateGraphics()
        statusLabel.configure(text="Started new game.")


# create GUI for Nim Game, including
# 1. canvas where balls will be shown
# 2. some buttons, to the right of the canvas, for taking balls or starting a new game
# 3. a label, below the canvas and buttons, for status messages
#
def createGUI():
    global rootWindow
    global canvas
    global statusLabel
    global whichHeapEntry
    global numBallsEntry
    global placeholder
    global compWinLabel
    global playerWinLabel
    
    rootWindow = Tk()
    rootWindow.title("Play Nim")
    canvasAndGUI = Frame(rootWindow)
    canvas = Canvas(canvasAndGUI, height=canvasHeight, width=canvasWidth, relief=SUNKEN, borderwidth=2, background = 'black')
    canvas.pack(side=LEFT)
    guiFrame = Frame(canvasAndGUI)

    ballsFrame = Frame(guiFrame)
    takeLabel = Label(ballsFrame, text='Take')
    numBallsEntry = Entry(ballsFrame)
    ballsLabel = Label(ballsFrame, text='balls')
    takeLabel.pack(side=LEFT)
    numBallsEntry.pack(side=LEFT)
    ballsLabel.pack()
       
    heapFrame = Frame(guiFrame)
    heapLabel = Label(heapFrame, text='from heap')
    whichHeapEntry = Entry(heapFrame)
    heapLabel.pack(side=LEFT)
    whichHeapEntry.pack()
    
    #imageFrame = Frame(guiFrame)
    execButton = Button(guiFrame, text='Do it!', command=executePlayerMove)
    
    # add a "New Game!" button and
    # newGameButton = ...
    # replace the widget below with an Entry widget
    placeholder = Entry(guiFrame)
    newGameButton = Button(guiFrame, text = 'New Game', command = initializeNewGame)
    compWinLabel = Label(text = "Computer Wins: {}".format(NimGame.computerWins))
    playerWinLabel = Label (text = "Player Wins: {}".format(NimGame.playerWins))
    
    
    compWinLabel.pack()
    playerWinLabel.pack()
    ballsFrame.pack()
    heapFrame.pack()
    execButton.pack()
    newGameButton.pack()
    placeholder.pack()
    guiFrame.pack(side=RIGHT)
    canvasAndGUI.pack()
    statusLabel = Label(rootWindow)
    statusLabel.pack()
    
# Call 'runNim' with the desired number of initial balls
#
def runNim(initialHeaps):
    createGUI()
    initializeNimAndGUI(initialHeaps)   
    rootWindow.mainloop()



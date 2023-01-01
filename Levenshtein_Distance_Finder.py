from tkinter import *
from tkinter.font import Font
from PIL import ImageTk, Image
import numpy as np

def updateBox(background, cell, dpTable):
    j,i = cell
    box_size = 50
    padding = 20
    box_gap = 10
    y = (box_gap + box_size)*(j+1) + padding
    x = (box_gap + box_size)*(i+1) + padding
    arrow = {
        'n':'↖',
        'i':'↑',
        'd':'←',
        'r':'↖',
    }

    background.create_rectangle(x, y, x + box_size, y + box_size, fill = '#FF6A6A', outline = "")
    if (i == 0 and j == 0):
        text = dpTable[j,i][:-1]
    else:
        text = dpTable[j,i].replace(dpTable[j,i][-1], arrow[dpTable[j,i][-1]])
    background.create_text(x+box_size/2, y+box_size/2, text = text, font = textFont)
    root.update()

def writeInBox(x, y, cell, background):
    background.create_text(x, y, text = cell, font = textFont)
    root.update()

def printLevenshteinDistance(dist, background):
    background.create_text(w/2 + 360, h/2 - 300, text = "Number Of Changes will be : " + str(dist), font = textFont)
    root.update()

def getInput(str1, str2):
    s1 = str1.get()
    s2 = str2.get()
    if s1 == '' or s2 == '': 
        screenError = Toplevel(root)
        screenError.geometry("2750x110")
        screenError.title("Warning!")
        Label(screenError, text = "Please Enter Both strings Only").pack()
        Button(screenError, text = "OK", command = screenError.destroy).pack()

    elif (not(s1.isalpha()) or not(s2.isalpha())):
        screenError = Toplevel(root)
        screenError.geometry("275x110")
        screenError.title("Warning!")
        Label(screenError, text = "Please Enter Strings Only.").pack()
        Button(screenError, text = "OK", command = screenError.destroy).pack()

    else:
        tableCreate(s1.lower(), s2.lower())

def calcDpTable(s1, s2):
    table = np.zeros([len(s1)+1, len(s2)+1], dtype=np.dtype('U3'))
    for i in range(len(s1)+1):
        table[i,0] = str(i) + 'i'

    for j in range(len(s2)+1):
        table[0,j] = str(j) + 'd'

    for i in range(1, len(s1)+1):
        for j in range(1, len(s2)+1):
            if (s1[i-1] == s2[j-1]):
                table[i, j] = table[i-1, j-1][:-1] + 'n'
            else:
                if (min(int(table[i-1, j-1][:-1]), int(table[i-1, j][:-1]), int(table[i, j-1][:-1])) == int(table[i-1, j-1][:-1])):
                    table[i,j] = str(int(table[i-1, j-1][:-1]) + 1) + 'r'
                elif (min(int(table[i-1, j-1][:-1]), int(table[i-1, j][:-1]), int(table[i, j-1][:-1])) == int(table[i, j-1][:-1])):
                    table[i,j] = str(int(table[i, j-1][:-1]) + 1) + 'd'
                elif (min(int(table[i-1, j-1][:-1]), int(table[i-1, j][:-1]), int(table[i, j-1][:-1])) == int(table[i-1, j][:-1])):
                    table[i,j] = str(int(table[i-1, j][:-1]) + 1) + 'i'
    return table

def calcChangesInString(table, s1, s2):
    i = len(s1)
    j = len(s2)
    changes = [] 
    path = []    
    flag = 0 
    changing_string = list(s2)
    
    while (i >= 0):
        if (flag == 1):
            break
        while (j >= 0):
            if (table[i,j][-1] == 'n'): 
                path.append([i,j])
                j-=1
                i-=1
            elif (table[i,j][-1] == 'r'):
                statement1 = str(s2[j-1]).upper() + ' changes to ' + str(s1[i-1]).upper()
                changing_string[j-1] = s1[i-1]
                statement2 = 'Thus, now the string becomes: ' + ''.join(changing_string)
                changes.append([statement1,statement2])
                path.append([i,j])
                i-=1
                j-=1
            elif (table[i,j][-1] == 'i'):
                statement1 = 'Insert ' + str(s1[i-1]).upper() + ' at position ' + str(j+1) + ' in string'
                changing_string.insert(j, s1[i-1])
                statement2 = 'Thus, now the string becomes: ' + ''.join(changing_string)
                changes.append([statement1,statement2])
                path.append([i,j])
                i-=1
            elif (table[i,j][-1] == 'd'):
                statement1 = 'Remove ' + str(s2[j-1]).upper()
                del changing_string[j-1]
                statement2 = 'Thus, now the string becomes: ' + ''.join(changing_string)
                changes.append([statement1,statement2])
                path.append([i,j])
                j-=1
            if (len(changes) == int(table[len(s1), len(s2)][:-1])):
                flag = 1
                break
    
    return changes, path

def inputScreen():
    background = Canvas(root, bg = "#FFE1FF", width = w, height = h)
    background.grid(row=0, column=0)
    background.create_text(w/2, h/2 - 300, text = "Levenshtein Distance", font = headingFont)

    background.create_text(w/2 - 310, h/2 - 200, text = "Enter the 1st String: ", font = textFont)
    str1 = Entry(background)
    background.create_window(w/2 + 120, h/2 - 200, window = str1, width = w/4)

    background.create_text(w/2 - 250, h/2 - 100, text = "Enter the 2nd String: ", font = textFont)
    str2 = Entry(background)
    background.create_window(w/2 + 120, h/2 - 100, window = str2, width = w/4)
    
    b1 = Button(background, text = "Enter", bg = '#FA8072', activebackground = '#FFE5CC', command=lambda:getInput(str1, str2))
    background.create_window(w/2, h/2, window = b1, width = w/8)

def tableCreate(s1, s2):
    background = Canvas(root, bg = "#AB82FF", width = w, height = h)
    background.grid(row=0, column=0)
    box_size = 50
    box_gap = 10
    table_width = len(s1) + 2
    table_height = len(s2) + 2
    padding = 20
    animation_gap = 100
    arrow = {
        'n':'↖',
        'i':'↑',
        'd':'←',
        'r':'↖',
    }

    for i in range(table_height):
        for j in range(table_width):
            if ((i,j) == (0,0) or (i,j) == (1,0) or (i,j) == (0,1)):
                continue
            else:
                x = (box_gap + box_size)*i + padding
                y = (box_gap + box_size)*j + padding
                background.create_rectangle(x, y, x + box_size, y + box_size, fill = '#9fe9fa', outline = "")

    for i in range(table_height-2):
        x = (box_gap + box_size)*(i+2) + padding + box_size/2
        background.create_text(x, padding + box_size/2, text = s2[i].upper(), font = textFont)

    for i in range(table_width-2):
        y = (box_gap + box_size)*(i+2) + padding + box_size/2
        background.create_text(padding + box_size/2, y, text = s1[i].upper(), font = textFont)
    
    formulaOnCanvas = background.create_image(w/2 + 100, h/2 - 250, anchor=NW, image=formula)
    background.update()
    dpTable = calcDpTable(s1, s2) 

    for i in range(dpTable.shape[0]):
        for j in range(dpTable.shape[1]):
            if i == 0 or j == 0:
                x = (box_gap + box_size)*(j+1) + padding + box_size/2
                y = (box_gap + box_size)*(i+1) + padding + box_size/2
                if i == 0 and j == 0:
                    cell = dpTable[i,j][:-1]
                else:
                    cell = dpTable[i,j].replace(dpTable[i,j][-1], arrow[dpTable[i,j][-1]])
                background.create_text(x, y, text = cell, font = textFont)

    for i in range(dpTable.shape[0]):
        for j in range(dpTable.shape[1]):
            if not(i == 0 or j == 0):
                x = (box_gap + box_size)*(j+1) + padding + box_size/2
                y = (box_gap + box_size)*(i+1) + padding + box_size/2

                cell = dpTable[i,j].replace(dpTable[i,j][-1], arrow[dpTable[i,j][-1]])
                background.after(animation_gap, writeInBox(x,y,cell,background))
    printLevenshteinDistance(dpTable[table_width-2, table_height-2][:-1], background)

    b3 = Button(background, text = "Total Number of Changes IN Detail", bg = '#FFA54F', activebackground = '#FFE5CC', command=lambda:displayChangeList(background, dpTable, s1, s2, formulaOnCanvas, button, animation_gap))
    button = background.create_window(w/2 + 340, h/2 - 60, window = b3, width = w/8)

def displayChangeList(background, dpTable, s1, s2, formulaOnCanvas, b3, animation_gap):
    background.delete(b3)
    background.delete(formulaOnCanvas)
    background.update()
    background.create_image(w/2 + 40, h/2 - 300, anchor=NW, image=back_table)
    changes, path = calcChangesInString(dpTable, s1, s2)

    for cell in path:
        background.after(animation_gap, updateBox(background, cell, dpTable))

    if len(changes) == 0:
        background.create_text(w/2 + 350, h/2 - 30, text = "Both the Strings are Same, So NO Changes.", font = smallTextFont)
        i=1
    else:
        background.create_text(w/2 + 350, h/2 - 30, text = "The Changes to be made in '" + s2 + "' are:", font = textFont)
        for i in range(len(changes)):
            statement = str(i+1) + ". " + changes[i][0] + '. ' + changes[i][1]
            background.create_text(w/2 + 370, h/2 + i*30, text = statement, font = smallTextFont)
        i+=1

    b3 = Button(background, text = "Exit", bg = '#D15FEE', activebackground = '#FFE5CC', command=lambda:root.destroy())
    background.create_window(w/2 + 450, h/2 + i*32, window = b3, width = w/8)
  
if __name__ == "__main__":
    root = Tk()
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    root.geometry("%dx%d" % (w, h))
    root.title("Levenshtein Distance Finder")

    smallTextFont = Font(family = 'Bookman Old Style', size = '12')
    textFont = Font(family = 'Bookman Old Style', size = '15')
    headingFont = Font(family = 'Bookman Old Style', size = '30')

    formula = Image.open("M:\Levenshtein Distance Finder\img\Formula.png")
    formula = formula.resize((500, 128), Image.ANTIALIAS)
    formula = ImageTk.PhotoImage(formula)

    back_table = Image.open("M:\Levenshtein Distance Finder\img\Square_Function.png")
    back_table = back_table.resize((600, 300), Image.ANTIALIAS)
    back_table = ImageTk.PhotoImage(back_table)

    inputScreen()
    root.mainloop()

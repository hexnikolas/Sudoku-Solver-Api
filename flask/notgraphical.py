#import numpy as np
import traceback
import sys
import time

## TODO: sixth stage : x-wing, skyscraper techniques

class Sudoku():

    #init the puzzle
    def __init__(self) -> None:
        #number of unsolved cells
        self.unsolved = 0

        #the puzzle
        self.sudoku = []

        #flags for stages execution
        self.third_flag = False
        self.fourth_flag = False
        self.fifth_flag = False


    #load puzzle from file, each line is a puzzle stored like following
    #.8..1......5....3.......4.....6.5.7.89....2.....3.....2.....1.9..67........4.....
    #dots or zeros denote empty cells
    def create_sudoku_puzzle(self, text):

        sudoku_array = []
        self.unsolved=0
        i=0
        for char in text:
            if char=='\n':
                pass
            else:
                if char==".":
                    self.unsolved+=1
                    char="0"
                sudoku_array.append(int(char))

        self.sudoku = [sudoku_array[x:x+9] for x in range(0, len(sudoku_array), 9)]
        self.show_puzzle()

        return str(self.sudoku)


    #in the first stage, every possible number is put in the empty cells
    def first_stage(self):
        for i in range(9):
            for j in range(9):
                if self.sudoku[i][j]==0:
                    self.sudoku[i][j]=[1,2,3,4,5,6,7,8,9]

        return self.sudoku


    #in the second stage, the most basic elimination rule of sudoku is applied, a line, column, and box, can't have the same digit twice
    #So for each given number in the puzzle, the same numbers in the line, column and box are removed
    def second_stage(self):
        for i in range(9):
            for j in range(9):
                if isinstance(self.sudoku[i][j], int):
                    self.sudoku = self.remove_from_box(i, j, self.sudoku[i][j])
                    self.sudoku = self.remove_from_line(i, self.sudoku[i][j])
                    self.sudoku = self.remove_from_column(j, self.sudoku[i][j])
        return self.sudoku


    #iterate over the lines, columns and boxes
    #if a number in a line, column or box has only one possible cell, then it's certain that it goes there
    def third_stage(self):
        self.third_flag=True
        while self.third_flag and self.unsolved!=0:
            self.third_flag=False
            #check the lines for unique numbers
            for i in range(9):
                line = []
                possiblepairs = []
                for x in self.sudoku[i]:
                    if isinstance(x, list):
                        line+=x
                while len(line)>0:
                    y=line[0]
                    if line.count(y)==1:
                        for counter,item in enumerate(self.sudoku[i]):
                            if isinstance(item, list):
                                if y in item:
                                    self.sudoku[i][counter]=y
                                    self.unsolved-=1
                                    self.third_flag=True
                                    self.fourth_flag = True
                                    self.fifth_flag = True
                                    print(f"only in row found [{i},{counter}]={self.sudoku[i][counter]}")
                                    self.remove_from_box(i, counter , self.sudoku[i][counter])
                                    self.remove_from_line( i, self.sudoku[i][counter])
                                    self.remove_from_column(counter, self.sudoku[i][counter])
                    elif line.count(y)<4:
                        possiblepairs.append(y)


                    line = list(filter((y).__ne__, line))

                if len(possiblepairs)>2:
                    index = 0
                    possiblepairspositions = [None] * len(possiblepairs)
                    for number in possiblepairs:
                        pos = []
                        for jj in range(9):
                            try:
                                if number in self.sudoku[i][jj]:
                                    pos.append(jj)
                            except TypeError:
                                pass
                            except AttributeError:
                                pass
                        possiblepairspositions[index]=pos
                        index += 1


                    while len(possiblepairspositions)>0:
                        numbers=[]
                        key_a = max(possiblepairspositions, key=len)
                        if len(key_a)>2:
                            for spot, abc in enumerate(possiblepairspositions):
                                if set(key_a)>=set(abc):
                                    numbers.append(possiblepairs[spot])
                            if len(numbers)==len(key_a):
                                same_box = [int(asd/3) for asd in key_a]
                                if not (self.all_equal(same_box)):
                                    self.remove_pairs_from_row(i, key_a, numbers)
                        possiblepairspositions.pop(0)
                        possiblepairs.pop(0)



            #check columns for unique values
            for j in range(9):
                sudo = [row[j] for row in self.sudoku]
                column=[]
                possiblepairss=[]
                for z in sudo:
                    if isinstance(z,list):
                        column+=z
                while len(column)>0:
                    k=column[0]
                    if column.count(k)==1:
                        for counters,items in enumerate(sudo):
                            if isinstance(items, list):
                                if k in items:
                                    self.sudoku[counters][j]=k
                                    self.third_flag=True
                                    self.fourth_flag = True
                                    self.fifth_flag = True
                                    self.unsolved-=1
                                    print(f"only in column found [{counters},{j}]={self.sudoku[counters][j]}")
                                    self.remove_from_box(counters, j ,self.sudoku[counters][j])
                                    self.remove_from_line(counters, self.sudoku[counters][j])
                                    self.remove_from_column(j, self.sudoku[counters][j])
                    elif column.count(k)<4:
                        possiblepairss.append(k)

                    column = list(filter((k).__ne__, column))

                if len(possiblepairss)>2:
                    index = 0
                    possiblepairspositionss = [None] * len(possiblepairss)
                    for number in possiblepairss:
                        pos = []
                        for ii in range(9):
                            try:
                                if number in self.sudoku[ii][j]:
                                    pos.append(ii)
                            except TypeError:
                                pass
                            except AttributeError:
                                pass
                        possiblepairspositionss[index]=pos
                        index += 1

                    while len(possiblepairspositionss)>0:
                        numbers=[]
                        key_b = max(possiblepairspositionss, key=len)
                        if len(key_b)>2:
                            for spot, abc in enumerate(possiblepairspositionss):
                                if set(key_b)>=set(abc):
                                    numbers.append(possiblepairss[spot])
                            if len(numbers)==len(key_b):
                                same_box = [int(asd/3) for asd in key_b]
                                if not (self.all_equal(same_box)):
                                    self.remove_pairs_from_column(j, key_b, numbers)
                        possiblepairspositionss.pop(0)
                        possiblepairss.pop(0)


            #check boxes for unique values
            for i in range(3):
                for j in range(3):
                    box=[]
                    for ii in range(3*i,3*i+3):
                        for jj in range(3*j,3*j+3):
                            if isinstance(self.sudoku[ii][jj], list):
                                box+=self.sudoku[ii][jj]
                    for l in box:
                        if box.count(l)==1:
                            for ii in range(3*i,3*i+3):
                                for jj in range(3*j,3*j+3):
                                    if isinstance(self.sudoku[ii][jj], list):
                                        if l in self.sudoku[ii][jj]:
                                            self.sudoku[ii][jj]=l
                                            self.third_flag=True
                                            self.fourth_flag = True
                                            self.fifth_flag = True
                                            self.unsolved-=1
                                            print(f"only in box found [{ii},{jj}]={self.sudoku[ii][jj]}")
                                            self.remove_from_box(ii, jj , self.sudoku[ii][jj])
                                            self.remove_from_line(ii, self.sudoku[ii][jj])
                                            self.remove_from_column(jj, self.sudoku[ii][jj])
                        else:
                            box = list(filter((l).__ne__, box))


    #in fourth stage we eliminate the 'shadow numbers'
    #for example, if number 2 can only be in two cells in the same row of the same box, the rest of the line, can't have that number
    def fourth_stage(self):
        self.fourth_flag=True
        while self.fourth_flag and self.unsolved!=0:
            self.fourth_flag=False

            #find shadow numbers in columns and rows of boxes
            for i in range(3):
                for j in range(3):
                    pairsthatmatch=[]
                    tripsthatmatch=[]
                    box=[]
                    for ii in range(3*i,3*i+3):
                        for jj in range(3*j,3*j+3):
                            try:
                                box.extend(self.sudoku[ii][jj])
                            except TypeError:
                                pass

                    #check the first number of the list, if that number can go to two or three cells, we keep it
                    while len(box)>0:
                        l=box[0]
                        if box.count(l)==2:
                            pairs=[]
                            for ii in range(3*i,3*i+3):
                                for jj in range(3*j,3*j+3):
                                    try:
                                        if l in self.sudoku[ii][jj]:
                                            pairs.append([ii,jj])
                                    except TypeError:
                                        pass
                            pairsthatmatch.append([pairs,l])
                            try:
                                if pairs[0][0]==pairs[1][0]:
                                    #if both of them are in the same line, we remove it from the rest of the line
                                    self.remove_shadow_from_line(pairs[0][0], int(pairs[0][1]/3), l)
                                elif pairs[0][1]==pairs[1][1]:
                                    #if both of them are in the same column, we remove it from the rest of the column
                                    self.remove_shadow_from_column(pairs[0][1], int(pairs[1][0]/3), l)
                            except IndexError:
                                pass

                        elif box.count(l)==3:
                            pairs=[]
                            for ii in range(3*i,3*i+3):
                                for jj in range(3*j,3*j+3):
                                    try:
                                        if l in self.sudoku[ii][jj]:
                                            pairs.append([ii,jj])
                                    except TypeError:
                                        pass
                            tripsthatmatch.append([pairs,l])
                            try:
                                if pairs[0][0]==pairs[1][0]==pairs[2][0]:
                                    #if all three of them are in the same line, we remove it from the rest of the line
                                    self.remove_shadow_from_line(pairs[0][0], int(pairs[0][1]/3), l)
                                elif pairs[0][1]==pairs[1][1]==pairs[2][1]:
                                    #if all three of them are in the same column, we remove it from the rest of the column
                                    self.remove_shadow_from_column(pairs[0][1], int(pairs[1][0]/3), l)
                            except IndexError:
                                pass


                        box = list(filter((l).__ne__, box))

                    #if we find two numbers that only go to the same two cells, we remove the rest numbers from these two cells
                    while len(pairsthatmatch)>1:
                        eye=pairsthatmatch[0]
                        for key in pairsthatmatch:
                            if eye[0]==key[0] and eye[1]!=key[1]:
                                if not len(self.sudoku[eye[0][0][0]][eye[0][0][1]])==len(self.sudoku[eye[0][1][0]][eye[0][1][1]])==2:
                                    self.remove_shadow_from_box(eye[0][0], eye[0][1], eye[1], key[1])
                        pairsthatmatch.pop(0)


                    #same for three numbers in three cells
                    pos=0
                    while pos<len(tripsthatmatch):
                        matches=0
                        eye=tripsthatmatch[pos]
                        for key in tripsthatmatch:
                            if eye[0]==key[0] and eye[1]!=key[1]:
                                matches+=1
                        if matches<2:
                            tripsthatmatch.pop(0)
                        else:
                            self.remove_trips_shadows_from_box(tripsthatmatch[pos][0],[key[1] for key in tripsthatmatch if key[0]==tripsthatmatch[pos][0]])
                            tripsthatmatch.pop(pos)

            self.third_stage()
        return self.sudoku

    def fifth_stage(self):
        self.fifth_flag = True
        x_wing= {}
        while self.fifth_flag and self.unsolved!=0:
            self.fifth_flag = False
            for i in range(9):
                line = []
                line_two = []
                for x in self.sudoku[i]:
                    if isinstance(x, list):
                        line.append(x)
                        line_two.extend(x)
                while len(line)>0:#for item in line:
                    item = line[0]
                    if line.count(item)>1:
                        positions=[]
                        for pos,x in enumerate(self.sudoku[i]):
                            if item == x:
                                positions.append(pos)
                                #print(x,pos)
                        #print(positions)
                        if len(positions)==2:
                            if int(positions[0]/3)!=int(positions[1]/3):
                                print(f'match found in row {i} positions {positions} and numbers {item}')
                                self.remove_pair_from_line(i, positions, item)
                        elif len(positions)==3:
                            print(f'three match found {item}')
                    line = list(filter((item).__ne__, line))

                while len(line_two)>0:
                    number = line_two[0]
                    position=[]
                    if line_two.count(number)==2 or line_two.count(number)==3:
                        for j in range(9):
                            try:
                                if number in self.sudoku[i][j]:
                                    position.append(j)
                            except TypeError:
                                pass
                        boxes = [int(k/3) for k in position]
                        if all(x==boxes[0] for x in boxes) and boxes:
                            self.remove_ghost_from_box_line(position, i, number)
                    line_two = list(filter((number).__ne__, line_two))


            #Έλεγχος των στηλών για μοναδικές τιμές
            for j in range(9):
                sudo = [row[j] for row in self.sudoku]
                column=[]
                column_two=[]
                for z in sudo:
                    if isinstance(z,list):
                        column.append(z)
                        column_two.extend(z)
                #print(column)
                while len(column)>0:
                    item = column[0]
                    if len(item)<4:
                        if column.count(item)>1:
                            positions=[]
                            for y in range(9):
                                if item==self.sudoku[y][j]:
                                    positions.append(y)
                            if len(positions)==2:
                                if not int(positions[0]/3)==int(positions[1]/3):
                                    self.remove_pair_from_column(j, positions, item)
                            #elif len(positions)==3:
                                #print(f'three column match found {item}')

                    column = list(filter((item).__ne__, column))

                while len(column_two)>0:
                    number = column_two[0]
                    position=[]
                    if column_two.count(number)==2 or column_two.count(number)==3:
                        for i in range(9):
                            try:
                                if number in self.sudoku[i][j]:
                                    position.append(i)
                            except TypeError:
                                pass
                        boxes = [int(k/3) for k in position]
                        if all(x==boxes[0] for x in boxes) and len(position)>0:
                            self.remove_ghost_from_box_column(position, j, number)
                    column_two = list(filter((number).__ne__, column_two))

            self.fourth_stage()

    def remove_shadow_from_box(self, spot1, spot2, number1, number2):
        print(f'found shadow in box {number1},{number2} in {spot1[0]},{spot1[1]} and {spot2[0]},{spot2[1]}')
        for i in range(1,10):
            if i!=number1 and i!=number2:
                try:
                    self.sudoku[spot1[0]][spot1[1]].remove(i)
                    print(f'removed {i} from position {spot1[0]},{spot1[1]}')
                    self.fourth_flag=True
                    self.fifth_flag = True
                    if len(self.sudoku[spot1[0]][spot1[1]])==1:
                        self.unsolved-=1
                        self.sudoku[spot1[0]][spot1[1]]=self.sudoku[spot1[0]][spot1[1]][0]
                        print(f"found [{spot1[0]},{spot1[1]}]={sudoku[spot1[0]][spot1[1]]}")
                        remove_from_box(spot1[0], spot1[1] , self.sudoku[spot1[0]][spot1[1]])
                        remove_from_line(spot1[0], self.sudoku[spot1[0]][spot1[1]])
                        remove_from_column(spot1[1], self.sudoku[spot1[0]][spot1[1]])
                except ValueError:
                    pass
                except AttributeError:
                    pass
                try:
                    self.sudoku[spot2[0]][spot2[1]].remove(i)
                    print(f'removed {i} from position {spot2[0]},{spot2[1]}')
                    self.fourth_flag = True
                    self.fifth_flag = True
                    if len(self.sudoku[spot2[0]][spot2[1]])==1:
                        #print(sudoku[spot2[0]][spot2[1]])
                        self.sudoku[spot2[0]][spot2[1]]=self.sudoku[spot2[0]][spot2[1]][0]
                        print(f"found [{spot2[0]},{spot2[1]}]={sudoku[spot2[0]][spot2[1]]}")
                        self.remove_from_box(spot2[0], spot2[1] , self.sudoku[spot2[0]][spot2[1]])
                        self.remove_from_line(spot2[0], self.sudoku[spot2[0]][spot2[1]])
                        self.remove_from_column(spot2[1], self.sudoku[spot2[0]][spot2[1]])
                except ValueError:
                    pass
                except AttributeError:
                    pass

    def remove_shadow_from_line(self, line, box, number):
        print(f'found shadow number {number} in line {line} and box {box}')
        for i in range(3):
            if i!=box:
                for ii in range(3*i,3*i+3):
                    try:
                        self.sudoku[line][ii].remove(number)
                        print(f'removed {number} from position {line},{ii}')
                        self.fourth_flag=True
                        if len(self.sudoku[line][ii])==1:
                            self.unsolved-=1
                            self.sudoku[line][ii]=self.sudoku[line][ii][0]
                            print(f"found [{line},{ii}]={self.sudoku[line][ii]}")
                            self.remove_from_box(line, ii , self.sudoku[line][ii])
                            self.remove_from_line(line, self.sudoku[line][ii])
                            self.remove_from_column(ii, self.sudoku[line][ii])
                    except ValueError:
                        pass
                    except AttributeError:
                        pass

    def remove_shadow_from_column(self, column, box, number):
        for i in range(3):
            if i!=box:
                for ii in range(3*i, 3*i+3):
                    try:
                        self.sudoku[ii][column].remove(number)
                        print(f'removed {number} from position {ii},{column}')
                        self.fourth_flag=True
                        self.fifth_flag = True
                        if len(self.sudoku[ii][column])==1:
                            self.unsolved-=1
                            self.sudoku[ii][column]=self.sudoku[ii][column][0]
                            print(f"found [{ii},{column}]={self.sudoku[ii][column]}")
                            self.remove_from_box(ii, column , self.sudoku[ii][column])
                            self.remove_from_line(ii, self.sudoku[ii][column])
                            self.remove_from_column(column, self.sudoku[ii][column])
                    except ValueError:
                        pass
                    except AttributeError:
                        pass

    def remove_trips_shadows_from_box(self, cells, keys):
        print(f'found triple {keys} in {cells}')
        for cell in cells:
            for i in range(1,10):
                if i not in keys:
                    try:
                        self.sudoku[cell[0]][cell[1]].remove(i)
                        print(f'removed {i} from position {cell[0]},{cell[1]}')
                        if len(self.sudoku[cell[0]][cell[1]])==1:
                            self.unsolved-=1
                            print(f"only in cell found (trips) [{ii},{jj}]={self.sudoku[cell[0]][cell[1]][0]}")
                            self.sudoku[cell[0]][cell[1]]=self.sudoku[cell[0]][cell[1]][0]
                            self.remove_from_box(cell[0],cell[1],self.sudoku[cell[0]][cell[1]])
                            self.remove_from_line(cell[0],self.sudoku[cell[0]][cell[1]])
                            self.remove_from_column(cell[1],self.sudoku[cell[0]][cell[1]])
                    except TypeError:
                        pass
                    except ValueError:
                        pass

    def remove_ghost_from_box_line(self, columns, line, number):
        print(f'found number {number} in line box {line} and columns {columns}')
        box_row = int(line/3)
        box_column = int(columns[0]/3)
        for i in range(3*box_row, 3*box_row+3):
            for j in range(3*box_column, 3*box_column+3):
                if line!=i:
                    try:
                        self.sudoku[i][j].remove(number)
                        self.fifth_flag = True
                        print(f'ghost line removed {number} from {i} {j}')
                        if len(self.sudoku[i][j])==1:
                            self.unsolved-=1
                            print(f"only in cell found [{i},{j}]={self.sudoku[i][j][0]}")
                            self.sudoku[i][j]=self.sudoku[i][j][0]
                            self.remove_from_box(i , j , self.sudoku[i][j])
                            self.remove_from_line(i, self.sudoku[i][j])
                            self.remove_from_column(j, self.sudoku[i][j])
                    except TypeError:
                        pass
                    except ValueError:
                        pass
                    except AttributeError:
                        pass
                else:
                    if j not in columns:
                        try:
                            self.sudoku[i][j].remove(number)
                            print(f'ghost line removed {number} from {i} {j}')
                            self.fifth_flag = True
                            if len(self.sudoku[i][j])==1:
                                self.unsolved-=1
                                print(f"only in cell found [{i},{j}]={self.sudoku[i][j][0]}")
                                self.sudoku[i][j]=self.sudoku[i][j][0]
                                self.remove_from_box(i , j , self.sudoku[i][j])
                                self.remove_from_line(i, self.sudoku[i][j])
                                self.remove_from_column(j, self.sudoku[i][j])
                        except TypeError:
                            pass
                        except ValueError:
                            pass
                        except AttributeError:
                            pass

    def remove_ghost_from_box_column(self, lines, column, number):
        print(f'found number {number} in box lines {lines} and column {column}')
        box_row = int(lines[0]/3)
        box_column = int(column/3)
        for i in range(3*box_row, 3*box_row+3):
            for j in range(3*box_column, 3*box_column+3):
                if j!=column:
                    try:
                        self.sudoku[i][j].remove(number)
                        self.fifth_flag = True
                        print(f'ghost column removed {number} from {i} {j}')
                        if len(self.sudoku[i][j])==1:
                            self.unsolved-=1
                            print(f"only in cell found [{i},{j}]={self.sudoku[i][j][0]}")
                            self.sudoku[i][j]=self.sudoku[i][j][0]
                            self.remove_from_box(i , j , self.sudoku[i][j])
                            self.remove_from_line(i, self.sudoku[i][j])
                            self.remove_from_column(j, self.sudoku[i][j])
                    except TypeError:
                        pass
                    except ValueError:
                        pass
                    except AttributeError:
                        pass
                else:
                    if i not in lines:
                        try:
                            self.sudoku[i][j].remove(number)
                            print(f'ghost column removed {number} from {i} {j}')
                            if len(self.sudoku[i][j])==1:
                                self.unsolved-=1
                                print(f"only in cell found [{i},{j}]={self.sudoku[i][j][0]}")
                                self.sudoku[i][j]=self.sudoku[i][j][0]
                                self.remove_from_box(i , j , self.sudoku[i][j])
                                self.remove_from_line(i, self.sudoku[i][j])
                                self.remove_from_column(j, self.sudoku[i][j])
                        except TypeError:
                            pass
                        except ValueError:
                            pass
                        except AttributeError:
                            pass

    #fixed output
    def remove_from_box(self, i, j, number):
        i = int(i/3)
        j = int(j/3)
        for ii in range(3*i,3*i+3):
            for jj in range(3*j, 3*j+3):
                try:
                    self.sudoku[ii][jj].remove(number)
                    if len(self.sudoku[ii][jj])==1:
                        self.unsolved-=1
                        print(f"only possible value in cell found [{ii},{jj}]={self.sudoku[ii][jj][0]}")
                        self.sudoku[ii][jj]=self.sudoku[ii][jj][0]
                        self.remove_from_box(ii,jj,self.sudoku[ii][jj])
                        self.remove_from_line(ii,self.sudoku[ii][jj])
                        self.remove_from_column(jj,self.sudoku[ii][jj])
                except AttributeError:
                    #Found an int instead of a list
                    pass
                except ValueError:
                    #Number not found in list
                    pass

        return self.sudoku

    #fixed output
    def remove_from_line(self, i , number):
        for j in range(9):
            try:
                self.sudoku[i][j].remove(number)
                if len(self.sudoku[i][j])==1:
                    self.unsolved-=1
                    print(f"only possible value in cell found [{i},{j}]={self.sudoku[i][j][0]}")
                    self.sudoku[i][j]=self.sudoku[i][j][0]
                    self.remove_from_box(i , j , self.sudoku[i][j])
                    self.remove_from_line(i, self.sudoku[i][j])
                    self.remove_from_column(j, self.sudoku[i][j])
            except AttributeError:
                #Found an int instead of a list
                pass
            except ValueError:
                #Number not found in list
                pass
        return self.sudoku

    #fixed output
    def remove_from_column(self, j, number):
        for i in range(9):
            try:
                self.sudoku[i][j].remove(number)
                if len(self.sudoku[i][j])==1:
                    self.unsolved-=1
                    print(f"only possible value in cell found [{i},{j}]={self.sudoku[i][j][0]}")
                    self.sudoku[i][j]=self.sudoku[i][j][0]
                    self.remove_from_box(i , j , self.sudoku[i][j])
                    self.remove_from_line(i, self.sudoku[i][j])
                    self.remove_from_column(j, self.sudoku[i][j])
            except AttributeError:
                #Found an int instead of a list
                pass
            except ValueError:
                #Number not found in list
                pass
        return self.sudoku

    def remove_pair_from_line(self, line, columns, numbers):
        print(f'found pair {numbers} in line {line} and columns {columns}')
        for j in range(9):
            if isinstance(self.sudoku[line][j], list) and self.sudoku[line][j] != numbers:
                for number in numbers:
                    try:
                        self.sudoku[line][j].remove(number)
                        self.fifth_flag = True
                        print(f'removed {number} from [{line},{j}]')
                        if len(self.sudoku[line][j])==1:
                            self.unsolved-=1
                            print(f"only possible value in cell found [{line},{j}]={self.sudoku[line][j][0]}")
                            self.sudoku[line][j]=self.sudoku[line][j][0]
                            self.remove_from_box(line , j , self.sudoku[line][j])
                            self.remove_from_line(line, self.sudoku[line][j])
                            self.remove_from_column(j, self.sudoku[line][j])
                    except ValueError:
                        pass
                    except AttributeError:
                        pass

    def remove_pair_from_column(self, column, rows, numbers):
        print(f'found pair {numbers} in line {rows} and column {column}')
        for i in range(9):
            if isinstance(self.sudoku[i][column], list) and self.sudoku[i][column]!=numbers:
                for number in numbers:
                    try:
                        self.sudoku[i][column].remove(number)
                        self.fifth_flag = True
                        print(f'removed {number} from [{i}{column}]')
                        if len(self.sudoku[i][column])==1:
                            self.unsolved-=1
                            print(f"only possible value in cell found [{i},{column}]={self.sudoku[i][column][0]}")
                            self.sudoku[i][column]=self.sudoku[i][column][0]
                            self.remove_from_box(i , column , self.sudoku[i][column])
                            self.remove_from_line(i, self.sudoku[i][column])
                            self.remove_from_column(column, self.sudoku[i][column])
                    except ValueError:
                        pass
                    except AttributeError:
                        pass

    def remove_pairs_from_row(self, i, columns, numbers):
        print(f'pair found {numbers} in row {i} and columns {columns} ')
        for j in columns:
            for number in range(1,10):
                if number not in numbers:
                    try:
                        self.sudoku[i][j].remove(number)
                        print(f'removed {number} from position {i},{j}')
                        self.third_flag = True
                        self.fourth_flag = True
                        self.fifth_flag = True

                    except ValueError:
                        pass
                    except AttributeError:
                        pass

    def remove_pairs_from_column(self, j, rows, numbers):
        print(f'pair found {numbers} in rows {rows} and column {j} ')
        for i in rows:
            for number in range(1,10):
                if number not in numbers:
                    try:
                        self.sudoku[i][j].remove(number)
                        self.third_flag = True
                        self.fourth = True
                        self.fifth_flag = True
                        print(f'removed {number} from position {i},{j}')
                    except ValueError:
                        pass
                    except AttributeError:
                        pass

    def all_equal(self, iterator):
        iterator = iter(iterator)
        try:
            first = next(iterator)
        except StopIteration:
            return True
        return all(first == x for x in iterator)

    def show_puzzle(self):
        for i in self.sudoku:
            print(i)
            #print()

    def return_result(self):
        result = [item for sublist in self.sudoku for item in sublist]
        return result


if __name__=="__main__":
    print('Script started')

    puzzle = Sudoku()

    puzzle.load_sudoku_puzzle()
    puzzle.first_stage()
    puzzle.second_stage()
    print('third stage')
    puzzle.third_stage()
    if puzzle.unsolved != 0:
        print('fourth stage')
        puzzle.fourth_stage()
    if puzzle.unsolved != 0:
        print('fifth stage')
        puzzle.fifth_stage()

    puzzle.show_puzzle()

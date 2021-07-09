import pygame
import math
from pygame.locals import*
from random import*
#import random
import os
from queue import PriorityQueue
import heapq

pygame.init()
WIDTH=20
white=(255,255,255)
grey=(192,192,192,192)
black = (0,0,0)
blue = (0,0,205)
red=(255,0,0)
yellow = (255, 255, 0)
purple = (102,0,102)
win=pygame.display.set_mode((800,800))
win.fill(white)
class Vertex:

	def __init__(self,row,col):
		self.width=20
		self.row=row
		self.col=col
		self.y=self.row*self.width
		self.x=self.col*self.width
		self.start=False
		self.end=False
		self.wall=False
		self.neighbors=[]
		self.opened=False
		self.closed=False
		self.prev=None
		self.h=float('inf')
		self.g=float('inf')
		self.f=float('inf')
		self.color=white
		self.g_neighbors=[]
		

	def printself(self):
		print(self.row,self.col)
		# print(self.x,self.y)
		# print(self.color)
		print(self.h,self.g,self.f)
		#print(self.neighbors)
		# for i in self.neighbors:
		# 	print(i.row,i.col)

	def calch(self,endpoint):
		if self.wall==True:
			return
		else:
			self.h= ((self.row-endpoint.row)**2+(self.col-endpoint.col)**2)**(1/2)

	def calcf(self):
		self.f=self.h+self.g 
		return

	def update_neighbors(self,mat):
		self.neighbors=[]
		if self.wall==True:
			return
		if self.row<29:
			if mat[self.row+1][self.col].wall==False:
				self.neighbors.append(mat[self.row+1][self.col])
		if self.row>0:
			if mat[self.row-1][self.col].wall==False:
				self.neighbors.append(mat[self.row-1][self.col])
		if self.col<39:
			if mat[self.row][self.col+1].wall==False:
				self.neighbors.append(mat[self.row][self.col+1])
		if self.col>0:
			if mat[self.row][self.col-1].wall==False:
				self.neighbors.append(mat[self.row][self.col-1])

	def generate_neighbors(self,mat):
		self.g_neighbors=[]

		if self.row<29:
			if mat[self.row+1][self.col].wall==False:
				self.g_neighbors.append(mat[self.row+1][self.col])
		if self.row>0:
			if mat[self.row-1][self.col].wall==False:
				self.g_neighbors.append(mat[self.row-1][self.col])
		if self.col<39:
			if mat[self.row][self.col+1].wall==False:
				self.g_neighbors.append(mat[self.row][self.col+1])
		if self.col>0:
			if mat[self.row][self.col-1].wall==False:
				self.g_neighbors.append(mat[self.row][self.col-1])



	def reset(self):
		self.start=False
		self.end=False
		self.wall=False
		self.neighbors=[]
		self.opened=False
		self.closed=False
		self.prev=None
		self.h=float('inf')
		self.g=float('inf')
		self.f=float('inf')
		self.color=white
		self.g_neighbors=[]

	def __lt__(self,other):
		return self.f < other.f


class button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.active=False
        self.clicked=False

    def draw(self):
        #Call this method to draw the button on the screen

        pos =pygame.mouse.get_pos()
        button_rect = Rect(self.x, self.y, self.width, self.height)


        if button_rect.collidepoint(pos):
        	if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
        		self.clicked=True
        	elif pygame.mouse.get_pressed()[0]==0 and self.clicked==True:	
        		if self.active==False:
	        		self.active=True
	        		#self.color=grey
	        		self.clicked=False
	        	else:
	        		self.active=False
	        		#self.color=white
	        		self.clicked=False
        if self.active==True:
        	self.color=grey
        else:
        	self.color=white	    


        pygame.draw.rect(win, black, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 25)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

  


    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

class clickbutton(button):
	def __init__(self, color, x,y,width,height, text=''):
		self.color = color
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.text = text
		self.active=False
		self.clicked=False

	def draw(self):
		pos =pygame.mouse.get_pos()
		button_rect = Rect(self.x, self.y, self.width, self.height)


		if button_rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
				self.clicked=True
			elif pygame.mouse.get_pressed()[0]==0 and self.clicked==True:	
				if self.active==False:
					self.active=True
					#self.color=grey
					self.clicked=False
				

		if self.clicked==True:
			self.color=grey
		else:
			self.color=white	    


		pygame.draw.rect(win, black, (self.x-2,self.y-2,self.width+4,self.height+4),0)
		    
		pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)

		if self.text != '':
			font = pygame.font.SysFont('comicsans', 25)
			text = font.render(self.text, 1, (0,0,0))
			win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))




class Grid:
	def __init__(self,row=None,col=None):
		if row==None:
			self.row=30
		else:
			self.row=row
			

		if col==None:
			self.col=40
		else:
			self.col=col

		self.startpoint=None
		self.endpoint=None

		self.mat=[[Vertex(i,j) for j in range(self.col)] for i in range(self.row)]
		self.generate=clickbutton(white,25,625,100,50,'Generate')
		self.wall_editor=button(white,25,700,100,50,'Wall')
		self.startbutton=button(white,175,625,100,50,'Start')
		self.endbutton=button(white,175,700,100,50,'End')
		self.Asearch=button(white,600,625,100,50,'A* search')
		self.clearbutton=clickbutton(white,600,700,100,50,'Clear')
		self.count=1200
		self.clear_list=[]
		self.g_set=[]
		self.wall_list=[]


	def make_wall(self,row,col):
		if self.startpoint==self.mat[row][col]:
			self.mat[row][col].reset()
			self.startpoint=None
		if self.endpoint==self.mat[row][col]:
			self.mat[row][col].reset()
			self.endpoint=None

		self.mat[row][col].reset()
		self.mat[row][col].wall=True
		self.mat[row][col].color=black

	def make_start(self,row,col):
		if self.startpoint != None:
			self.startpoint.reset()

		if self.startpoint==self.endpoint:
			self.mat[row][col].reset()
			self.endpoint=None

		self.mat[row][col].reset()
		self.startpoint=self.mat[row][col]
		self.mat[row][col].start=True
		self.mat[row][col].color=blue

		
	def make_end(self,row,col):
		if self.endpoint != None:
			self.endpoint.reset()

		if self.startpoint==self.endpoint:
			self.mat[row][col].reset()
			self.startpoint=None

		self.mat[row][col].reset()
		self.endpoint=self.mat[row][col]
		self.mat[row][col].end=True
		self.mat[row][col].color=red

	def clearfn(self):
		self.startpoint=None
		self.endpoint=None
		self.clear_list=[]
		self.g_set=[]
		self.wall_list=[]
		self.count=1200
		self.reset_neighbor()
		for i in range(self.row):
			for j in range(self.col): 
				square=self.mat[i][j]
				square.reset()

	def reset_neighbor(self):
		for i in range(self.row):
			for j in range(self.col): 
				square=self.mat[i][j]
				square.neighbors=[]
				square.g_neighbors=[]
	def drawgrid(self):

		if pygame.mouse.get_pressed()[0]==1:
			pos =pygame.mouse.get_pos()
			if (self.wall_editor.isOver(pos)):
				self.startbutton.active=False
				self.endbutton.active=False
			elif (self.startbutton.isOver(pos)):
				self.wall_editor.active=False
				self.endbutton.active=False
			elif (self.endbutton.isOver(pos)):
				self.wall_editor.active=False
				self.startbutton.active=False

		if pygame.mouse.get_pressed()[0]==0 and self.clearbutton.active==True and self.clearbutton.clicked==False:
			self.clearfn()
			self.clearbutton.active=False

		if pygame.mouse.get_pressed()[0]==0 and self.generate.active==True and self.generate.clicked==False:
			self.clearfn()
			self.generatefn()
			# for i in range(self.row):
			# 	for j in range(self.col):
			# 		if (random()<0.3):
			# 			self.make_wall(i,j)
			self.generate.active=False
			

		self.drawboard()


		self.generate.draw()
		self.wall_editor.draw()
		self.startbutton.draw()
		self.endbutton.draw()
		self.Asearch.draw()
		self.clearbutton.draw()
		pygame.display.update()

	def clear_left(self,square,count,clear_list):
		if square.col>0:
			if self.mat[square.row][square.col-1].wall==True:
				self.mat[square.row][square.col-1].reset()
				self.clear_list.append(self.mat[square.row][square.col-1])
				self.count=self.count-1
				return True

	def clear_right(self,square,count,clear_list):
		if square.col<39:
			if self.mat[square.row][square.col+1].wall==True:
				self.mat[square.row][square.col+1].reset()
				self.clear_list.append(self.mat[square.row][square.col+1])
				self.count=self.count-1
				return True

	def clear_up(self,square,count,clear_list):
		if square.row>0:
			if self.mat[square.row-1][square.col].wall==True:
				self.mat[square.row-1][square.col].reset()
				self.clear_list.append(self.mat[square.row-1][square.col])
				self.count=self.count-1
				return True

	def clear_down(self,square,count,clear_list):
		if square.row<29:
			if self.mat[square.row+1][square.col].wall==True:
				self.mat[square.row+1][square.col].reset()
				self.clear_list.append(self.mat[square.row+1][square.col])
				self.count=self.count-1
				return True

	def generatefn(self):
		self.reset_neighbor()
		wall_list=[]

		for i in range(self.row):
			for j in range(self.col):
				if (random()<0.3):
					self.make_wall(i,j)
					
		for i in range(self.row):
			for j in range(self.col):
				wall_list.append(self.mat[i][j])
				self.mat[i][j].generate_neighbors
		
		square=self.mat[15][20]
		square.reset()
		square_set={square}
			
		square_queue=[square]
		while len(square_queue)!=0:	
			i=square_queue[0]
			i.generate_neighbors(self.mat)

			for j in i.g_neighbors:
				if j not in square_set:
					square_set.add(j)
					square_queue.append(j)

			square_queue.remove(i)

			
		for a in range(self.row):
			for b in range(self.col):


				square1=self.mat[a][b]
				if square1.wall==False:
					if square1 not in square_set:
						temp_set={square1}							
						temp_queue=[square1]
						while len(temp_queue)!=0:	
							i=temp_queue[0]
							i.generate_neighbors(self.mat)

							for j in i.g_neighbors:
								if j not in temp_set:
									temp_set.add(j)
									temp_queue.append(j)
							temp_queue.remove(i)
						for i in wall_list:
							if (square_set.isdisjoint(i.g_neighbors)==False and temp_set.isdisjoint(i.g_neighbors)==False):
								wall_list.remove(i)
								i.reset()
								square_set.add(i)
								square_set=square_set.union(temp_set)
								temp_set={}
						

						if len(temp_set)!=0:
							for i in temp_set:
								self.make_wall(i.row,i.col)


							





					







		# for i in range(self.row):
		# 	for j in range(self.col):
		# 			self.make_wall(i,j)

		# x=random.randint(0,29)
		# y=random.randint(0,39)

		# square=self.mat[x][y]
		# square.reset()
		# self.clear_list=[]
		# self.clear_down(square,self.count,self.clear_list)
		# self.clear_up(square,self.count,self.clear_list)
		# self.clear_left(square,self.count,self.clear_list)
		# self.clear_right(square,self.count,self.clear_list)

		# while self.count>600:
		# 	square=random.choice(self.clear_list)
		# 	z=random.randint(0,4)
		# 	square.generate_neighbors(self.mat)
		# 	if (len(square.g_neighbors)==1):
		# 		old_count
		# 		#fn_list=[self.clear_down(square,self.count,self.clear_list),self.clear_up(square,self.count,self.clear_list),self.clear_left(square,self.count,self.clear_list),self.clear_right(square,self.count,self.clear_list)]
				
				
		# 	self.clear_list.remove(square)

		# 	print(self.count)
		# 	if (len(self.clear_list)==0):
		# 		break







			




		




	def drawboard(self):
		for i in range(self.row):
			for j in range(self.col):
				square=self.mat[i][j]
				if (square.opened==True):
					square.color=yellow
				elif (square.closed==True and square!=self.startpoint and square.color!=purple):
					square.color=grey

				pygame.draw.rect(win,square.color,(square.x,square.y,square.width,square.width))
				pygame.draw.rect(win,black,(square.x,square.y,square.width,square.width),1)


	def printself(self):
		print("start")
		for i in range(self.row):
			for j in range(self.col):
				square=self.mat[i][j]
				if square.start==True:
					square.printself()

		print("end")
		for i in range(self.row):
			for j in range(self.col):
				square=self.mat[i][j]
				if square.end==True:
					square.printself()

		print("wall")
		for i in range(self.row):
			for j in range(self.col):
				square=self.mat[i][j]
				if square.wall==True:
					square.printself()

		print("startpoint")
		self.startpoint.printself()

		print("endpoint")
		self.endpoint.printself()

def Astar(grid):
	#q=PriorityQueue()
	#grid.reset_neighbor()
	open_list=[]
	for i in range(grid.row):
		for j in range(grid.col):
			square=grid.mat[i][j]
			square.calch(grid.endpoint)
			square.update_neighbors(grid.mat)

	grid.startpoint.g=0
	grid.startpoint.closed=True
	grid.startpoint.calcf()
	#grid.startpoint.printself()


	for i in grid.startpoint.neighbors:
		if grid.startpoint.g +1 <i.g and i.closed==False and i.opened==False:
			i.g=grid.startpoint.g +1
			i.calcf()
			i.prev=grid.startpoint
			i.opened==True
			open_list.append(i)
			#q.put((i.f,i.row,i.col))

	heapq.heapify(open_list)

	# while not q.empty():
	# 	item = q.get()
	# 	print(item)
	# for i in open_list:
	# 	i.printself()

	while len(open_list):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				#grid.printself()							
				os.sys.exit()

		curr_square=heapq.heappop(open_list)
		#curr_square.printself()

		if (curr_square==grid.endpoint):

			grid.drawboard()
			pygame.display.update()
			break

		curr_square.closed=True
		curr_square.opened=False

		for i in curr_square.neighbors:
			grid.drawboard()
			pygame.display.update()
			if i.closed==True:
				continue
			elif curr_square.g+1<i.g :
				i.g=curr_square.g+1
				i.calcf()
				i.prev=curr_square

				if i.opened==False:
					open_list.append(i)
					i.opened==True

		heapq.heapify(open_list)


	prev_square=grid.endpoint.prev
	prev_square.color=purple
	while (prev_square!=None and prev_square!=grid.startpoint):
		prev_square=prev_square.prev
		if (prev_square!=grid.startpoint):
			prev_square.color=purple
		else:
			break
	grid.drawboard()
	pygame.display.update()



		









			



run=True
a=Grid()


# b=a.mat[29][39]
# b.wall=True
# b.printself()

while run==True:
	
	a.drawgrid()
	pos =pygame.mouse.get_pos()
	for event in pygame.event.get():
		if event.type==pygame.locals.QUIT:
			run=False

		if a.Asearch.active==True:
			if a.startpoint ==None or a.endpoint==None:
				a.Asearch.active=False
				a.Asearch.color=white
			else:
				Astar(a)


		if pygame.mouse.get_pressed()[0]==1:
			#pos =pygame.mouse.get_pos()
			x=pos[0]
			y=pos[1]

			row=y//WIDTH
			col=x//WIDTH

			if(row>29 or col >39):
				continue				
			else:
				if a.wall_editor.active==True:
					a.make_wall(row,col)

				elif a.startbutton.active==True:
					a.make_start(row,col)

				elif a.endbutton.active==True:
					a.make_end(row,col)

		elif pygame.mouse.get_pressed()[2]==1:
			pos =pygame.mouse.get_pos()
			x=pos[0]
			y=pos[1]

			row=y//WIDTH
			col=x//WIDTH

			a.mat[row][col].reset()

	
pygame.quit()

# a.clearfn()
#a.printself()



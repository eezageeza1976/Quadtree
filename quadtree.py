import random
import pygame as pg
import math

class Point:
    def __init__(self, x, y, randomise=False):
        if randomise:
            self.x = random.randrange(0, 1200)
            self.y = random.randrange(0, 980)
        elif not randomise:
            self.x = x
            self.y = y

    def draw(self, point, window, colour):
        pg.draw.circle(window, colour, (point.x, point.y), 2)
        
    def distanceToCentre(self, centre):
        return math.sqrt((centre.x - self.x)**2 + (centre.y - self.y)**2)

 

class Rectangle:
    def __init__(self, centre, width, height):
        self.centre = centre
        self.width = width
        self.height = height
        self.west = self.centre.x - self.width     #West edge of the rectangle
        self.east = self.centre.x + self.width     #East edge
        self.north = self.centre.y - self.height   #North edge
        self.south = self.centre.y + self.height   #South edge
    
    #Checks if rectangle contains a point
    def containsPoint(self, point):
        return (self.west <= point.x < self.east and
                self.north <= point.y < self.south)
    
    #checks if a range(rectangle/perception range) overlaps a quadtree rectangle
    def intersects(self, range):
        return not (range.west > self.east or
                    range.east < self.west or
                    range.north > self.south or
                    range.south < self.north)
        
        
class Quadtree:
    def __init__(self, boundary, capacity = 4):
        self.boundary = boundary    #Rectangle class for the boundary of a rectangle
        self.capacity = capacity    #The amount of points per area
        self.points = []            #Array to keep the amount of points in this boundary
        self.divided = False        #Flag if this boundary has been divided
        
    def insert(self, point):
        #Check if the point is in the current quadtree
        if not self.boundary.containsPoint(point):
            return False
        
        #Check if the current quadtree is full, if not append to current points
        if len(self.points) < self.capacity:
            self.points.append(point)
            return True

        if not self.divided:
            self.divide()
            
        if self.nw.insert(point):
            return True
        elif self.ne.insert(point):
            return True
        elif self.sw.insert(point):
            return True
        elif self.se.insert(point):
            return True
        
        return False
    
    def queryRange(self, range):
        found_points = []
        
        if not self.boundary.intersects(range):
            return []
        
        for point in self.points:
            if range.containsPoint(point):
                found_points.append(point)
                
        if self.divided:
            found_points.extend(self.nw.queryRange(range))
            found_points.extend(self.ne.queryRange(range))
            found_points.extend(self.sw.queryRange(range))
            found_points.extend(self.se.queryRange(range))
            
        return found_points

    def queryRadius(self, _range, centre):
        found_points = []
        
        if not self.boundary.intersects(_range): #enters if False is returned
            return []
        
        for point in self.points:
            if _range.containsPoint(point) and point.distanceToCentre(centre) <= _range.width:
                found_points.append(point)
                
        if self.divided:
            found_points.extend(self.nw.queryRadius(_range, centre))
            found_points.extend(self.ne.queryRadius(_range, centre))
            found_points.extend(self.sw.queryRadius(_range, centre))
            found_points.extend(self.se.queryRadius(_range, centre))

        return found_points


    def divide(self):
        centre_x = self.boundary.centre.x
        centre_y = self.boundary.centre.y
        new_width = self.boundary.width / 2
        new_height = self.boundary.height / 2
        
        nw = Rectangle(Point(centre_x - new_width, centre_y - new_height), new_width, new_height)
        self.nw = Quadtree(nw)
        
        ne = Rectangle(Point(centre_x + new_width, centre_y - new_height), new_width, new_height)
        self.ne = Quadtree(ne)
        
        sw = Rectangle(Point(centre_x - new_width, centre_y + new_height), new_width, new_height)
        self.sw = Quadtree(sw)
        
        se = Rectangle(Point(centre_x + new_width, centre_y + new_height), new_width, new_height)
        self.se = Quadtree(se)
        
        self.divided = True

    def __len__(self):
        count = len(self.points)
        if self.divided:
            count+= len(self.nw) + len(self.ne) + len(self.sw) + len(self.se)
            
        return count
    

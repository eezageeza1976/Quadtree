import pygame as pg
from quadtree import Point, Rectangle, Quadtree

pg.init()

def windowSetup():
    window = pg.display.set_mode((1200, 980))
    window.fill((0, 0, 0))
    return window

screen = windowSetup()

def main():
    running = True
    flock_list = []
    
    for i in range(1000):
        flock_list.append(Point(0, 0, True))
        
    found_points = []
    perception_range = Rectangle(Point(1200/2, 980/2), 200, 200)
    
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                
        screen.fill((0, 0, 0))
        
        root = Rectangle(Point(1200/2, 980/2), 1200, 980)
        qTree = Quadtree(root)
        
        for point in flock_list:
            qTree.insert(point)
        
        #quiries the quadtree for anything within the perception range rectangle
#         found_points = qTree.queryRange(perception_range)
#         left = perception_range.west
#         top = perception_range.north
#         width = perception_range.width*2
#         height = perception_range.height*2
#         pg.draw.rect(screen, (255, 0, 0), (left, top, width, height), 1)
        
        #quiries the quadtree for anything within the perception range circle
        radius = min(200, 200)
        perception_range = Rectangle(Point(1200/2, 980/2), radius, radius)
        found_points = qTree.queryRadius(perception_range, Point(1200/2, 980/2))
        pg.draw.circle(screen, (255, 0, 0), (1200/2, 980/2), radius, 1)
        
        
        
        for point in flock_list:
            point.draw(point, screen, (0, 255, 0))
            
        for point in found_points:
            point.draw(point, screen, (255, 0, 0))

        
        pg.display.flip()
    
    pg.quit()




# run the App
if __name__ == '__main__':
    main()
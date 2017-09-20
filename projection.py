#!/bin/env python

import wireframe
import pygame
import time
from random import randint

class ProjectionViewer:
    """ Displays 3D objects on a Pygame screen """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.scl = 20
        self.flying = 0
        self.yoff = 0
        self.xoff = 0

        
        self.cols = int(self.width / 2)
        self.rows = int(self.width / 2)
        self.terrain = [None]*self.cols, [None]*self.rows
        
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Terrain')
        self.background = (0,0,0)

        self.wireframes = {}
        self.displayNodes = True
        self.displayEdges = True
        self.nodeColour = (255,255,255)
        self.edgeColour = (200,200,200)
        self.nodeRadius = 4

    def addWireframe(self, name, wireframe):
        """ Add a named wireframe object. """

        self.wireframes[name] = wireframe

    def run(self):
        """ Create a pygame screen until it is closed. """
        
        running = True
        clock = pygame.time.Clock()
        while running:
            #clock.tick(16)
            self.flying = round(self.flying - 0.1, 1) #round to 1d.p

            terrain.addNodes([(x,y,z) for x in range(-20,2000,20) for y in range(-20,620,20) for z in range(0,1)])

            for i in range(0,1791):
                terrain.changeHeight(i)
            
            terrain.addEdges([(x,x+1) for x in range(0,1791)])  # X-axis
            terrain.addEdges([(y,y+32) for y in range(0,1759)])  # Y-axis
            terrain.addEdges([(y,y+33) for y in range(0,1758)])  #diagonal

            terrain.rotateX(530,290,0,0.9)
            terrain.rotateY(530,290,0,0.05)
                        
            #self.yoff = self.flying

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            self.display()  
            pygame.display.flip()
            time.sleep(0.8)
            terrain.clear()
        
    def display(self):
        """ Draw the wireframes on the screen. """

        self.screen.fill(self.background)

        for wireframe in self.wireframes.values():
            if self.displayEdges:
                for edge in wireframe.edges:
                    pygame.draw.aaline(self.screen, self.edgeColour, (edge.start.x, edge.start.y), (edge.stop.x, edge.stop.y), 1)

            if self.displayNodes:
                for node in wireframe.nodes:
                    pygame.draw.circle(self.screen, self.nodeColour, (int(node.x), int(node.y)), self.nodeRadius, 0)

    def translateAll(self, axis, d):
        """ Translate all wireframes along a given axis by d units. """

        for wireframe in self.wireframes.itervalues():
            wireframe.translate(axis, d)

    def scaleAll(self, scale):
        """ Scale all wireframes by a given scale, centred on the centre of the screen. """

        centre_x = self.width/2
        centre_y = self.height/2

        for wireframe in self.wireframes.itervalues():
            wireframe.scale((centre_x, centre_y), scale)

    def rotateAll(self, axis, theta):
        """ Rotate all wireframe about their centre, along a given axis by a given angle. """

        rotateFunction = 'rotate' + axis

        for wireframe in self.wireframes.itervalues():
            centre = wireframe.findCentre()
            getattr(wireframe, rotateFunction)(centre, theta)

if __name__ == '__main__':
    pv = ProjectionViewer(900, 600)  #size of window

    terrain = wireframe.Wireframe()
    
    pv.addWireframe('terrain', terrain)
    pv.run() ##runs the main loop

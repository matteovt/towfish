#!/usr/bin/env python

# v0.1 - Initial construct, generic input & display
# v0.2 - Removed extra axes,
# v0.3 - Removed all extra, only essential info displayed.  
import pygame

#define colors
BLACK = (   0,  0,  0)
WHITE = (255, 255, 255)

#define constants
MAX_ANGLE = 15
MAX_ANGLE_PER_SECOND = 6
JOY_AXIS = 1
FPS = 40
#Classes
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None,20)

    def Print(self, screen, textString):
        textBitmap = self.font.render(textString,True,BLACK)
        screen.blit(textBitmap,[self.x,self.y])
        self.y += self.line_height
        
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


pygame.init()

#set width and height of screen [width, height]
size = [500, 500]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Joystick Read")

#loop until user clicks close button
done = False

#Used for screen update rate
clock = pygame.time.Clock()

#initialize the joysticks
pygame.joystick.init()

#Prep print
textPrint = TextPrint()

#initialize variables
joy_button_pressed = False
joystick_commanded_angle = 0
hydrofoil_set_angle = 0
hydrofoil_commanded_angle = 0
joy_button_pressed = False
joy_button_last = False



# ------------- Main Program ------------
while done == False:
    #EVENT PROCESSING
    for event in pygame.event.get():    #User changed joystick parameter
        if event.type == pygame.QUIT:   #if user closed window
            done = True

        #Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        
        if event.type == pygame.JOYBUTTONDOWN:
            joy_button_pressed ^= True
            #if button pressed, update commanded value
            if(joy_button_pressed == True):
                hydrofoil_commanded_angle = hydrofoil_set_angle
                

        #DRAW SCREEN
        #Clear screen to be white
        screen.fill(WHITE)
        textPrint.reset()

        #get count of joysticks
        joystick_count = pygame.joystick.get_count()


        #for each joystick:
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

            
            textPrint.Print(screen,"Hold Hydrofoil Angle: {}".format(joy_button_pressed) )
            textPrint.Print(screen,'')
            
            joystick_commanded_angle = joystick.get_axis(JOY_AXIS) * MAX_ANGLE_PER_SECOND/FPS
            hydrofoil_commanded_angle += joystick_commanded_angle

            if(hydrofoil_commanded_angle > MAX_ANGLE):
                hydrofoil_commanded_angle = MAX_ANGLE
                
            if(hydrofoil_commanded_angle < -MAX_ANGLE):
                hydrofoil_commanded_angle = -MAX_ANGLE

            if(joy_button_pressed == True):
                #hydrofoil_set_angle = hydrofoil_commanded_angle
                joy_button_last = True
            else:               
                hydrofoil_set_angle =  hydrofoil_commanded_angle
                joy_button_last = False
            
                
            textPrint.Print(screen, "Joystick Command Angle: {:>6.1f}".format(joystick_commanded_angle) )
            textPrint.Print(screen, "Hydrofoil Set Angle: {:>6.1f}".format(hydrofoil_set_angle) )

        #Update screen
        pygame.display.flip()

        #Limit to 20 frames per second
        clock.tick(FPS)

#close the window and quit
pygame.quit()

            
            
            


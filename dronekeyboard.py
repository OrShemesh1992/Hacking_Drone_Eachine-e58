import logging
import sys
import pygame
import os
from dronecontrol import DroneControl
from Image import get_image

# byte must be in range(0, 256)
def clamp(n, minn, maxn): return max(min(maxn, n), minn)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting keyboard control app")
    pygame.init()
    #break the while
    done=False
    #screen
    screen = pygame.display.set_mode((300, 300))
    #call to DroneControl object
    drone = DroneControl()
    #call to founction connect
    drone.connect()

    airborne = False  # flag denoting whether the drone is airborne

    speeds = [0.3, 0.6, 1]  # list of speeds to select from (0-1)
    speed_idx = 0  # selected speed

    r = 128  # Left | right
    p = 128  # forward | backward
    t = 128  # up | down
    y = 128  # rotation left | right

    #print
    screen.blit(get_image('pictures/RSG.jpg'), (0, 0))
    pygame.display.flip()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                key = event.key

                if event.type == pygame.KEYDOWN:
                    direction = 1
                else:
                    direction = -1

                if key == 27:  # ESC
                    #print
                    screen.blit(get_image('pictures/crash.jpg'), (0, 0))
                    pygame.display.flip()
                    logging.info("Exiting...")
                    drone.stop()
                    pygame.quit()
                    done=True

                elif key == 32 and event.type == pygame.KEYDOWN:  # spacebar
                    if airborne:
                        #print
                        screen.blit(get_image('pictures/land.jpg'), (0, 0))
                        pygame.display.flip()

                        drone.land()
                        airborne = False
                    else:
                        #print
                        screen.blit(get_image('pictures/take-off.jpg'), (0, 0))
                        pygame.display.flip()

                        drone.take_off()
                        airborne = True

                elif key == 9 and event.type == pygame.KEYDOWN:  # tab
                    speed_idx += 1
                    if speed_idx == len(speeds):
                        speed_idx = 0

                    #print
                    screen.blit(get_image('pictures/speed.jpg'), (0, 0))
                    pygame.display.flip()
                    print("speed: {0}".format(speeds[speed_idx]))

                elif key == 119:  # w
                    #print
                    screen.blit(get_image('pictures/up.jpg'), (0, 0))
                    pygame.display.flip()
                    p += int(direction * 128 * speeds[speed_idx])  # forward
                elif key == 115:  # s
                    #print
                    screen.blit(get_image('pictures/down.png'), (0, 0))
                    pygame.display.flip()
                    p -= int(direction * 128 * speeds[speed_idx])  # backward
                elif key == 97:  # a
                    #print
                    screen.blit(get_image('pictures/left.jpg'), (0, 0))
                    pygame.display.flip()
                    r -= int(direction * 128 * speeds[speed_idx])  # left
                elif key == 100:  # d
                    #print
                    screen.blit(get_image('pictures/right.png'), (0, 0))
                    pygame.display.flip()
                    r += int(direction * 128 * speeds[speed_idx])  # right
                elif key == 273:  # up arrow
                    #print
                    screen.blit(get_image('pictures/take-off.jpg'), (0, 0))
                    pygame.display.flip()
                    t += int(direction * 128 * speeds[speed_idx])  # up
                elif key == 274:  # down arrow
                    #print
                    screen.blit(get_image('pictures/land.jpg'), (0, 0))
                    pygame.display.flip()
                    t -= int(direction * 128 * speeds[speed_idx])  # down
                elif key == 275:  # right arrow
                    #print
                    screen.blit(get_image('pictures/rotate right.png'), (0, 0))
                    pygame.display.flip()
                    y += direction * 128  # rotation right
                elif key == 276:  # left arrow
                    #print
                    screen.blit(get_image('pictures/rotate left.jpg'), (0, 0))
                    pygame.display.flip()
                    y -= direction * 128  # rotation left


                r = clamp(r, 0, 255)
                p = clamp(p, 0, 255)
                t = clamp(t, 0, 255)
                y = clamp(y, 0, 255)
        drone.cmd(r, p, t, y)

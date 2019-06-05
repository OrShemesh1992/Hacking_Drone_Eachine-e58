import logging
import sys
import time
import pygame

from dronecontrol import DroneControl

# byte must be in range(0, 256)
def clamp(n, minn, maxn): return max(min(maxn, n), minn)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting keyboard control app")
    pygame.init()
    done=False
    screen = pygame.display.set_mode((400, 300))
    drone = DroneControl()
    drone.connect()

    airborne = False  # flag denoting whether the drone is airborne

    speeds = [0.3, 0.6, 1]  # list of speeds to select from (0-1)
    speed_idx = 0  # selected speed

    r = 128  # Left | right
    p = 128  # forward | backward
    t = 128  # up | down
    y = 128  # rotation left | right

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
                    logging.info("Exiting...")
                    drone.stop()
                    pygame.quit()
                    done=True

                elif key == 32 and event.type == pygame.KEYDOWN:  # spacebar
                    if airborne:
                        drone.land()
                        airborne = False
                    else:
                        drone.take_off()
                        airborne = True

                elif key == 9 and event.type == pygame.KEYDOWN:  # tab
                    speed_idx += 1
                    if speed_idx == len(speeds):
                        speed_idx = 0
                    print("speed: {0}".format(speeds[speed_idx]))

                elif key == 119:  # w
                    p += int(direction * 128 * speeds[speed_idx])  # forward
                elif key == 115:  # s
                    p -= int(direction * 128 * speeds[speed_idx])  # backward
                elif key == 97:  # a
                    r -= int(direction * 128 * speeds[speed_idx])  # left
                elif key == 100:  # d
                    r += int(direction * 128 * speeds[speed_idx])  # right
                elif key == 273:  # up arrow
                    t += int(direction * 128 * speeds[speed_idx])  # up
                elif key == 274:  # down arrow
                    t -= int(direction * 128 * speeds[speed_idx])  # down
                elif key == 275:  # right arrow
                    y += direction * 128  # rotation right
                elif key == 276:  # left arrow
                    y -= direction * 128  # rotation left


                r = clamp(r, 0, 255)
                p = clamp(p, 0, 255)
                t = clamp(t, 0, 255)
                y = clamp(y, 0, 255)
        drone.cmd(r, p, t, y)


# Constant Values
FPS = 30            # Frames per second
RField = (2370, 1140)    # Green Field
R_WALL_WIDTH = 100        # Wall width in mm
RTapewidth = 50        # Line width in mm
RGoalwidth = 630        # Goal width in mm
RGoaldepth = 50        # Goal depth in mm
RBallsize = 50        # Ball diameter in mm

RPitch = (RField[0]+2*(R_WALL_WIDTH+RTapewidth), RField[1]+2*(R_WALL_WIDTH+RTapewidth))    # X, Y in mm
Rdx = 2            # To fit on screen
Rdy = 2
Fntsize = 36
PITCH = (RPitch[0]/Rdx, (RPitch[1]/Rdy))
Field = ((RField[0]+RTapewidth)/Rdx, ((RField[1]+RTapewidth)/Rdy))
WALL_WIDTH = R_WALL_WIDTH / Rdx
Tapewidth = RTapewidth / Rdx
Goalwidth = RGoalwidth / Rdy
Goaldepth = RGoaldepth / Rdx
BALL_SIZE = RBallsize / Rdx
BALL_RADIUS = BALL_SIZE / 2
CENTRE = (PITCH[0]/2, PITCH[1]/2)
Res = (PITCH[0], PITCH[1] + Fntsize)        # Window Resolution
Xres = Res[0]
Yres = Res[1]
Edge = WALL_WIDTH + Tapewidth
Linewidth = 3 * Tapewidth
GRASS = (0, 148, 10)        # Field Colour
WALL = (0, 0, 0)            # Wall Colour
TAPE = (255, 255, 255)        # Line Colour
TITLE = (10, 10, 10)        # Title font Colour
TITLEBACK = (240, 240, 240)    # Title Background Colour
LINE = (150, 150, 150)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 140, 0)
TABLE_FRICTION = 0.99
COLLISION_FRICTION = 0.9            # Collision TABLE_FRICTION
MARGIN = 1

TITLE_TEXT = 'Foosball Match'
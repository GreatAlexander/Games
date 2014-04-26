#==============================================================================
# Global Constant Values
#==============================================================================

# Real world constants
FPS = 30			# Frames per second
R_FIELD = (2370, 1140)	# Green field size
R_WALL_WIDTH = 100	# Wall width in mm
R_TAPE_WIDTH = 50		# Line width in mm
R_GOAL_WIDTH = 630	# Goal width in mm
R_GOAL_DEPTH = 50		# Goal depth in mm
R_BALL_SIZE = 50		# Ball diameter in mm
R_PITCH = (R_FIELD[0]+2*(R_WALL_WIDTH+R_TAPE_WIDTH), R_FIELD[1]+2*(R_WALL_WIDTH+R_TAPE_WIDTH))    # X, Y in mm

# Simulation constants
Rdx = 2
Rdy = 2			# Reducing resolution to fit on screen

PITCH = (R_PITCH[0]/Rdx, (R_PITCH[1]/Rdy))
FIELD = ((R_FIELD[0]+R_TAPE_WIDTH)/Rdx, ((R_FIELD[1]+R_TAPE_WIDTH)/Rdy))
WALL_WIDTH = R_WALL_WIDTH / Rdx
TAPE_WIDTH = R_TAPE_WIDTH / Rdx
GOAL_WIDTH = R_GOAL_WIDTH / Rdy
Goaldepth = R_GOAL_DEPTH / Rdx
BALL_SIZE = R_BALL_SIZE / Rdx
BALL_RADIUS = BALL_SIZE / 2
CENTRE = (PITCH[0]/2, PITCH[1]/2)
EDGE = WALL_WIDTH + TAPE_WIDTH
LINE_WIDTH = 3 * TAPE_WIDTH
BLUE1_START_POS = (PITCH[0]*1/8 + EDGE, PITCH[1]*1/2 + EDGE)
BLUE2_START_POS = (PITCH[0]*5/8 + EDGE, PITCH[1]*1/2 + EDGE)
RED1_START_POS = (PITCH[0]*7/8 + EDGE, PITCH[1]*1/2 + EDGE)
RED2_START_POS = (PITCH[0]*3/8 + EDGE, PITCH[1]*1/2 + EDGE)
BLUE_START_ANGLE = -90
RED_START_ANGLE = 90

# Screen constants
FONT_SIZE = 36
Res = (PITCH[0], PITCH[1] + FONT_SIZE)	# Window Resolution
Xres = Res[0]
Yres = Res[1]

# Colours
GRASS = (0, 148, 10)		# Field Colour
WALL = (0, 0, 0)			# Wall Colour
TAPE = (255, 255, 255)		# Line Colour
TITLE = (10, 10, 10)		# Title font Colour
TITLEBACK = (240, 240, 240)	# Title Background Colour
LINE = (150, 150, 150)		# Central line Colour
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 140, 0)

# Physics constants
TABLE_FRICTION = 0.99		# Speed reduction via rolling
COLLISION_FRICTION = 0.9	# Speed reduction after collision
MARGIN = TAPE_WIDTH / 2	# Collision margin for ball Sprite
RANDOM_DEVIATION = 0.2		# Deviation of the ball

TITLE_TEXT = 'Foosball Match'
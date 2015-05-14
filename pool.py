import pygame
import math
import random

# Initialize the Pygame engine.
pygame.init()

# ------------------------------------------------------------
# GLOBAL CONSTANTS -------------------------------------------
# ------------------------------------------------------------
# Colors, sizes, other parameters: a variable that doesn't change over the course of the game is considered a constant.
# All constants are spelled LIKE THIS.

# Screen parameters.
SCREEN_CAPTION = '8-Ball Pool'
SCREEN_SIZE = (1050, 600)

# Ball parameters.
BALL_RADIUS = 11

# Ball colors.
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
PURPLE_COLOR = (69, 52, 130)
GREEN_COLOR = (45, 133, 70)
BLUE_COLOR = (48, 89, 179)
ORANGE_COLOR = (252, 76, 18)
YELLOW_COLOR = (240, 187, 12)
RED_COLOR = (209, 23, 29)
BROWN_COLOR = (115, 32, 32)
PURPLE_STRIPED_COLOR = (69, 52, 130, 255)
GREEN_STRIPED_COLOR = (45, 133, 70, 255)
BLUE_STRIPED_COLOR = (48, 89, 179, 255)
ORANGE_STRIPED_COLOR = (252, 76, 18, 255)
YELLOW_STRIPED_COLOR = (240, 187, 12, 255)
RED_STRIPED_COLOR = (209, 23, 29, 255)
BROWN_STRIPED_COLOR = (115, 32, 32, 255)

# Pool table parameters.
POOL_TABLE_SIZE = (1050, 550)
POOL_TABLE_POCKET_RADIUS = 23

# Pool table colors.
POOL_TABLE_MAIN_COLOR = (99, 166, 112)
POOL_TABLE_SIDE_COLOR = (122, 66, 54)

# Bottom bar parameters.
BAR_SIZE = (1050, 50)
MUSIC_BOX_SIZE = (111, 33)
PLAYER_BOX_SIZE = (143, 38)
SHOTS_BOX_SIZE = (94, 33)
RULES_BOX_SIZE = (203, 38)
COLOR_BOX_SIZE = (83, 38)
BAR_MARGIN = 10

# Physics parameters.
DRAG = 0.995
ELASTICITY = 0.775
SPEED_THRESHOLD = 0.01

# ------------------------------------------------------------
# CLASS SCREEN -----------------------------------------------
# ------------------------------------------------------------

class Screen(object):
    # Initialize a class instance.
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE) # Create a screen and set its size.
        pygame.display.set_caption(SCREEN_CAPTION) # Set the screen caption.
        self.mouse_pos = (0, 0) # Mouse position.
        self.music_box = pygame.image.load('images/music_off.png').convert_alpha() # Shows whether the music is on or off.
        self.player_box = pygame.image.load('images/player1_turn.png').convert_alpha() # Shows whose turn it is or whether the player has won.
        self.rules_box = pygame.image.load('images/blank.png').convert_alpha() # Shows whether an illegal ball has been pocketed.
        self.shots_box = pygame.image.load('images/shots_1.png').convert_alpha() # Shows how many shots the player has left.
        self.color_box = pygame.image.load('images/blank2.png').convert_alpha() # Shows players' colors.

    # Fill the screen with a color.
    def fill(self):
        self.screen.fill(BLACK_COLOR)

    # Draw a pool table.
    def draw_pool_table(self):
        # Draw sides.
        pygame.draw.rect(self.screen, POOL_TABLE_SIDE_COLOR, (0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1] - BAR_SIZE[1]))
        
        # Draw a playable area.
        pygame.draw.rect(self.screen, POOL_TABLE_MAIN_COLOR, (2 * POOL_TABLE_POCKET_RADIUS, 2 * POOL_TABLE_POCKET_RADIUS, POOL_TABLE_SIZE[0] - 4 * POOL_TABLE_POCKET_RADIUS, POOL_TABLE_SIZE[1] - 4 * POOL_TABLE_POCKET_RADIUS))

        # Draw top pockets.
        pygame.draw.circle(self.screen, BLACK_COLOR, (2 * POOL_TABLE_POCKET_RADIUS, 2 * POOL_TABLE_POCKET_RADIUS), POOL_TABLE_POCKET_RADIUS)
        pygame.draw.circle(self.screen, BLACK_COLOR, (POOL_TABLE_SIZE[0] / 2, 2 * POOL_TABLE_POCKET_RADIUS), POOL_TABLE_POCKET_RADIUS)
        pygame.draw.circle(self.screen, BLACK_COLOR, (POOL_TABLE_SIZE[0] - 2 * POOL_TABLE_POCKET_RADIUS, 2 * POOL_TABLE_POCKET_RADIUS), POOL_TABLE_POCKET_RADIUS)

        # Draw bottom pockets.
        pygame.draw.circle(self.screen, BLACK_COLOR, (2 * POOL_TABLE_POCKET_RADIUS, POOL_TABLE_SIZE[1] - 2 * POOL_TABLE_POCKET_RADIUS), POOL_TABLE_POCKET_RADIUS)
        pygame.draw.circle(self.screen, BLACK_COLOR, (POOL_TABLE_SIZE[0] / 2, POOL_TABLE_SIZE[1] - 2 * POOL_TABLE_POCKET_RADIUS), POOL_TABLE_POCKET_RADIUS)
        pygame.draw.circle(self.screen, BLACK_COLOR, (POOL_TABLE_SIZE[0] - 2 * POOL_TABLE_POCKET_RADIUS, POOL_TABLE_SIZE[1] - 2 * POOL_TABLE_POCKET_RADIUS), POOL_TABLE_POCKET_RADIUS)

        # Draw a head string.
        pygame.draw.line(self.screen, WHITE_COLOR, (POOL_TABLE_SIZE[0] / 4, 2 * POOL_TABLE_POCKET_RADIUS), (POOL_TABLE_SIZE[0] / 4, POOL_TABLE_SIZE[1] - 2 * POOL_TABLE_POCKET_RADIUS))

    # Draw the bottom bar.
    def draw_bar(self):
        self.screen.blit(self.music_box, (BAR_MARGIN, SCREEN_SIZE[1] - BAR_SIZE[1] / 2 - MUSIC_BOX_SIZE[1] / 2))
        self.screen.blit(self.shots_box, (SCREEN_SIZE[0] - BAR_MARGIN - SHOTS_BOX_SIZE[0], SCREEN_SIZE[1] - BAR_SIZE[1] / 2 - SHOTS_BOX_SIZE[1] / 2))
        self.screen.blit(self.player_box, (SCREEN_SIZE[0] - 2 * BAR_MARGIN - SHOTS_BOX_SIZE[0] - PLAYER_BOX_SIZE[0], SCREEN_SIZE[1] - BAR_SIZE[1] / 2 + MUSIC_BOX_SIZE[1] / 2 - PLAYER_BOX_SIZE[1] + BAR_MARGIN / 1.6))
        self.screen.blit(self.rules_box, (SCREEN_SIZE[0] - 3 * BAR_MARGIN - SHOTS_BOX_SIZE[0] - PLAYER_BOX_SIZE[0] - RULES_BOX_SIZE[0], SCREEN_SIZE[1] - BAR_SIZE[1] / 2 + MUSIC_BOX_SIZE[1] / 2 - PLAYER_BOX_SIZE[1] + BAR_MARGIN / 1.6))
        self.screen.blit(self.color_box, (SCREEN_SIZE[0] - 4 * BAR_MARGIN - SHOTS_BOX_SIZE[0] - PLAYER_BOX_SIZE[0] - RULES_BOX_SIZE[0] - COLOR_BOX_SIZE[0], SCREEN_SIZE[1] - BAR_SIZE[1] / 2 + MUSIC_BOX_SIZE[1] / 2 - PLAYER_BOX_SIZE[1] + BAR_MARGIN / 1.6))

    # Update the bottom bar.
    def update_bar(self):
        if rules.who_won == 1:
            self.player_box = pygame.image.load('images/player1_won.png').convert_alpha()
        elif rules.who_won == 2:
            self.player_box = pygame.image.load('images/player2_won.png').convert_alpha()
        else:
            if rules.player == 1:
                self.player_box = pygame.image.load('images/player1_turn.png').convert_alpha()
            else:
                self.player_box = pygame.image.load('images/player2_turn.png').convert_alpha()

        if rules.shots == 1:
            self.shots_box = pygame.image.load('images/shots_1.png').convert_alpha()
        else:
            self.shots_box = pygame.image.load('images/shots_2.png').convert_alpha()

        if rules.player == 1 and rules.colors == ('solid', 'striped'):
            self.color_box = pygame.image.load('images/solid.png').convert_alpha()
        elif rules.player == 1 and rules.colors == ('striped', 'solid'):
            self.color_box = pygame.image.load('images/striped.png').convert_alpha()
        elif rules.player == 2 and rules.colors == ('solid', 'striped'):
            self.color_box = pygame.image.load('images/striped.png').convert_alpha()
        elif rules.player == 2 and rules.colors == ('striped', 'solid'):
            self.color_box = pygame.image.load('images/solid.png').convert_alpha()

    # Update the rules box.
    def update_rules_box(self, hits, is_illegal_ball_pocketed):
        if hits == None:
            self.rules_box = pygame.image.load('images/no_balls_hit.png').convert_alpha()
        elif hits == 'illegal':
            self.rules_box = pygame.image.load('images/illegal_ball_hit_first.png').convert_alpha()  
        elif is_illegal_ball_pocketed:
            self.rules_box = pygame.image.load('images/illegal_ball_pocketed.png').convert_alpha()  
        self.draw_bar()
        self.update()
        pygame.time.wait(3000)
        self.rules_box = pygame.image.load('images/blank.png').convert_alpha()
        self.draw_bar()

    # Game over.
    def game_over(self):
        self.fill()
        self.draw_pool_table()
        self.update_bar()
        self.draw_bar()
        for ball in game.balls:
            ball.draw()
        self.update()
        pygame.time.wait(5000) 

    # Update the screen.
    def update(self):
        pygame.display.flip()

# ------------------------------------------------------------
# CLASS GAME -------------------------------------------------
# ------------------------------------------------------------

class Game(object):
    # Initialize a class instance.
    def __init__(self):
        self.running = True # If it's False, the program window closes.
        self.balls = [] # An array for the balls.
        self.music_list = ('music/dub_eastern.ogg', 'music/easy_jam.ogg', 'music/firmament.ogg', 'music/niles_blues.ogg') # Music list.
        self.currently_playing = None # Current song.
        self.next_song = None # Next song.

    # Create balls as instances of the Ball class and append them to the balls array.
    def create_balls(self):
        self.balls.append(Ball(WHITE_COLOR))
        self.balls.append(Ball(BLACK_COLOR))
        self.balls.append(Ball(PURPLE_COLOR))
        self.balls.append(Ball(GREEN_COLOR))
        self.balls.append(Ball(BLUE_COLOR))
        self.balls.append(Ball(ORANGE_COLOR))
        self.balls.append(Ball(YELLOW_COLOR))
        self.balls.append(Ball(RED_COLOR))
        self.balls.append(Ball(BROWN_COLOR))
        self.balls.append(Ball(PURPLE_STRIPED_COLOR))
        self.balls.append(Ball(GREEN_STRIPED_COLOR))
        self.balls.append(Ball(BLUE_STRIPED_COLOR))
        self.balls.append(Ball(ORANGE_STRIPED_COLOR))
        self.balls.append(Ball(YELLOW_STRIPED_COLOR))
        self.balls.append(Ball(RED_STRIPED_COLOR))
        self.balls.append(Ball(BROWN_STRIPED_COLOR))

    # Turn the music on/off.
    def music_player(self):
        if screen.mouse_pos[0] >= BAR_MARGIN and screen.mouse_pos[0] <= BAR_MARGIN + screen.music_box.get_width() and screen.mouse_pos[1] >= SCREEN_SIZE[1] - BAR_SIZE[1] / 2 - MUSIC_BOX_SIZE[1] / 2 and screen.mouse_pos[1] <= SCREEN_SIZE[1] - BAR_SIZE[1] / 2 - MUSIC_BOX_SIZE[1] / 2 + screen.music_box.get_height():
            if screen.music_box.get_width() == 109:
                screen.music_box = pygame.image.load('images/music_off.png').convert_alpha()
                game.currently_playing = None
                game.next_song = None
                pygame.mixer.music.stop()
            else:
                screen.music_box = pygame.image.load('images/music_on.png').convert_alpha()
                game.next_song = random.choice(game.music_list)
                game.currently_playing_song = game.next_song
                pygame.mixer.music.load(game.currently_playing_song)
                pygame.mixer.music.play()

    # Set random song from the music list to play next.
    def music_queue(self):
        while self.next_song == self.currently_playing_song:
            self.next_song = random.choice(self.music_list)
        self.currently_playing_song = self.next_song
        pygame.mixer.music.load(self.next_song)
        pygame.mixer.music.play()

# ------------------------------------------------------------
# CLASS RULES ------------------------------------------------
# ------------------------------------------------------------

class Rules(object):
    # Initialize a class instance.
    def __init__(self):
        self.is_cue_ball_selected = False # If it's True, the cue ball is selected.
        self.is_cue_ball_moveable = True # If it's True, the cue ball can be moved.
        self.is_cue_ball_moved = False # If it's True, the cue ball has been moved.
        self.is_cue_ball_thrown = False # If it's True, the cue ball has been thrown.
        self.player = random.choice([1, 2]) # Randomly choose which player goes first.
        self.balls_pocketed = [] # Record which balls were pocketed this turn.
        self.colors = (None, None) # Set the colors for both players.
        self.shots = 1 # Record how many shots the player has left.
        self.hits = [] # Detect which ball was hit first by the cue ball.
        self.who_won = None # Shows who won the game.

    # Check the game rules after the player made a move.
    def check_rules(self):
        if not self.are_balls_moving() and self.is_cue_ball_thrown: # No balls are moving and the cue ball has been thrown.
            self.is_cue_ball_thrown = False
            
            if self.is_illegal_ball_pocketed() and self.who_won == None: # An illegal ball has been pocketed.
                screen.update_rules_box(1, True)
                self.shots = 2 # The next player has 2 shots because the rules were broken.
                self.change_player() # Change the player.

            elif len(self.hits) == 0 and self.who_won == None: # No balls were hit.
                screen.update_rules_box(None, False)
                self.shots = 2
                self.change_player()
                
            elif self.is_illegal_ball_hit_first() and self.who_won == None: # An illegal ball has been hit first.
                screen.update_rules_box('illegal', False)
                self.shots = 2
                self.change_player()

            elif self.who_won == None: # No rules were broken.
                if len(self.balls_pocketed) == 0: # No balls were pocketed.
                    if self.shots == 1:
                        self.change_player()
                    else:
                        self.shots -= 1

                else: # Some balls were pocketed.
                    if not self.are_balls_left():
                        self.end_game(True) # The player won.
                    else:
                        if self.colors == (None, None):
                            self.set_colors() # Set the colors if no colors are set yet.

            self.is_cue_ball_moveable = True
            self.balls_pocketed = []
            self.hits = []
                                  
    def are_balls_moving(self):
        if all(ball.speed == 0 for ball in game.balls): # If all speeds are 0.
            return False
        return True

    def is_illegal_ball_pocketed(self):
        if any(ball.color == BLACK_COLOR for ball in self.balls_pocketed): # The eight ball was pocketed.
            if len(self.balls_pocketed) > 1: # Some other ball was pocketed as well.
                self.end_game(False) # The player lost.
            elif self.player == 1 and self.colors == ('solid', 'striped'):
                for ball in game.balls:
                    if len(ball.color) == 3 and ball.color != WHITE_COLOR:
                        self.end_game(False)
            elif self.player == 1 and self.colors == ('striped', 'solid') and any(len(ball.color) == 4 for ball in game.balls):
                self.end_game(False)
            elif self.player == 2 and self.colors == ('striped', 'solid'):
                for ball in game.balls:
                    if len(ball.color) == 3 and ball.color != WHITE_COLOR:
                        self.end_game(False)
            elif self.player == 2 and self.colors == ('solid', 'striped') and any(len(ball.color) == 4 for ball in game.balls):
                self.end_game(False)
            elif self.colors == (None, None):
                self.end_game(False)
            elif self.is_illegal_ball_hit_first():
                self.end_game(False)
            else:
                self.end_game(True) # The player won.

        elif any(ball.color == WHITE_COLOR for ball in self.balls_pocketed): # The cue ball was pocketed.
            game.balls.insert(0, Ball(WHITE_COLOR)) # "Get" the cue ball out of the pocket.
            game.balls[0].place() # Place it at its starting position.
            return True

        elif self.player == 1 and self.colors == ('striped', 'solid') and any(len(ball.color) == 3 for ball in self.balls_pocketed): # Wrong color was pocketed.
            return True

        elif self.player == 1 and self.colors == ('solid', 'striped') and any(len(ball.color) == 4 for ball in self.balls_pocketed):
            return True

        elif self.player == 2 and self.colors == ('striped', 'solid') and any(len(ball.color) == 4 for ball in self.balls_pocketed):
            return True

        elif self.player == 2 and self.colors == ('solid', 'striped') and any(len(ball.color) == 3 for ball in self.balls_pocketed):
            return True

        return False

    def is_illegal_ball_hit_first(self):
        if self.hits[0].color == BLACK_COLOR:
            if self.player == 1 and self.colors == ('solid', 'striped'):
                for ball in game.balls:
                    if len(ball.color) == 3 and ball.color != WHITE_COLOR:
                        return True
            elif self.player == 1 and self.colors == ('striped', 'solid') and any(len(ball.color) == 4 for ball in game.balls):
                return True
            if self.player == 2 and self.colors == ('striped', 'solid'):
                for ball in game.balls:
                    if len(ball.color) == 3 and ball.color != WHITE_COLOR:
                        return True
            elif self.player == 2 and self.colors == ('solid', 'striped') and any(len(ball.color) == 4 for ball in game.balls):
                return True
            elif self.colors == (None, None):
                return True
            
        else:
            if self.player == 1 and self.colors == ('solid', 'striped') and len(self.hits[0].color) == 4:
                return True
            elif self.player == 1 and self.colors == ('striped', 'solid') and len(self.hits[0].color) == 3:
                return True
            elif self.player == 2 and self.colors == ('solid', 'striped') and len(self.hits[0].color) == 3:
                return True
            elif self.player == 2 and self.colors == ('striped', 'solid') and len(self.hits[0].color) == 4:
                return True

        return False
            
    def change_player(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    def are_balls_left(self):
        if any(ball.color == BLACK_COLOR for ball in self.balls_pocketed):
            return False
        return True

    def set_colors(self):
        if len(self.balls_pocketed[0].color) == 3:
            if self.player == 1:
                self.colors = ('solid', 'striped')
            else:
                self.colors = ('striped', 'solid')
        else:
            if self.player == 1:
                self.colors = ('striped', 'solid')
            else:
                self.colors = ('solid', 'striped')

    def end_game(self, is_won):
        if is_won:
            if self.player == 1:
                self.who_won = 1
            else:
                self.who_won = 2
        else:
            if self.player == 1:
                self.who_won = 2
            else:
                self.who_won = 1
        screen.game_over()
        game.running = False

# ------------------------------------------------------------
# CLASS BALL -------------------------------------------------
# ------------------------------------------------------------

class Ball(object):
    # Initialize a class instance.
    def __init__(self, color):
        self.color = color # Ball's color.
        self.pos = [0, 0] # Ball's position.
        self.angle = 0 # Ball's movement angle.
        self.speed = 0 # Ball's movement speed.

    # Place the ball at its starting position (depending on its color).
    def place(self):
        if self.color == WHITE_COLOR:
            self.pos = [POOL_TABLE_SIZE[0] / 4, POOL_TABLE_SIZE[1] / 2]
        elif self.color == BLACK_COLOR:
            self.pos = [POOL_TABLE_SIZE[0] * 3 / 4 + 4 * BALL_RADIUS, POOL_TABLE_SIZE[1] / 2]
        elif self.color == PURPLE_COLOR:
            self.pos = [POOL_TABLE_SIZE[0] * 3 / 4, POOL_TABLE_SIZE[1] / 2]
        elif self.color == GREEN_COLOR:
            self.pos = [POOL_TABLE_SIZE[0] * 3 / 4 + 6 * BALL_RADIUS, POOL_TABLE_SIZE[1] / 2 + 3 * BALL_RADIUS]
        elif self.color == BLUE_COLOR:
            self.pos = [POOL_TABLE_SIZE[0] * 3 / 4 + 8 * BALL_RADIUS, POOL_TABLE_SIZE[1] / 2 + 4 * BALL_RADIUS]
        elif self.color == ORANGE_COLOR:
            self.pos = [POOL_TABLE_SIZE[0] * 3 / 4 + 8 * BALL_RADIUS, POOL_TABLE_SIZE[1] / 2 - 2 * BALL_RADIUS]
        elif self.color == YELLOW_COLOR:
            self.pos = [POOL_TABLE_SIZE[0] * 3 / 4 + 4 * BALL_RADIUS, POOL_TABLE_SIZE[1] / 2 - 2 * BALL_RADIUS]
        elif self.color == RED_COLOR:
            self.pos = [POOL_TABLE_SIZE[0] * 3 / 4 + 4 * BALL_RADIUS, POOL_TABLE_SIZE[1] / 2 + 2 * BALL_RADIUS]
        elif self.color == BROWN_COLOR:
            self.pos = [POOL_TABLE_SIZE[0] * 3 / 4 + 8 * BALL_RADIUS, POOL_TABLE_SIZE[1] / 2]
        elif self.color == PURPLE_STRIPED_COLOR:
            self.pos = [POOL_TABLE_SIZE[0] * 3 / 4 + 8 * BALL_RADIUS, POOL_TABLE_SIZE[1] / 2 - 4 * BALL_RADIUS]
        elif self.color == GREEN_STRIPED_COLOR:
            self.pos = [POOL_TABLE_SIZE[0] * 3 / 4 + 2 * BALL_RADIUS, POOL_TABLE_SIZE[1] / 2 + BALL_RADIUS]
        elif self.color == BLUE_STRIPED_COLOR:
            self.pos = [POOL_TABLE_SIZE[0] * 3 / 4 + 2 * BALL_RADIUS, POOL_TABLE_SIZE[1] / 2 - BALL_RADIUS]
        elif self.color == ORANGE_STRIPED_COLOR:
            self.pos = [POOL_TABLE_SIZE[0] * 3 / 4 + 6 * BALL_RADIUS, POOL_TABLE_SIZE[1] / 2 - BALL_RADIUS]
        elif self.color == YELLOW_STRIPED_COLOR:
            self.pos = [POOL_TABLE_SIZE[0] * 3 / 4 + 8 * BALL_RADIUS, POOL_TABLE_SIZE[1] / 2 + 2 * BALL_RADIUS]
        elif self.color == RED_STRIPED_COLOR:
            self.pos = [POOL_TABLE_SIZE[0] * 3 / 4 + 6 * BALL_RADIUS, POOL_TABLE_SIZE[1] / 2 + BALL_RADIUS]
        elif self.color == BROWN_STRIPED_COLOR:
            self.pos = [POOL_TABLE_SIZE[0] * 3 / 4 + 6 * BALL_RADIUS, POOL_TABLE_SIZE[1] / 2 - 3 * BALL_RADIUS]

    # Move the ball.
    def move(self):
        if self.speed < SPEED_THRESHOLD: # If the speed is low enough, set it to 0.
            self.speed = 0
        
        self.pos[0] += math.cos(self.angle) * self.speed
        self.pos[1] += math.sin(self.angle) * self.speed
        self.speed *= DRAG # Apply air resistance.

    # Check if the ball has collided with a border.
    def bounce(self):
        if self.pos[0] >= POOL_TABLE_SIZE[0] - 2 * POOL_TABLE_POCKET_RADIUS - BALL_RADIUS:
            if self.color == WHITE_COLOR and rules.is_cue_ball_moveable: # Special case for the cue ball when it's being moved by the mouse.
                self.pos[0] = POOL_TABLE_SIZE[0] - 2 * POOL_TABLE_POCKET_RADIUS - BALL_RADIUS
            else:
                self.pos[0] = 2 * (POOL_TABLE_SIZE[0] - 2 * POOL_TABLE_POCKET_RADIUS - BALL_RADIUS) - self.pos[0]
                self.angle = math.pi - self.angle
                self.speed *= ELASTICITY # Apply friction.
        elif self.pos[0] <= 2 * POOL_TABLE_POCKET_RADIUS + BALL_RADIUS:
            if self.color == WHITE_COLOR and rules.is_cue_ball_moveable:
                self.pos[0] = 2 * POOL_TABLE_POCKET_RADIUS + BALL_RADIUS
            else:
                self.pos[0] = 2 * (2 * POOL_TABLE_POCKET_RADIUS + BALL_RADIUS) - self.pos[0]
                self.angle = math.pi - self.angle
                self.speed *= ELASTICITY
            
        if self.pos[1] >= POOL_TABLE_SIZE[1] - 2 * POOL_TABLE_POCKET_RADIUS - BALL_RADIUS:
            if self.color == WHITE_COLOR and rules.is_cue_ball_moveable:
                self.pos[1] = POOL_TABLE_SIZE[1] - 2 * POOL_TABLE_POCKET_RADIUS - BALL_RADIUS
            else:
                self.pos[1] = 2 * (POOL_TABLE_SIZE[1] - 2 * POOL_TABLE_POCKET_RADIUS - BALL_RADIUS) - self.pos[1]
                self.angle = -self.angle
                self.speed *= ELASTICITY
        elif self.pos[1] <= 2 * POOL_TABLE_POCKET_RADIUS + BALL_RADIUS:
            if self.color == WHITE_COLOR and rules.is_cue_ball_moveable:
                self.pos[1] = 2 * POOL_TABLE_POCKET_RADIUS + BALL_RADIUS
            else:
                self.pos[1] = 2 * (2 * POOL_TABLE_POCKET_RADIUS + BALL_RADIUS) - self.pos[1]
                self.angle = -self.angle
                self.speed *= ELASTICITY

    # Select the cue ball.
    def select_cue_ball(self):
        if math.hypot(self.pos[0] - screen.mouse_pos[0], self.pos[1] - screen.mouse_pos[1]) <= BALL_RADIUS:
            return True
        return False

    # Move the cue ball.
    def move_cue_ball(self):
        (dx, dy) = (screen.mouse_pos[0] - self.pos[0], screen.mouse_pos[1] - self.pos[1])
        self.angle = math.atan2(dy, dx)
        self.speed = math.hypot(dx, dy) * 0.1

    # Pocket the ball.
    def pocket(self):
        if self.pos[0] < 3 * POOL_TABLE_POCKET_RADIUS and self.pos[1] < 3 * POOL_TABLE_POCKET_RADIUS:
            i = game.balls.index(self)
            rules.balls_pocketed.append(game.balls[i]) # Append the pocketed ball to the pocketed balls array.
            if self.color == WHITE_COLOR: # If the cue ball is pocketed while being held with the mouse, this condition prevents a major bug.
                rules.is_cue_ball_selected = False
            del game.balls[i] # Remove the pocketed ball from the balls array (and from the screen).
            
        elif self.pos[0] > POOL_TABLE_SIZE[0] / 2 - POOL_TABLE_POCKET_RADIUS and self.pos[0] < POOL_TABLE_SIZE[0] / 2 + POOL_TABLE_POCKET_RADIUS and self.pos[1] < 3 * POOL_TABLE_POCKET_RADIUS:
            i = game.balls.index(self)
            rules.balls_pocketed.append(game.balls[i])
            if self.color == WHITE_COLOR:
                rules.is_cue_ball_selected = False
            del game.balls[i]
            
        elif self.pos[0] > POOL_TABLE_SIZE[0] - 3 * POOL_TABLE_POCKET_RADIUS and self.pos[1] < 3 * POOL_TABLE_POCKET_RADIUS:
            i = game.balls.index(self)
            rules.balls_pocketed.append(game.balls[i])
            if self.color == WHITE_COLOR:
                rules.is_cue_ball_selected = False
            del game.balls[i]
            
        elif self.pos[0] < 3 * POOL_TABLE_POCKET_RADIUS and self.pos[1] > POOL_TABLE_SIZE[1] - 3 * POOL_TABLE_POCKET_RADIUS:
            i = game.balls.index(self)
            rules.balls_pocketed.append(game.balls[i])
            if self.color == WHITE_COLOR:
                rules.is_cue_ball_selected = False
            del game.balls[i]
            
        
        elif self.pos[0] > POOL_TABLE_SIZE[0] / 2 - POOL_TABLE_POCKET_RADIUS and self.pos[0] < POOL_TABLE_SIZE[0] / 2 + POOL_TABLE_POCKET_RADIUS and self.pos[1] > POOL_TABLE_SIZE[1] - 3 * POOL_TABLE_POCKET_RADIUS:
            i = game.balls.index(self)
            rules.balls_pocketed.append(game.balls[i])
            if self.color == WHITE_COLOR:
                rules.is_cue_ball_selected = False
            del game.balls[i]
            
        elif self.pos[0] > POOL_TABLE_SIZE[0] - 3 * POOL_TABLE_POCKET_RADIUS and self.pos[1] > POOL_TABLE_SIZE[1] - 3 * POOL_TABLE_POCKET_RADIUS:
            i = game.balls.index(self)
            rules.balls_pocketed.append(game.balls[i])
            if self.color == WHITE_COLOR:
                rules.is_cue_ball_selected = False
            del game.balls[i]

    # Draw the ball at its current position.
    def draw(self):
        if len(self.color) == 4: # Draw a striped ball.
            pygame.draw.circle(screen.screen, self.color, (int(self.pos[0]), int(self.pos[1])), BALL_RADIUS, 5)
        else: # Draw a solid ball.
            pygame.draw.circle(screen.screen, self.color, (int(self.pos[0]), int(self.pos[1])), BALL_RADIUS)

# ------------------------------------------------------------
# GLOBAL VARIABLES -------------------------------------------
# ------------------------------------------------------------

screen = Screen()
game = Game()
rules = Rules()

# ------------------------------------------------------------
# COLLISION DETECTION FUNCTION--------------------------------
# ------------------------------------------------------------

def collide(b1, b2):
    # Calculate the distance between the centers of two balls. If it's less or equal than 2 * BALL_RADIUS, the balls have collided.
    (dx, dy) = (b1.pos[0] - b2.pos[0], b1.pos[1] - b2.pos[1])
    dist = math.hypot(dx, dy)
    
    if dist <= 2 * BALL_RADIUS:
        if b1.color == WHITE_COLOR and len(rules.hits) == 0: # Record which ball was hit first by the cue ball.
            rules.hits.append(b2)
        elif b2.color == WHITE_COLOR and len(rules.hits) == 0:
            rules.hits.append(b1)
        
        tangent = math.atan2(dy, dx) + math.pi / 2 # The angle tangent to the balls.
        angle = tangent - math.pi / 2 # The angle between two balls which is perpendicular to the tangent angle.

        # Apply these rules if one ball if moving and another ball is stationary. Source: http://en.wikipedia.org/wiki/Elastic_collision#Two-_and_three-dimensional
        if b1.speed == 0:
            angle2 = math.atan2(math.sin(angle), 1 + math.cos(angle))
            angle1 = (math.pi - angle) / 2
            speed2 = (b2.speed * math.sqrt((1 + math.cos(angle)) / 2)) * ELASTICITY # Apply the friction.
            speed1 = (b2.speed * math.sin(angle / 2)) * ELASTICITY
        elif b2.speed == 0:
            angle1 = math.atan2(math.sin(angle), 1 + math.cos(angle))
            angle2 = (math.pi - angle) / 2
            speed1 = (b1.speed * math.sqrt((1 + math.cos(angle)) / 2)) * ELASTICITY
            speed2 = (b1.speed * math.sin(angle / 2)) * ELASTICITY

        # Apply these rules if both balls are moving. Source: http://en.wikipedia.org/wiki/Elastic_collision#Two-_and_three-dimensional
        else:
            vx1_after = b2.speed * math.cos(b2.angle - angle) * math.cos(angle) + b1.speed * math.sin(b1.angle - angle) * math.cos(angle + math.pi / 2)
            vy1_after = b2.speed * math.cos(b2.angle - angle) * math.sin(angle) + b1.speed * math.sin(b1.angle - angle) * math.sin(angle + math.pi / 2)
            vx2_after = b1.speed * math.cos(b1.angle - angle) * math.cos(angle) + b2.speed * math.sin(b2.angle - angle) * math.cos(angle + math.pi / 2)
            vy2_after = b1.speed * math.cos(b1.angle - angle) * math.sin(angle) + b2.speed * math.sin(b2.angle - angle) * math.sin(angle + math.pi / 2)
            angle1 = math.atan2(vy1_after, vx1_after)
            angle2 = math.atan2(vy2_after, vx2_after)
            speed1 = (vx1_after / math.cos(angle1)) * ELASTICITY
            speed2 = (vx2_after / math.cos(angle2)) * ELASTICITY

        # Set the new angle/speed for both balls.
        (b1.angle, b1.speed) = (angle1, speed1)
        (b2.angle, b2.speed) = (angle2, speed2)

        # Since time is discrete (i.e. the screen cannot be updated every microsecond), by the time the screen is updated the balls have already overlapped.
        # We need to set them apart so that they won't "stick" together.
        overlap = 2 * BALL_RADIUS - dist + 1
        b1.pos[0] += math.cos(angle) * 0.5 * overlap
        b1.pos[1] += math.sin(angle) * 0.5 * overlap
        b2.pos[0] -= math.cos(angle) * 0.5 * overlap
        b2.pos[1] -= math.sin(angle) * 0.5 * overlap
    
# ------------------------------------------------------------
# MAIN FUNCTION ----------------------------------------------
# ------------------------------------------------------------

def main():
    # Create a custom event which will detect when the song ends.
    SONG_END = pygame.USEREVENT + 1
    pygame.mixer.music.set_endevent(SONG_END)
    
    # Create the balls and place them at their starting positions.
    game.create_balls()
    for ball in game.balls:
        ball.place()

    # The game loop.
    while game.running:
        # The event loop.
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # The user closes the window.
                game.running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # The user presses the ESC key.
                    game.running = False
                    
            if event.type == pygame.MOUSEMOTION: # The user moves the mouse.
                screen.mouse_pos = pygame.mouse.get_pos() # Record the mouse position.
                
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == 1: # The user presses the left mouse button.
                game.music_player() # Turn the music on/off.
                rules.is_cue_ball_selected = game.balls[0].select_cue_ball() # Select the cue ball.
                
            if event.type == pygame.MOUSEBUTTONUP: # The user releases a mouse button.
                rules.is_cue_ball_selected = False # Release the cue ball.
                if rules.is_cue_ball_moved: # Throw the cue ball.
                    rules.is_cue_ball_moveable = False
                    rules.is_cue_ball_moved = False
                    rules.is_cue_ball_thrown = True
                
            if event.type == SONG_END: # Check if the current music theme ended.
                game.music_queue() # Select the next song to play.

        # Clear the screen and draw graphics.
        screen.fill()
        screen.draw_pool_table()
        screen.update_bar()
        screen.draw_bar()

        # Move the cue ball if it's selected.
        if rules.is_cue_ball_selected and rules.is_cue_ball_moveable:
            game.balls[0].move_cue_ball()
            rules.is_cue_ball_moved = True

        # For each ball do this: move, bounce (check for collision with borders), check for collision with other balls, and draw.
        for i, ball1 in enumerate(game.balls):
            ball1.move()
            ball1.pocket()
            ball1.bounce()
            for ball2 in game.balls[i + 1:]:
                collide(ball1, ball2)
            ball1.draw()

        # Update the screen.
        screen.update()  

        # Check the game rules.
        rules.check_rules()

        # Update the screen again.
        screen.update()  

if __name__ == '__main__':
    main()
    pygame.quit() # Stop the Pygame engine.

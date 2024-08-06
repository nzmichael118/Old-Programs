import pygame
import sys, os
# Local Modules
import cards
import client


RESOLUTION = WIDTH, HEIGHT = 800, 900
FPS = 30 # 60FPS is probably excessive for this

class Gui():
    """
    Flow:
    __init__ > self.display_menu > self.pre_lobby > self.lobby >
    self.game_gui
    """
    def __init__(self):
        self.background_color = "green"
        self.colors ={
            "red":   "#AB1A1A",
            "green": "#4FAB1A",
            "dark":  "#080E12",
            "darker":"#000000"
            }
        pygame.init()
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.font = pygame.font.SysFont(None, 30)
        self.clock =  pygame.time.Clock()

        self.display_menu()

    def pre_lobby(self):
        """Gets username (ip if we weren't forcing localhost)"""
        # GUI stuff blah blah blah
        waiting_input = True
        input_box = InputBox((400, 40), (100, 300), "name")
        while waiting_input:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.name = input_box.msg
                        waiting_input = False
                        print("pp")
                input_box.event_check(event)
                
                self.screen.fill(self.colors[self.background_color])
                input_box.render(self.screen)
                pygame.display.update()

        self.curr_client = client.Client(self.name)
        self.lobby()



    def lobby(self):
        # check if game ready beofre start
        player_list = ListBox((100,100), (400, 400), self.curr_client.game_state.connected_players)
        while not self.curr_client.game_state.has_started:
            self.clock.tick(FPS)
            player_list.items = self.curr_client.game_state.connected_players
            for event in pygame.event.get():
                # Event loop
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill(self.colors[self.background_color])
            player_list.render(self.screen)
            pygame.display.update()
        self.game_gui()

    def game_gui(self):
        print("Yoda gamign")

    def display_menu(self):
        """Displays the main menu of the GUI"""
        in_menu = True
        
        self.start_button = Button((400, 50), (200, 400), "Start Game")
        start_box = pygame.Surface((400, 50))
        start_box.fill('White')
        while in_menu:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                # Event loop
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.is_cursor_over():
                        in_menu = False
                        self.pre_lobby()


            self.start_button.is_cursor_over()
                
            self.screen.fill(self.colors[self.background_color])
            self.start_button.render(self.screen)
            pygame.display.update()
            

class Button():
    """Sets up rendering for on screen buttons"""
    def __init__(self, size, pos, text, font_size=30):
        """size: int(x, y), pos: int(x, y), text: str"""
        self.font = pygame.font.SysFont(None, font_size)
        self.size = size
        self.pos = pos
        self.text = text
        self.box_surface = pygame.Surface(self.size)
        self.box_surface.fill('White')
        self.text_surface = self.font.render(self.text, True, '#000000')
        self.text_rect = pygame.Rect((0,0), (self.font.size(text)))

    def render(self, screen):
        """Blits button on screen with text centred"""
        screen.blit(self.box_surface, self.pos)
        # Gets middle of box in full coords of screen
        self.text_rect.centerx = int((self.size[0] / 2) + self.pos[0]) 
        self.text_rect.centery = int((self.size[1] / 2) + self.pos[1])
        screen.blit(self.text_surface, self.text_rect)

    def is_cursor_over(self):
        """returns true if cursor pos is over button changes color"""
        cursor_pos = pygame.mouse.get_pos()
        if self.pos[0] < cursor_pos[0] < (self.pos[0] + self.size[0]):
            if self.pos[1] < cursor_pos[1] < (self.pos[1] + self.size[1]):
                self.box_surface.fill('#DDDDDD')
                return(True)
        
        self.box_surface.fill('white')
        return(False)

                
class InputBox():
    def __init__(self, default_size, pos, default_msg, font_size=30):
        """default_size=(x,y), defaultmsg="string" ,fontsize=int"""
        self.size = default_size
        self.pos = pos # (x,y)
        self.content = default_msg
        self.box_surface = pygame.Surface(self.size)
        self.box_surface.fill('White')
        self.font = pygame.font.Font(None, font_size)
        self.msg = default_msg
        self.active = False
        

    def event_check(self, event):
        """Passes in event from event loop to manage all
        logic within class"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.pos[0] <mouse_pos[0] < (self.pos[0] + self.size[0]):
                if self.pos[1] < mouse_pos[1] < (self.pos[1] + self.size[1]):
                    self.active = True
                    self.box_surface.fill("#EEEEEE")
                else:
                    self.active = False
                    self.box_surface.fill('White')
            else:
                self.active = False
                self.box_surface.fill('White')


        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.msg = self.msg[:-1]
                else:
                    self.msg += event.unicode

    def render(self, screen):
        msg_surface = self.font.render(self.msg, True, (0,0,0))
        screen.blit(self.box_surface, self.pos)
        screen.blit(msg_surface, self.pos)


class ListBox():
    """Box containing a list of content"""
    def __init__(self, pos, size, items, font_size=30):
        """pos(x,y), size(x,y), items str[]"""
        self.items = items
        self.pos = pos
        self.size = size
        self.background_surface = pygame.Surface(self.size)
        self.background_surface.fill('White')
        self.font = pygame.font.Font(None, font_size)

    def render(self, screen):

        screen.blit(self.background_surface, self.pos)
        for i in range(len(self.items)):
            self.msg_surface = self.font.render(self.items[i], True, (0,0,0))
            screen.blit(self.msg_surface, (self.pos[0] + 10, (self.pos[1] + 20*i )))

class CardManager():
    """renders cards"""
    def __init__(self, pos):
        self.pos = pos
        # TODO: load card images to surfaces
        self.card_surfaces = {}

    def render(self, face):
        pass

if __name__ == "__main__":
    gui = Gui()
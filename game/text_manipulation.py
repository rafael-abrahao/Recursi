from pygame.font import Font
from pygame import Surface, SRCALPHA, Rect

BASE_COLOR = 'White'

def get_vertical_surface(render_lines) -> Surface:
    max_width = 0
    total_height = 0
    for render in render_lines:
        if render != None:
            max_width = max(render.get_width(), max_width)
            total_height += render.get_height()

    return Surface((max_width, total_height))

def render_dif(render_lines, reverse = False) -> Surface:
    new_surf = get_vertical_surface(render_lines)

    curr_height = 0
    if reverse:
        curr_height = new_surf.get_height()
    for render in render_lines:
        if render != None:
            if reverse:
                curr_height -= render.get_height()
            new_surf.blit(render, (0, curr_height))
            if not reverse:
                curr_height += render.get_height()
    
    return new_surf

def render_same(render_lines) -> Surface:
    total_width = 0
    max_height = 0
    for render in render_lines:
        if render != None:
            max_height = max(render.get_height(), max_height)
            total_width += render.get_width()

    new_surf = Surface((total_width, max_height))
    curr_width = 0
    for render in render_lines:
        if render != None:
            new_surf.blit(render, (curr_width, 0))
            curr_width += render.get_width()
    
    return new_surf

def render_mult(text, font: Font) -> list:
    renders = []
    for line in text:
        renders.append(font.render(line, True, BASE_COLOR))
    
    return renders

def format_text(text: str, font: Font, max_width) -> list:
    test_str = ''
    formated_text = []
    for word in text.split(' '):
        previous_str = test_str
        test_str += word + ' '
        test_render = font.render(test_str.strip(), False, 'White')
        if test_render.get_width() > max_width:
            formated_text.append(previous_str.strip())
            test_str = word + ' '
    if len(test_str.strip()) > 0:
        formated_text.append(test_str.strip())
    return formated_text

class Typewriter:
    def __init__(self, text, font: Font):
        self.text = text
        self.font = font
        self.current_text = ""
        self.current_index = 0
        self.delay = 2  # Delay between letter display (in frames)
        self.timer = 0
        self.finished = False

    def update(self):
        if not self.finished:
            if self.timer == self.delay:
                self.current_index += 1
                self.current_text = self.text[:self.current_index]
                if self.current_index >= len(self.text):
                    self.finished = True
                self.timer = 0
            else:
                self.timer += 1

    def get_render(self) -> Surface:
        return self.font.render(self.current_text, True, 'White')

class Dialogue:
    def __init__(self, screen: Surface, text: str, display_rect: Rect, font: Font) -> None:
        self.screen = screen
        self.text = format_text(text, font, display_rect.width)
        self.display_rect = display_rect
        self.font = font
        self.line_index = 0
        self.active_writers = []
        self.active_rectangles = []
        self.finished = False
        self.topleft_coord = (display_rect.topleft[0] + 10, display_rect.topleft[1] + 10)
        self.__add_writer()
    
    def __add_writer(self):
        new_writer = Typewriter(self.text[self.line_index], self.font)
        self.active_writers.append(new_writer)
        self.line_index += 1

    def write(self):
        for writer_index in range(len(self.active_writers)):
            self.active_writers[writer_index].update()
            render = self.active_writers[writer_index].get_render()
            render_rect = render.get_rect(topleft = self.topleft_coord)
            self.topleft_coord = render_rect.bottomleft
            self.screen.blit(render, render_rect)

        self.topleft_coord = (self.display_rect.topleft[0] + 10, self.display_rect.topleft[1] + 10)

        if not self.finished and self.active_writers[-1].finished:
            if self.line_index < len(self.text):
                self.__add_writer()
            else:
                self.finished = True

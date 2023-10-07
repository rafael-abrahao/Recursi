from pygame.font import Font
from pygame import Surface, SRCALPHA, Rect, draw

from text_manipulation import render_dif, render_mult, render_same, get_vertical_surface

BASE_COLOR = 'White'
N_COLOR = 'Green'
RECCALL_COLOR = 'Yellow'
RET_COLOR = 'Orange'
FINAL_COLOR = 'Red'

class FatRender:
    def __init__(self, font: Font) -> None:
        self.font = font
        self.image = None
        self.rect = None
        self.__start()
        self.__renders = self.__base_renders.copy()
        self.update()

    def __start(self):
        fat_text = ['int fat(','int n','){',
                    '    if(','n',' <= 1)',
                    '        ','return 1',';',
                    '    return ','n * fat(n - 1)',';',
                    '}']
        self.__n_render = self.font.render('n', True, BASE_COLOR)
        self.__base_renders = render_mult(fat_text, self.font)

    def __update_rect(self):
        if self.rect != None:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        else:
            self.rect = self.image.get_rect()

    def update(self):
        temp_renders = []
        temp_renders.append(render_same(self.__renders[0:3]))
        temp_renders.append(render_same(self.__renders[3:6]))
        temp_renders.append(render_same(self.__renders[6:9]))
        temp_renders.append(render_same(self.__renders[9:12]))
        temp_renders.append(self.__renders[12])

        self.image = render_dif(temp_renders)
        self.__update_rect()

    def change_n(self, number, is_base = False):
        self.__n_render = self.font.render(str(number), True, N_COLOR)
        self.__renders[1] = self.__renders[4] = self.__n_render
        if not is_base:
            self.__renders[10] = render_same([self.__n_render,
                                            self.font.render(' * fat( n - 1)', True, BASE_COLOR)])

    def change_reccall(self, number):
        self.__renders[10] = render_same([self.__n_render,
                                        self.font.render(' * fat(', True, BASE_COLOR),
                                        self.font.render(str(number), True, RECCALL_COLOR),
                                        self.font.render(')', True, BASE_COLOR)])

    def change_ret(self, number):
        self.__renders[10] = render_same([self.__n_render,
                                        self.font.render(' * ', True, BASE_COLOR),
                                        self.font.render(str(number), True, RET_COLOR)])
    
    def change_final(self, number):
        self.__renders[10] = self.font.render(str(number), True, FINAL_COLOR)

    def change_base(self):
        self.__renders[7] = render_same([self.font.render('return ', True, BASE_COLOR),
                                         self.font.render('1', True, RET_COLOR)])

    def reset(self):
        self.__renders = self.__base_renders.copy()
        self.__n_render = self.font.render('n', True, BASE_COLOR)

class FibRender:
    def __init__(self, font: Font) -> None:
        self.font = font
        self.image = None
        self.rect = None
        self.__start()
        self.__renders = self.__base_renders.copy()
        self.render()

    def __start(self):
        fib_text = ['int fib(','int n','){',
                    '   if(','n',' == 1)',
                    '       return ','1',';',
                    '   if(','n',' <= 0)',
                    '       return ','0',';',
                    '   return ','fib(n - 1) + fib(n - 2)',';',
                    '}']
        self.__base_renders = render_mult(fib_text, self.font)

    def __update_rect(self):
        if self.rect != None:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        else:
            self.rect = self.image.get_rect()
    
    def render(self):
        temp_renders = []
        temp_renders.append(render_same(self.__renders[0:3]))
        temp_renders.append(render_same(self.__renders[3:6]))
        temp_renders.append(render_same(self.__renders[6:9]))
        temp_renders.append(render_same(self.__renders[9:12]))
        temp_renders.append(render_same(self.__renders[12:15]))
        temp_renders.append(render_same(self.__renders[15:18]))
        temp_renders.append(self.__renders[18])

        self.image = render_dif(temp_renders)
        self.__update_rect()

    def change_n(self, number):
        n_render = self.font.render(str(number), True, N_COLOR)
        self.__renders[1] = self.__renders[4] = self.__renders[10] = n_render

        self.render()

    def change_reccall(self, number):
        self.__renders[16] = render_same([self.font.render('fib(', True, BASE_COLOR),
                                        self.font.render(str(number - 1), True, RECCALL_COLOR),
                                        self.font.render(') + fib(', True, BASE_COLOR),
                                        self.font.render(str(number - 2), True, RECCALL_COLOR),
                                        self.font.render(')', True, BASE_COLOR)])
        
        self.render()

    def __reset_reccall(self):
        self.__renders[16] = self.font.render('fib(n - 1) + fib(n - 2)', True, BASE_COLOR)
        
        self.render()

    def change_ret(self, ret1, ret2, n = None):
        if n != None:
            render2 = render_same([self.font.render('fib(', True, BASE_COLOR),
                                  self.font.render(str(n - 2), True, RECCALL_COLOR),
                                  self.font.render(')', True, BASE_COLOR)])
        else:
            render2 = self.font.render(str(ret2), True, RET_COLOR)

        self.__renders[16] = render_same([self.font.render(str(ret1), True, RET_COLOR),
                                        self.font.render(' + ', True, BASE_COLOR),
                                        render2])

        self.render()

    def change_final(self, number):
        self.__renders[16] = self.font.render(str(number), True, FINAL_COLOR)

        self.render()

    def highlight_one(self):
        self.__renders[7] = self.font.render('1', True, FINAL_COLOR)
        self.__reset_reccall()

        self.render()

        self.__renders[7] = self.font.render('1', True, BASE_COLOR)

    def highlight_zero(self):
        self.__renders[13] = self.font.render('0', True, FINAL_COLOR)
        self.__reset_reccall()

        self.render()

        self.__renders[13] = self.font.render('0', True, BASE_COLOR)

    def reset(self):
        self.__renders = self.__base_renders.copy()

class FatStackEntry:
    def __init__(self, n_value: int, below_ret: int, ret_add: str):
        self.n_value = n_value
        self.below_ret = below_ret
        if n_value > 1:
            self.ret_value = n_value * below_ret
        else:
            self.ret_value = 1
        self.ret_add = ret_add

    def __str__(self) -> str:
        return f'n:{self.n_value}, below:{self.below_ret}, ret_value:{self.ret_value}, ret_add:{self.ret_add}'

def simulate_fat(n):
    stack = []
    __fat(n, stack, 'main')
    stack.reverse()

    return stack

def __fat(n, stack: list, add: str):
    if n <= 1:
        return 1
    ret_below = __fat(n - 1, stack, f'fat({n})')
    stack.append(FatStackEntry(n, ret_below, add))
    return n * ret_below

class StackRender:
    def __init__(self, font: Font, stack: list) -> None:
        self.font = font
        self.__renders = []
        self.size = len(stack)
        for entry in stack:
            self.__renders.append(render_dif(render_mult([f'RET: {entry.ret_add}',
                                                          f'N: {entry.n_value}'], font)))
        self.__base_surface = get_vertical_surface(self.__renders)
        self.image = self.__base_surface.copy()
        self.rect = self.image.get_rect()

    def update_render(self, stack_index):
        self.image = self.__base_surface.copy()
        curr_height = self.image.get_height()
        for index in range(stack_index):
            curr_surf = self.__renders[index]
            curr_height -= curr_surf.get_height()
            self.image.blit(curr_surf, (0, curr_height))

class FatHandler:
    def __init__(self, fat: FatRender):
        fat.reset()
        fat.update()
        self.fat = fat
        self.index = 0
        self.unstacking = False
        self.finished = True

    def reset(self):
        self.index = 0
        self.unstacking = False
        self.finished = True

    def load(self, stack: list, n_value):
        self.reset()
        self.fat.reset()
        self.finished = False
        self.n_value = n_value

        if len(stack) > 0:
            self.stack = stack.copy()
            stack.reverse()
            self.stack.append(None)
            self.stack.extend(stack)
            stack.reverse()
            self.has_recursion = True
        else:
            self.has_recursion = False

        if self.has_recursion:
            entry = self.stack[self.index]
            self.fat.change_n(entry.n_value)
            self.fat.change_reccall(entry.n_value - 1)
            self.fat.update()
        else:
            self.fat.change_n(self.n_value, True)
        self.fat.update()

    def advance(self):
        if not self.has_recursion and not self.finished:
            self.fat.change_base()
            self.fat.update()
            self.finished = True
        if not self.has_recursion or self.finished:
            return

        self.index += 1

        if self.index == len(self.stack):
            entry = self.stack[-1]
            self.fat.change_n(entry.n_value)
            self.fat.change_final(entry.ret_value)
            self.fat.update()
            self.finished = True
            return

        entry = self.stack[self.index]
        if entry == None:
            self.unstacking = True
            self.fat.reset()
            self.fat.change_n(1, True)
            self.fat.change_base()
            self.fat.update()
            self.fat.reset()
        else:
            self.fat.change_n(entry.n_value)
            if not self.unstacking:
                self.fat.change_reccall(entry.n_value - 1)
            else:
                self.fat.change_ret(entry.below_ret)
            self.fat.update()

class StackHandler:
    def __init__(self, stack_render: StackRender) -> None:
        self.render = stack_render
        self.index = 0
        self.add = 1

    def advance(self):
        if self.render.size == 0:
            return
        if self.index < 0: self.index = 0
        self.index += self.add
        self.render.update_render(self.index)
        if self.index == self.render.size:
            self.add = -1

class TreeNode:
    def __init__(self, text: str) -> None:
        self.text = text
        self.value = None
        self.right = None
        self.left = None
        self.rect = Rect(0, 0, 5, 5)

    def load_rect(self, size):
        self.rect = Rect(0, 0, size, size)

def get_level(root: TreeNode):
    level = 0
    while root.left != None:
        level += 1
        root = root.left
    return level

def tree_to_stack(tree: TreeNode):
    stack = []
    __tree_to_stack_aux(tree, stack)
    return stack

def __tree_to_stack_aux(root: TreeNode, stack: list):
    stack.append(root.text)
    if root.left != None:
        __tree_to_stack_aux(root.left, stack)
        stack.append(root.text)
    if root.right != None:
        __tree_to_stack_aux(root.right, stack)
        stack.append(root.text)
    stack.append(root.value)

def generate_fibtree(n) -> TreeNode:
    return __fib_aux(n)[1]

def __fib_aux(n):
    node = TreeNode(f'fib({n})')
    if n <= 0:
        node.value = 0
        return (node.value, node)
    if n == 1:
        node.value = 1
        return (node.value, node)
    value1 = __fib_aux(n - 1)
    value2 = __fib_aux(n - 2)
    node.value = value1[0] + value2[0]
    node.left = value1[1]
    node.right = value2[1]
    return (node.value, node)

class TreeRender:
    def __init__(self, screen: Surface, root: TreeNode) -> None:
        self.__render_index = 0
        self.__root = root

        self.__level = get_level(self.__root)
        self.__node_size = 50
        min_size = 2 ** self.__level * (self.__node_size + 10)
        self.image = Surface((max(screen.get_width(), min_size), screen.get_height()), SRCALPHA)
        self.rect = self.image.get_rect()
        self.should_scroll = False
        if min_size > screen.get_width():
            self.should_scroll = True
        self.__load_rects(self.__root)
        spacing = (self.__root.rect.width/2 + 5) * 2 ** (max(self.__level, 3) - 1)

        self.__text_font = Font(None, int(self.__node_size/2))
        self.__value_font = Font(None, int(self.__node_size))
        self.__renders = []
        self.__load_first_node()

        self.__run(self.__root, spacing)

    def advance(self):
        if self.__render_index < len(self.__renders):
            self.image.blit(self.__renders[self.__render_index], (0,0))
            self.__render_index += 1


    def reset(self):
        self.image = Surface((self.image.get_width(), self.image.get_height()), SRCALPHA)
        self.__render_index = 0

    def __load_first_node(self):
        self.__root.rect.midtop = (self.image.get_width()/2, 10)
        new_surf = Surface((self.image.get_width(), self.image.get_height()), SRCALPHA)
        draw.rect(new_surf, '#0a6405', self.__root.rect)
        text = self.__text_font.render(str(self.__root.text), True, 'Green')
        text_rect = text.get_rect(center = self.__root.rect.center)
        new_surf.blit(text, text_rect)
        self.__renders.append(new_surf)

    def __load_rects(self, root: TreeNode):
        if root == None:
            return
        root.load_rect(self.__node_size)
        self.__load_rects(root.left)
        self.__load_rects(root.right)

    def __run(self, root: TreeNode, spacing, back_surf = None):
        back = Surface((self.image.get_width(), self.image.get_height()), SRCALPHA)
        back_txt = self.__text_font.render(str(root.text), True, 'Yellow')
        back_txt_rect = back_txt.get_rect(center = root.rect.center)
        back.blit(back_txt, back_txt_rect)
        if root.left != None:
            root.left.rect.midtop = root.rect.midtop
            root.left.rect.x -= spacing
            root.left.rect.y += self.__node_size + 10
            self.__renders.append(self.__paint((root, root.left)))
            self.__run(root.left, spacing/2, back.copy())
        if root.right != None:
            root.right.rect.midtop = root.rect.midtop
            root.right.rect.x += spacing
            root.right.rect.y += self.__node_size + 10
            self.__renders.append(self.__paint((root, root.right)))
            self.__run(root.right, spacing/2, back.copy())
        new_surf = None
        if back_surf == None:
            new_surf = Surface((self.image.get_width(), self.image.get_height()), SRCALPHA)
        else:
            new_surf = back_surf
        draw.rect(new_surf, '#0a6405', root.rect)
        txt = self.__value_font.render(str(root.value), True, 'White')
        txt_rect = txt.get_rect(center = root.rect.center)
        new_surf.blit(txt, txt_rect)
        self.__renders.append(new_surf)
        
    def __paint(self, nodes: tuple, colors = ('White', 'Yellow')):
        new_surf = Surface((self.image.get_width(), self.image.get_height()), SRCALPHA)
        draw.line(new_surf, 'Brown', nodes[0].rect.center, nodes[1].rect.center, int(self.__node_size/8))
        for x in range(2):
            draw.rect(new_surf, '#0a6405', nodes[x])
            txt = self.__text_font.render(nodes[x].text, True, colors[x])
            txt_rect = txt.get_rect(center = nodes[x].rect.center)
            new_surf.blit(txt, txt_rect)
        return new_surf

class FibState:
    def __init__(self, n: int, reccall: bool, ret1: int, ret2: int, final: int, highzero: bool, highone: bool):
        self.n = n
        self.reccall = reccall
        self.ret1 = ret1
        self.ret2 = ret2
        self.final = final
        self.highlight_zero = highzero
        self.highlight_one = highone

    def __str__(self) -> str:
        return f'n:{self.n} rets:{self.ret1},{self.ret2}, final:{self.final}'

    def apply(self, render: FibRender):
        render.change_n(self.n)
        if self.reccall:
            render.change_reccall(self.n)
        if self.ret1 != None:
            if self.ret2 == None:
                render.change_ret(self.ret1, None, self.n)
            else:
                render.change_ret(self.ret1, self.ret2)
        if self.final != None:
            render.change_final(self.final)
        if self.highlight_one:
            render.highlight_one()
        elif self.highlight_zero:
            render.highlight_zero()

def __simulate_fib_aux(n, stack: list):
    if n == 1:
        stack.append(FibState(1, False, None, None, None, False, True))
        return 1
    if n == 0:
        stack.append(FibState(0, False, None, None, None, True, False))
        return 0
    stack.append(FibState(n, True, None, None, None, False, False))
    ret1 = __simulate_fib_aux(n - 1, stack)
    stack.append(FibState(n, True, ret1, None, None, False, False))
    ret2 = __simulate_fib_aux(n - 2, stack)
    stack.append(FibState(n, True, ret1, ret2, None, False, False))
    return ret1 + ret2

def simulate_fib(n) -> list:
    states = []
    __simulate_fib_aux(n, states)
    last = states[-1]
    if n > 1:
        states.append(FibState(n, False, None, None, last.ret1 + last.ret2, False, False))
    return states
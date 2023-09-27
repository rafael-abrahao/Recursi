import pygame
import sys

from text_manipulation import render_mult
import func_renders

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

MAIN_MODE = 0
FAT_MODE = 1
FIB_MODE = 2

FUNC_MODE = 1
TREE_MODE = -1

MINITREE_RES = (256, 144)

running = True

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Recursi')
clock = pygame.time.Clock()

curr_mode = 0

font = pygame.font.Font(None, 60)

main_func_text = ['int main(){',
                  ' ',
                  '    fat(','9',');',
                  ' ',
                  '    fib(','9',');',
                  ' ',
                  '    return 0;',
                  '}']

main_func_renders = render_mult(main_func_text, font)
empty_surf = pygame.Surface((40, 41), pygame.SRCALPHA)
empty_surf.fill('Black')

main_func_renders[3] = empty_surf.copy()
main_func_renders[7] = empty_surf.copy()
main_func_rects = []
main_func_rects.append(main_func_renders[0].get_rect(midtop = (screen.get_width()/2, 200)))
main_func_rects.append(main_func_renders[1].get_rect(topleft = main_func_rects[0].bottomleft))
main_func_rects.append(main_func_renders[2].get_rect(topleft = main_func_rects[1].bottomleft))
main_func_rects.append(main_func_renders[3].get_rect(midleft = main_func_rects[2].midright))
main_func_rects.append(main_func_renders[4].get_rect(midleft = main_func_rects[3].midright))
main_func_rects.append(main_func_renders[5].get_rect(topleft = main_func_rects[2].bottomleft))
main_func_rects.append(main_func_renders[6].get_rect(topleft = main_func_rects[5].bottomleft))
main_func_rects.append(main_func_renders[7].get_rect(midleft = main_func_rects[6].midright))
main_func_rects.append(main_func_renders[8].get_rect(midleft = main_func_rects[7].midright))
main_func_rects.append(main_func_renders[9].get_rect(topleft = main_func_rects[6].bottomleft))
main_func_rects.append(main_func_renders[10].get_rect(topleft = main_func_rects[9].bottomleft))
main_func_rects.append(main_func_renders[11].get_rect(topleft = main_func_rects[10].bottomleft))

show_cursor = font.render('|', True, 'White')
hide_cursor = pygame.Surface(show_cursor.get_size(), pygame.SRCALPHA)
cursor_states = [show_cursor, hide_cursor]
cursor_rect = show_cursor.get_rect()
cursor_index = 0
curr_cursor = cursor_states[cursor_index]
cursor_timer = 0
cursor_delay = 15

fat_input = False
fib_input = False

fat_value = None
fib_value = None

includes = font.render('#include <stdio.h>', True, 'White')
includes_rect = includes.get_rect(bottomleft = main_func_rects[0].topleft)
includes_rect.y -= 30

go_btn = font.render('go', True, 'White')
go_hover = font.render('go', True, 'Yellow')
go_fat_rect = go_btn.get_rect(topleft = main_func_rects[4].topright)
go_fat_rect.x += 20
go_fib_rect = go_btn.get_rect(topleft = main_func_rects[8].topright)
go_fib_rect.x += 20

back_to_main = font.render('<< back', True, 'White')
back_to_main_hover = font.render('<< back', True, 'Yellow')
back_to_main_rect = back_to_main.get_rect(topleft = (0,0))
back_to_main_rect.x += 10
back_to_main_rect.y += 10

#fat objects
stack_font = pygame.font.Font(None, 35)

fat = func_renders.FatRender(font)
fat.rect.midtop = (SCREEN_WIDTH/2 - 100, 100)
fat_handler = func_renders.FatHandler(fat)

stack_render = None
stack_handler = None
stack = []

ntx_fat_btn = font.render('next', True, 'White')
ntx_fat_hover = font.render('next', True, 'Yellow')
ntx_fat_rect = ntx_fat_btn.get_rect()
ntx_fat_rect.midtop = (fat.rect.midbottom[0], fat.rect.midbottom[1] + 15)

#fib objects
root = None
states = None
state_index = 0
fib_finished = False
inner_mode = FUNC_MODE

func = func_renders.FibRender(font)
func.rect.midtop = (SCREEN_WIDTH/2 - 100, 20)
minitree = pygame.Surface(MINITREE_RES)
minitree_rect = minitree.get_rect(topleft = (func.rect.topright[0] + 40, func.rect.topright[1]))

func_btn = font.render('func', True, 'White')
func_btn_hover = font.render('func', True, 'Yellow')
func_btn_rect = func_btn.get_rect(topright = (SCREEN_WIDTH/2 - 20, SCREEN_HEIGHT - 60))

ntx_fib_image = font.render('next', True, 'White')
ntx_fib_hover = font.render('next', True, 'Yellow')
ntx_fib_rect = ntx_fib_image.get_rect(topleft = (SCREEN_WIDTH/2 + 20, SCREEN_HEIGHT - 60))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if curr_mode == MAIN_MODE:
            if event.type == pygame.MOUSEBUTTONUP:
                if main_func_rects[3].collidepoint(event.pos):
                    fat_input = True
                    if fat_value == None:
                        cursor_rect.topleft = main_func_rects[3].topleft
                    else:
                        cursor_rect.topright = main_func_rects[3].topright
                else:
                    fat_input = False
                if main_func_rects[7].collidepoint(event.pos):
                    fib_input = True
                    if fib_value == None:
                        cursor_rect.topleft = main_func_rects[7].topleft
                    else:
                        cursor_rect.topright = main_func_rects[7].topright
                else:
                    fib_input = False
                if fat_value != None and go_fat_rect.collidepoint(event.pos):
                    stack = func_renders.simulate_fat(fat_value)
                    fat_handler.load(stack, fat_value)
                    stack_render = func_renders.StackRender(stack_font, stack)
                    stack_render.rect.topleft = fat.rect.topright
                    stack_render.rect.x += 85
                    stack_render.rect.y -= 50
                    stack_handler = func_renders.StackHandler(stack_render)
                    curr_mode = FAT_MODE
                if fib_value != None and go_fib_rect.collidepoint(event.pos):
                    func.reset()
                    func.render()
                    minitree = pygame.Surface(MINITREE_RES)
                    root = func_renders.generate_fibtree(fib_value)
                    states = func_renders.simulate_fib(fib_value)
                    state_index = 0
                    tree = func_renders.TreeRender(screen, root)
                    curr_mode = FIB_MODE
            if event.type == pygame.KEYDOWN:
                if event.unicode.isdigit():
                    input_render = font.render(event.unicode, True, 'White')
                    if fat_input:
                        fat_value = int(event.unicode)
                        main_func_renders[3] = empty_surf.copy()
                        main_func_renders[3].blit(input_render, (7, 5))
                        cursor_rect.topright = main_func_rects[3].topright
                    if fib_input:
                        fib_value = int(event.unicode)
                        main_func_renders[7] = empty_surf.copy()
                        main_func_renders[7].blit(input_render, (7, 5))
                        cursor_rect.topright = main_func_rects[7].topright
                elif event.key == pygame.K_BACKSPACE:
                    if fat_input:
                        main_func_renders[3] = empty_surf.copy()
                        fat_value = None
                        cursor_rect.topleft = main_func_rects[3].topleft
                    if fib_input:
                        main_func_renders[7] = empty_surf.copy()
                        fib_value = None
                        cursor_rect.topleft = main_func_rects[7].topleft
        #fat events
        if curr_mode == FAT_MODE:
            if event.type == pygame.MOUSEBUTTONUP:
                if ntx_fat_rect.collidepoint(event.pos):
                    fat_handler.advance()
                    stack_handler.advance()
                if fat_handler.finished and back_to_main_rect.collidepoint(event.pos):
                    curr_mode = MAIN_MODE
        #fib events
        if curr_mode == FIB_MODE:
            if event.type == pygame.MOUSEBUTTONUP:
                if ntx_fib_rect.collidepoint(event.pos):
                    tree.advance()
                    pygame.transform.scale(tree.image, MINITREE_RES, minitree)
                    states[state_index].apply(func)
                    if state_index < len(states) - 1:
                        state_index += 1
                    else:
                        fib_finished = True
                if inner_mode == TREE_MODE:
                    if func_btn_rect.collidepoint(event.pos):
                        ntx_fib_rect.midtop = (SCREEN_WIDTH/2, SCREEN_HEIGHT - 60)
                        inner_mode = -inner_mode
                elif inner_mode == FUNC_MODE:
                    if minitree_rect.collidepoint(event.pos):
                        ntx_fib_rect.topleft = (SCREEN_WIDTH/2 + 20, SCREEN_HEIGHT - 60)
                        inner_mode = -inner_mode
                if fib_finished and back_to_main_rect.collidepoint(event.pos):
                    curr_mode = MAIN_MODE

    screen.fill('Black')

    #main blits
    if curr_mode == MAIN_MODE:
        screen.blit(includes, includes_rect)
        for x in range(12):
            screen.blit(main_func_renders[x], main_func_rects[x])
        if fib_input or fat_input:
            if cursor_timer == cursor_delay:
                cursor_index = (cursor_index+1)%2
                curr_cursor = cursor_states[cursor_index]
                cursor_timer = 0
            else:
                cursor_timer += 1
            if fat_input:
                screen.blit(curr_cursor, cursor_rect)
            elif fib_input:
                screen.blit(curr_cursor, cursor_rect)
        
        if fat_value != None:
            if go_fat_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(go_hover, go_fat_rect)
            else:
                screen.blit(go_btn, go_fat_rect)
        if fib_value != None:
            if go_fib_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(go_hover, go_fib_rect)
            else:
                screen.blit(go_btn, go_fib_rect)
    #fat blits
    if curr_mode == FAT_MODE:
        screen.blit(fat.image, fat.rect)
        if stack_render != None:
            screen.blit(stack_render.image, stack_render.rect)
            if ntx_fat_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(ntx_fat_hover, ntx_fat_rect)
            else:
                screen.blit(ntx_fat_btn, ntx_fat_rect)
        if fat_handler.finished:
            if back_to_main_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(back_to_main_hover, back_to_main_rect)
            else:
                screen.blit(back_to_main, back_to_main_rect)
    #fib blits
    if curr_mode == FIB_MODE:
        mouse_pos = pygame.mouse.get_pos()
        if ntx_fib_rect.collidepoint(mouse_pos):
            screen.blit(ntx_fib_hover, ntx_fib_rect)
        else:
            screen.blit(ntx_fib_image, ntx_fib_rect)
        if inner_mode == TREE_MODE:
            screen.blit(tree.image, (0,0))
            if func_btn_rect.collidepoint(mouse_pos):
                screen.blit(func_btn_hover, func_btn_rect)
            else:
                screen.blit(func_btn, func_btn_rect)
        elif inner_mode == FUNC_MODE:
            screen.blit(func.image, func.rect)
            screen.blit(minitree, minitree_rect)
        if fib_finished:
            if back_to_main_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(back_to_main_hover, back_to_main_rect)
            else:
                screen.blit(back_to_main, back_to_main_rect)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()
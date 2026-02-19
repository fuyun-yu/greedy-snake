import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import sys
import pygame

pygame.init()
import json
from others import get_file
import running
import pause
import menu
import settings


def save_config(global_dict, config, file):
    for k in config.keys():
        if k in global_dict.keys():
            config[k] = global_dict[k]
    if global_dict['enter_settings'] or global_dict['enter_running']:
        with open(get_file(file), 'w') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)


with open(get_file('assets/config.json'), 'r', encoding='utf-8') as f:
    config = json.load(f)

global_dict = {
                  'score': 0
              } | config

global_dict['color'] = {color_name: tuple(rgb) for color_name, rgb in global_dict['color'].items()}
state = 'menu'  # state is menu|running|settings|pause

pygame.display.set_caption('greedy snake')
window_size = (global_dict['screen']['width'], global_dict['screen']['height'])
screen = pygame.display.set_mode(window_size)

theme_path = get_file('gui_theme.json')
font_path = get_file('assets/simkai.ttf')
fps = global_dict['screen']['fps']
clock = pygame.Clock()
surface = None
font_52 = pygame.font.Font(get_file('assets/simkai.ttf'), 52)
global_dict['font_52'] = font_52
font_24 = pygame.font.Font(get_file('assets/simkai.ttf'), 24)
global_dict['font_24'] = font_24
font_40 = pygame.font.Font(get_file('assets/simkai.ttf'), 40)
global_dict['font_40'] = font_40
click_button = get_file(global_dict['sfx'][global_dict['settings_sfx']])
click_sound = pygame.mixer.Sound(click_button)
global_dict['enter_settings']=False
global_dict['enter_running'] = False
while True:
    clock.tick(fps)
    cur=pygame.time.get_ticks()
    p = get_file(global_dict['sfx'][global_dict['settings_sfx']])
    if click_button != p:
        click_button = p
        click_sound = pygame.mixer.Sound(click_button)
    settings_sfx_volume = global_dict['volume']['master'] * global_dict['volume']['sfx']
    if state == 'pause':
        surface, state = pause.pause(global_dict)
    elif state == 'running':
        surface, state = running.running(global_dict)
    elif state == 'settings':
        surface, state = settings.settings(global_dict)
    else:
        surface, state = menu.menu(global_dict)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_config(global_dict, config, get_file('assets/config.json'))
            pygame.quit()
            sys.exit()

        if state == 'pause':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = 'running'
                    global_dict['game_start_instance'] += pygame.time.get_ticks() - global_dict['game_pause_instance']
                    pygame.mixer.music.unpause()
                if event.key == pygame.K_b:
                    state = 'menu'
                    if 'menu_button' in global_dict.keys():
                        for button_rect in global_dict['menu_button'].keys():
                            global_dict[button_rect + '_in'] = False
                    del global_dict['running_channel']
                    pygame.mixer.music.stop()
        elif state == 'running':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    global_dict['direct'] = 'north' if global_dict['direct'] != 'south' else 'south'
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    global_dict['direct'] = 'south' if global_dict['direct'] != 'north' else 'north'
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    global_dict['direct'] = 'west' if global_dict['direct'] != 'east' else 'east'
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    global_dict['direct'] = 'east' if global_dict['direct'] != 'west' else 'west'
                if event.key == pygame.K_ESCAPE:
                    state = 'pause'
                    global_dict['game_pause_instance'] = pygame.time.get_ticks()
        elif state == 'settings':
            if event.type == pygame.MOUSEMOTION:
                if 'settings_button' in global_dict.keys():
                    for button_rect in global_dict['settings_button'].keys():
                        if global_dict['settings_button'][button_rect].collidepoint(event.pos):
                            global_dict[button_rect + '_in'] = True
                        else:
                            global_dict[button_rect + '_in'] = False
                if 'settings_ui_manager' in global_dict.keys():
                    for index, (left, right) in global_dict['settings_ui_manager'].items():
                        if left.collidepoint(event.pos):
                            global_dict['settings_ui_rect_in'][index][0] = True
                        else:
                            global_dict['settings_ui_rect_in'][index][0] = False
                        if right.collidepoint(event.pos):
                            global_dict['settings_ui_rect_in'][index][2] = True
                        else:
                            global_dict['settings_ui_rect_in'][index][2] = False
                if 'settings_ui_manager_slider' in global_dict.keys():
                    begin = 0
                    step = 2
                    hover = 3
                    change = 4
                    offset = 5
                    keep = 6
                    for index, (hover_rect, left, right, limit) in global_dict['settings_ui_manager_slider'].items():
                        if hover_rect.collidepoint(event.pos):
                            global_dict['settings_ui_rect_in_slider'][index][hover] = True
                        else:
                            global_dict['settings_ui_rect_in_slider'][index][hover] = False
                        if global_dict['settings_ui_rect_in_slider'][index][offset] is not None:
                            x_new = event.pos[0] - global_dict['settings_ui_rect_in_slider'][index][offset]
                            x_new = max(left, min(right, x_new))
                            s = global_dict['settings_ui_rect_in_slider'][index][step]
                            b = global_dict['settings_ui_rect_in_slider'][index][begin]
                            k = global_dict['settings_ui_rect_in_slider'][index][keep]
                            display = round(b + round((x_new - left) / (right - left) * (limit - b) / s) * s, k)
                            global_dict['settings_temp_dict'][settings.map_dict_slider[index]] = display
                        global_dict['settings_ui_rect_in_slider'][index][change] = global_dict['settings_temp_dict'][
                                                                                       settings.map_dict_slider[index]] \
                                                                                   != global_dict[
                                                                                       'settings_temp_ori_dict'][
                                                                                       settings.map_dict_slider[index]]

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 'settings_button' in global_dict.keys():
                    if global_dict['settings_button']['game_back_to_menu_txt_surface_rect'].collidepoint(event.pos):
                        click_sound.set_volume(settings_sfx_volume)
                        click_sound.play(maxtime=global_dict['sfx_duration'])
                        state = 'menu'
                        del global_dict['settings_first']
                        pygame.mixer.music.stop()
                        for button_rect in global_dict['settings_button'].keys():
                            global_dict[button_rect + '_in'] = False
                        del global_dict['settings_channel']
                        del global_dict['settings_ui_rect_in']
                        break
                    if global_dict['settings_button']['game_confirm_settings_txt_surface_rect'].collidepoint(event.pos):
                        click_sound.set_volume(settings_sfx_volume)
                        click_sound.play(maxtime=global_dict['sfx_duration'])
                        settings.update_ori_dict(global_dict['settings_temp_dict'],
                                                 global_dict['settings_temp_ori_dict'])
                        settings.update_global_dict(global_dict['settings_temp_ori_dict'], global_dict)
                        global_dict['enter_settings'] = True
                if global_dict['settings_button']['game_cross_wall_btn_txt_surface_rect'].collidepoint(event.pos):
                    click_sound.set_volume(settings_sfx_volume)
                    click_sound.play(maxtime=global_dict['sfx_duration'])
                    global_dict['settings_temp_dict']['cross_wall'] = not global_dict['settings_temp_dict'][
                        'cross_wall']
                global_dict['game_cross_wall_txt_surface_rect_change'] = global_dict['settings_temp_dict'][
                                                                             'cross_wall'] != \
                                                                         global_dict['settings_temp_ori_dict'][
                                                                             'cross_wall']
                if 'settings_ui_manager' in global_dict.keys():
                    for index, (left, right) in global_dict['settings_ui_manager'].items():
                        plus = 0
                        if left.collidepoint(event.pos):
                            click_sound.set_volume(settings_sfx_volume)
                            click_sound.play(maxtime=global_dict['sfx_duration'])
                            plus = -1
                        elif right.collidepoint(event.pos):
                            click_sound.set_volume(settings_sfx_volume)
                            click_sound.play(maxtime=global_dict['sfx_duration'])
                            plus = 1
                        if 1 <= index <= 2:
                            global_dict['settings_temp_dict'][settings.map_dict[index]] = settings.get_next_key(
                                global_dict['color'],
                                global_dict[
                                    'settings_temp_dict'][settings.map_dict[index]],
                                plus)
                        if 3 <= index <= 5:
                            global_dict['settings_temp_dict'][settings.map_dict[index]] = settings.get_next_key(
                                global_dict['bgm'],
                                global_dict[
                                    'settings_temp_dict'][settings.map_dict[index]],
                                plus)

                        if 6 <= index <= 7:
                            global_dict['settings_temp_dict'][settings.map_dict[index]] = settings.get_next_key(
                                global_dict['sfx'],
                                global_dict[
                                    'settings_temp_dict'][settings.map_dict[index]],
                                plus)
                        global_dict['settings_ui_rect_in'][index][1] = global_dict['settings_temp_dict'][
                                                                           settings.map_dict[index]] != \
                                                                       global_dict['settings_temp_ori_dict'][
                                                                           settings.map_dict[index]]
                if 'settings_ui_manager_slider' in global_dict.keys():
                    begin = 0
                    step = 2
                    hover = 3
                    change = 4
                    offset = 5
                    for index, (hover_rect, left, right, limit) in global_dict['settings_ui_manager_slider'].items():
                        if hover_rect.collidepoint(event.pos):
                            click_sound.set_volume(settings_sfx_volume)
                            click_sound.play(maxtime=global_dict['sfx_duration'])
                            if global_dict['settings_ui_rect_in_slider'][index][offset] is None:
                                mouse_x, _ = event.pos
                                global_dict['settings_ui_rect_in_slider'][index][offset] = mouse_x - hover_rect.centerx

            if event.type == pygame.MOUSEBUTTONUP:
                if 'settings_ui_manager_slider' in global_dict.keys():
                    hover = 3
                    change = 4
                    offset = 5
                    for index, (hover_rect, _, _, _) in global_dict['settings_ui_manager_slider'].items():
                        if hover_rect.collidepoint(event.pos) or global_dict['settings_ui_rect_in_slider'][index][
                            offset] is not None:
                            click_sound.set_volume(settings_sfx_volume)
                            click_sound.play(maxtime=global_dict['sfx_duration'])
                        global_dict['settings_ui_rect_in_slider'][index][offset] = None

        else:
            if event.type == pygame.MOUSEMOTION:
                if 'menu_button' in global_dict.keys():
                    for button_rect in global_dict['menu_button'].keys():
                        if global_dict['menu_button'][button_rect].collidepoint(event.pos):
                            global_dict[button_rect + '_in'] = True
                        else:
                            global_dict[button_rect + '_in'] = False
            if ((event.type == pygame.MOUSEBUTTONDOWN and 'menu_button' in global_dict.keys() and
                 global_dict['menu_button']['game_start_txt_surface_rect'].collidepoint(
                     event.pos))
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE)):
                click_sound.set_volume(settings_sfx_volume)
                click_sound.play(maxtime=global_dict['sfx_duration'])
                state = 'running'
                pygame.mixer.music.stop()
                reset = ['score', 'menu_channel', 'snake_body', 'snake_set', 'food_set', 'food_num',
                         'game_start_instance', 'game_duration', 'last_move_instance', 'direct', 'grid', 'grid_bg']
                for target in reset:
                    if target in global_dict.keys():
                        del global_dict[target]
                for ui in global_dict['menu_ui'].values():
                    ui.kill()
                del global_dict['menu_ui']
            if ((event.type == pygame.MOUSEBUTTONDOWN and 'menu_button' in global_dict.keys() and
                 global_dict['menu_button']['game_settings_txt_surface_rect'].collidepoint(
                     event.pos))
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                click_sound.set_volume(settings_sfx_volume)
                click_sound.play(maxtime=global_dict['sfx_duration'])
                state = 'settings'
                del global_dict['menu_channel']
                global_dict['settings_first'] = True
                pygame.mixer.music.stop()
                for ui in global_dict['menu_ui'].values():
                    ui.kill()
                del global_dict['menu_ui']
    screen.blit(surface)
    pygame.display.flip()

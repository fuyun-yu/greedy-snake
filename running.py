import pygame
import random
from others import get_file
from collections import deque

direction = {'north': (-1, 0), 'south': (1, 0), 'east': (0, 1), 'west': (0, -1)}


def snake_move(snake_body, snake_set, food_set,
               direct, cross_wall, num_w, num_h, eat_sound, sfx_duration, sfx_volume):
    tail = snake_body[-1]
    i = snake_body[0][0] + direction[direct][0]
    j = snake_body[0][1] + direction[direct][1]
    if cross_wall:
        i %= num_h
        j %= num_w
    next_location = (i, j)
    score_change = 0
    if 0 <= j < num_w and 0 <= i < num_h and (next_location not in snake_set or next_location == tail):
        snake_body.appendleft(next_location)
        snake_set.add(next_location)
        if next_location in food_set:
            score_change = 1
            food_set.discard(next_location)
            eat_sound.set_volume(sfx_volume)
            eat_sound.play(maxtime=sfx_duration)
        else:
            snake_body.pop()
            snake_set.discard(tail)
    else:
        return 0, False
    return score_change, True


def running(global_dict):
    max_move_interval = global_dict['snake']['speed']['max_move_interval']
    min_move_interval = global_dict['snake']['speed']['min_move_interval']
    attenuation_rate = global_dict['snake']['speed']['attenuation_rate']
    len_w = global_dict['screen']['width']
    len_h = global_dict['screen']['height']
    window_size = (len_w, len_h)
    num_w = global_dict['screen']['num_w']
    num_h = global_dict['screen']['num_h']
    message_h = global_dict['screen']['message_h']
    color_black = global_dict['color']['极夜黑']
    color_gray = global_dict['color'][global_dict['screen']['bg_color']]
    surface = pygame.Surface(window_size)
    size_w = len_w // num_w
    size_h = (len_h - message_h) // num_h

    if 'running_channel' not in global_dict.keys():
        global_dict['running_channel'] = True
        pygame.mixer.music.set_volume(global_dict['volume']['master'] * global_dict['volume']['bgm'])
        pygame.mixer.music.load(get_file(global_dict['bgm'][global_dict['running_bgm']]))
        pygame.mixer.music.play(loops=-1)

    if 'grid' not in global_dict.keys():
        grid = [
            [(col * size_w, row * size_h, size_w, size_h) for col in range(num_w)] for row in range(num_h)
        ]
        global_dict['grid'] = grid
    else:
        grid = global_dict['grid']

    if 'grid_bg' not in global_dict.keys():
        grid_bg = pygame.Surface(window_size, pygame.SRCALPHA)
        for row in range(num_h):
            end = size_h * row
            pygame.draw.aaline(grid_bg, color_black, (0, end), (len_w, end))
        for col in range(num_w):
            end = size_w * col
            pygame.draw.aaline(grid_bg, color_black, (end, 0), (end, len_h - message_h))
        global_dict['grid_bg'] = grid_bg
    else:
        grid_bg = global_dict['grid_bg']

    if 'snake_body' not in global_dict.keys():
        snake_body = deque()
        snake_set = set()
        snake_i = num_h // 2
        snake_j = num_w // 2
        for i in range(global_dict['snake']['init_length']):
            snake_body.append((snake_i + i, snake_j))
            snake_set.add((snake_i + i, snake_j))
        global_dict['snake_body'] = snake_body
        global_dict['snake_set'] = snake_set
    else:
        snake_body = global_dict['snake_body']
        snake_set = global_dict['snake_set']

    if 'food_num' not in global_dict.keys():
        food = global_dict['screen']['food_at_least']
        food_num = random.randint(min(food, num_w * num_h // global_dict['screen']['food_left']),
                                  max(food, num_w * num_h // global_dict['screen']['food_right']))
        global_dict['food_num'] = food_num
    else:
        food_num = global_dict['food_num']

    if 'food_set' not in global_dict.keys():
        food_set = set()
        global_dict['food_set'] = food_set
    else:
        food_set = global_dict['food_set']
    cnt=0
    while len(food_set) < food_num:
        if cnt >= 1000:
            break
        ti = random.randint(0, num_h - 1)
        tj = random.randint(0, num_w - 1)
        if (ti, tj) not in food_set and (ti, tj) not in snake_set:
            food_set.add((ti, tj))
        cnt+=1

    if 'score' not in global_dict.keys():
        global_dict['score'] = 0

    if 'game_start_instance' not in global_dict.keys():
        global_dict['game_start_instance'] = pygame.time.get_ticks()

    if 'game_duration' not in global_dict.keys():
        global_dict['game_duration'] = 0
    global_dict['game_duration'] = pygame.time.get_ticks() - global_dict['game_start_instance']

    if 'last_move_instance' not in global_dict.keys():
        global_dict['last_move_instance'] = 0

    if 'direct' not in global_dict.keys():
        global_dict['direct'] = 'north'

    sfx_duration = global_dict['sfx_duration']

    if 'eat_sound' not in global_dict.keys():
        eat_sound = pygame.mixer.Sound(get_file(global_dict['sfx'][global_dict['eat_sfx']]))
    else:
        eat_sound = global_dict['eat_sound']

    cross_wall = global_dict['cross_wall']

    move_interval = max(min_move_interval, max_move_interval * (attenuation_rate ** global_dict['score']))

    cur_instance = pygame.time.get_ticks()

    res = True
    score_new = 0
    if cur_instance - global_dict['last_move_instance'] >= move_interval:
        global_dict['last_move_instance'] = cur_instance
        sfx_volume = global_dict['volume']['master'] * global_dict['volume']['sfx']
        score_new, res = snake_move(snake_body, snake_set, food_set,
                                    global_dict['direct'], cross_wall, num_w, num_h, eat_sound, sfx_duration,
                                    sfx_volume)
    surface.fill(color_gray)
    surface.blit(grid_bg)
    for snake in snake_body:
        pygame.draw.rect(surface, global_dict['color'][global_dict['snake']['color']['body']],
                         grid[snake[0]][snake[1]])
    pygame.draw.aacircle(surface, global_dict['color'][global_dict['snake']['color']['eye']],
                         pygame.Rect(grid[snake_body[0][0]][snake_body[0][1]]).center,
                         min(size_h, size_w) // 5)
    for food in food_set:
        pygame.draw.rect(surface, global_dict['color'][global_dict['food_color']],
                         grid[food[0]][food[1]])
    surface.fill(global_dict['color']['冷色青'], (0, len_h - message_h, len_w, message_h))
    game_score_display_surface = global_dict['font_52'].render(f'本局当前已获得{global_dict["score"]}分', True,
                                                               global_dict['color']['荧光红'],
                                                               color_black)
    surface.blit(game_score_display_surface, (0, len_h - message_h))
    game_duration_display_surface = global_dict['font_52'].render(
        f'本局持续时间为{global_dict["game_duration"] / 1000:06.2f}秒', True,
        global_dict['color']['荧光红'],
        color_black)
    surface.blit(game_duration_display_surface, (len_w // 2, len_h - message_h))
    if res:
        global_dict['score'] += score_new
        out = 'running'
    else:
        out = 'menu'
        if 'menu_button' in global_dict.keys():
            for button_rect in global_dict['menu_button'].keys():
                    global_dict[button_rect+'_in'] = False
        if global_dict['score'] > global_dict['max_score']:
            global_dict['max_score'] = global_dict['score']
            global_dict['seconds_when_max_score'] = global_dict['game_duration']
            global_dict['enter_running'] = True
        del global_dict['running_channel']
        pygame.mixer.music.stop()
    return surface, out

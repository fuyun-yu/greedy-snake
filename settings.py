import pygame
from others import get_file


def get_width(string):
    width = 0
    for ch in string:
        if 0 <= ord(ch) < 256:
            width += 1
        else:
            width += 2
    return width


def set_in_mid(txt, length):
    txt = str(txt)
    t = get_width(txt)
    if t >= length:
        return txt
    length -= t
    mid = length // 2
    arr = [' ' * mid, txt, ' ' * (length - mid)]
    return ''.join(arr)


def get_next_key(dict, key, plus):
    arr = list(dict.keys())
    for i in range(len(arr)):
        if arr[i] == key:
            return arr[(i + plus) % len(arr)]
    return None


def init_temp_dict(global_dict):
    temp_dict = {
        'snake_init_length': global_dict['snake']['init_length'],
        'snake_color_body': global_dict['snake']['color']['body'],
        'snake_color_eye': global_dict['snake']['color']['eye'],
        'master_volume': global_dict['volume']['master'],
        'bgm_volume': global_dict['volume']['bgm'],
        'sfx_volume': global_dict['volume']['sfx'],
        'running_bgm': global_dict['running_bgm'],
        'menu_bgm': global_dict['menu_bgm'],
        'settings_bgm': global_dict['settings_bgm'],
        'max_speed': 7500 // global_dict['snake']['speed']['min_move_interval'],
        'min_speed': 7500 // global_dict['snake']['speed']['max_move_interval'],
        'attenuation_rate': global_dict['snake']['speed']['attenuation_rate'],
        'eat_sfx': global_dict['eat_sfx'],
        'settings_sfx': global_dict['settings_sfx'],
        'cross_wall': global_dict['cross_wall']
    }
    return temp_dict


map_dict = {
    0: 'snake_init_length',
    1: 'snake_color_body',
    2: 'snake_color_eye',
    3: 'menu_bgm',
    4: 'settings_bgm',
    5: 'running_bgm',
    6: 'eat_sfx',
    7: 'settings_sfx'
}

map_dict_slider = {
    0: 'snake_init_length',
    1: 'master_volume',
    2: 'bgm_volume',
    3: 'sfx_volume',
    4: 'max_speed',
    5: 'min_speed',
    6: 'attenuation_rate'
}

color_black = (0, 0, 0)
color_white = (245, 245, 240)
color_special = (0, 230, 200)
color_sand = (193, 145, 107)
color_yellow = (255, 234, 180)
color_gray = (200, 200, 200)


def create_label_button(surface, txt, left, right, font, left_location, arr):
    left_surface = font.render(left, True, color_black, color_special if arr[0] else color_sand)
    right_surface = font.render(right, True, color_black, color_special if arr[2] else color_sand)
    txt_surface = font.render(' ' + txt + ' ', True, color_sand if arr[1] else color_black, color_white)
    left_surface_rect = left_surface.get_rect(midleft=left_location)
    txt_surface_rect = txt_surface.get_rect(midleft=left_surface_rect.midright)
    right_surface_rect = right_surface.get_rect(midleft=txt_surface_rect.midright)
    surface.blit(left_surface, left_surface_rect)
    surface.blit(txt_surface, txt_surface_rect)
    surface.blit(right_surface, right_surface_rect)
    return left_surface_rect, right_surface_rect


def create_horizontal_slider(surface, font, label, arr, display, x, y,
                             size=13):
    begin = arr[0]
    end = arr[1]
    step = arr[2]
    limit = round((end - begin) / step) * step + begin
    display = min(max(display, begin), limit)
    label_width = get_width(label)
    track_surface = font.render(' ' * max(13, (size - label_width)), False, color_yellow, color_yellow)
    thumb_surface = font.render(' ', False, color_special if arr[3] else color_gray,
                                color_special if arr[3] else color_gray)
    thumb_surface_rect = thumb_surface.get_rect()
    r = thumb_surface_rect.centerx - thumb_surface_rect.left
    label_surface = font.render(label, True, color_black, color_white)
    label_surface_rect = label_surface.get_rect(topleft=(x, y))
    track_surface_rect = track_surface.get_rect(topleft=label_surface_rect.topright)
    left = track_surface_rect.left + r
    right = track_surface_rect.right - r
    display_surface = font.render(set_in_mid(str(int(display) if arr[6] == 0 else round(display, arr[6])), 5), True,
                                  color_special if arr[4] else color_black,
                                  color_white)
    display_surface_rect = display_surface.get_rect(topleft=track_surface_rect.topright)
    center_x = (display - begin) / (limit - begin) * (right - left) + track_surface_rect.left + r
    thumb_surface_rect = thumb_surface.get_rect(center=(center_x, track_surface_rect.centery))
    surface.blit(label_surface, label_surface_rect)
    surface.blit(track_surface, track_surface_rect)
    surface.blit(display_surface, display_surface_rect)
    surface.blit(thumb_surface, thumb_surface_rect)
    return thumb_surface_rect, left, right, limit


def update_ori_dict(temp, ori):
    for k, v in temp.items():
        if k in ori.keys():
            ori[k] = v


def update_global_dict(ori, global_dict):
    global_dict['snake']['init_length'] = ori['snake_init_length']
    global_dict['snake']['color']['body'] = ori['snake_color_body']
    global_dict['snake']['color']['eye'] = ori['snake_color_eye']
    global_dict['volume']['master'] = ori['master_volume']
    global_dict['volume']['bgm'] = ori['bgm_volume']
    global_dict['volume']['sfx'] = ori['sfx_volume']
    global_dict['running_bgm'] = ori['running_bgm']
    global_dict['menu_bgm'] = ori['menu_bgm']
    global_dict['settings_bgm'] = ori['settings_bgm']
    global_dict['snake']['speed']['min_move_interval'] = 7500 / ori['max_speed']
    global_dict['snake']['speed']['max_move_interval'] = 7500 / ori['min_speed']
    global_dict['snake']['speed']['attenuation_rate'] = ori['attenuation_rate']
    global_dict['eat_sfx'] = ori['eat_sfx']
    global_dict['settings_sfx'] = ori['settings_sfx']
    global_dict['cross_wall'] = ori['cross_wall']


def settings(global_dict):
    if 'settings_channel' not in global_dict.keys():
        global_dict['settings_channel'] = True
        pygame.mixer.music.set_volume(global_dict['volume']['master'] * global_dict['volume']['bgm'])
        pygame.mixer.music.load(get_file(global_dict['bgm'][global_dict['settings_bgm']]))
        pygame.mixer.music.play(loops=-1)
    window_size = (global_dict['screen']['width'], global_dict['screen']['height'])
    surface = pygame.Surface(window_size)
    if 'settings_button' not in global_dict.keys():
        global_dict['settings_button'] = {}
    if 'game_back_to_menu_txt_surface_rect' not in global_dict['settings_button'].keys():
        global_dict['game_back_to_menu_txt_surface_rect_in'] = False
        global_dict['game_confirm_settings_txt_surface_rect_in'] = False
        global_dict['game_cross_wall_txt_surface_rect_change'] = False
        global_dict['game_cross_wall_btn_txt_surface_rect_in'] = False
    game_back_to_menu_txt_surface = global_dict['font_52'].render(
        '返回', True, global_dict['color']['极夜黑'],
        global_dict['game_txt_surface_rect_entry_color'] if
        global_dict['game_back_to_menu_txt_surface_rect_in'] else
        global_dict['game_txt_surface_rect_not_entry_color']
    )
    global_dict['settings_button']['game_back_to_menu_txt_surface_rect'] = game_back_to_menu_txt_surface.get_rect(
        topleft=(100, 50)
    )
    surface.blit(game_back_to_menu_txt_surface, global_dict['settings_button']['game_back_to_menu_txt_surface_rect'])
    game_confirm_settings_txt_surface = global_dict['font_52'].render(
        '确认', True, global_dict['color']['极夜黑'],
        global_dict['game_txt_surface_rect_entry_color'] if
        global_dict['game_confirm_settings_txt_surface_rect_in'] else
        global_dict['game_txt_surface_rect_not_entry_color']
    )
    global_dict['settings_button'][
        'game_confirm_settings_txt_surface_rect'] = game_confirm_settings_txt_surface.get_rect(
        topright=(window_size[0] - 100, 50)
    )
    surface.blit(game_confirm_settings_txt_surface,
                 global_dict['settings_button']['game_confirm_settings_txt_surface_rect'])
    if global_dict['settings_first']:
        global_dict['settings_temp_dict'] = init_temp_dict(global_dict)
        global_dict['settings_temp_ori_dict'] = init_temp_dict(global_dict)
        global_dict['settings_first'] = False
        global_dict['settings_temp_dict']['length'] = length = max(
            [max(
                [get_width(str(i)) for i in global_dict['color'].keys()]),
                max([get_width(str(i)) for i in global_dict['bgm'].keys()]),
                max([get_width(str(i)) for i in global_dict['sfx'].keys()])
            ]
        )
    else:
        length = global_dict['settings_temp_dict']['length']

    if 'settings_ui_rect_in' not in global_dict.keys():
        settings_ui_rect_in = {
            1: [False, False, False],
            2: [False, False, False],
            3: [False, False, False],
            4: [False, False, False],
            5: [False, False, False],
            6: [False, False, False],
            7: [False, False, False]
        }
        global_dict['settings_ui_rect_in'] = settings_ui_rect_in
    else:
        settings_ui_rect_in = global_dict['settings_ui_rect_in']
    if 'settings_ui_rect_in_slider' not in global_dict.keys():
        settings_ui_rect_in_slider = {
            0: [1, 10, 1, False, False, None, 0],
            1: [0, 1, 0.01, False, False, None, 2],
            2: [0, 1, 0.01, False, False, None, 2],
            3: [0, 1, 0.01, False, False, None, 2],
            4: [50, 300, 1, False, False, None, 0],
            5: [50, 300, 1, False, False, None, 0],
            6: [0.05, 1, 0.01, False, False, None, 2],
        }
        global_dict['settings_ui_rect_in_slider'] = settings_ui_rect_in_slider
    else:
        settings_ui_rect_in_slider = global_dict['settings_ui_rect_in_slider']
    x = 30
    y = 100
    font = global_dict['font_40']
    settings_ui_manager = {
        1: create_label_button(surface,
                               f'蛇身初始颜色是{set_in_mid(global_dict["settings_temp_dict"]["snake_color_body"], length)}',
                               '上个', '下个', font, (x, y + 50), settings_ui_rect_in[1]),
        2: create_label_button(surface,
                               f'蛇眼初始颜色是{set_in_mid(global_dict["settings_temp_dict"]["snake_color_eye"], length)}',
                               '上个', '下个', font, (x, y + 100), settings_ui_rect_in[2]),
        3: create_label_button(surface,
                               f'菜单界面音乐是{set_in_mid(global_dict["settings_temp_dict"]["menu_bgm"], length)}',
                               '上个', '下个', font, (x, y + 150), settings_ui_rect_in[3]),
        4: create_label_button(surface,
                               f'设置界面音乐是{set_in_mid(global_dict["settings_temp_dict"]["settings_bgm"], length)}',
                               '上个', '下个', font, (x, y + 200), settings_ui_rect_in[4]),
        5: create_label_button(surface,
                               f'游戏界面音乐是{set_in_mid(global_dict["settings_temp_dict"]["running_bgm"], length)}',
                               '上个', '下个', font, (x, y + 250), settings_ui_rect_in[5]),
        6: create_label_button(surface,
                               f'游戏界面音效是{set_in_mid(global_dict["settings_temp_dict"]["eat_sfx"], length)}',
                               '上个', '下个', font, (x, y + 300), settings_ui_rect_in[6]),
        7: create_label_button(surface,
                               f'程序点击音效是{set_in_mid(global_dict["settings_temp_dict"]["settings_sfx"], length)}',
                               '上个', '下个', font, (x, y + 350), settings_ui_rect_in[7])
    }
    half = window_size[0] // 2
    adjust = 8
    settings_ui_manger_slider = {
        0: create_horizontal_slider(surface, font, '初始蛇身长度',
                                    settings_ui_rect_in_slider[0],
                                    global_dict['settings_temp_dict']['snake_init_length'],
                                    x, y + 400, size=adjust + length),
        1: create_horizontal_slider(surface, font, '全局音量响度',
                                    settings_ui_rect_in_slider[1], global_dict['settings_temp_dict']['master_volume'],
                                    x, y + 450, size=adjust + length),
        2: create_horizontal_slider(surface, font, '背景音乐响度',
                                    settings_ui_rect_in_slider[2], global_dict['settings_temp_dict']['bgm_volume'],
                                    x, y + 500, size=adjust + length),
        3: create_horizontal_slider(surface, font, '程序音效响度',
                                    settings_ui_rect_in_slider[3], global_dict['settings_temp_dict']['sfx_volume'],
                                    x, y + 550, size=adjust + length),
        4: create_horizontal_slider(surface, font, '蛇行最大速率',
                                    settings_ui_rect_in_slider[4], global_dict['settings_temp_dict']['max_speed'],
                                    x + half, y + 400, size=adjust + length),
        5: create_horizontal_slider(surface, font, '蛇行最小速率',
                                    settings_ui_rect_in_slider[5], global_dict['settings_temp_dict']['min_speed'],
                                    x + half, y + 450, size=adjust + length),
        6: create_horizontal_slider(surface, font, '速率衰减系数',
                                    settings_ui_rect_in_slider[6],
                                    global_dict['settings_temp_dict']['attenuation_rate'],
                                    x + half, y + 500, size=adjust + length)

    }
    game_cross_wall_txt_surface = global_dict['font_40'].render(
        f"穿墙功能：", True, color_sand if global_dict['game_cross_wall_txt_surface_rect_change'] else color_black,
        color_white
    )
    game_cross_wall_txt_surface_rect = game_cross_wall_txt_surface.get_rect(center=(x + half + 100, y + 575))
    game_cross_wall_btn_txt_surface = global_dict['font_40'].render(
        '开启中' if global_dict['settings_temp_dict']['cross_wall'] else '关闭中',
        True,
        color_black,
        color_special if global_dict['game_cross_wall_btn_txt_surface_rect_in'] else color_sand
    )
    game_cross_wall_btn_txt_surface_rect = game_cross_wall_btn_txt_surface.get_rect(
        midleft=game_cross_wall_txt_surface_rect.midright
    )
    global_dict['settings_button']['game_cross_wall_btn_txt_surface_rect'] = game_cross_wall_btn_txt_surface_rect
    surface.blit(game_cross_wall_txt_surface, game_cross_wall_txt_surface_rect)
    surface.blit(game_cross_wall_btn_txt_surface, game_cross_wall_btn_txt_surface_rect)
    global_dict['settings_ui_manager'] = settings_ui_manager
    global_dict['settings_ui_manager_slider'] = settings_ui_manger_slider
    return surface, 'settings'

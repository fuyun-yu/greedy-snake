import pygame
import others


def menu(global_dict):
    if 'game_txt_surface_rect_entry_color' not in global_dict.keys():
        global_dict['game_txt_surface_rect_entry_color'] = global_dict['color']['冷色青']
        global_dict['game_txt_surface_rect_not_entry_color'] = global_dict['color']['月光白']
        global_dict['game_start_txt_surface_rect_in'] = False
        global_dict['game_settings_txt_surface_rect_in'] = False
    if 'menu_channel' not in global_dict.keys():
        global_dict['menu_channel'] = True
        pygame.mixer.music.set_volume(global_dict['volume']['master'] * global_dict['volume']['bgm'])
        pygame.mixer.music.load(others.get_file(global_dict['bgm'][global_dict['menu_bgm']]))
        pygame.mixer.music.play(loops=-1)
    window_size = (global_dict['screen']['width'], global_dict['screen']['height'])
    surface = pygame.Surface(window_size)
    if 'game_menu_txt_surface' not in global_dict.keys():
        global_dict['game_menu_txt_surface'] = global_dict['font_24'].render(
            global_dict['menu']['txt'],
            True,
            global_dict['color'][global_dict['menu']['txt_color']]
        )
    surface.blit(global_dict['game_menu_txt_surface'],
                 global_dict['game_menu_txt_surface'].get_rect(midtop=(global_dict['screen']['width'] // 2, 0)))
    if 'menu_ui' not in global_dict.keys():
        global_dict['menu_ui'] = {}
    # if 'game_start_txt_surface_rect' not in global_dict.keys():
    game_start_txt = '开始游戏'
    game_settings_txt = '游戏设置'
    game_start_txt_surface = global_dict['font_52'].render(game_start_txt, True,
                                                           global_dict['color']['极夜黑'],
                                                           global_dict['game_txt_surface_rect_entry_color'] if
                                                           global_dict['game_start_txt_surface_rect_in'] else
                                                           global_dict['game_txt_surface_rect_not_entry_color'])
    game_settings_txt_surface = global_dict['font_52'].render(game_settings_txt, True,
                                                              global_dict['color']['极夜黑'],
                                                              global_dict['game_txt_surface_rect_entry_color'] if
                                                              global_dict['game_settings_txt_surface_rect_in'] else
                                                              global_dict['game_txt_surface_rect_not_entry_color'])
    # game_start_btn_surface = pygame_gui.elements.UIButton(
    #     relative_rect=game_start_btn_txt_surface.get_rect(center=(window_size[0] // 2, window_size[1] // 2)),
    #     manager=global_dict['manager'],
    #     text=game_start_txt
    # )
    if 'menu_button' not in global_dict.keys():
        global_dict['menu_button'] = {}
    game_start_txt_surface_rect = game_start_txt_surface.get_rect(center=(window_size[0] // 2, window_size[1] // 2))
    global_dict['menu_button']['game_start_txt_surface_rect'] = game_start_txt_surface_rect
    game_settings_txt_surface_rect = game_settings_txt_surface.get_rect(
        bottomleft=(100, global_dict['screen']['height'] - global_dict['screen']['message_h']))
    global_dict['menu_button']['game_settings_txt_surface_rect'] = game_settings_txt_surface_rect
    surface.blit(game_start_txt_surface, global_dict['menu_button']['game_start_txt_surface_rect'])
    surface.blit(game_settings_txt_surface, global_dict['menu_button']['game_settings_txt_surface_rect'])
    game_score_last = global_dict['score'] if 'score' in global_dict.keys() else 0
    game_duration_last = global_dict['game_duration'] if 'game_duration' in global_dict.keys() else 0
    game_score_max = global_dict['max_score']
    game_duration_max_when_max_score = global_dict['seconds_when_max_score']
    font = global_dict['font_40']
    game_last_score_txt_surface = font.render(f"上一局总共获得了{game_score_last}分",
                                              True, global_dict['color']['极夜黑'], global_dict['color']['月光白'])
    game_last_score_txt_surface_rect = game_last_score_txt_surface.get_rect(
        topleft=(0, global_dict['screen']['height'] // 2 - 100))
    surface.blit(game_last_score_txt_surface, game_last_score_txt_surface_rect)
    game_last_duration_txt_surface = font.render(f"上一局总共用时{game_duration_last / 1000:06.2f}秒",
                                                 True, global_dict['color']['极夜黑'], global_dict['color']['月光白'])
    x, y = game_last_score_txt_surface_rect.bottomleft
    game_last_duration_txt_surface_rect = game_last_duration_txt_surface.get_rect(
        topleft=(x, y + 100))
    surface.blit(game_last_duration_txt_surface, game_last_duration_txt_surface_rect)
    game_max_score_txt_surface = font.render(f"历史最高为{game_score_max}分",
                                             True, global_dict['color']['极夜黑'], global_dict['color']['月光白'])
    game_max_score_txt_surface_rect = game_max_score_txt_surface.get_rect(topright=
                                                                          (global_dict['screen']['width'],
                                                                           global_dict['screen']['height'] // 2 - 100))
    surface.blit(game_max_score_txt_surface, game_max_score_txt_surface_rect)
    game_duration_when_max_score_txt_surface = font.render(
        f"历史最高分的对局用时为{game_duration_max_when_max_score / 1000:06.2f}秒",
        True, global_dict['color']['极夜黑'], global_dict['color']['月光白'])
    x, y = game_max_score_txt_surface_rect.bottomright
    game_duration_when_max_score_txt_surface_rect = game_duration_when_max_score_txt_surface.get_rect(
        topright=(global_dict['screen']['width'], y + 100))
    surface.blit(game_duration_when_max_score_txt_surface, game_duration_when_max_score_txt_surface_rect)

    return surface, 'menu'

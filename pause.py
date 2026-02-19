import pygame


def pause(global_dict):
    pygame.mixer.music.pause()
    surface = pygame.Surface((global_dict['screen']['width'], global_dict['screen']['height']))
    surface.fill(global_dict['color']['底色灰'])
    surface.set_alpha(18)
    game_pause_remind_surface = global_dict['font_52'].render('游戏暂停中……', True, global_dict['color']['血泊红'])
    surface.blit(game_pause_remind_surface,
                 game_pause_remind_surface.get_rect(
                     center=(global_dict['screen']['width'] // 2, global_dict['screen']['height'] // 2)))
    return surface, 'pause'

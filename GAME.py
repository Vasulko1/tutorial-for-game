import pygame

image_path = '/data/data/com.name/files/app/'

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((1280, 720)) # flags=pygame.NOFRAME
pygame.display.set_caption("PORTFOLIO")
icon = pygame.image.load(image_path + 'images/icon.webp')
pygame.display.set_icon(icon)


# Player
bg = pygame.image.load(image_path +'images/Game.png')
walk_left = [
    pygame.image.load(image_path +'images/Playerleft/Stay2.png').convert_alpha(),
    pygame.image.load(image_path +'images/Playerleft/Walk2.png').convert_alpha(),
    pygame.image.load(image_path +'images/Playerleft/Run2.png').convert_alpha(),
    pygame.image.load(image_path +'images/Playerleft/Stay2.png').convert_alpha(),
]
walk_right = [
    pygame.image.load(image_path +'images/Playerright/Stay.png').convert_alpha(),
    pygame.image.load(image_path +'images/Playerright/Walk.png').convert_alpha(),
    pygame.image.load(image_path +'images/Playerright/Run.png').convert_alpha(),
    pygame.image.load(image_path +'images/Playerright/Stay.png').convert_alpha(),
]

devil = pygame.image.load(image_path +'images/devil.png').convert_alpha()
# devil_x = 565
devil_list_in_game = []

player_anim_count = 0
bg_x = 0

player_speed = 5
player_x = 150
player_y = 565

is_jump = False
jump_count = 8

bg_sound = pygame.mixer.Sound(image_path +'music/History.mp3')
# bg_sound.play()

devil_timer = pygame.USEREVENT + 1
pygame.time.set_timer(devil_timer, 4500)


label = pygame.font.Font(image_path +'fonts/Pixel.ttf', 40)
lose_label = label.render('You are lose!', False, (193, 196, 199))
restart_label = label.render('Restart play!', False, (115, 132, 148))
restart_label_rect = restart_label.get_rect(topleft=(400, 300))

bullets_left = 5

bullet = pygame.image.load(image_path +'images/bullet.png').convert_alpha()
bullets = []

gameplay = True

running = True
while running:



    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 1280, 0))
    # screen.blit(devil, (devil_x, 550))
     
    if gameplay:

        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        
        
        # devil_rect = devil.get_rect(topleft=(devil_x, 565))
        
            
        if devil_list_in_game:
            for (i, el) in enumerate(devil_list_in_game):
               screen.blit(devil, el)
               el.x -= 10

               if el.x < -10:
                   devil_list_in_game.pop(i)


        
               if player_rect.colliderect(el):
                   gameplay = False




        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        
        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif  keys[pygame.K_RIGHT] and player_x < 200:
            player_x += player_speed


        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8:

                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:      
                is_jump = False
                jump_count = 8

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 2
        if bg_x == -618:
            bg_x = 0
          

        
        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 4


                if el.x > 1280:
                    bullets.pop(i)

                if devil_list_in_game:
                    for (index, devil_el) in enumerate(devil_list_in_game):
                        if el.colliderect(devil_el):
                            devil_list_in_game.pop(index)
                            bullets.pop(i)

    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label, (300, 400))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            devil_list_in_game.clear()
            bullets.clear()
            bullets_left = 5
    # devil_x -= 10

    
    

    # screen.fill((92, 46, 46))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type == devil_timer:
            devil_list_in_game.append(devil.get_rect(topleft=(1600, 565)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_b and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))
            bullets_left -= 1

        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_a:
        #         screen.fill((133, 46, 46))
            
    clock.tick(10)
import pygame    
import random    
import sys    
   
pygame.init()    
   
WIDTH = 800    
HEIGHT = 600    
FPS = 60    
   
BLUE = (135, 206, 235)    
BLACK = (0, 0, 0)    
RED = (255, 0, 0)    
WHITE = (255, 255, 255)    
GREEN = (0, 255, 0)    
   
screen = pygame.display.set_mode((WIDTH, HEIGHT))    
pygame.display.set_caption("Jump Over Spikes")    
   
clock = pygame.time.Clock()    
gravity = 1    
jump_strength = -20      
player_width = 50    
player_height = 50    
spike_width = 50    
spike_height = 30    
spike_speed = 5    
spikes = []    
floor_height = HEIGHT - 50    
on_block = False      
flying = False      
gravity_enabled = True      
   
font = pygame.font.SysFont(None, 55)    
   
def draw_player(x, y):    
    pygame.draw.rect(screen, WHITE, (x, y, player_width, player_height))    
   
def draw_spikes(spikes):    
    for spike in spikes:    
        pygame.draw.polygon(screen, BLACK, [(spike.x, spike.y + spike.height),    
                                              (spike.x + spike.width // 2, spike.y),    
                                              (spike.x + spike.width, spike.y + spike.height)])    
   
def draw_text(text, font, color, x, y):    
    label = font.render(text, True, color)    
    screen.blit(label, (x, y))    
   
def main_game():    
    global on_block, flying, gravity_enabled      
    player_x = 100    
    player_y = HEIGHT - 50 - player_height    
    player_velocity = 0    
    jumping = False    
    spikes.clear()      
    timer = 0      
   
    running = True    
    while running:    
        screen.fill(BLUE)      
        pygame.draw.rect(screen, GREEN, (0, floor_height, WIDTH, HEIGHT - floor_height))    
   
        timer += 1 / FPS    
        draw_text(f"Time: {int(timer)}s", font, WHITE, 10, 10)    
   
        if random.random() < 0.015:      
            spike_height = random.randint(30, 60)    
            spike = pygame.Rect(WIDTH, floor_height - spike_height, spike_width, spike_height)    
            spikes.append(spike)    
   
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:    
                running = False    
   
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if not jumping:    
                if on_block:      
                    player_velocity = jump_strength * 2      
                else:    
                    player_velocity = jump_strength    
                jumping = True    
   
        if keys[pygame.K_UP]:    
            if flying:      
                player_y -= 5    
        if keys[pygame.K_DOWN]:    
            if flying:      
                player_y += 5    
   
        if gravity_enabled:    
            player_velocity += gravity    
        player_y += player_velocity    
           
        if player_y >= floor_height - player_height:    
            player_y = floor_height - player_height    
            jumping = False    
            on_block = False      
   
        for spike in spikes:    
            spike.x -= spike_speed    
           
        for spike in spikes:    
            if spike.colliderect(pygame.Rect(player_x, player_y, player_width, player_height)):    
                screen.fill(RED)    
                draw_text("You Died", font, WHITE, WIDTH // 2 - 150, HEIGHT // 2 - 50)    
                draw_text(f"Time: {int(timer)}s", font, WHITE, WIDTH // 2 - 150, HEIGHT // 2)      
                draw_text("Press Spacebar to Restart", font, WHITE, WIDTH // 2 - 220, HEIGHT // 2 + 50)    
                pygame.display.flip()    
                waiting_for_input = True    
                while waiting_for_input:    
                    for event in pygame.event.get():    
                        if event.type == pygame.QUIT:    
                            pygame.quit()    
                            sys.exit()    
                        if event.type == pygame.KEYDOWN:    
                            if event.key == pygame.K_SPACE:    
                                main_game()      
                                return    
   
        on_block = False      
        for spike in spikes:    
            if spike.colliderect(pygame.Rect(player_x, player_y, player_width, player_height)):    
                if player_y + player_height <= spike.y + gravity:      
                    player_y = spike.y - player_height      
                    player_velocity = 0      
                    jumping = False    
                    on_block = True      
   
        draw_player(player_x, player_y)    
        draw_spikes(spikes)    
   
        pygame.display.update()    
        clock.tick(FPS)    
   
if __name__ == "__main__":    
    main_game()   

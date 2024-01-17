import pygame
from pygame.sprite import Group, Sprite
import random
import sys


class Ships:
    def __init__(self, screen, si_setting):
        self.screen = screen
        self.img = pygame.image.load("ship.bmp")
        self.screen_rect = self.screen.get_rect()
        self.rect = self.img.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom - 50
        self.movements = {
            "right": False,
            "left": False
        }
        self.si_setting = si_setting
        self.center = float(self.rect.centerx)

    def movement(self, motion):
        for key, value in self.movements.items():
            if key == motion:
                self.movements[key] = True

    def move(self, motion):

        if motion == "left":
            if self.movements["left"] and self.rect.left < self.screen_rect.left:
                pass
            else:
                self.center -= self.si_setting.ship_speed_factor

        if motion == "right":
            if self.movements["right"] and self.rect.right > self.screen_rect.right:
                pass
            else:
                self.center += self.si_setting.ship_speed_factor

        self.rect.centerx = int(self.center)

    def blitme(self):
        self.screen.blit(self.img, self.rect)


class Bullet(Sprite):
    def __init__(self, si_setting, screen, ship):
        super(Bullet, self).__init__()
        self.screen = screen
        self.image = pygame.image.load("beam.bmp")
        self.screen_rect = self.screen.get_rect()
        self.rect = self.image.get_rect()
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top - 20
        self.y = float(self.rect.y)
        self.speed_factor = si_setting.bullet_speed_factor

    def draw_me(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.y -= self.speed_factor
        self.rect.y = int(self.y)


class Base(Sprite):
    def __init__(self, screen, row, column, number, si_setting):
        super(Base, self).__init__()
        self.screen = screen
        self.row = row
        self.column = column
        self.number = number
        self.screen_rect = self.screen.get_rect()
        self.color = (0, 150, 0)
        self.width = 5
        self.height = 5
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.something = self.number * (self.width * si_setting.base_colomn + 50)
        self.left = self.screen_rect.left + 50 + self.column * self.width + self.something
        self.top = self.screen_rect.bottom - 180 + self.row * self.height
        self.rect = self.image.get_rect()
        self.rect.top = self.top
        self.rect.left = self.left

    def blit_me(self):
        self.screen.blit(self.image, self.rect)


class Settings:
    def __init__(self, width=560, height=640, bgcolor=(0, 0, 0)):
        self.screen_width = width
        self.screen_height = height
        self.bgcolor = bgcolor
        self.ship_speed_factor = 2.3

        self.bullet_speed_factor = 4
        self.bullet_number_limit = 1

        self.meteor_limit = 80

        self.alien_rows = 5
        self.alien_columns = 11
        self.alien_speed_factor = 0.2
        self.alien_fleet_direction = 1.0

        self.beam_speed_factor = 2

        self.matrix = []
        self.base_matrix = []
        self.base_row = 7
        self.base_colomn = 16
        self.base_number = 4
        self.fire_factor = 600
        self.fire_rate = 10
        self.frame_rate = 60
        self.switch_time = 0.5

        self.life = 40
        self.score = 0


class AlienBeams(Sprite):
    def __init__(self, screen, alien, si_setting):
        super(AlienBeams, self).__init__()
        self.screen = screen
        self.image = pygame.image.load("alien_beam.bmp")
        self.screen_rect = self.screen.get_rect()
        self.rect = self.image.get_rect()
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.top - 5
        self.y = float(self.rect.y)
        self.speed_factor = si_setting.beam_speed_factor

    def draw_me(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.y += self.speed_factor
        self.rect.y = int(self.y)


class Aliens(Sprite):
    def __init__(self, screen, row, column, si_setting):
        super(Aliens, self).__init__()
        self.image = pygame.image.load("alien.bmp")
        self.image_name = "alien.bmp"
        self.screen = screen
        self.row = row
        self.column = column
        self.current_frame = 0
        self.rect = self.image.get_rect()
        self.rect.height = self.rect.bottom - self.rect.top
        self.rect.width = self.rect.right - self.rect.left
        self.screen_rect = self.screen.get_rect()
        self.rect.left += column * (15 + self.rect.width)
        self.rect.top += row * (15 + self.rect.height) + 40
        self.dx = si_setting.alien_speed_factor
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)
        self.row_n_column = []

    def draw_me(self):
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        if self.rect.right > self.screen_rect.right:
            return False
        if self.rect.left < self.screen_rect.left:
            return False
        else:
            return True

    def image_switch(self):
        if self.image_name == "alien.bmp":
            self.image_name = "alien1_up.bmp"
            self.image = pygame.image.load(self.image_name)
        else:
            self.image_name = "alien.bmp"
            self.image = pygame.image.load(self.image_name)

    def move(self, si_setting):
        self.dx = si_setting.alien_speed_factor
        self.x += self.dx * si_setting.alien_fleet_direction
        self.rect.centerx = int(self.x)
        if self.row >= 1:
            if self.row < 3:
                if self.current_frame % (si_setting.frame_rate * si_setting.switch_time) == 0:
                    self.image_switch()

    def update_type(self):
        if self.row == 0:
            self.image = pygame.image.load("mushroom.bmp")
        elif self.row == 1:
            self.image = pygame.image.load("alien.bmp")
        elif self.row == 2:
            self.image = pygame.image.load("alien.bmp")
        else:
            self.image = pygame.image.load("jelly.bmp")

    def dead(self, si_setting):
        self.row_n_column = [self.row, self.column]
        si_setting.matrix[self.row][self.column] = False
        return self.row_n_column

    def is_lowest(self, si_setting):
        if si_setting.matrix[self.row][self.column]:
            return True

        else:
            return False

    def set_lowest(self, si_setting, boolean):
        si_setting.matrix[self.row][self.column] = boolean


class Meteor(Sprite):
    def __init__(self, screen):
        super(Meteor, self).__init__()
        self.width = random.randint(3, 5)
        self.height = random.randint(5, 6)
        self.dy = random.uniform(0.5, 1.5)
        self.light_col = []
        self.dark_col = []
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.three_color = (
            random.randint(220, 255),
            random.randint(220, 255),
            random.randint(220, 255)
        )
        self.xcor = random.randint(self.screen_rect.left, self.screen_rect.right)
        self.rect = pygame.Rect(self.xcor, 0, self.width, self.height)
        self.y = float(self.rect.top)

    def draw_me(self):
        pygame.draw.rect(self.screen, self.three_color, self.rect)

    def update(self):
        self.y += self.dy
        self.rect.y = int(self.y)


def time_fit(screen, meteors):
    if random.randrange(1, 15) == 1:
        create_meteor(screen, meteors)


def check_event(si_setting, ship, screen, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Thanks for playing")
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_key_down_events(event, si_setting, ship, screen, bullets)
        elif event.type == pygame.KEYUP:
            check_key_up_events(ship)


def check_key_down_events(event, si_setting, ship, screen, bullets):
    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_a]:
        ship.movement("left")
        ship.img = pygame.image.load("ship_left.bmp")

    if keys_pressed[pygame.K_d]:
        ship.movement("right")
        ship.img = pygame.image.load("ship_right.bmp")

    if keys_pressed[pygame.K_SPACE]:
        fire_bullet(si_setting, ship, screen, bullets)

    if event.key == pygame.K_q:
        print("Thanks for playing")
        sys.exit()


def check_key_up_events(ship):
    for key in ship.movements.keys():
        ship.movements[key] = False
    ship.img = pygame.image.load("ship.bmp")


def update_screen(si_setting, ship, screen, bullets, meteors, aliens, beams, bases, text):
    screen.fill(si_setting.bgcolor)
    time_fit(screen, meteors)
    for meteor in meteors.sprites():
        meteor.draw_me()
    ship.blitme()
    for bullet in bullets.sprites():
        bullet.draw_me()
    for alien in aliens.sprites():
        alien.draw_me()
    for beam in beams.sprites():
        beam.draw_me()
    for base in bases.sprites():
        base.blit_me()
    screen.blit(text, (0, 0))
    pygame.display.flip()


def update_ship(ship, beams, aliens, si_setting):
    for key, value in ship.movements.items():
        if value:
            ship.move(key)

    check_ship_hit(ship, beams, aliens, si_setting)


def fire_bullet(si_setting, ship, screen, bullets):
    if len(bullets) < si_setting.bullet_number_limit:
        new_bullet = Bullet(si_setting, screen, ship)
        bullets.add(new_bullet)
    else:
        pass


def create_meteor(screen, meteors):
    new_meteor = Meteor(screen)
    meteors.add(new_meteor)


def update_bullets(bullets, beams):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullets_collide(bullets, beams)


def update_meteors(meteors):
    meteors.update()
    for meteor in meteors.copy():
        if meteor.rect.top >= 600:
            meteors.remove(meteor)


def update_aliens(aliens, si_setting, bullets, current_frame, bases):
    aliens.update()
    for alien in aliens.sprites():
        alien.current_frame = current_frame
        alien.move(si_setting)
    check_alien_hit(aliens, bullets, si_setting, bases)


def update_fleet(aliens, si_setting, bullets, current_frame, bases):
    check_fleet_edges(si_setting, aliens)
    update_aliens(aliens, si_setting, bullets, current_frame, bases)
    if len(aliens) == 0:
        game_over()


def update_fleet_direction(si_setting, aliens):
    for alien in aliens.sprites():
        alien.rect.centery += 9
    si_setting.alien_fleet_direction *= -1


def create_alien(aliens, si_setting, screen):
    for row in range(si_setting.alien_rows):
        for column in range(si_setting.alien_columns):
            alien = Aliens(screen, row, column, si_setting)
            aliens.add(alien)


def check_fleet_edges(si_setting, aliens):
    for alien in aliens.sprites():
        if not alien.check_edges():
            update_fleet_direction(si_setting, aliens)
            break


def check_alien_hit(aliens, bullets, si_setting, bases):
    for alien in aliens.copy():
        for bullet in bullets.copy():
            if touch(alien, bullet):
                data = alien.dead(si_setting)
                si_setting.matrix[data[0]][data[1]] = "dead"
                try:
                    for u in range(5):
                        if si_setting.matrix[data[0] - (u+1)][data[1]] != "dead":
                            si_setting.matrix[data[0] - (u+1)][data[1]] = True
                            break
                except IndexError:
                    pass
                score(si_setting, alien)
                print(si_setting.score)
                aliens.remove(alien)
                bullets.remove(bullet)

    pygame.sprite.groupcollide(bases, aliens, True, False)


def change_alien_type(aliens):
    for alien in aliens.sprites():
        alien.update_type()


def create_alien_beam(beams, screen, alien, si_setting):
    beam = AlienBeams(screen, alien, si_setting)
    beams.add(beam)


def update_beam(beams):
    beams.update()
    for beam in beams.copy():
        if beam.rect.bottom > beam.screen_rect.bottom - 30:
            beams.remove(beam)


def random_fire(aliens, beams, screen, si_setting):
    for alien in aliens.sprites():
        if alien.is_lowest(si_setting):
            if random.randrange(1, abs(si_setting.fire_rate * si_setting.frame_rate)) == 1:
                create_alien_beam(beams, screen, alien, si_setting)


def create_matrix(si_setting):
    matrix = []
    for row in range(si_setting.alien_rows):
        first_dimension = []
        for column in range(si_setting.alien_columns):
            if row == si_setting.alien_rows - 1:
                first_dimension.append(True)
            else:
                first_dimension.append(False)
        matrix.append(first_dimension)
    si_setting.matrix = matrix


def touch(obj_1, obj_2):
    if obj_1.rect.top <= obj_2.rect.bottom:
        if obj_1.rect.bottom >= obj_2.rect.top:
            if obj_1.rect.left <= obj_2.rect.right:
                if obj_1.rect.right >= obj_2.rect.left:
                    return True
    else:
        return False


def check_ship_hit(ship, beams, aliens, si_setting):
    for beam in beams.copy():
        if touch(beam, ship):
            si_setting.score -= 100
            if si_setting.score < 0:
                si_setting.score = 0
                print("You Suck!")
            beams.remove(beam)

    for alien in aliens.copy():
        if touch(alien, ship):
            aliens.empty()
            game_over()
            sys.exit()


def check_bullets_collide(bullets, beams):
    for beam in beams.copy():
        for bullet in bullets.copy():
            if touch(bullet, beam):
                bullets.remove(bullet)
                beams.remove(beam)


def update_alien_attribute(si_setting, aliens):
    dead_aliens = 55 - len(aliens)
    speed_level = dead_aliens
    if speed_level < 14:
        si_setting.switch_time = 0.5
        si_setting.alien_speed_factor = 0.3
        fire_rate = 20
    elif speed_level < 28:
        si_setting.switch_time = 0.4
        si_setting.alien_speed_factor = 0.5
        fire_rate = 15
    elif speed_level < 32:
        si_setting.switch_time = 0.2
        si_setting.alien_speed_factor = 0.6
        fire_rate = 10
    else:
        si_setting.switch_time = 0.1
        si_setting.alien_speed_factor = 1.0
        fire_rate = 5
    si_setting.fire_rate = fire_rate


def create_base(si_setting, bases, screen):
    for i in range(si_setting.base_number):
        for j in range(si_setting.base_row):
            for k in range(si_setting.base_colomn):
                if can_create(si_setting, j, k):
                    base = Base(screen, j, k, i, si_setting)
                    bases.add(base)


def base_update(bases, bullets, beams):
    for base in bases.copy():
        for bullet in bullets.copy():
            if touch(base, bullet):
                bases.remove(base)
                bullets.remove(bullet)

    for beam in beams.copy():
        for base in bases.copy():
            if touch(base, beam):
                if beam.rect.centerx <= base.rect.right:
                    if beam.rect.centerx > base.rect.left:
                        beams.remove(beam)
                        bases.remove(base)


def game_over():
    print("game over")
    sys.exit()


def score(si_setting, alien):
    local_score = 0
    if alien.row == 0:
        local_score += 30
    else:
        if alien.row < 3:
            local_score += 20
        else:
            local_score += 10
    si_setting.score += local_score


def can_create(si_setting, row, column):
    local_row = row + 1
    local_column = column + 1
    if local_row >= 1:
        if local_row <= 4:
            if local_column >= (4 - row):
                if local_column <= si_setting.base_colomn - (4 - local_row):
                    return True
            else:
                return False
        else:
            local_row -= 4
            if local_column >= (4 - (row - 4)):
                if local_column <= si_setting.base_colomn - (4 - local_row):
                    return False
                else:
                    return True
            else:
                return True


def run_game():
    pygame.init()
    clock = pygame.time.Clock()
    si_setting = Settings()
    screen = pygame.display.set_mode((si_setting.screen_width, si_setting.screen_height))
    pygame.display.set_caption("Space Invader")
    ship = Ships(screen, si_setting)
    bullets = Group()
    meteors = Group()
    aliens = Group()
    beams = Group()
    bases = Group()
    font = pygame.font.SysFont("C:\Windows\Fonts\smalle.fon", 30)
    current_frame = 0
    create_matrix(si_setting)
    create_alien(aliens, si_setting, screen)
    create_base(si_setting, bases, screen)
    change_alien_type(aliens)
    while True:
        text = font.render("Score: " + str(si_setting.score), True, (255, 255, 255))
        check_event(si_setting, ship, screen, bullets)
        update_ship(ship, beams, aliens, si_setting)
        update_bullets(bullets, beams)
        update_meteors(meteors)
        update_fleet(aliens, si_setting, bullets, current_frame, bases)
        random_fire(aliens, beams, screen, si_setting)
        update_beam(beams)
        base_update(bases, bullets, beams)
        update_screen(si_setting, ship, screen, bullets, meteors, aliens, beams, bases, text)
        update_alien_attribute(si_setting, aliens)
        current_frame += 1
        clock.tick(si_setting.frame_rate)

if __name__ == "__main__":
    print('''
    a, d to move
    space to shoot
    ''')
    run_game()


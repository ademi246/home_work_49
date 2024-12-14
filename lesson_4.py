from random import randint, choice


class GameEntity:
    def __init__(self, name, health, damage):
        self.__name = name
        self.__health = health
        self.__damage = damage

    @property
    def name(self):
        return self.__name

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        if value < 0:
            self.__health = 0
        else:
            self.__health = value

    @property
    def damage(self):
        return self.__damage

    @damage.setter
    def damage(self, value):
        self.__damage = value

    def __str__(self):
        return f'{self.__name} health: {self.__health} damage: {self.__damage}'


class Boss(GameEntity):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage)
        self.__defence = None

    @property
    def defence(self):
        return self.__defence

    def choose_defence(self, heroes):
        hero = choice(heroes)
        self.__defence = hero.ability

    def attack(self, heroes):
        for hero in heroes:
            if hero.health > 0:
                if type(hero) == Berserk and self.defence != hero.ability:
                    block = choice([5, 10])  # 5 or 10
                    hero.blocked_damage = block
                    hero.health -= (self.damage - block)
                else:
                    hero.health -= self.damage

    def __str__(self):
        return f'BOSS ' + super().__str__() + f' defence: {self.__defence}'


class Hero(GameEntity):
    def __init__(self, name, health, damage, ability):
        super().__init__(name, health, damage)
        self.__ability = ability

    @property
    def ability(self):
        return self.__ability

    def attack(self, boss):
        boss.health -= self.damage

    def apply_super_power(self, boss, heroes):
        pass


class Warrior(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'CRIT')

    def apply_super_power(self, boss, heroes):
        coef = randint(2, 5)
        boss.health -= self.damage * coef
        print(f'Warrior {self.name} hit critically {self.damage * coef}')


class Magic(Hero):
    def __init__(self, name, health, damage, boost_poinst):
        super().__init__(name, health, damage,'BOOST')
        self.__boost_poinst = boost_poinst


    def apply_super_power(self, boss, heroes):
            for hero in heroes:
                if hero.health > 0 and self != hero:
                    boss.health -= (hero.damage * (self.__boost_poinst * 1))
                    print(f'Magic {self.name} boosted {hero.name}: {int(hero.damage * (self.__boost_poinst * 1))}')



class Medic(Hero):
    def __init__(self, name, health, damage, heal_points):
        super().__init__(name, health, damage, 'HEAL')
        self.__heal_points = heal_points

    def apply_super_power(self, boss, heroes):
        for hero in heroes:
            if hero.health > 0 and self != hero:
                hero.health += self.__heal_points

class Witcher(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage,'REVIVES')

    def apply_super_power(self, boss, heroes):
        dead_here = None
        for hero in heroes:
            if hero.health == 0:
                dead_here = hero
                break

        if dead_here:
            chance = choice([0, 5])
            if chance == 1:
                dead_here.health = 20
                self.health = 0
                print(f'Witcher {self.name} revived: {dead_here}')
            else:
                print(f'Witcher {self.name} attempted revival but failed')
        return(dead_here)


class Hacker(Hero):
    def __init__(self, name, health, attack, defense, steal_amount):
        super().__init__(name, health, attack, defense)
        self.steal_amount = steal_amount

    def apply_super_power(self, boss, heroes):
        if boss.is_alive():
            damage = min(self.steal_amount, boss.health)
            boss.take_damage(damage)
            hero_to_heal = random.choice([hero for hero in heroes if hero.is_alive])
            hero_to_heal.heal(damage)
            print(f"{self.name} stole {damage} the boss's health and handed it over{hero_to_heal.name}!")


class Berserk(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'BLOCK_REVERT')
        self.__blocked_damage = 0

    @property
    def blocked_damage(self):
        return self.__blocked_damage

    @blocked_damage.setter
    def blocked_damage(self, value):
        self.__blocked_damage = value

    def apply_super_power(self, boss, heroes):
        boss.health -= self.blocked_damage
        print(f'Berserk {self.name} reverted {self.__blocked_damage} damage to boss')


round_number = 0
while round_number <= 4:
    break


def is_game_over(boss, heroes):
    if boss.health <= 0:
        print('Heroes won!!!')
        return True
    all_heroes_dead = True
    for hero in heroes:
        if hero.health > 0:
            all_heroes_dead = False
            break
    if all_heroes_dead:
        print('Boss won!!!')
        return True
    return False


def play_round(boss, heroes):
    global round_number
    round_number += 1
    boss.choose_defence(heroes)
    boss.attack(heroes)
    for hero in heroes:
        if hero.health > 0 and boss.health > 0 and hero.ability != boss.defence:
            hero.attack(boss)
            hero.apply_super_power(boss, heroes)
    show_statistics(boss, heroes)


def show_statistics(boss, heroes):
    print(f'ROUND {round_number} -------------')
    print(boss)
    for hero in heroes:
        print(hero)


def start_game():
    boss = Boss('Lord', 1000, 50)
    warrior_1 = Warrior('Brane', 280, 15)
    warrior_2 = Warrior('Alucard', 270, 20)
    magic = Magic('Subaru', 290, 15,1.2)
    doc = Medic('Merlin', 250, 5, 15)
    assistant = Medic('Florin', 300, 5, 5)
    berserk = Berserk('Guts', 260, 0)
    witcher = Witcher('koil',220,0)

    heroes_list = [warrior_1, warrior_2, magic, doc, assistant, berserk,witcher]

    show_statistics(boss, heroes_list)
    while not is_game_over(boss, heroes_list):
        play_round(boss, heroes_list)


start_game()
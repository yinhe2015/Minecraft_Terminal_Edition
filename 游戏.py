import traceback
import readline
import random
import atexit
import time
import json
import os

class MinecraftText:
    def _init_constants(self):
        '''初始化游戏配置常量'''
        # 历史记录文件路径
        self.HISTORY_PATH = './history.txt'

        # 饥饿值
        self.HUNGER_COST_COLLECT = 1             # 采集资源消耗饥饿值
        self.HUNGER_COST_MOVE = (2,4)            # 移动消耗饥饿值
        self.EAT_FOOD_INCREASES_HUNGER = (1,6)   # 吃食物增加饥饿值

        # 生命值
        self.MAX_HEALTH = 20                     # 最大生命值
        self.MAX_HUNGER = 20                     # 最大饥饿值
        self.MAX_ENDER_DRAGON_HEALTH = 100       # 最大末影龙生命值

        self.EAT_FOOD_INCREASES_HEALTH = (1,3)   # 吃食物增加生命值
        self.EAT_CACTUS_REDUCES_HEALTH = (1,2)   # 吃仙人掌减少生命值

        self.MONSTER_ATTACK_DAMAGE = (1, 3)      # 怪物攻击伤害范围
        self.ENDER_DRAGON_ATTACK_DAMAGE = (1, 5) # 末影龙攻击伤害范围

        # 时间
        self.TIME_CYCLE = ['凌晨', '早晨', '上午', '中午', '下午', '黄昏', '夜晚', '深夜'] # 时间周期
        self.TIME_PASS_PROBABILITY = 15          # 时间流逝概率(%)

        # 物品列表
        self.FOODS = ['肉', '浆果', '仙人掌']  # 可食用物品
        self.PICKAXE_LEVELS = ['无', '木镐', '石镐', '铁镐', '钻石镐'] # 工具等级列表
        self.WEAPON_LEVELS = ['空手', '木剑', '石剑', '铁剑', '钻石剑'] # 武器等级列表

        # 物品配方
        self.RECIPES = {
            # 木
            '木板':   {'木头': 1,                             '产出': {'木板': 4},   '文档': '1个木头制作4个木板'},
            '木棍':   {'木板': 2,                             '产出': {'木棍': 4},   '文档': '2个木板制作4个木棍'},

            # 工作台和熔炉
            '工作台': {'木板': 4,                              '产出': {'工作台': 1}, '文档': '4个木板制作1个工作台'},
            '熔炉':   {'石头': 8,            '工具': ['工作台'], '产出': {'熔炉': 1},  '文档': '8个石头制作1个熔炉'},

            # 烧制
            '铁锭':   {'铁矿石': 1,          '工具': ['熔炉'], '产出': {'铁锭': 1},  '文档': '1个铁矿石烧制1个铁锭'},
            '玻璃':   {'沙子': 1,            '工具': ['熔炉'],  '产出': {'玻璃': 1},  '文档': '1沙子烧制1个玻璃'},

            # 镐子
            '木镐':   {'木板': 3, '木棍': 2, '工具': ['工作台'], '产出': {'木镐': 1},  '文档': '3木板+2木棍制作1个木镐'},
            '石镐':   {'石头': 3, '木棍': 2, '工具': ['工作台'], '产出': {'石镐': 1},  '文档': '3石头+2木棍制作1个石镐'},
            '铁镐':   {'铁锭': 3, '木棍': 2, '工具': ['工作台'], '产出': {'铁镐': 1},  '文档': '3铁锭+2木棍制作1个铁镐'},
            '钻石镐': {'钻石': 3, '木棍': 2, '工具': ['工作台'], '产出': {'钻石镐': 1}, '文档': '3钻石+2木棍制作1个钻石镐'},

            # 剑
            '木剑':   {'木板': 1, '木棍': 1, '工具': ['工作台'], '产出': {'木剑': 1},  '文档': '1木板+1木棍制作1个木剑'},
            '石剑':   {'石头': 1, '木棍': 1, '工具': ['工作台'], '产出': {'石剑': 1},  '文档': '1石头+1木棍制作1个石剑'},
            '铁剑':   {'铁锭': 1, '木棍': 1, '工具': ['工作台'], '产出': {'铁剑': 1},  '文档': '1铁锭+1木棍制作1个铁剑'},
            '钻石剑': {'钻石': 1, '木棍': 1, '工具': ['工作台'], '产出': {'钻石剑': 1}, '文档': '1钻石+1木棍制作1个钻石剑'},
        }

        # 生物群系配置
        self.BIOMES = {
            '森林': {
                '文档': '树木繁茂的区域,有许多橡树和草丛',
                'resources': ['橡树', '橡树', '石头', '石头', '石头', '小动物', '草丛', '草丛'],
            },
            '平原': {
                '文档': '开阔的草地,有少量树木和许多小动物',
                'resources': ['橡树', '草丛', '草丛', '小动物', '小动物', '小动物'],
            },
            '山脉': {
                '文档': '高耸的山脉,有丰富的石头资源',
                'resources': ['石头', '石头', '石头', '石头', '铁矿石', '铁矿石', '怪物'],
            },
            '沙漠': {
                '文档': '炎热干燥的沙漠,有少量仙人掌和沙子',
                'resources': ['沙子', '沙子', '仙人掌', '仙人掌', '怪物'],
            },
            '洞穴': {
                '文档': '深不见底的洞穴,有怪物和矿石',
                'resources': ['怪物', '怪物', '铁矿石', '铁矿石', '铁矿石', '钻石矿石', '钻石矿石', '钻石矿石'],
            },
            '末地': {
                '文档': '充满神秘力量的维度,末影龙的栖息地',
                'resources': ['末影龙', '末地水晶', '末地水晶'],
            }
        }

        # 指令映射表
        self.COMMAND_MAP = {
            'chop': self.collect_wood,          # 砍伐树木获取木头
            'mine': self.collect_stone,         # 挖掘石头
            'mineiron': self.collect_iron,      # 挖掘铁矿石
            'minediamond': self.collect_diamond,# 挖掘钻石矿石
            'minesand': self.collect_sand,      # 挖掘沙子

            'craft': self.craft_item,           # 制作物品(需指定物品名)
            'food': self.find_food,             # 寻找食物
            'eat': self.eat_food,               # 吃东西恢复饥饿值

            'help': self.show_help,             # 查看帮助
            'status': self.print_status,        # 查看当前状态
            'inv': self.print_inventory,        # 查看背包
            'enderdragon': self.print_ender_dragon_status,  # 查看末影龙状态

            'kill': self.attack_entity,         # 攻击生物(怪物/末影龙)

            'move': self.move_to_biome,         # 移动到其他生物群系
            'map': self.show_map,               # 查看已探索地图

            'clear': self.clear_screen,         # 清空屏幕
            'save': self.save_game,             # 手动保存游戏
        }

    def __init__(self, data_path: str) -> None:
        self.data_path = data_path
        self._init_constants()

        try:
            readline.read_history_file(self.HISTORY_PATH)
        except FileNotFoundError:
            pass

        atexit.register(readline.write_history_file, self.HISTORY_PATH)
    
    def run(self) -> None:
        self.load_game()
        self._print_welcome_msg()
        self.play()
        print('\n感谢游玩! 再见～')
        self.save_game()

    def _print_welcome_msg(self) -> None:
        '''打印欢迎信息'''
        print('=== 文字版我的世界 ===')
        print('欢迎来到方块世界!你需要生存下去并建造东西')
        print('输入指令来操作(查看指令输入 \'help\')')
        self.print_status()

    def _init_default_status(self) -> None:
        '''初始化默认游戏状态'''
        # 玩家状态
        self.health = self.MAX_HEALTH
        self.hunger = self.MAX_HUNGER
        self.ender_dragon_health = self.MAX_ENDER_DRAGON_HEALTH

        # 初始背包
        self.inventory = {
            '木头': 0, '木板': 0, '木棍': 0,
            '肉': 5, '浆果': 0, '仙人掌': 0,
            '石头': 0, '工作台': 0, '熔炉': 0,
            '铁矿石': 0, '铁锭': 0, '钻石': 0,
            '木镐': 0, '石镐': 0, '铁镐': 0, '钻石镐': 0,
            '木剑': 0, '石剑': 0, '铁剑': 0, '钻石剑': 0,
            '沙子': 0, '玻璃': 0,
        }

        # 世界状态
        self.biome = '森林'
        self.time_of_day = '早晨'
        self.nearby = {}
        self._generate_nearby_resources() # 生成初始资源
        self.explored_biomes = {self.biome}

    def load_game(self) -> None:
        '''加载游戏数据'''
        try:
            if os.path.exists(self.data_path):
                print('找到存档,正在加载...')
                with open(self.data_path, 'r', encoding='utf-8') as f:
                    data: dict = json.load(f)
                self.health = data.get('health', self.MAX_HEALTH)
                self.hunger = data.get('hunger', self.MAX_HUNGER)
                self.inventory = data.get('inventory', {})
                self.biome = data.get('biome', '森林')
                self.time_of_day = data.get('time_of_day', '早晨')
                self.nearby = data.get('nearby', {})
                self.ender_dragon_health = data.get('ender_dragon_health', self.MAX_ENDER_DRAGON_HEALTH)
                self.explored_biomes = set(data.get('explored_biomes', ['森林']))
            else:
                print('未找到存档,将创建新游戏')
                self._init_default_status()
            
            print('✅ 加载完成!')
        except Exception as error:
            print(f'❌ 存档加载失败: {error}')
            exit(1)

    def save_game(self) -> None:
        '''保存游戏数据'''
        try:
            data = {
                'health': self.health,
                'hunger': self.hunger,
                'inventory': self.inventory,
                'biome': self.biome,
                'time_of_day': self.time_of_day,
                'nearby': self.nearby,
                'explored_biomes': list(self.explored_biomes),
                'ender_dragon_health': self.ender_dragon_health,
            }
            with open(self.data_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f'✅ 游戏已保存到 {self.data_path}')
        except Exception as error:
            print(f'❌ 保存失败: {error}')

    def show_help(self) -> None:
        '''显示帮助信息'''
        print('\n=== 指令列表 ===')
        print('📦 资源采集:')
        print('  chop      - 砍伐树木获取木头')
        print('  mine      - 挖掘石头(需要木镐)')
        print('  mineiron  - 挖掘铁矿石(需要石镐)')
        print('  minediamond - 挖掘钻石矿石(需要铁镐)')
        print('  minesand - 挖掘沙子(需要无工具)')

        print('\n🔨 制作系统:')
        print('  craft [物品] - 制作物品(例如\'craft 木板\',在后面加上\'help\'查看文档)')
        print('  可制作物品:', ', '.join(self.RECIPES.keys()))

        print('\n🍖 生存系统:')
        print('  food      - 寻找食物(从小动物/草丛/仙人掌获取)')
        print('  eat       - 吃东西恢复饥饿值')

        print('\n📊 信息查看:')
        print('  status    - 查看当前状态(生命值/位置等)')
        print('  inv       - 查看背包物品')
        print('  enderdragon - 查看末影龙状态')
        print('  map       - 查看已探索的生物群系')

        print('\n⚔️ 战斗系统:')
        print('  kill      - 攻击周围的怪物或末影龙')

        print('\n🌍 移动:')
        print('  move      - 移动到其他生物群系')
        print('  clear     - 清空屏幕')

        print('\n🔄 其他:')
        print('  help      - 查看指令帮助')
        print('  save      - 保存游戏')
        print('  exit      - 退出游戏')

    def _generate_nearby_resources(self) -> None:
        '''生成当前生物群系的资源'''
        if self.biome not in self.nearby:
            self.nearby[self.biome] = []

        # 资源不足时补充(保持资源数量在5-8个)
        current_count = len(self.nearby[self.biome])
        if current_count < 5:
            need = random.randint(5 - current_count, 8 - current_count)
            new_resources = random.choices(
                self.BIOMES[self.biome]['resources'],
                k=need
            )
            new_resources = [item for item in new_resources if item != '末影龙']
            self.nearby[self.biome].extend(new_resources)

    def _count_resources(self) -> dict[str, int]:
        '''统计周围资源数量'''
        resource_counts = {}
        for item in self.nearby.get(self.biome, []):
            resource_counts[item] = resource_counts.get(item, 0) + 1
        return resource_counts

    def _has_resource(self, resource: str) -> bool:
        '''检查周围是否有指定资源'''
        return resource in self.nearby.get(self.biome, [])

    def _check_monster_attack(self) -> None:
        '''检查怪物是否袭击'''
        if self._has_resource('怪物') and random.random() < 0.5:
            print('\n😈 一只怪物突然袭击了你!')
            weapon, level = self._get_best_weapon()

            # 有武器时受到的伤害减少
            base_damage = random.randint(*self.MONSTER_ATTACK_DAMAGE)
            damage = max(1, base_damage - (level // 2))  # 武器等级越高,受伤越少
            self.health -= damage

            print(f'你受到了{damage}点伤害! ')
            self.nearby[self.biome].remove('怪物')
            print(f'你用{weapon}击败了怪物!')

    def _attack_monster(self, weapon: str, level: int) -> None:
        '''攻击怪物'''
        print(f'\n你用{weapon}攻击怪物!')
        self.nearby[self.biome].remove('怪物')

        # 计算伤害与反击
        monster_damage = random.randint(*self.MONSTER_ATTACK_DAMAGE)
        self.health -= monster_damage
        print(f'怪物对你造成了{monster_damage}点伤害!')
        print(f'你击败了怪物! ')

    def _attack_dragon(self, weapon: str, level: int) -> None:
        '''攻击末影龙'''
        if weapon == '空手':
            print('\n你没有武器,无法伤害末影龙!')
            dragon_damage = random.randint(*self.ENDER_DRAGON_ATTACK_DAMAGE)
            self.health -= dragon_damage
            print(f'末影龙对你造成了{dragon_damage}点伤害!')
            return

        # 计算对末影龙的伤害(与武器等级挂钩)
        damage = level * 8  # 钻石剑(等级4)造成32点伤害
        self.ender_dragon_health -= damage
        if self.ender_dragon_health < 0:
            self.ender_dragon_health = 0

        print(f'\n你用{weapon}攻击末影龙,造成了{damage}点伤害!')
        self.print_ender_dragon_status()

        # 末影龙反击
        if self.ender_dragon_health > 0:
            dragon_damage = random.randint(*self.ENDER_DRAGON_ATTACK_DAMAGE)
            self.health -= dragon_damage
            print(f'末影龙反击,对你造成了{dragon_damage}点伤害!')

    def _get_pickaxe(self, min_level: str = '无') -> tuple[str|None, int]:
        '''获取当前最佳镐子及等级'''
        for pickaxe in reversed(self.PICKAXE_LEVELS):  # 从高级到低级检查
            if self.inventory.get(pickaxe, 0) > 0:
                level = self.PICKAXE_LEVELS.index(pickaxe)
                min_idx = self.PICKAXE_LEVELS.index(min_level)
                if level >= min_idx:
                    return pickaxe, level

        # 无符合条件的镐子
        if min_level != '无':
            print(f'\n需要至少{min_level}才能进行此操作!')
        return '空手', 0  # 空手作为最低等级

    def _get_best_weapon(self) -> tuple[str, int]:
        '''获取当前最佳武器及等级'''
        for weapon in reversed(self.WEAPON_LEVELS):
            if self.inventory.get(weapon, 0) > 0:
                return weapon, self.WEAPON_LEVELS.index(weapon)
        return '空手', 0

    def _check_hunger(self) -> None:
        '''检查饥饿值'''
        if self.hunger <= 0:
            self.health -= 1
            print('饥饿值为0,生命值减1')
        elif self.hunger >= self.MAX_HUNGER:
            self.hunger = self.MAX_HUNGER
        elif self.hunger <= 5:
            print('\n肚子咕咕叫了,该吃东西了!')
        print(f'饥饿值: {self.hunger}/{self.MAX_HUNGER}')

    def _check_health(self) -> None:
        '''检查生命值'''
        dead = False

        if self.health <= 0:
            self.dead()
            dead = True
        elif self.health >= self.MAX_HEALTH:
            self.health = self.MAX_HEALTH
        print(f'生命值: {self.health}/{self.MAX_HEALTH}')

        return dead

    def dead(self) -> None:
        '''游戏结束处理'''
        print('\n=== 你死了! ===')
        return
        if os.path.exists(self.data_path):
            os.remove(self.data_path)
            print('游戏数据已删除,请重新开始')

    def clear_screen(self) -> None:
        '''清除终端屏幕'''
        os.system('cls' if os.name == 'nt' else 'clear')
        self._print_welcome_msg()

    def print_status(self) -> None:
        '''显示玩家当前状态'''
        print(f'\n=== 状态 ===')
        # 生命值展示(用不同符号区分)
        health_full = self.health // 2
        health_empty = (self.MAX_HEALTH - self.health) // 2
        print(f'生命值: {'❤' * health_full}{'♡' * health_empty} ({self.health}/{self.MAX_HEALTH})')

        # 饥饿值展示
        hunger_full = self.hunger // 2
        hunger_empty = (self.MAX_HUNGER - self.hunger) // 2
        print(f'饥饿值: {'🍖' * hunger_full}{'░' * hunger_empty} ({self.hunger}/{self.MAX_HUNGER})')

        # 环境信息
        print(f'时间: {self.time_of_day}')
        print(f'位置: {self.biome} - {self.BIOMES[self.biome]['文档']}')

        # 周围资源分类展示(优化可读性)
        resource_counts = self._count_resources()
        print('周围资源:')
        for item, count in resource_counts.items():
            if item in ['怪物', '末影龙']:
                print(f'  ⚠️ 危险: {item} x{count}')
            elif item in ['小动物','草丛','仙人掌']:
                print(f'  🍖 可食用: {item} x{count}')
            elif item in ['铁矿石', '钻石矿石']:
                print(f'  ⛏️ 矿石: {item} x{count}')
            else:
                print(f'  🌿 资源: {item} x{count}')

        # 装备信息
        print(f'\n当前装备: 最佳武器={self._get_best_weapon()[0]} | 最佳镐={self._get_pickaxe()[0]}')

    def print_inventory(self) -> None:
        '''显示背包物品'''
        print(f'\n=== 背包 ===')
        total_items = sum(self.inventory.values())

        if total_items == 0:
            print('背包是空的!')
            return

        # 按类别分组展示
        categories = {
            '基础资源': ['木头', '木板', '木棍', '石头', '沙子', '玻璃'],
            '矿石资源': ['铁矿石', '铁锭', '钻石'],
            '工具': ['木镐', '石镐', '铁镐', '钻石镐', '工作台', '熔炉'],
            '武器': ['木剑', '石剑', '铁剑', '钻石剑'],
            '消耗品': ['肉', '浆果', '仙人掌']
        }

        show_items = []
        for category, items in categories.items():
            has_item = False
            print(f'\n{category}:')
            for item in items:
                show_items.append(item)
                if self.inventory[item] > 0:
                    print(f'  - {item}: {self.inventory[item]}个')
                    has_item = True
            if not has_item:
                print('  - 无')

        has_item = False
        print('\n其他:')
        for item,count in self.inventory.items():
            if item not in show_items:
                print(f'  - {item}: {count}个')
                has_item = True
        if not has_item:
            print('  - 无')

        print(f'\n总物品数: {total_items}')

    def print_ender_dragon_status(self) -> None:
        '''显示末影龙状态'''
        if self.biome != '末地' and self.ender_dragon_health > 0:
            print('\n你还没找到末影龙,去末地看看吧!')
            return

        print(f'\n=== 末影龙 ===')
        dragon_full = self.ender_dragon_health // 10
        dragon_empty = (self.MAX_ENDER_DRAGON_HEALTH - self.ender_dragon_health) // 10
        print(f'血量: {'❤' * dragon_full}{'♡' * dragon_empty} ({self.ender_dragon_health}/{self.MAX_ENDER_DRAGON_HEALTH})')
        if self.ender_dragon_health <= 0:
            print('末影龙已被击败!恭喜你完成挑战!')

    def collect_wood(self) -> None:
        '''砍伐树木获取木头'''
        if not self._has_resource('橡树'):
            print('\n周围没有树可以砍!')
            return

        print('\n你开始砍伐树木...')
        time.sleep(1)

        # 根据工具决定效率
        pickaxe, level = self._get_pickaxe('无')  # 砍树不需要特定镐子
        gain = random.randint(level + 1, level + 3)  # 提高获取量随机性

        print(f'你用{pickaxe}砍伐树木')
        self.inventory['木头'] += gain
        print(f'成功获得 {gain} 个木头!')
        self.hunger -= self.HUNGER_COST_COLLECT  # 消耗饥饿值

        # 30%概率让树消失(平衡资源再生)
        if random.random() < 0.3:
            self.nearby[self.biome].remove('橡树')
            print('这棵树被砍倒了')

    def collect_stone(self) -> None:
        '''采集石头'''
        if not self._has_resource('石头'):
            print('\n周围没有石头可以挖!')
            return

        # 检查工具要求(至少木镐)
        pickaxe, level = self._get_pickaxe('木镐')
        if pickaxe is None:
            return

        gain = random.randint(level, level + 2)
        print(f'你用{pickaxe}采集石头')
        self.inventory['石头'] += gain
        print(f'成功获得 {gain} 个石头!')
        self.hunger -= self.HUNGER_COST_COLLECT

        self.nearby[self.biome].remove('石头')
        print('这块石头被你挖断了')

    def collect_iron(self) -> None:
        '''采集铁矿石'''
        if not self._has_resource('铁矿石'):
            print('\n周围没有铁矿石可以挖掘!')
            return

        # 检查工具要求(至少石镐)
        pickaxe, level = self._get_pickaxe('石镐')
        if pickaxe is None:
            return

        gain = random.randint(level - 1, level + 1)  # 矿石获取量略少
        print(f'你用{pickaxe}采集铁矿石')
        self.inventory['铁矿石'] += gain
        print(f'成功获得 {gain} 个铁矿石!')
        self.hunger -= self.HUNGER_COST_COLLECT

        self.nearby[self.biome].remove('铁矿石')

    def collect_diamond(self) -> None:
        '''采集钻石矿石'''
        if not self._has_resource('钻石矿石'):
            print('\n周围没有钻石矿石可以挖掘!')
            return

        # 检查工具要求(至少铁镐)
        pickaxe, level = self._get_pickaxe('铁镐')
        if pickaxe is None:
            return

        gain = random.randint(level - 2, level)  # 钻石获取更稀有
        print(f'你用{pickaxe}采集钻石矿石')
        self.inventory['钻石'] += gain
        print(f'成功获得 {gain} 个钻石!')
        self.hunger -= self.HUNGER_COST_COLLECT

        self.nearby[self.biome].remove('钻石矿石')
        print('这块钻石矿石被你挖断了')

    def collect_sand(self) -> None:
        '''采集沙子'''
        if not self._has_resource('沙子'):
            print('\n周围没有沙子可以挖掘!')
            return

        # 检查工具要求(至少无)
        pickaxe, level = self._get_pickaxe('无')
        if pickaxe is None:
            return

        gain = random.randint(1, 2)  # 沙子获取量少
        print(f'你用{pickaxe}采集沙子')
        self.inventory['沙子'] += gain
        print(f'成功获得 {gain} 个沙子!')
        self.hunger -= self.HUNGER_COST_COLLECT

        self.nearby[self.biome].remove('沙子')
        print('这块沙子被你挖断了')

    def craft_item(self, item_name: str|None = None, count: int|str=1) -> None:
        '''制作物品'''
        if not item_name:
            print('\n请指定要制作的物品,例如输入\'craft 木板\'')
            print('可制作物品列表：', ', '.join(self.RECIPES.keys()))
            return

        if item_name not in self.RECIPES:
            print(f'\n无法制作 {item_name}! 输入\'craft\'查看可制作物品')
            return

        recipe = self.RECIPES[item_name]

        if count == 'help':
            print(recipe['文档'])
            return

        count = int(count)

        # 检查工具要求
        if '工具' in recipe:
            for tool in recipe['工具']:
                if self.inventory.get(tool, 0) <= 0:
                    print(f'\n需要{tool}才能制作{item_name}!')
                    return

        # 检查材料(过滤非材料字段)
        materials = {k: v for k, v in recipe.items() if k not in ['产出', '工具', '文档']}
        for mat, need in materials.items():
            if self.inventory.get(mat, 0) < (need * count):
                print(f'\n材料不足! 需要{need * count}个{mat},当前只有{self.inventory.get(mat, 0)}个')
                return

        # 消耗材料
        for mat, need in materials.items():
            self.inventory[mat] -= need * count
            print(f'消耗 {need * count} 个{mat}')

        # 特殊处理：熔炉需要消耗木板作为燃料
        if recipe.get('工具', None):
            if '熔炉' in recipe['工具']:
                if self.inventory.get('木板', 0) < count:
                    print(f'\n需要{count}个木板作为燃料!')
                    return
                self.inventory['木板'] -= count
                print(f'消耗{count}个木板作为燃料')

        # 生成物品
        for name, item_count in recipe['产出'].items():
            self.inventory[name] += item_count * count
            print(f'成功制作 {item_count * count} 个 {name}')

    def find_food(self) -> None:
        '''寻找食物'''
        # 检查可能的食物来源
        all_food_sources = ['小动物', '草丛', '仙人掌']
        food_sources = []
        for food_source in all_food_sources:
            if self._has_resource(food_source):
                food_sources.append(food_source)

        if not food_sources:
            print('\n周围没有可以获取食物的资源')
            return

        print('\n你开始寻找食物...')
        time.sleep(1)

        # 随机选择食物来源
        source = random.choice(food_sources)
        gain = random.randint(1, 3)

        if source == '小动物':
            print(f'你猎杀了小动物,获得了{gain}份食物!')
            self.inventory['肉'] += gain
        elif source == '草丛':
            print(f'你从草丛中找到了{gain}份浆果!')
            self.inventory['浆果'] += gain
        elif source == '仙人掌':
            print(f'你采集了仙人掌,获得了{gain}份食物(有点扎嘴)...')
            self.inventory['仙人掌'] += gain

        # 消耗食物来源
        self.nearby[self.biome].remove(source)
        print(f'{source}被消耗了')

        self.hunger -= self.HUNGER_COST_COLLECT

    def eat_food(self) -> None:
        '''吃东西恢复饥饿值'''
        if self.hunger >= self.MAX_HUNGER:
            print('\n你已经很饱了,不需要再吃了')
            return

        food_count = sum([self.inventory.get(food_name, 0) for food_name in self.FOODS])
        if food_count < 1:
            print('\n没有食物了! 用\'food\'命令寻找食物吧')
            return

        print(f'食物列表: ')
        for index, item in enumerate(self.FOODS, start=1):
            print(f'{index}. {item}: {self.inventory.get(item, 0)}')
        food_index = input('请输入要吃的食物序号: ')
        try:
            food_index = int(food_index) - 1
            food = self.FOODS[food_index]
        except (ValueError, IndexError):
            print('输入无效,请重新输入')
            return

        if self.inventory[food] < 1:
            print('你没有那么多食物!')
            return

        # 随机恢复饥饿值
        recover = random.randint(self.EAT_FOOD_INCREASES_HUNGER[0], self.EAT_FOOD_INCREASES_HUNGER[1])
        self.inventory[food] -= 1
        self.hunger += recover
        print(f'\n🍽️ 你吃了 1 份 {food} ,恢复了 {recover} 点饥饿值')
        if self.hunger >= self.MAX_HUNGER:
            print('\n你吃饱了!')

        if food == '仙人掌':
            reduce_health = random.randint(*self.EAT_CACTUS_REDUCES_HEALTH)
            self.health -= reduce_health
            print(f'你减少了 {reduce_health} 点生命值! ')
        else:
            add_health = random.randint(*self.EAT_FOOD_INCREASES_HEALTH)
            self.health += add_health
            print(f'你恢复了 {add_health} 点生命值! ')

    def time_pass(self) -> None:
        '''随机时间流逝'''
        if random.randint(0,100) == self.TIME_PASS_PROBABILITY:
            return

        current_idx = self.TIME_CYCLE.index(self.time_of_day)
        self.time_of_day = self.TIME_CYCLE[(current_idx + 1) % len(self.TIME_CYCLE)]

        # 更新资源
        self._generate_nearby_resources()

        # 时间变化提示
        print(f'\n⏳ 时间流逝... 现在是{self.time_of_day}')

        # 特殊事件
        if self.time_of_day == '夜晚':
            print('天黑了!周围传来奇怪的叫声,小心怪物!')
            self._check_monster_attack()
        elif self.time_of_day == '早晨':
            print('天亮了!怪物们躲了起来')

    def move_to_biome(self) -> None:
        '''移动到不同的生物群系'''
        print('\n可前往的生物群系:')
        for i, biome in enumerate(self.BIOMES.keys(), 1):
            status = '已探索' if biome in self.explored_biomes else '未探索'
            print(f'{i}. {biome} ({status}) - {self.BIOMES[biome]['文档']}')

        choice = input('\n输入要前往的生物群系编号 (0取消): ')
        if choice == '0':
            return

        try:
            idx = int(choice) - 1
            new_biome = list(self.BIOMES.keys())[idx]
        except ValueError:
            print('请输入数字!')
            return
        except IndexError:
            print('请输入正确的数字!')
            return

        if new_biome not in self.explored_biomes:
            print(f'\n你发现了新的生物群系: {new_biome}!')
            self.explored_biomes.add(new_biome)

        print(f'正在前往{new_biome}...')
        time_ = 3000
        for i in range(1,time_+1):
            time.sleep(0.001) # 1毫秒
            print(f'\r正在前往{new_biome} ... {i}/{time_}毫秒', end='', flush=True)

        # 消耗饥饿值
        hunger_cost = random.randint(*self.HUNGER_COST_MOVE)
        self.hunger -= hunger_cost

        # 移动后时间流逝
        self.time_pass()
        self.biome = new_biome
        self._generate_nearby_resources()

        self.print_status()

    def show_map(self) -> None:
        '''显示已探索的地图'''
        print('\n=== 已探索地图 ===')
        for biome in self.explored_biomes:
            print(f'📍 {biome}: {self.BIOMES[biome]['文档']}')
        print(f'\n当前位置: {self.biome}')

    def attack_entity(self) -> None:
        '''攻击生物'''
        # 检查目标
        weapon, level = self._get_best_weapon()
        if self._has_resource('怪物'):
            self._attack_monster(weapon, level)
        elif self._has_resource('末影龙'):
            self._attack_dragon(weapon, level)
        else:
            print('\n周围没有可以攻击的目标!')

    def runcmd(self, command: str) -> None:
        '''运行指令('''
        command = command.strip().lower()
        if not command:
            return -1
        argv = [arg for arg in command.split() if arg]
        main_cmd = argv[0]

        if main_cmd == 'exit':
            return -2

        if main_cmd in self.COMMAND_MAP:
            try:
                return self.COMMAND_MAP[main_cmd](*argv[1:])
            except:
                print('\n指令执行错误!')
                traceback.print_exc()
                return -4
        else:
            print('\n未知指令! 输入\'help\'查看可用指令')
            return -3

    def play(self) -> None:
        '''游戏主循环'''
        print()
        while True:
            command = input('输入指令: ')

            out = self.runcmd(command)
            if out == -1:
                continue
            elif out == -2:
                break

            print()

            self._check_hunger()
            self._check_health()

            self.time_pass()

def 运行() -> None:
    MAP_DIR = './maps'
    MAP_FORMAT = '.map'

    # 确保地图目录存在
    os.makedirs(MAP_DIR, exist_ok=True)

    save_name = input('请输入存档名称: ').strip()
    data_path = os.path.join(MAP_DIR, save_name+MAP_FORMAT)

    game = MinecraftText(data_path)
    game.run()
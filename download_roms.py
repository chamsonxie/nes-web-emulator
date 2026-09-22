import urllib.request, os, json

GAMES = [
    ("alter-ego", "Alter Ego", "解谜平台", "Shiru", "2011", "https://buildbot.libretro.com/assets/cores/Nintendo%20-%20Nintendo%20Entertainment%20System/Alter%20Ego.nes", "在两个重力翻转的分身之间切换，挑战单屏解谜平台关卡。"),
    ("nova-the-squirrel", "Nova the Squirrel", "平台跳跃", "NovaSquirrel", "2018", "https://buildbot.libretro.com/assets/cores/Nintendo%20-%20Nintendo%20Entertainment%20System/Nova%20the%20Squirrel.nes", "敏捷的小松鼠在广阔开放世界中冒险的免费平台跳跃游戏。"),
    ("super-tilt-bro", "Super Tilt Bro", "格斗", "Sylvain Gadrat", "2018", "https://buildbot.libretro.com/assets/cores/Nintendo%20-%20Nintendo%20Entertainment%20System/Super%20Tilt%20Bro%20%28USA%29.nes", "NES 上的大乱斗式平台格斗游戏，作者免费发布的版本。"),
    ("tower-of-turmoil", "The Tower of Turmoil", "平台跳跃", "CutterCross", "2020", "https://buildbot.libretro.com/assets/cores/Nintendo%20-%20Nintendo%20Entertainment%20System/The%20Tower%20of%20Turmoil%20%28v1.03%29.nes", "带领剑士 Takemaru 逐层登上被诅咒的高塔。"),
    ("what-remains", "What Remains", "冒险", "Iodine Dynamics", "2019", "https://buildbot.libretro.com/assets/cores/Nintendo%20-%20Nintendo%20Entertainment%20System/What%20Remains%20%28v1.0.2%29.nes", "关于媒体操纵与告密者的剧情向互动冒险游戏。"),
    ("rumblefest-89", "Rumblefest 89", "体育", "Jurassic Sunset Games", "2020", "https://buildbot.libretro.com/assets/cores/Nintendo%20-%20Nintendo%20Entertainment%20System/Rumblefest%2089.nes", "80 年代职业摔跤动作游戏，NESmaker Byte-Off 2020 参赛作品。"),
    ("shadow-animus", "Shadow Animus", "角色扮演", "Chronicler of Legends", "2020", "https://buildbot.libretro.com/assets/cores/Nintendo%20-%20Nintendo%20Entertainment%20System/Shadow%20Animus.nes", "黑暗奇幻冒险 RPG，探索被诅咒的村庄、对抗暗影之心。"),
    ("bobl", "Bobl", "解谜平台", "Morphcat Games", "2020", "https://buildbot.libretro.com/assets/cores/Nintendo%20-%20Nintendo%20Entertainment%20System/Bobl%20%28v1.1%29.nes", "Morphcat Games 出品的精巧解谜平台游戏。"),
    ("project-dart", "Project DART", "动作", "CutterCross", "2021", "https://buildbot.libretro.com/assets/cores/Nintendo%20-%20Nintendo%20Entertainment%20System/Project%20DART%20%28v1.0%29.nes", "在无尽之路上的高速街机动作游戏。"),
    ("witch-n-wiz", "Witch n' Wiz", "解谜", "Matt Hughson", "2017", "https://archive.org/download/witch-n-wiz-usa-europe_202505/Witch%20n'%20Wiz%20%28USA%2C%20Europe%29.nes", "女巫与她的巫师伙伴合作的推箱子解谜冒险。"),
    ("slow-mole", "Slow Mole", "解谜", "KHAN Games", "2021", "https://archive.org/download/slow-mole-/Slow_Mole_PD_2021.nes", "引导慢吞吞的鼹鼠穿过迷宫般的解谜关卡，公有领域作品。"),
    ("aethos-beginnings", "Aethos Beginnings", "类银河战士", "RetroBroGaming", "2024", "https://archive.org/download/aethos-beginnings/AethosVER1.1.nes", "科幻类银河战士恶魔城试玩版，随 AI 探险家 Kyra 探索 Aethos 星。"),
    ("cheril-the-goddess", "Cheril the Goddess", "平台跳跃", "Mojon Twins", "2016", "https://archive.org/download/mojon-twins--cheril-the-writer/mojon-twins--cheril-the-goddess.nes", "Mojon Twins NESdev Compo 2016 参赛平台跳跃游戏。"),
    ("cheril-the-writer", "Cheril the Writer", "动作冒险", "Mojon Twins", "2018", "https://archive.org/download/mojon-twins--cheril-the-writer/mojon-twins--cheril-the-writer.nes", "Cheril 前往 Pepinoni 撰写小说的动作冒险游戏。"),
    ("cheril-perils-classic", "Cheril Perils Classic", "平台跳跃", "Mojon Twins", "2018", "https://archive.org/download/NES-CherilPerilsClassic/mojon-twins--cheril-perils-classic.nes", "经典风格的 Cheril 平台跳跃冒险。"),
    ("lala-the-magical", "Lala the Magical", "射击", "Mojon Twins", "2016", "https://archive.org/download/NES-LalaTheMagical/mojon-twins--lala-the-magical-%28gnrom%29.nes", "魔法少女题材的射击游戏。"),
    ("cadaverion", "Cadaverion", "动作冒险", "Mojon Twins", "2018", "https://archive.org/download/NES-Cadaverion/mojon-twins--cadaverion.nes", "带点恐怖氛围的动作冒险游戏。"),
    ("bootee", "Bootee", "解谜", "Mojon Twins", "2018", "https://archive.org/download/NES-Bootee/mojon-twins--bootee.nes", "用靴子踢东西解谜的趣味益智游戏。"),
    ("yun", "Yun", "平台跳跃", "Mojon Twins", "2016", "https://archive.org/download/NES-Yun/mojon-twins--yun.nes", "复古重制风格的平台跳跃游戏。"),
    ("journey-center-alien", "Journey to the Center of the Alien", "冒险", "Mojon Twins", "2019", "https://archive.org/download/NES-JourneyCenterAlien/mojon-twins--journey-gnrom-EN.nes", "探索异星地心的冒险游戏。"),
    ("chrono-knight", "Chrono Knight", "动作", "Artix", "2020", "https://archive.org/download/action-53-volume-4homebrews-and-extras.-7z/Chrono_Knight_PD_2020.nes", "时间主题动作游戏，Action 53 Vol.4 公有领域合集。"),
    ("f-theta", "F-Theta", "竞速", "LITTLE SOUND SOFT", "2021", "https://archive.org/download/action-53-volume-4homebrews-and-extras.-7z/F-_952__F-Theta__PD_2021.nes", "日本 homebrew 竞速游戏，旋转赛道、天气与车灯效果。"),
    ("mine-mayhem", "Mine Mayhem", "动作", "FG Soft", "2021", "https://archive.org/download/action-53-volume-4homebrews-and-extras.-7z/Mine_Mayhem_PD_2021.nes", "Ludum Dare 48 采矿主题街机动作游戏。"),
    ("utaco", "Utaco", "音乐节奏", "Zurashu", "2015", "https://archive.org/download/action-53-volume-4homebrews-and-extras.-7z/Utaco_PD_2015.nes", "日本 homebrew 音乐节奏游戏。"),
    ("zdey-the-game", "Zdey the Game", "平台跳跃", "Art'Cade", "2021", "https://archive.org/download/action-53-volume-4homebrews-and-extras.-7z/Zdey_the_Game_PD_2021.nes", "Action 53 Vol.4 公有领域合集中的平台跳跃游戏。"),
]

os.makedirs("roms", exist_ok=True)
meta = []
ok = 0
for gid, name, genre, author, year, url, desc in GAMES:
    fn = f"roms/{gid}.nes"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as r, open(fn, "wb") as f:
            data = r.read()
            f.write(data)
        with open(fn, "rb") as f:
            magic = f.read(4)
        size = os.path.getsize(fn)
        valid = magic == b"NES\x1a" and 16*1024 <= size <= 1024*1024
        print(("OK " if valid else "BAD ") + f"{name} ({size} bytes)")
        if valid:
            ok += 1
            meta.append({"id": gid, "name": name, "file": f"{gid}.nes", "genre": genre, "author": author, "year": year, "desc": desc})
        else:
            os.remove(fn)
    except Exception as e:
        print(f"FAIL {name}: {e}")

with open("games.json", "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False, indent=1)
print(f"\n{ok}/{len(GAMES)} 下载验证通过")

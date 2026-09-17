import dataclasses
import pathlib
import shutil
import subprocess
import typing
from urllib import request


@dataclasses.dataclass
class Story:
    name: str
    description: str
    files: list[str | tuple[str, str]]


@dataclasses.dataclass
class Chapter:
    name: str
    description: str
    stories: list[Story]


def _chapter_starting():
    return Chapter(
        name='Prologue',
        # description='首次进入游戏自动播放',
        description='',
        stories=[
            Story(name=f'Section {i + 1}', description='',
                  files=[f'startavg/start{i}.txt'])
            for i in range(11 + 1)
        ],
    )


def _extra_stories_va11():
    return [
        (
            'Didgeridoo Manual',
            '',
            [
                ('-32-1-1.txt', 'Part 1'),
                ('battleavg/-32-specialbattletips-fly.txt', 'Minigame tips 1'),
                ('battleavg/-32-specialbattletips-spdup.txt', 'Minigame tips 2'),
                ('-32-1-2first.txt', 'Part 2'),
                ('va11/va11_1.txt', 'Bartender Story'),
            ],
        ),
        (
            'Puberty',
            '',
            [
                ('-32-2-1.txt', 'Part 1'),
                ('-32-ext-2-1-point94524.txt', 'Point Event'),
                ('-32-10-4-point12875.txt', 'Point Event'),
                ('-32-2-2first.txt', 'Part 2'),
                ('va11/va11_2.txt', 'Bartender Story'),
            ],
        ),
        (
            'Pioneer',
            '',
            [
                ('-32-3-1.txt', 'Part 1'),
                ('-32-3-2first.txt', 'Part 2'),
                ('va11/va11_3.txt', 'Bartender Story'),
            ],
        ),
        (
            'Sonic Boom',
            '',
            [
                ('-32-4-1.txt', 'Part 1'),
                ('-32-ext-4-1.txt', 'Points Event'),
                ('-32-12-4-point12932.txt', 'Point Event'),
                ('-32-4-2first.txt', 'Part 2'),
                ('va11/va11_4.txt', 'Bartender Story'),
            ],
        ),
        (
            'Chicken Breast',
            '',
            [
                ('-32-5-1.txt', 'Part 1'),
                ('-32-13-4-point12945.txt', 'Point Event'),
                ('-32-5-2first.txt', 'Part 2'),
                ('va11/va11_5.txt', 'Bartender Story'),
            ],
        ),
        (
            'Glossophobia',
            '',
            [
                ('-32-6-1.txt', 'Part 1'),
                ('-32-ext-6-1.txt', 'Point Event'),
                ('-32-6-2first.txt', 'Part 2'),
                ('va11/va11_6.txt', 'Bartender Story'),
            ],
        ),
        (
            'Truth or Dare',
            '',
            [
                ('-32-7-1.txt', 'Part 1'),
                ('-32-15-4-point13027.txt', 'Point Event'),
                ('-32-7-2first.txt', 'Part 2'),
                ('va11/va11_7.txt', 'Bartender Story'),
            ],
        ),
        (
            'Last Rain in the World',
            '',
            [
                ('-32-8-1.txt', 'Part 1'),
                ('-32-16-4-point13052.txt', 'Point Event'),
                ('-32-8-4-point12833.txt', 'Point Event'),
                ('-32-8-2first.txt', 'Part 2'),
                ('-32-8-2end.txt', 'Part 3'),
                ('va11/va11_8.txt', 'Bartender Story'),
            ],
        ),
    ]


def _extra_stories_cocoon():
    return [
        ('Cold, Endless Night', '', ['-42-1-1first.txt']),
        ('Discourse in the Rain', '', ['-42-1-2.txt']),
        ('Reflection', '', ['-42-2-1first.txt']),
        ('Reminiscence', '', ['-42-2-2.txt']),
        ('The Nameless', '', [
            ('-42-3-1first.txt', 'Storyline'),
            ('-42-3-2.txt', 'Broken Echoes 1'),
            ('-42-3-3.txt', 'Broken Echoes 2'),
            ('-42-3-4.txt', 'Broken Echoes 3'),
            ('-42-3-5.txt', 'Broken Echoes 4'),
            ('-42-3-6.txt', 'Broken Echoes 5'),
            ('-42-3-7.txt', 'Broken Echoes 6'),
        ]),
        ('Trackless Tears', '', ['-42-3-8.txt']),
        ('Evanescent Butterfly', '', ['-42-4-1first.txt']),
        ('Breaking the Cocoon', '', ['-42-4-2.txt']),
    ]


def _extra_stories_sac2045():
    return [
        ('Stranger\'s Boon', '', ['-64-1-0.txt']),
        ('Beneath the Chestnut Tree', '', ['-64-2-0.txt']),
        ('Morning, New World', '', ['-64-3-0.txt']),
        ('Potato\'s Legend', '', ['-64-3-1.txt']),
        ('Internet Rehab', '', ['-64-3-2.txt']),
        ('Earl Grey Grin', '', ['-64-3-3.txt']),
        ('Grape Juice', '', ['-64-3-4.txt']),
        ('Sakura Flowers and You', '', ['-64-4-0.txt']),
        ('Major\'s Request', '', ['-64-5-1.txt']),
        ('A Free Prisoner', '', ['-64-5-2.txt']),
        ('To Retrace Steps', '', ['-64-6-0.txt']),
        ('Botched Ascension', '', ['-64-6-1.txt']),
        ('Best Wishes', '', ['-64-7-1.txt']),
        ('Hidden Behind the Photograph', '', ['-64-7-2.txt']),
        ('Furor', '', ['-64-8-1.txt']),
        ('Ghost in the Channel', '', ['-64-8-2.txt']),
        ('Crying Pudding', '', ['-64-9-1.txt']),
        ('A War Just For Me', '', ['-64-9-2.txt']),
        ('Sundown at World\'s End', '', ['-64-10-0.txt']),
    ]


def _extra_stories_gunslinger():
    return [
        ('No. 9', '', ['-38-0-1.txt']),
        ('Kaleidoscope', '', ['-38-1-1.txt']),
        ('New Fork', '', ['-38-2-1.txt', '-38-2-2first.txt', '-38-2-2round.txt', '-38-2-2end.txt']),
        ('Twilight Stars', '', ['-38-2-3.txt']),
        ('Full-Length PlayⅠ', '', ['-38-3-1.txt']),
        ('Full-Length PlayⅡ', '', ['-38-3-1first.txt', '-38-3-2round.txt', '-38-3-2end.txt']),
        ('Magic of Happiness', '', ['-38-3-3.txt']),
        ('Agency Shooting Range', '', ['battleavg/-38-specialbattletips.txt']),
        ('Honest PinocchioⅠ', '', ['-38-4-1first.txt', '-38-4-1round.txt']),
        ('Honest PinocchioⅡ', '', ['-38-4-1end.txt']),
        ('Garden of OldⅠ', '', ['-38-5-1first.txt', '-38-5-1round.txt']),
        ('Garden of OldⅡ', '', ['-38-5-1end.txt']),
        ('Hai capito', '', ['-38-6-1first.txt', '-38-6-1round.txt', '-38-6-1end.txt']),
        ('Perfect Harmony', '', ['-38-7-1.txt']),
    ]


_extra_chapters: list[tuple[str, str, str, list]] = [
    ('-42', 'Butterfly in a Cocoon', '2020', _extra_stories_cocoon()),
    ('-50', 'Love Bakery', '2022', []),
    ('-52', 'Lycan Sanctuary', '2022', []),

    ('-8', 'Operation Rabbit Hunt', 'BlazBlue x Guilty Gear collab', []),
    ('-14,-15', 'Only Master', 'Guns Girl Z collab', []),
    ('-19,-20,-22', 'Glory Day', 'DJMAX RESPECT collab', []),
    ('-32', 'Valhalla', 'VA-11 HALL-A collab', _extra_stories_va11()),
    ('-38', 'Dream Theater', 'Gunslinger Girl collab', _extra_stories_gunslinger()),
    ('-43', 'Bounty Feast', 'The Division collab', []),
    ('-46', 'My Devil\'s Frontline', 'Jashin-chan Dropkick collab', []),
    ('-57', 'The Glistening Bloom', 'Zombie Land Saga collab', []),
    ('-64', 'Through the Looking-Glass', 'Ghost in the Shell: SAC_2045 collab', _extra_stories_sac2045()),
    ('-73', 'Lorenz Butterfly', 'Arena Breakout collab', []),
]


def _get_extra_chapters():
    return dict(
        (
            (i + 5000),
            Chapter(name, description,
                    [Story(s[0], s[1], s[2]) for s in stories]),
        )
        for i, (_, name, description, stories) in enumerate(_extra_chapters)
    )


def _get_extra_chapter_mapping():
    mapping: dict[str, int] = {}
    for i, chapter in enumerate(_extra_chapters):
        for j in chapter[0].split(','):
            mapping[j] = i + 5000
    return mapping


def get_recorded_chapters():
    chapters: dict[int, Chapter] = {
        0: _chapter_starting(),
    }
    id_mapping: dict[str, int] = {'0': 0}

    chapters.update(_get_extra_chapters())
    id_mapping.update(_get_extra_chapter_mapping())

    recorded_files: set[str] = set()
    for chapter in chapters.values():
        for story in chapter.stories:
            recorded_files.update((f if isinstance(f, str) else f[0])
                                  for f in story.files)
    return chapters, id_mapping, recorded_files

_attached_stories_motor_race = [
    '-31-3c3-1.txt',
    'battleavg/-31-specialbattletips-1.txt',
    'battleavg/-31-specialbattletips-3.txt',
    'battleavg/-31-specialbattletips-4.txt',
    'battleavg/-31-specialbattletips-5.txt',
    'battleavg/-31-specialbattletips-6.txt',
    'battleavg/-31-specialbattletips-fly.txt',
    'battleavg/-31-specialbattletips-spdup.txt',
    'battleavg/-31-specialbattletips-lose.txt',
    'battleavg/-31-specialbattletips-victory.txt',
]
_attached_stories: list[tuple[str, str, str]] = [
    ('0-2-1.txt', '0-2-3round2.txt'),
    # This is just a copy of the last few lines of -2-1-1
    #('-2-1-1.txt', '-2-1-4-point2207.txt'),

    # 焙炒爱意，白色庆典位点剧情
    ('-50-1-4.txt', '-50-3-1.txt', 'Wrong chocolate'),
    ('-50-3-1.txt', '-50-3-2.txt', 'Lewis'),
    ('-50-3-2.txt', '-50-3-3.txt', 'Falcon'),
    ('-50-3-3.txt', '-50-3-4.txt', 'Type 79'),
    ('-50-3-4.txt', '-50-3-5.txt', 'Type 97'),
    ('-50-3-5.txt', '-50-3-6.txt', 'Hunter'),
    ('-50-3-6.txt', '-50-3-7.txt', 'LWMMG'),
    ('-50-3-7.txt', '-50-3-8.txt', 'K5'),
    ('-50-3-8.txt', '-50-3-9.txt', 'M1 Garand'),
    ('-50-3-9.txt', '-50-3-10.txt', 'P22'),
    ('-50-3-10.txt', '-50-3-11.txt', 'T77'),
    ('-50-3-11.txt', '-50-3-12.txt', 'Persica'),
    # 焙炒爱意，小怪
    ('-50-1-4.txt', '-50-ext-1-4-1.txt', 'Dessert Dinergate'),
    ('-50-ext-1-4-1.txt', '-50-ext-1-4-2.txt', 'Dessert Cerberus'),
    ('-50-ext-1-4-2.txt', '-50-ext-1-4-3.txt', 'Calorie Bomb（Chocolate）'),
    ('-50-ext-1-4-3.txt', '-50-ext-1-4-4.txt', 'Calorie Bomb（Chocthulhu）'),
    ('-50-ext-1-4-4.txt', '-50-ext-1-4-5.txt', 'Cacao New World'),
    ('-50-ext-1-4-5.txt', '-50-ext-1-4-6.txt', 'Chocthulhu'),
    # 焙炒爱意，巧克力制作
    ('-50-1-3.txt', '-50-ext-1-3-2.txt', 'Sheet of recipes'),
    ('-50-ext-1-3-2.txt', '-50-ext-1-3.txt', 'Recipe？'),
    ('-50-ext-1-3.txt', '-50-ext-0-1.txt', 'House of Mint'),
    ('-50-ext-0-1.txt', '-50-ext-0-2.txt', 'Sweet Saber'),
    ('-50-ext-0-2.txt', '-50-ext-0-3.txt', 'Kiss of Destiny'),
    ('-50-ext-0-3.txt', '-50-ext-0-4.txt', 'Chocolate Duet'),
    ('-50-ext-0-4.txt', '-50-ext-0-5.txt', 'Classic Memory'),
    ('-50-ext-0-5.txt', '-50-ext-0-6.txt', 'Cacao New World'),
    ('-50-ext-0-6.txt', '-50-ext-0-7.txt', 'Chocthulhu'),

    # 里坎禁猎区
    ('-52-1-1.txt', 'battleavg/-52-dxg.txt', 'Watermelon Game Rules'),

    # 盲拆法则：感觉应该是第二周目的变化？
    ('-7-1-3round1.txt', '-7-1-3round2.txt', 'Stage 2.5'),
    ('-7-2-3round1.txt', '-7-2-3round2.txt', 'Stage 2.5'),
    ('-7-3-3round1.txt', '-7-3-3round2.txt', 'Stage 2.5'),
    ('-7-4-3round1.txt', '-7-4-3round2.txt', 'Stage 2.5'),

    # 有序紊流
    ('-24-2-1.txt', '-24-2-2.txt'),
    ('-24-3-2first.txt', '-24-3-2.txt'),
    ('-24-4-2first.txt', '-24-4-2.txt'),
    ('-24-6-1.txt', '-24-6-2.txt'),
    ('-24-7-2first.txt', '-24-7-2.txt'),
    ('-24-8-2first.txt', '-24-8-2.txt'),
    ('-24-9-2first.txt', '-24-9-2.txt'),
    ('-24-10-2first.txt', '-24-10-2.txt'),
    ('-24-11-2first.txt', '-24-11-2.txt'),
    ('-24-12-2first.txt', '-24-12-2.txt'),
    ('-24-13-2first.txt', '-24-13-2.txt'),
    ('-24-14-2first.txt', '-24-14-2.txt'),
    ('-24-15-1.txt', '-24-15-2first.txt'),
    ('-24-15-2first.txt', '-24-15-2.txt'),

    # 裂变链接
    # ('-33-59-4-point13290.txt', '-33-59-4-point80174.txt'), # 两个点位事件一样
    ('-33-59-4-point13290.txt', 'battleavg/-33-24-1first.txt'),

    # 偏振光
    ('-36-5-ex.txt', 'battleavg/-36-specialbattletips.txt'),
] + [ # 异构体飙车小游戏局内剧情
    (prev, after)
    for prev, after in zip(
        _attached_stories_motor_race[:-1],
        _attached_stories_motor_race[1:],
    )
]
_attached_events: list[tuple[str, Story]] = [
    # 裂变链接：吞噬一切的花海-战斗
    ('-33-42-1first.txt', Story(
        name='All-Devouring Sea of Flowers - Battle',
        description='Combat Tutorial',
        files=['battleavg/-33-44-1first.txt'],
    )),
    # 愚人节
    ('1-1-1.txt', Story(
        name='Drill - April Fools',
        description='Welcome back, Father.',
        files=['always-404-1-1-1.txt', 'battleavg/always-404-1-1-2.txt', 'always-404-1-1-3.txt'],
    )),
    # 雪浪映花颜
    ('-57-0-1.txt', Story(
        name='Day 1 – Morning',
        description='',
        files=[
            ('-57-a1-1.txt', 'Dance Studio - Head Up, Back Straight, Hip Turned'),
            ('-57-c1-1.txt', 'Karaoke Box - Do-Re-Mi'),
            ('-57-w1-1.txt', 'Bathhouse - Glup, Glup'),
            ('-57-x1-1.txt', 'Fast Food Restaurant - Hiss, Sizzle, Whoosh'),
            ('-57-d1-1.txt', 'Convenience Store - Welcome!'),
        ],
    )),
    ('-57-1-1.txt', Story(
        name='Day 1 - Night',
        description='',
        files=[
            ('-57-w1-2.txt', 'Dance Studio - Head Up, Back Straight, Hip Turned'),
            ('-57-x1-2.txt', 'Karaoke Box - Do-Re-Mi'),
            ('-57-a1-2.txt', 'Bathhouse - Glup, Glup'),
            ('-57-d1-2.txt', 'Fast Food Restaurant - Hiss, Sizzle, Whoosh'),
            ('-57-l1-2.txt', 'Convenience Store - Welcome!'),
        ],
    )),
    ('-57-1-2.txt', Story(
        name='Day 2 - Morning',
        description='',
        files=[
            ('-57-x2-1.txt', 'Dance Studio - Head Up, Back Straight, Hip Turned'),
            ('-57-y2-1.txt', 'Karaoke Box - Do-Re-Mi'),
            ('-57-c2-1.txt', 'Bathhouse - Glup, Glup'),
            ('-57-l2-1.txt', 'Fast Food Restaurant - Hiss, Sizzle, Whoosh'),
            ('-57-d2-1.txt', 'Convenience Store - Welcome!'),
        ],
    )),
    ('-57-2-1.txt', Story(
        name='Day 2 - Night',
        description='',
        files=[
            ('-57-l2-2.txt', 'Dance Studio - Head Up, Back Straight, Hip Turned'),
            ('-57-c2-2.txt', 'Karaoke Box - Do-Re-Mi'),
            ('-57-w2-2.txt', 'Bathhouse - Glup, Glup'),
            ('-57-x2-2.txt', 'Fast Food Restaurant - Hiss, Sizzle, Whoosh'),
            ('-57-y2-2.txt', 'Convenience Store - Welcome!'),
        ],
    )),
    ('-57-2-2.txt', Story(
        name='Day 3 - Morning',
        description='',
        files=[
            ('-57-l3-1.txt', 'Dance Studio - Head Up, Back Straight, Hip Turned'),
            ('-57-y3-1.txt', 'Karaoke Box - Do-Re-Mi'),
            ('-57-w3-1.txt', 'Bathhouse - Glup, Glup'),
            ('-57-x3-1.txt', 'Fast Food Restaurant - Hiss, Sizzle, Whoosh'),
            ('-57-d3-1.txt', 'Convenience Store - Welcome!'),
        ],
    )),
    ('-57-3-1.txt', Story(
        name='Day 3 - Night',
        description='',
        files=[
            ('-57-3-point1.txt', 'Karaoke Box - Do-Re-Mi'),
            ('-57-3-point2.txt', 'Fast Food Restaurant - Hiss, Sizzle, Whoosh'),
        ],
    )),
    ('-57-3-2.txt', Story(
        name='Day 4 - Morning',
        description='',
        files=[
            ('-57-a4-1.txt', 'Dance Studio - Head Up, Back Straight, Hip Turned'),
            ('-57-c4-1.txt', 'Karaoke Box - Do-Re-Mi'),
            ('-57-y4-1.txt', 'Convenience Store - Welcome!'),
        ],
    )),
    ('-57-4-1.txt', Story(
        name='Day 4 - Night',
        description='',
        files=[
            ('-57-l4-2.txt', 'Dance Studio - Head Up, Back Straight, Hip Turned'),
            ('-57-y4-2.txt', 'Karaoke Box - Do-Re-Mi'),
            ('-57-a4-2.txt', 'Bathhouse - Glup, Glup'),
            ('-57-x4-2.txt', 'Fast Food Restaurant - Hiss, Sizzle, Whoosh'),
            ('-57-d4-2.txt', 'Convenience Store - Welcome!'),
        ],
    )),
    ('-57-4-2.txt', Story(
        name='Day 5 - Morning',
        description='',
        files=[
            ('-57-l5-1.txt', 'Dance Studio - Head Up, Back Straight, Hip Turned'),
            ('-57-a5-1.txt', 'Karaoke Box - Do-Re-Mi'),
            ('-57-w5-1.txt', 'Bathhouse - Glup, Glup'),
            ('-57-x5-1.txt', 'Fast Food Restaurant - Hiss, Sizzle, Whoosh'),
            ('-57-d5-1.txt', 'Convenience Store - Welcome!'),
        ],
    )),
    ('-57-5-1.txt', Story(
        name='Day 5 - Night',
        description='',
        files=[
            ('-57-w5-2.txt', 'Dance Studio - Head Up, Back Straight, Hip Turned'),
            ('-57-d5-2.txt', 'Karaoke Box - Do-Re-Mi'),
            ('-57-x5-2.txt', 'Bathhouse - Glup, Glup'),
            ('-57-l5-2.txt', 'Fast Food Restaurant - Hiss, Sizzle, Whoosh'),
            ('-57-c5-2.txt', 'Convenience Store - Welcome!'),
        ],
    )),
    ('-57-5-2.txt', Story(
        name='Day 6 - Morning',
        description='',
        files=[
            ('-57-a6-1.txt', 'Dance Studio - Head Up, Back Straight, Hip Turned'),
            ('-57-c6-1.txt', 'Karaoke Box - Do-Re-Mi'),
            ('-57-w6-1.txt', 'Bathhouse - Glup, Glup'),
            ('-57-x6-1.txt', 'Fast Food Restaurant - Hiss, Sizzle, Whoosh'),
            ('-57-d6-1.txt', 'Convenience Store - Welcome!'),
        ],
    )),
    ('-57-6-1.txt', Story(
        name='Day 6 - Night',
        description='',
        files=[
            ('-57-6-point1.txt', 'Dance Studio - Head Up, Back Straight, Hip Turned'),
            ('-57-6-point2.txt', 'Convenience Store - Welcome!'),
        ],
    )),
    ('-57-6-2.txt', Story(
        name='Day 7 - Morning',
        description='',
        files=[
            ('-57-a7-1.txt', 'Dance Studio - Head Up, Back Straight, Hip Turned'),
            ('-57-l7-1.txt', 'Karaoke Box - Do-Re-Mi'),
            ('-57-d7-1.txt', 'Bathhouse - Glup, Glup'),
            ('-57-w7-1.txt', 'Fast Food Restaurant - Hiss, Sizzle, Whoosh'),
            ('-57-y7-1.txt', 'Convenience Store - Welcome!'),
        ],
    )),
]


_extra_chapter_mapping = {
    '-27': '-24',  # 有序紊流：飓风营救
    '-45': '-24',  # 飓风营救复刻
    '-99': '-58',  # 慢休克 END
}


def add_extra_chapter_mappings(id_mapping: dict[str, int]):
    for extra, mapping in _extra_chapter_mapping.items():
        id_mapping[extra] = id_mapping[mapping]

_manual_processed = set().union(
)
def is_manual_processed(file: str):
    return file in _manual_processed
def manually_process(chapters: dict[int, Chapter], id_mapping: dict[str, int], mapped_files: set[str]):
    # 佐贺
    c = chapters[id_mapping['-57']]
    specials = {
        'Sakura Minamoto': ['Keep Clear!', 'Precious Treasure', 'Heart of the Cherry Blossom'],
        'Saki Nikaido': ['Rampaging Radio Show!', 'Rampaging Memories!', 'Rampage at the Graduation Ceremony'],
        'Ai Mizuno': ['Pavilion in the Rain', 'Moonlit Ocean', 'Dazzling Love'],
        'Junko Konno': ['Strangers in a Foreign Land', 'When Did the Moon Start Shining?', 'Drifting Apart in the Haze'],
        'Yugiri': ['Traveler in Time', 'Sound of the Sea', 'Until the Sun Goes Down'],
        'Lily Hoshikawa': ['Perfect Strangers', 'Top Secret Agent', 'The Remains of the Day'],
        'Tae Yamada': ['Night-Time Fantasia', 'Gift Giver', '"Please Don\'t Go"'],
    }
    endings = [
        'A Night of Laughter and Tears',
        'A Night of Neon Colors',
        'A Night of Rising Wind',
        'A Night of Grayish White',
        'A Loose Backdrop',
        'Don\'t Let the Music Stop, Dance Till You Drop',
        'The Distance from Shoulder to Shoulder',
        'Do Your Best, Part-Timer!',
        'Rush! To the Top!',
        'Springing Forth!',
    ]
    files: dict[str, str] = {}
    names = set(n for ns in specials.values() for n in ns)
    for s in c.stories:
        if s.name in names:
            assert len(s.files) == 1
            file = s.files[0]
            assert isinstance(file, str)
            files[s.name] = file
    c.stories = [s for s in c.stories if s.name not in names]
    for s in c.stories:
        if s.name in endings:
            s.description = f'Ending {endings.index(s.name) + 1}'
    for character, stories in specials.items():
        c.stories.append(Story(
            name=character,
            description='Storyline',
            files=[(files[name], name) for name in stories],
        ))


def manual_naming(story: Story, campaign: int):
    if campaign == -43:  # 暗金潮命名有问题
        story.name, story.description = story.description, story.name
        if story.description == 'Breaking the Cocoon':  # 这个是 -42 茧中蝶影的介绍，应该是复制错了
            story.description = ''
    if campaign == -38:  # 梦间剧，有问题
        story.name = story.description
        story.description = ''


# Add the difficulty to the description of the main story chapters
def chapter_difficulty(id: int, description: str):
    normal_chapters = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 19, 20, 21, 22, 23, 24,
                       33, 34, 35, 36, 37, 38, 47, 48, 49, 50, 51, 52, 57, 58,
                       59, 60, 61, 62, 67,68, 69, 70, 71, 72, 81, 82, 83, 84, 85,
                       86, 116, 117, 118, 119, 120, 121, 130, 131, 132, 133, 134,
                       135, 140, 141, 142, 143, 144, 145, 170, 171, 172, 173, 174,
                       175, 458, 459, 460, 461, 462, 463, 535, 536, 537, 538, 539, 540]
    emergency_chapters = [11, 12, 13, 14, 25, 26, 27, 28, 39, 40, 41, 42, 53, 54, 55, 56,
                          63, 64, 65, 66, 73, 74, 75, 76, 87, 88, 89, 90, 122, 123, 124,
                          125, 136, 137, 138, 139, 146, 147, 148, 149, 176, 177, 178, 179,
                          464, 465, 466, 467, 541, 542, 543, 544]
    night_chapters = [15, 16, 17, 18, 29, 30, 31, 32, 43, 44, 45, 46, 77, 78, 79, 80,
                      91, 92, 93, 94, 126, 127, 128, 129, 162, 163, 164, 165, 166, 167,
                      168, 169, 361, 362, 363, 364, 450, 451, 452, 453]
    if id in normal_chapters:
        return 'Normal'
    elif id in emergency_chapters:
        return 'Emergency'
    elif id in night_chapters:
        return 'Night Battle'
    else:
        return description


def _index_of_file(story: Story, file: str):
    for i, f in enumerate(story.files):
        if isinstance(f, str):
            if f == file:
                return i
        else:
            if f[0] == file:
                return i
    raise ValueError(f'{file} not found in {story}')


def post_insert(chapters: dict[int, Chapter], mapped_files: set[str]):
    stories: dict[str, tuple[Chapter, Story]] = {}
    for chapter in chapters.values():
        for story in chapter.stories:
            for file in story.files:
                stories[file if isinstance(file, str) else file[0]] = (chapter, story)
    for attachment in _attached_stories:
        file, attached = attachment[0:2]
        assert attached not in mapped_files, attached
        c, story = stories[file]
        assert isinstance(story.files[0], str)
        stories[attached] = (c, story)
        story.files.insert(
            _index_of_file(story, file) + 1,
            attached if len(attachment) == 2 else (attached, attachment[2]),
        )
        mapped_files.add(attached)
    for file, attached in _attached_events:
        assert all(
            f not in mapped_files and f[0] not in mapped_files for f in attached.files
        ), [f for f in attached.files if f in mapped_files or f[0] in mapped_files]
        c, story = stories[file]
        c.stories.insert(c.stories.index(story) + 1, attached)
        for f in attached.files:
            if not isinstance(f, str):
                f = f[0]
            stories[f] = (c, attached)
            mapped_files.add(f)


def get_block_list():
    return set(
        [
            '0-0-0.txt',  # 空白，“替代剧情”
            '0-0-1.txt',  # 空白，“替代教程”
            'profiles.txt',
            'avgplaybackprofiles.txt',

            # 魔方行动，例如 -6-1-1 和 -1-1-1 的内容是一模一样的……
            '-6-1-1.txt',
            '-6-1-2first.txt',
            '-6-2-1.txt',
            '-6-2-2end.txt',
            '-6-2-2first.txt',
            '-6-3-1.txt',
            '-6-3-2end.txt',
            '-6-3-2first.txt',
            '-6-4-1.txt',
            '-6-4-2end.txt',
            '-6-4-2first.txt',

            # 裂变链接，两个点位事件内容是一样的
            '-33-59-4-point80174.txt',

            # 各种秃洞复刻提示
            '-39-ex1-4-point91502.txt',
            '-55-ext.txt',
            '-60-tips.txt',
            '-63-tips.txt',
            '-65-tips.txt',
            '-65-tips2.txt',
            '-404-ext-1-1.txt',
            # 飓风营救复刻 (-45 -> -24)
            '-45-ext-04.txt',
            '-45-ext-01.txt',
            '-45-ext-02.txt',
            '-45-ext-03.txt',

            # 盲拆法则：这些是英文版
            '-7-1-4-point3498.txt',
            '-7-2-4-point3342.txt',
            '-7-3-4-point3533.txt',
            '-7-4-4-point3612.txt',

            # 神枪少女联动，玩法说明而已
            '-38-ex-point91820.txt',
            '-38-ex-point91829.txt',
            '-38-ex1-5-point91849.txt',
            '-38-ex1-2-point91865.txt',
            '-38-2-4first.txt', # 和 '-38-2-1.txt', '-38-2-2first.txt' 重复，用了修了错别字的版本

            # 一币之遥，游戏提示
            '-49-3-1-point94780.txt',
            '-49-ext-1-1.txt',
            '-49-ext-4-1.txt',

            # 捩浪人，游戏提示
            '-47-2-skill-1.txt',
            '-47-2-skill-2.txt',
            '-47-2-skill-3.txt',

            # 焙炒爱意，“文本待替换”
            '-50-ext-0.txt',
            '-50-ext-1-4-0.txt',

            # 里坎禁猎区，小游戏提示文本
            '-52-ext-2-1.txt',
            '-52-ext-3-1.txt',
            '-52-ext-4-1.txt',
            '-52-ext-5-1.txt',
            '-52-ext-5-2.txt',
            '-52-ext-5-3.txt',
            '-52-pachinko0.txt',
            '-52-pachinko1.txt',
            '-52-pachinko2.txt',
            '-52-pachinko3.txt',
            '-52-pachinko4.txt',
            '-52-pachinko5.txt',
            '-52-pachinko6.txt',
            '-52-pachinko7.txt',
            '-52-pachinko8.txt',
            '-52-pachinko9.txt',
            '-52-pachinkornd2.txt',

            # 许可！二次加载
            '-62-sangvis-tutorial-4kill.txt',
            '-62-sangvis-tutorial-8kill.txt',
            '-62-sangvis-tutorial-missionstart.txt',

            # 佐贺联动
            '-57-ext-5.txt',
            '-57-ext-6.txt',
            '-57-ext-7-00.txt',
            '-57-ext-7-01.txt',
            '-57-ext-7-11.txt',
            '-57-ext-7-12.txt',
            '-57-ext-7-13.txt',
            '-57-ext-7-14.txt',
            '-57-ext-7-15.txt',
            '-57-ext-7-16.txt',
            '-57-ext-7-17.txt',
            '-57-ext-7-24.txt',
            '-57-ext-7-26.txt',
            '-57-ext-7-27.txt',
            '-57-ext-7-36.txt',
            '-57-ext-7-41.txt',
            '-57-ext-7-42.txt',
            '-57-ext-7-43.txt',
            '-57-ext-7-44.txt',
            '-57-ext-7-45.txt',
            '-57-ext-7-46.txt',
            '-57-ext-7-47.txt',
            '-57-ext-7-48.txt',
            '-57-ext-7-51.txt',
            '-57-ext-7-54.txt',
            '-57-ext-7-57.txt',
            '-57-ext-7-61.txt',
            '-57-ext-7-62.txt',
            '-57-ext-7-63.txt',
            '-57-ext-7-64.txt',
            '-57-ext-7-65.txt',
            '-57-ext-7-66.txt',
            '-57-ext-7-67.txt',
            '-57-ext-7-68.txt',
            '-57-ext-7-71.txt',
            '-57-ext-7-74.txt',
            '-57-ext-7-77.txt',
            '-57-ext-7-78.txt',
            '-57-ext-7-81.txt',
            '-57-ext-7-82.txt',
            '-57-ext-7-83.txt',
            '-57-ext-7-84.txt',
            'battleavg/-57-dance.txt',
            'battleavg/-57-sing.txt',
            'battleavg/-57-work.txt',

            # SAC 2045
            '-64-ext-1.txt',
            '-64-ext-2.txt',
            '-64-ext-3.txt',

            # 22重困境
            '-69-ext-1.txt',

            # 双联乱数
            '-41-3-4-point71201.txt',
            '-41-3-4-point71305.txt',
            '-41-3-4-point72006.txt',
            '-41-2-4-ex1point91924.txt',
            '-41-2-4-ex1point91926.txt',
            '-41-2-4-ex2point92278.txt',
            '-41-2-4-ex3point92127.txt',
            '-41-2-4-ex4point92161.txt',
            '-41-2-4-ex5point92614.txt',
            '-41-2-4-ex6point92372.txt',
            '-41-3-4-ex1point91991.txt',
            '-41-3-4-ex2point91990.txt',
            '-41-3-4-ex3point92264.txt',
            '-41-3-4-ex4point92396.txt',
            '-41-3-4-ex5point92254.txt',
            '-41-3-4-ex6point92335.txt',

            # DJMAX collab
            '-19-1-2.txt', # Same as -19-1-2first.txt
            '-19-2-2.txt',
        ]
    )


def get_extra_stories(destination: pathlib.Path):
    downloadables = [
        # (
        #     'https://gcore.jsdelivr.net/gh/gf-data-tools/gf-data-ch@42b067b833a5e10a8f9cedf198fe182f1df122f1/asset/avgtxt/-52-e-1.txt',
        #     '-52-e-1-springfield.txt',
        # ),
    ]
    for url, file in downloadables:
        path = destination.joinpath(file)
        if not path.is_file():
            request.urlretrieve(url, path)


def get_extra_anniversary_stories(destination: pathlib.Path):
    directory = pathlib.Path('GFLData', 'en', 'text', 'avgtxt', 'anniversary')
    if not pathlib.Path('GFLData').is_dir():
        subprocess.run([
            'git', 'clone', 'https://github.com/randomqwerty/GFLData.git',
        ], stdout=subprocess.DEVNULL).check_returncode()
        subprocess.run([
            'git', 'checkout', '3cfdc2c8b0922b18f2689c79aee3a35ef6379a99',
        ], cwd='GFLData').check_returncode()
    if not destination.joinpath('anniversary3').is_dir():
        subprocess.run([
            'git', 'checkout', '9d0dae0066ccf1bc9e32abf35401d5ef7eaf7746',
        ], cwd='GFLData').check_returncode()
        shutil.copytree(directory, destination.joinpath('anniversary3'))
    if not destination.joinpath('anniversary4').is_dir():
        subprocess.run([
            'git', 'checkout', 'af8bfda4f9383d229e76dd57234b719e4bdd223e',
        ], cwd='GFLData').check_returncode()
        shutil.copytree(directory, destination.joinpath('anniversary4'))
        dup = destination.joinpath('anniversary4/55-102686.txt')
        if dup.is_file():
            dup.unlink()
    if not destination.joinpath('anniversary5').is_dir():
        subprocess.run([
            'git', 'checkout', '2ef576988ba9571636c51a87edd70561c3c31319',
        ], cwd='GFLData').check_returncode()
        shutil.copytree(directory, destination.joinpath('anniversary5'))
        # 四周年的残留？
        dup = destination.joinpath('anniversary5/55-102686.txt')
        if dup.is_file():
            dup.unlink()


def fill_in_chapter_info(main: list[Chapter], events: list[Chapter]):
    mapping = {
        0: 'Seed',
        1: 'Awakening',
        2: 'Echo',
        3: 'Silence',
        4: 'Message',
        5: 'Kindling',
        6: 'Comet',
        7: 'Partner',
        8: 'Spark',
        9: 'Lost',
        10: 'Purgatory',
        11: 'The Hunt',
        12: 'Gasp',
        13: 'The Oblivione',
    }
    for c in main:
        if c.description.isdigit():
            ch_num = int(c.description)
            if ch_num in mapping:
                c.name = c.name.replace(f"Chapter {ch_num}", mapping[ch_num])
        c.description = ''

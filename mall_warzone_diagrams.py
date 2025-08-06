from graphviz import Digraph

# Game Flow Diagram
game_flow = Digraph(comment="Mall Warzone Game Flow", format='png')
game_flow.attr(rankdir='LR', size='8')

# Nodes
game_flow.node('A', 'ورود بازیکن به MallQuest\n(اتصال به Wi-Fi Mall)')
game_flow.node('B', 'انتخاب حالت بازی\n(Solo / Team) + Stake سکه')
game_flow.node('C', 'ورود به Lobby و انتظار بازیکنان')
game_flow.node('D', 'شروع مسابقه\n(Spawn در نقشه Mall)')
game_flow.node('E', 'Safe Zone فعال + جمع‌آوری آیتم')
game_flow.node('F', 'مبارزه / حذف رقبا + ایونت‌ها')
game_flow.node('G', 'پایان مسابقه\n(آخرین بازیکن یا بیشترین امتیاز)')
game_flow.node('H', 'انتقال سکه به برنده')
game_flow.node('I', 'Customer Service\n(تبدیل سکه به واچر/جایزه)')

# Edges
game_flow.edges([
    ('A', 'B'),
    ('B', 'C'),
    ('C', 'D'),
    ('D', 'E'),
    ('E', 'F'),
    ('F', 'G'),
    ('G', 'H'),
    ('H', 'I'),
])

# Database Diagram
db = Digraph(comment="Mall Warzone Database Schema", format='png')
db.attr(rankdir='TB', size='8')

# Tables
db.node(
    'Users',
    'users\n- id\n- name\n- coins\n- vip_level',
    shape='box',
)
db.node(
    'Matches',
    'warzone_matches\n- id\n- name\n- stake_each\n- pot_total\n- status\n- safe_zone',
    shape='box',
)
db.node(
    'Players',
    'warzone_players\n- user_id\n- match_id\n- team_id\n- kills\n- alive\n- coins_earned',
    shape='box',
)
db.node(
    'Ads',
    'warzone_ads\n- id\n- title\n- content\n- type\n- target_area\n- start_time\n- end_time',
    shape='box',
)
db.node(
    'Missions',
    'warzone_missions\n- id\n- title\n- description\n- reward\n- target_area\n- type',
    shape='box',
)

# Relations
db.edge('Users', 'Players', label='1:N')
db.edge('Matches', 'Players', label='1:N')
db.edge('Ads', 'Matches', label='targeted to')
db.edge('Missions', 'Matches', label='assigned to')

if __name__ == "__main__":
    game_flow_path = "mall_warzone_game_flow"
    db_path = "mall_warzone_db_schema"
    game_flow.render(game_flow_path, cleanup=True)
    db.render(db_path, cleanup=True)
    print(game_flow_path + ".png", db_path + ".png")

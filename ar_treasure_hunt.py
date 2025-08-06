import datetime


class TreasureHuntManager:
    def __init__(self, db):
        self.db = db
        self._create_tables()

    def _create_tables(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS treasures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            location TEXT,
            prize_type TEXT,
            prize_amount INTEGER,
            start_time TEXT,
            end_time TEXT,
            is_active INTEGER DEFAULT 1
        )''')
        self.db.commit()

    def place_treasure(self, name, location, prize_type, prize_amount, start_time, end_time):
        self.db.execute('''INSERT INTO treasures (name, location, prize_type, prize_amount, start_time, end_time, is_active)
                           VALUES (?, ?, ?, ?, ?, ?, 1)''',
                        (name, location, prize_type, prize_amount, start_time, end_time))
        self.db.commit()
        print(f"[TreasureHunt] Treasure '{name}' placed at {location} with prize {prize_amount} {prize_type}")

    def get_active_treasures(self):
        now = datetime.datetime.now()
        treasures = self.db.execute('''SELECT id, name, location, prize_type, prize_amount
                                       FROM treasures
                                       WHERE is_active = 1 AND start_time <= ? AND end_time >= ?''',
                                    (now.isoformat(), now.isoformat())).fetchall()
        return treasures

    def claim_treasure(self, user_id, treasure_id):
        treasure = self.db.execute('''SELECT prize_type, prize_amount FROM treasures WHERE id = ? AND is_active = 1''',
                                   (treasure_id,)).fetchone()
        if treasure:
            prize_type, prize_amount = treasure
            from mall_gamification_system import CurrencyManager
            cm = CurrencyManager(self.db)
            cm.add_currency(user_id, prize_type, prize_amount)

            self.db.execute('''UPDATE treasures SET is_active = 0 WHERE id = ?''', (treasure_id,))
            self.db.commit()
            print(f"[TreasureHunt] User {user_id} claimed treasure {treasure_id} and won {prize_amount} {prize_type}")
            return True
        return False

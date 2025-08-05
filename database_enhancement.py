#!/usr/bin/env python3
"""
Database Enhancement for Deerfields Mall Gamification System
Adds missing tables, indexes, and operations to meet requirements
"""

import sqlite3
import json
import os
import shutil
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging
from pathlib import Path

class DatabaseEnhancer:
    """Enhances existing database with missing tables and indexes"""
    
    def __init__(self, db_path: str = 'mall_gamification.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging"""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('DatabaseEnhancer')
    
    def create_missing_tables(self):
        """Create missing tables as per requirements"""
        try:
            # Achievements table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS achievements (
                    achievement_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    achievement_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    points INTEGER DEFAULT 0,
                    icon TEXT,
                    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT,  -- JSON object for additional data
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # User sessions table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS user_sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    token_hash TEXT NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Enhanced security audit log table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS security_audit_log (
                    log_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    action TEXT NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    details TEXT,  -- JSON object for additional details
                    severity TEXT DEFAULT 'info',  -- info, warning, error, critical
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Enhanced rate limits table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS rate_limits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip_address TEXT NOT NULL,
                    endpoint TEXT NOT NULL,
                    request_count INTEGER DEFAULT 1,
                    window_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_request TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(ip_address, endpoint)
                )
            ''')
            
            # Database migrations table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS migrations (
                    migration_id TEXT PRIMARY KEY,
                    version TEXT NOT NULL,
                    description TEXT,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.conn.commit()
            self.logger.info("Missing tables created successfully")
            
        except Exception as e:
            self.logger.error(f"Error creating missing tables: {e}")
            raise
    
    def create_required_indexes(self):
        """Create required indexes for performance"""
        try:
            # User indexes
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_users_vip_tier ON users(vip_tier)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_users_level ON users(level)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_users_last_login ON users(last_login)')
            
            # Receipt indexes
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_receipts_user_id ON receipts(user_id)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_receipt_date ON receipts(created_at)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_receipts_status ON receipts(status)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_receipts_store ON receipts(store_name)')
            
            # Mission indexes
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_missions_user_id ON missions(user_id)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_mission_user_status ON missions(user_id, status)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_missions_type ON missions(mission_type)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_missions_expires ON missions(expires_at)')
            
            # Achievement indexes
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_achievements_user_id ON achievements(user_id)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_achievements_type ON achievements(achievement_type)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_achievements_earned ON achievements(earned_at)')
            
            # Security audit log indexes
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_security_log_user ON security_audit_log(user_id)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_security_log_action ON security_audit_log(action)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_security_log_timestamp ON security_audit_log(timestamp)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_security_log_ip ON security_audit_log(ip_address)')
            
            # Rate limit indexes
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_rate_limit_ip_endpoint ON rate_limits(ip_address, endpoint)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_rate_limit_window ON rate_limits(window_start)')
            
            # User session indexes
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON user_sessions(user_id)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_sessions_token ON user_sessions(token_hash)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_sessions_expires ON user_sessions(expires_at)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_sessions_active ON user_sessions(is_active)')
            
            # Activity indexes
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_activities_user_id ON user_activities(user_id)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_activities_type ON user_activities(activity_type)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_activities_created ON user_activities(created_at)')
            
            # Store indexes
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_stores_category ON stores(category)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_stores_zone ON stores(zone)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_stores_rating ON stores(rating)')
            
            # Support ticket indexes
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_tickets_user_id ON support_tickets(user_id)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_tickets_status ON support_tickets(status)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_tickets_priority ON support_tickets(priority)')
            
            self.conn.commit()
            self.logger.info("Required indexes created successfully")
            
        except Exception as e:
            self.logger.error(f"Error creating indexes: {e}")
            raise
    
    def add_missing_columns(self):
        """Add missing columns to existing tables"""
        try:
            # Add missing columns to users table
            columns_to_add = [
                ('users', 'vip_points', 'INTEGER DEFAULT 0'),
                ('users', 'total_spent', 'REAL DEFAULT 0.0'),
                ('users', 'total_purchases', 'INTEGER DEFAULT 0'),
                ('users', 'visited_categories', 'TEXT'),
                ('users', 'achievement_points', 'INTEGER DEFAULT 0'),
                ('users', 'social_score', 'INTEGER DEFAULT 0'),
                ('users', 'friends', 'TEXT'),
                ('users', 'team_id', 'TEXT'),
                ('users', 'leaderboard_position', 'INTEGER DEFAULT 0'),
                ('users', 'social_achievements', 'TEXT'),
                ('users', 'event_participation', 'TEXT'),
                ('users', 'seasonal_progress', 'TEXT'),
                ('users', 'language', 'TEXT DEFAULT "en"')
            ]
            
            for table, column, definition in columns_to_add:
                try:
                    self.conn.execute(f'ALTER TABLE {table} ADD COLUMN {column} {definition}')
                except sqlite3.OperationalError as e:
                    if "duplicate column name" not in str(e).lower():
                        self.logger.warning(f"Could not add column {column} to {table}: {e}")
            
            # Add missing columns to receipts table
            receipt_columns = [
                ('receipts', 'category', 'TEXT'),
                ('receipts', 'status', 'TEXT DEFAULT "pending"'),
                ('receipts', 'verified_at', 'TIMESTAMP')
            ]
            
            for table, column, definition in receipt_columns:
                try:
                    self.conn.execute(f'ALTER TABLE {table} ADD COLUMN {column} {definition}')
                except sqlite3.OperationalError as e:
                    if "duplicate column name" not in str(e).lower():
                        self.logger.warning(f"Could not add column {column} to {table}: {e}")
            
            # Add missing columns to missions table
            mission_columns = [
                ('missions', 'difficulty', 'TEXT DEFAULT "normal"'),
                ('missions', 'personalized', 'BOOLEAN DEFAULT FALSE')
            ]
            
            for table, column, definition in mission_columns:
                try:
                    self.conn.execute(f'ALTER TABLE {table} ADD COLUMN {column} {definition}')
                except sqlite3.OperationalError as e:
                    if "duplicate column name" not in str(e).lower():
                        self.logger.warning(f"Could not add column {column} to {table}: {e}")
            
            self.conn.commit()
            self.logger.info("Missing columns added successfully")
            
        except Exception as e:
            self.logger.error(f"Error adding missing columns: {e}")
            raise
    
    def run_migrations(self):
        """Run database migrations"""
        try:
            # Check if migrations table exists
            cursor = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='migrations'")
            if not cursor.fetchone():
                self.logger.info("Migrations table not found, creating...")
                self.conn.execute('''
                    CREATE TABLE migrations (
                        migration_id TEXT PRIMARY KEY,
                        version TEXT NOT NULL,
                        description TEXT,
                        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                self.conn.commit()
            
            # Get applied migrations
            cursor = self.conn.execute("SELECT version FROM migrations")
            applied_migrations = {row['version'] for row in cursor.fetchall()}
            
            # Define migrations
            migrations = [
                {
                    'version': '1.0.0',
                    'description': 'Initial schema creation'
                },
                {
                    'version': '1.1.0',
                    'description': 'Add achievements table'
                },
                {
                    'version': '1.2.0',
                    'description': 'Add user_sessions table'
                },
                {
                    'version': '1.3.0',
                    'description': 'Add missing columns to users table'
                },
                {
                    'version': '1.4.0',
                    'description': 'Add missing columns to receipts table'
                },
                {
                    'version': '1.5.0',
                    'description': 'Add missing columns to missions table'
                },
                {
                    'version': '1.6.0',
                    'description': 'Create required indexes'
                }
            ]
            
            # Apply pending migrations
            for migration in migrations:
                if migration['version'] not in applied_migrations:
                    self.logger.info(f"Applying migration {migration['version']}: {migration['description']}")
                    
                    # Record migration
                    self.conn.execute('''
                        INSERT INTO migrations (migration_id, version, description)
                        VALUES (?, ?, ?)
                    ''', (str(uuid.uuid4()), migration['version'], migration['description']))
                    self.conn.commit()
                    
                    self.logger.info(f"Migration {migration['version']} applied successfully")
            
            self.logger.info("All migrations completed successfully")
            
        except Exception as e:
            self.logger.error(f"Error running migrations: {e}")
            raise
    
    def backup_database(self, backup_path: str = None) -> bool:
        """Create a backup of the database"""
        try:
            if not backup_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = f"backup_mall_gamification_{timestamp}.db"
            
            # Create backup directory if it doesn't exist
            backup_dir = Path(backup_path).parent
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Close current connection
            self.conn.close()
            
            # Copy database file
            shutil.copy2(self.db_path, backup_path)
            
            # Reopen connection
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            
            self.logger.info(f"Database backup created: {backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating backup: {e}")
            # Reopen connection in case of error
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            return False
    
    def restore_database(self, backup_path: str) -> bool:
        """Restore database from backup"""
        try:
            if not os.path.exists(backup_path):
                self.logger.error(f"Backup file not found: {backup_path}")
                return False
            
            # Close current connection
            self.conn.close()
            
            # Create current database backup before restore
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            current_backup = f"pre_restore_backup_{timestamp}.db"
            shutil.copy2(self.db_path, current_backup)
            
            # Restore from backup
            shutil.copy2(backup_path, self.db_path)
            
            # Reopen connection
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            
            self.logger.info(f"Database restored from: {backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error restoring database: {e}")
            # Reopen connection in case of error
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            return False
    
    def optimize_database(self) -> bool:
        """Optimize database performance"""
        try:
            # Analyze tables for better query planning
            self.conn.execute("ANALYZE")
            
            # Vacuum database to reclaim space
            self.conn.execute("VACUUM")
            
            # Update statistics
            self.conn.execute("ANALYZE")
            
            self.conn.commit()
            self.logger.info("Database optimization completed")
            return True
            
        except Exception as e:
            self.logger.error(f"Error optimizing database: {e}")
            return False
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics and health information"""
        try:
            stats = {}
            
            # Table sizes
            cursor = self.conn.execute("""
                SELECT name, sql FROM sqlite_master 
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
            """)
            tables = cursor.fetchall()
            
            for table in tables:
                table_name = table['name']
                cursor = self.conn.execute(f"SELECT COUNT(*) as count FROM {table_name}")
                count = cursor.fetchone()['count']
                stats[f"{table_name}_count"] = count
            
            # Database file size
            if os.path.exists(self.db_path):
                stats['file_size_mb'] = round(os.path.getsize(self.db_path) / (1024 * 1024), 2)
            
            # Index information
            cursor = self.conn.execute("SELECT name FROM sqlite_master WHERE type='index'")
            stats['index_count'] = len(cursor.fetchall())
            
            # Migration status
            cursor = self.conn.execute("SELECT COUNT(*) as count FROM migrations")
            stats['migrations_applied'] = cursor.fetchone()['count']
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting database stats: {e}")
            return {}
    
    def verify_schema(self) -> Dict[str, Any]:
        """Verify that all required tables and indexes exist"""
        try:
            verification = {
                'tables': {},
                'indexes': {},
                'overall_status': 'PASS'
            }
            
            # Required tables
            required_tables = [
                'users', 'receipts', 'missions', 'achievements', 
                'security_audit_log', 'rate_limits', 'user_sessions',
                'companions', 'stores', 'user_activities', 
                'admin_logs', 'support_tickets', 'migrations'
            ]
            
            for table in required_tables:
                cursor = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
                exists = cursor.fetchone() is not None
                verification['tables'][table] = {
                    'exists': exists,
                    'status': 'PASS' if exists else 'FAIL'
                }
                if not exists:
                    verification['overall_status'] = 'FAIL'
            
            # Required indexes
            required_indexes = [
                'idx_users_email', 'idx_receipts_user_id', 'idx_receipt_date',
                'idx_mission_user_status', 'idx_achievements_user_id',
                'idx_security_log_user', 'idx_rate_limit_ip_endpoint',
                'idx_sessions_user_id', 'idx_sessions_token'
            ]
            
            for index in required_indexes:
                cursor = self.conn.execute("SELECT name FROM sqlite_master WHERE type='index' AND name=?", (index,))
                exists = cursor.fetchone() is not None
                verification['indexes'][index] = {
                    'exists': exists,
                    'status': 'PASS' if exists else 'FAIL'
                }
                if not exists:
                    verification['overall_status'] = 'FAIL'
            
            return verification
            
        except Exception as e:
            self.logger.error(f"Error verifying schema: {e}")
            return {'overall_status': 'ERROR', 'error': str(e)}
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.logger.info("Database connection closed")

# Enhanced CRUD operations
class SecureDatabaseOperations:
    """Secure database operations with parameterized queries"""
    
    def __init__(self, db_enhancer: DatabaseEnhancer):
        self.db = db_enhancer
        self.logger = logging.getLogger('SecureDatabaseOperations')
    
    def add_achievement(self, achievement_data: Dict[str, Any]) -> bool:
        """Add a new achievement with security validation"""
        try:
            # Validate required fields
            required_fields = ['achievement_id', 'user_id', 'achievement_type', 'title']
            for field in required_fields:
                if field not in achievement_data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Sanitize input
            achievement_id = str(achievement_data['achievement_id']).strip()
            user_id = str(achievement_data['user_id']).strip()
            achievement_type = str(achievement_data['achievement_type']).strip()
            title = str(achievement_data['title']).strip()[:100]  # Limit length
            
            self.db.conn.execute('''
                INSERT INTO achievements (achievement_id, user_id, achievement_type, title, description, points, icon, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                achievement_id,
                user_id,
                achievement_type,
                title,
                achievement_data.get('description'),
                achievement_data.get('points', 0),
                achievement_data.get('icon'),
                json.dumps(achievement_data.get('metadata', {}))
            ))
            self.db.conn.commit()
            self.logger.info(f"Achievement added: {achievement_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error adding achievement: {e}")
            return False
    
    def get_user_achievements(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's achievements with security validation"""
        try:
            if not user_id or not isinstance(user_id, str):
                return []
            
            cursor = self.db.conn.execute('''
                SELECT * FROM achievements 
                WHERE user_id = ? 
                ORDER BY earned_at DESC
            ''', (user_id.strip(),))
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            self.logger.error(f"Error getting user achievements: {e}")
            return []
    
    def add_user_session(self, session_data: Dict[str, Any]) -> bool:
        """Add a new user session with security validation"""
        try:
            # Validate required fields
            required_fields = ['session_id', 'user_id', 'token_hash', 'expires_at']
            for field in required_fields:
                if field not in session_data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Sanitize input
            session_id = str(session_data['session_id']).strip()
            user_id = str(session_data['user_id']).strip()
            token_hash = str(session_data['token_hash']).strip()
            
            self.db.conn.execute('''
                INSERT INTO user_sessions (session_id, user_id, token_hash, ip_address, user_agent, expires_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                session_id,
                user_id,
                token_hash,
                session_data.get('ip_address'),
                session_data.get('user_agent'),
                session_data['expires_at']
            ))
            self.db.conn.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error adding user session: {e}")
            return False
    
    def get_user_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get user session by ID with security validation"""
        try:
            if not session_id or not isinstance(session_id, str):
                return None
            
            cursor = self.db.conn.execute('''
                SELECT * FROM user_sessions 
                WHERE session_id = ? AND is_active = TRUE AND expires_at > CURRENT_TIMESTAMP
            ''', (session_id.strip(),))
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            self.logger.error(f"Error getting user session: {e}")
            return None
    
    def invalidate_user_session(self, session_id: str) -> bool:
        """Invalidate a user session with security validation"""
        try:
            if not session_id or not isinstance(session_id, str):
                return False
            
            self.db.conn.execute('''
                UPDATE user_sessions 
                SET is_active = FALSE 
                WHERE session_id = ?
            ''', (session_id.strip(),))
            self.db.conn.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error invalidating session: {e}")
            return False
    
    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions and return count of cleaned sessions"""
        try:
            cursor = self.db.conn.execute('''
                UPDATE user_sessions 
                SET is_active = FALSE 
                WHERE expires_at <= CURRENT_TIMESTAMP AND is_active = TRUE
            ''')
            self.db.conn.commit()
            return cursor.rowcount
        except Exception as e:
            self.logger.error(f"Error cleaning up expired sessions: {e}")
            return 0
    
    def log_security_event(self, user_id: str, action: str, ip_address: str = None, details: str = None) -> bool:
        """Log security event with validation"""
        try:
            if not action or not isinstance(action, str):
                return False
            
            self.db.conn.execute('''
                INSERT INTO security_audit_log (log_id, user_id, action, ip_address, details)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                str(uuid.uuid4()),
                user_id,
                action.strip(),
                ip_address,
                details
            ))
            self.db.conn.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error logging security event: {e}")
            return False
    
    def get_security_logs(self, user_id: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get security audit logs with validation"""
        try:
            if limit <= 0 or limit > 1000:  # Reasonable limit
                limit = 100
            
            if user_id:
                cursor = self.db.conn.execute('''
                    SELECT * FROM security_audit_log 
                    WHERE user_id = ?
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (user_id, limit))
            else:
                cursor = self.db.conn.execute('''
                    SELECT * FROM security_audit_log 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            self.logger.error(f"Error getting security logs: {e}")
            return []

# Main enhancement function
def enhance_database(db_path: str = 'mall_gamification.db') -> bool:
    """Main function to enhance the database with missing tables and indexes"""
    try:
        enhancer = DatabaseEnhancer(db_path)
        
        # Create backup before making changes
        enhancer.backup_database()
        
        # Create missing tables
        enhancer.create_missing_tables()
        
        # Add missing columns
        enhancer.add_missing_columns()
        
        # Create required indexes
        enhancer.create_required_indexes()
        
        # Run migrations
        enhancer.run_migrations()
        
        # Optimize database
        enhancer.optimize_database()
        
        # Verify schema
        verification = enhancer.verify_schema()
        
        enhancer.close()
        
        if verification['overall_status'] == 'PASS':
            print("✅ Database enhancement completed successfully!")
            print(f"📊 Database stats: {enhancer.get_database_stats()}")
            return True
        else:
            print("❌ Database enhancement completed with issues:")
            print(f"Verification: {verification}")
            return False
            
    except Exception as e:
        print(f"❌ Database enhancement failed: {e}")
        return False

# Utility functions
def create_backup(db_path: str = 'mall_gamification.db') -> bool:
    """Create a database backup"""
    try:
        enhancer = DatabaseEnhancer(db_path)
        result = enhancer.backup_database()
        enhancer.close()
        return result
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return False

def restore_from_backup(backup_path: str, db_path: str = 'mall_gamification.db') -> bool:
    """Restore database from backup"""
    try:
        enhancer = DatabaseEnhancer(db_path)
        result = enhancer.restore_database(backup_path)
        enhancer.close()
        return result
    except Exception as e:
        print(f"❌ Restore failed: {e}")
        return False

def get_database_health(db_path: str = 'mall_gamification.db') -> Dict[str, Any]:
    """Get database health information"""
    try:
        enhancer = DatabaseEnhancer(db_path)
        stats = enhancer.get_database_stats()
        verification = enhancer.verify_schema()
        enhancer.close()
        
        return {
            'stats': stats,
            'verification': verification,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {'error': str(e), 'timestamp': datetime.now().isoformat()}

if __name__ == "__main__":
    # Run database enhancement
    success = enhance_database()
    if success:
        print("🎉 Database is now ready for production use!")
    else:
        print("⚠️ Please check the logs for issues.") 
# MallQuest Migration & Improvement Script
# این اسکریپت تمام تغییرات لازم را پیاده‌سازی می‌کند

import os
import shutil
from pathlib import Path

# ===============================
# STEP 1: Update Requirements
# ===============================

NEW_REQUIREMENTS = """
# Core Flask
Flask==3.1.1
Werkzeug==3.1.3
Jinja2==3.1.6
MarkupSafe==3.0.2
itsdangerous==2.2.0
click==8.1.7
blinker==1.9.0

# Database
SQLAlchemy==2.0.42
alembic==1.16.4
psycopg2-binary==2.9.10

# Cache & Session
redis==6.3.0
Flask-Session==0.5.0

# Real-time (CRITICAL - جایگزین pygame)
flask-socketio==5.3.6
python-socketio==5.11.0
eventlet==0.33.3

# API & Documentation (CRITICAL)
flask-restx==1.3.0
flask-cors==4.0.0
marshmallow==3.20.2

# Security
PyJWT==2.10.1
bcrypt==4.3.0
Flask-Limiter==3.5.0
flask-talisman==1.1.0
cryptography==42.0.0
flask-wtf==1.2.2
pyotp==2.9.0

# Internationalization
Flask-Babel==4.0.0
Babel==2.17.0
pytz==2025.2

# Async Tasks
celery==5.3.4
celery[redis]==5.3.4

# Geolocation (CRITICAL for mall gaming)
geopy==2.4.1
shapely==2.0.2

# Utilities
python-dotenv==1.1.1
requests==2.31.0
psutil==7.0.0

# Push Notifications
pyfcm==2.0.0

# Testing
pytest==8.0.0
pytest-flask==1.3.0
pytest-cov==4.1.0

# Monitoring
sentry-sdk[flask]==1.40.0
prometheus-flask-exporter==0.23.0
"""

# ===============================
# STEP 2: New App Structure
# ===============================

APP_INIT = """
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_babel import Babel
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_restx import Api

# Initialize extensions
db = SQLAlchemy()
redis_client = FlaskRedis()
socketio = SocketIO()
jwt = JWTManager()
babel = Babel()
limiter = Limiter(key_func=get_remote_address)

def create_app(config_name='production'):
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['REDIS_URL'] = os.environ.get('REDIS_URL', 'redis://localhost:6379')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
    
    # Initialize extensions with app
    db.init_app(app)
    redis_client.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*", async_mode='eventlet')
    jwt.init_app(app)
    babel.init_app(app)
    limiter.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register API blueprints
    from app.api.v1 import create_api_v1
    api_v1 = create_api_v1()
    app.register_blueprint(api_v1, url_prefix='/api/v1')
    
    # Register WebSocket events
    from app.websocket import register_socketio_events
    register_socketio_events(socketio)
    
    # Register regular routes
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
"""

# ===============================
# STEP 3: WebSocket Implementation
# ===============================

WEBSOCKET_CODE = """
# app/websocket.py
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms
from flask_jwt_extended import decode_token
import json
from datetime import datetime

def register_socketio_events(socketio):
    
    @socketio.on('connect', namespace='/game')
    def handle_connect(auth):
        '''Handle player connection'''
        try:
            # Verify JWT token
            token = auth.get('token') if auth else None
            if token:
                decoded = decode_token(token)
                user_id = decoded['sub']
                
                # Join user's personal room
                join_room(f'user_{user_id}')
                
                # Send connection confirmation
                emit('connected', {
                    'status': 'success',
                    'user_id': user_id,
                    'timestamp': datetime.utcnow().isoformat()
                })
                
                # Update user online status
                update_user_online_status(user_id, True)
        except Exception as e:
            emit('error', {'message': 'Authentication failed'})
            return False
    
    @socketio.on('disconnect', namespace='/game')
    def handle_disconnect():
        '''Handle player disconnection'''
        # Update user offline status
        for room in rooms():
            if room.startswith('user_'):
                user_id = room.split('_')[1]
                update_user_online_status(user_id, False)
    
    @socketio.on('location_update', namespace='/game')
    def handle_location_update(data):
        '''Handle real-time location updates'''
        user_id = get_user_from_session()
        location = data.get('location')
        
        # Validate location
        if not validate_location(location):
            emit('error', {'message': 'Invalid location'})
            return
        
        # Check for nearby coins
        nearby_coins = get_nearby_coins(location)
        
        # Check for nearby players
        nearby_players = get_nearby_players(location, user_id)
        
        # Emit updates
        emit('location_updated', {
            'nearby_coins': nearby_coins,
            'nearby_players': nearby_players
        })
    
    @socketio.on('join_battle', namespace='/game')
    def handle_join_battle(data):
        '''Handle joining a battle room'''
        battle_id = data.get('battle_id')
        team_id = data.get('team_id')
        user_id = get_user_from_session()
        
        # Join battle room
        room = f'battle_{battle_id}'
        join_room(room)
        
        # Join team room
        if team_id:
            team_room = f'team_{team_id}'
            join_room(team_room)
        
        # Notify other players
        emit('player_joined', {
            'user_id': user_id,
            'username': get_username(user_id),
            'team_id': team_id
        }, room=room, include_self=False)
    
    @socketio.on('collect_coin', namespace='/game')
    def handle_collect_coin(data):
        '''Handle coin collection'''
        user_id = get_user_from_session()
        coin_id = data.get('coin_id')
        location = data.get('location')
        
        # Validate and process
        result = process_coin_collection(user_id, coin_id, location)
        
        if result['success']:
            # Emit to user
            emit('coin_collected', result)
            
            # Update leaderboard
            emit('leaderboard_update', get_leaderboard(), broadcast=True)
    
    @socketio.on('team_chat', namespace='/game')
    def handle_team_chat(data):
        '''Handle team chat messages'''
        team_id = data.get('team_id')
        message = data.get('message')
        user_id = get_user_from_session()
        
        # Validate user is in team
        if not is_user_in_team(user_id, team_id):
            emit('error', {'message': 'Not in team'})
            return
        
        # Broadcast to team
        emit('team_message', {
            'user_id': user_id,
            'username': get_username(user_id),
            'message': message,
            'timestamp': datetime.utcnow().isoformat()
        }, room=f'team_{team_id}')
"""

# ===============================
# STEP 4: API Routes
# ===============================

API_ROUTES = """
# app/api/v1/__init__.py
from flask import Blueprint
from flask_restx import Api

def create_api_v1():
    api_v1 = Blueprint('api_v1', __name__)
    
    api = Api(api_v1,
        version='1.0',
        title='MallQuest API',
        description='Location-based mall gaming API',
        doc='/docs'
    )
    
    # Import and add namespaces
    from .auth import api as auth_ns
    from .coins import api as coins_ns
    from .battles import api as battles_ns
    from .teams import api as teams_ns
    from .users import api as users_ns
    
    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(coins_ns, path='/coins')
    api.add_namespace(battles_ns, path='/battles')
    api.add_namespace(teams_ns, path='/teams')
    api.add_namespace(users_ns, path='/users')
    
    return api_v1

# app/api/v1/coins.py
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('coins', description='Coin operations')

# Models for Swagger documentation
location_model = api.model('Location', {
    'lat': fields.Float(required=True, description='Latitude'),
    'lng': fields.Float(required=True, description='Longitude'),
    'floor': fields.Integer(description='Mall floor number'),
    'accuracy': fields.Float(description='GPS accuracy in meters')
})

coin_model = api.model('Coin', {
    'id': fields.String(description='Coin ID'),
    'value': fields.Integer(description='Coin value'),
    'location': fields.Nested(location_model),
    'expires_at': fields.DateTime(description='Expiration time')
})

@api.route('/nearby')
class NearbyCoins(Resource):
    @api.doc('get_nearby_coins')
    @api.expect(location_model)
    @api.marshal_list_with(coin_model)
    @jwt_required()
    @limiter.limit("30 per minute")
    def post(self):
        '''Get coins near current location'''
        user_id = get_jwt_identity()
        location = api.payload
        
        # Get nearby coins
        coins = get_coins_near_location(
            location, 
            radius=50,  # 50 meters
            user_id=user_id
        )
        
        return coins

@api.route('/collect/<string:coin_id>')
class CollectCoin(Resource):
    @api.doc('collect_coin')
    @api.expect(location_model)
    @jwt_required()
    @limiter.limit("10 per minute")
    def post(self, coin_id):
        '''Collect a specific coin'''
        user_id = get_jwt_identity()
        location = api.payload
        
        # Process collection
        result = process_coin_collection(user_id, coin_id, location)
        
        if result['success']:
            return result, 200
        else:
            return {'error': result['message']}, 400
"""

# ===============================
# STEP 5: Game Engine (Web-based)
# ===============================

GAME_ENGINE_JS = """
// app/static/js/game_engine.js
class MallQuestGame {
    constructor() {
        this.socket = null;
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.userLocation = null;
        this.coins = new Map();
        this.players = new Map();
        this.isConnected = false;
        
        this.init();
    }
    
    async init() {
        // Get JWT token
        this.token = localStorage.getItem('access_token');
        
        // Initialize WebSocket
        this.connectWebSocket();
        
        // Setup canvas
        this.setupCanvas();
        
        // Start location tracking
        this.startLocationTracking();
        
        // Start game loop
        this.gameLoop();
    }
    
    connectWebSocket() {
        this.socket = io('/game', {
            auth: {
                token: this.token
            }
        });
        
        // Connection events
        this.socket.on('connected', (data) => {
            console.log('Connected to game server:', data);
            this.isConnected = true;
        });
        
        this.socket.on('error', (error) => {
            console.error('Socket error:', error);
        });
        
        // Game events
        this.socket.on('coin_spawned', (coin) => {
            this.coins.set(coin.id, coin);
            this.animateCoinSpawn(coin);
        });
        
        this.socket.on('coin_collected', (data) => {
            this.handleCoinCollected(data);
        });
        
        this.socket.on('player_moved', (data) => {
            this.updatePlayerPosition(data);
        });
        
        this.socket.on('battle_started', (battle) => {
            this.enterBattleMode(battle);
        });
    }
    
    startLocationTracking() {
        if ("geolocation" in navigator) {
            navigator.geolocation.watchPosition(
                (position) => {
                    this.updateLocation({
                        lat: position.coords.latitude,
                        lng: position.coords.longitude,
                        accuracy: position.coords.accuracy
                    });
                },
                (error) => {
                    console.error('Location error:', error);
                },
                {
                    enableHighAccuracy: true,
                    maximumAge: 5000,
                    timeout: 10000
                }
            );
        }
    }
    
    updateLocation(location) {
        this.userLocation = location;
        
        // Send to server
        if (this.isConnected) {
            this.socket.emit('location_update', {
                location: location
            });
        }
        
        // Check for nearby collectibles
        this.checkNearbyItems();
    }
    
    checkNearbyItems() {
        this.coins.forEach((coin, id) => {
            const distance = this.calculateDistance(
                this.userLocation,
                coin.location
            );
            
            if (distance < 10) { // 10 meters radius
                this.collectCoin(id);
            }
        });
    }
    
    collectCoin(coinId) {
        const coin = this.coins.get(coinId);
        if (!coin || coin.collected) return;
        
        // Mark as collected locally
        coin.collected = true;
        
        // Send to server
        this.socket.emit('collect_coin', {
            coin_id: coinId,
            location: this.userLocation
        });
        
        // Visual feedback
        this.showCoinCollectionAnimation(coin);
    }
    
    calculateDistance(loc1, loc2) {
        // Haversine formula for distance
        const R = 6371e3; // Earth radius in meters
        const φ1 = loc1.lat * Math.PI/180;
        const φ2 = loc2.lat * Math.PI/180;
        const Δφ = (loc2.lat - loc1.lat) * Math.PI/180;
        const Δλ = (loc2.lng - loc1.lng) * Math.PI/180;
        
        const a = Math.sin(Δφ/2) * Math.sin(Δφ/2) +
                  Math.cos(φ1) * Math.cos(φ2) *
                  Math.sin(Δλ/2) * Math.sin(Δλ/2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        
        return R * c;
    }
    
    gameLoop() {
        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw mall map
        this.drawMallMap();
        
        // Draw coins
        this.coins.forEach(coin => {
            if (!coin.collected) {
                this.drawCoin(coin);
            }
        });
        
        // Draw players
        this.players.forEach(player => {
            this.drawPlayer(player);
        });
        
        // Draw UI
        this.drawUI();
        
        // Continue loop
        requestAnimationFrame(() => this.gameLoop());
    }
    
    // ... more game methods
}

// Initialize game when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.game = new MallQuestGame();
});
"""

# ===============================
# STEP 6: Docker Configuration
# ===============================

DOCKER_COMPOSE = """
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://mallquest:password@db:5432/mallquest
      - REDIS_URL=redis://redis:6379
      - SECRET_KEY=${SECRET_KEY}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
    depends_on:
      - db
      - redis
    volumes:
      - ./app:/app
    command: gunicorn -k eventlet -w 4 --bind 0.0.0.0:5000 app:app

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=mallquest
      - POSTGRES_USER=mallquest
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app

volumes:
  postgres_data:
  redis_data:
"""

DOCKERFILE = """
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run migrations
RUN flask db upgrade

# Expose port
EXPOSE 5000

# Start application
CMD ["gunicorn", "-k", "eventlet", "-w", "4", "--bind", "0.0.0.0:5000", "app:app"]
"""

# ===============================
# Migration Script
# ===============================

def migrate_project():
    """Execute migration steps"""
    
    print("🚀 Starting MallQuest Migration...")
    
    # Step 1: Backup current project
    print("📦 Creating backup...")
    if os.path.exists("MallQuest"):
        shutil.copytree("MallQuest", "MallQuest_backup")
    
    # Step 2: Update requirements.txt
    print("📝 Updating requirements.txt...")
    with open("requirements.txt", "w") as f:
        f.write(NEW_REQUIREMENTS)
    
    # Step 3: Create new structure
    print("🏗️ Creating new project structure...")
    directories = [
        "app/api/v1",
        "app/static/js",
        "app/static/css",
        "app/templates",
        "app/websocket",
        "tests",
        "migrations"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    # Step 4: Write new files
    print("✍️ Writing new code files...")
    
    files_to_create = {
        "app/__init__.py": APP_INIT,
        "app/websocket.py": WEBSOCKET_CODE,
        "app/api/v1/__init__.py": API_ROUTES,
        "app/static/js/game_engine.js": GAME_ENGINE_JS,
        "docker-compose.yml": DOCKER_COMPOSE,
        "Dockerfile": DOCKERFILE
    }
    
    for filepath, content in files_to_create.items():
        with open(filepath, "w") as f:
            f.write(content)
    
    # Step 5: Remove pygame code
    print("🗑️ Removing pygame dependencies...")
    remove_pygame_code()
    
    # Step 6: Install new dependencies
    print("📦 Installing new dependencies...")
    os.system("pip install -r requirements.txt")
    
    print("✅ Migration completed successfully!")
    print("📚 Next steps:")
    print("  1. Run: docker-compose up")
    print("  2. Visit: http://localhost:5000/api/v1/docs")
    print("  3. Test WebSocket: http://localhost:5000/test")

def remove_pygame_code():
    """Remove all pygame references"""
    python_files = Path(".").glob("**/*.py")
    
    for file in python_files:
        try:
            with open(file, "r") as f:
                content = f.read()
            
            # Remove pygame imports
            content = content.replace("import pygame", "")
            content = content.replace("from pygame import", "")
            
            with open(file, "w") as f:
                f.write(content)
        except:
            pass

if __name__ == "__main__":
    migrate_project()

/* Basic browser game engine logic for MallQuest. */

const socket = io();
const playerId = Math.random().toString(36).slice(2);

socket.on('connected', (data) => {
  console.log('connected', data);
});

socket.on('location_ack', (data) => {
  console.log('nearby coins', data.nearby_coins);
});

socket.on('coin_collected', (data) => {
  console.log('coin collected', data);
});

socket.on('battle_update', (data) => {
  console.log('battle update', data);
});

function sendLocation(x, y) {
  socket.emit('location_update', { player_id: playerId, x: x, y: y });
}

function collectCoin(id) {
  socket.emit('collect_coin', { player_id: playerId, coin_id: id });
}

function joinBattle() {
  socket.emit('join_battle', { player_id: playerId });
}

window.MallQuestGame = { sendLocation, collectCoin, joinBattle };

from utils import *


def test_druid():
	game = prepare_game(DRUID, DRUID)
	assert game.player1.hero.id == DRUID
	assert game.player2.hero.id == DRUID
	assert game.player1.hero.health == 30
	assert game.player1.hero.armor == 0
	assert game.player1.hero.atk == 0
	assert not game.player1.hero.can_attack()
	game.player1.hero.power.use()
	assert game.player1.hero.armor == 1
	assert game.player1.hero.atk == 1
	assert game.player1.hero.can_attack()


def test_mage():
	game = prepare_game(MAGE, MAGE)
	assert game.player1.hero.id == MAGE
	assert game.player2.hero.id == MAGE
	assert game.player1.hero.health == 30
	assert game.player1.opponent.hero.health == 30
	assert game.player1.times_hero_power_used_this_game == 0
	assert game.player1.hero.power.controller is game.player1
	assert game.player2.hero.power.controller is game.player2

	# Fireblast the opponent hero
	game.player1.hero.power.use(target=game.player2.hero)
	assert game.player1.hero.health == 30
	assert game.player1.opponent.hero.health == 29
	assert game.player1.times_hero_power_used_this_game == 1
	assert not game.player1.hero.power.is_usable()


def test_paladin():
	game = prepare_game(PALADIN, PALADIN)
	assert game.player1.hero.id == PALADIN
	assert game.player2.hero.id == PALADIN
	game.player1.hero.power.use()
	assert len(game.board) == 1
	assert len(game.player1.field) == 1
	assert game.player1.field[0].id == "CS2_101t"

	# ensure that hero power cannot be used on full board
	game.end_turn(); game.end_turn()
	assert game.player1.hero.power.is_usable()
	for i in range(6):
		game.player1.give(WISP).play()
	assert len(game.player1.field) == 7
	assert not game.player1.hero.power.is_usable()


def test_priest():
	game = prepare_game(PRIEST, PRIEST)
	assert game.player1.hero.id == PRIEST
	# Heal self
	assert game.player1.hero.health == 30
	game.player1.hero.power.use(target=game.player1.hero)
	assert game.player1.hero.health == 30

	game.end_turn(); game.end_turn()
	game.player1.give(MOONFIRE).play(target=game.player1.hero)
	assert game.player1.hero.health == 29
	game.player1.hero.power.use(target=game.player1.hero)
	assert game.player1.hero.health == 30
	assert not game.player1.hero.power.is_usable()


def test_shaman():
	game = prepare_game(SHAMAN, SHAMAN)
	assert game.player1.hero.id == SHAMAN
	assert game.player2.hero.id == SHAMAN
	assert len(game.player1.hero.power.data.entourage) == 4

	# use hero power four times
	for i in range(4):
		assert len(game.player1.field) == i
		assert game.player1.hero.power.is_usable()
		game.player1.hero.power.use()
		assert len(game.player1.field) == i + 1
		assert game.player1.field[-1].id in game.player1.hero.power.data.entourage
		game.end_turn(); game.end_turn()

	# ensure hero power can only be used again after a totem was destroyed
	assert not game.player1.hero.power.is_usable()
	game.player1.field[0].destroy()
	assert game.player1.hero.power.is_usable()

	# ensure that hero power cannot be used on full board
	for i in range(4):
		game.player1.give(WISP).play()
	assert len(game.player1.field) == 7
	assert not game.player1.hero.power.is_usable()


def test_warlock():
	game = prepare_game(WARLOCK, WARLOCK)
	assert game.player1.hero.id == WARLOCK
	assert game.player2.hero.id == WARLOCK
	game.player1.discard_hand()
	assert not game.player1.hero.power.targets
	assert game.player1.hero.power.is_usable()
	game.player1.hero.power.use()
	assert len(game.player1.hand) == 1
	assert game.player1.hero.health == 28

from game_engine import GameEngine

engine = GameEngine(True)

new_game = engine.new_game([11777, 77474], 3)

new_game.select(player_id=11777, pos=2)
new_game.select(player_id=77474, pos=4)
new_game.select(player_id=11777, pos=1)
new_game.select(player_id=77474, pos=5)
new_game.select(player_id=11777, pos=0)


winner = new_game.winner
if winner:
    print(f"[!] Выиграл игрок с ID: {winner}")
    exit()
print("Никто не выиграл!")
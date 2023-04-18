import os
import sqlite3
from typing import Union

class Database:
    def __init__(self, path: Union[str, os.PathLike] = ""):
        if not os.path.exists(path):
            raise Exception(f"Path %{path}% doesnt exist!")

        self.db = sqlite3.connect(path)
        self.cursor = self.db.cursor()
        self.initialize()

    def initialize(self):
        queries = [
            '''CREATE TABLE games IF NOT EXISTS 
            (id INTEGER PRIMARY KEY AUTO_INCREMENT, game_id TEXT NOT NULL, players TEXT NOT NULL, board TEXT NOT NULL, status INTEGER NOT NULL, winner INTEGER NOT NULL, last_step INTEGER NOT NULL)
            ''',

            '''CREATE TABLE players IF NOT EXISTS
            (id INTEGER PRIMARY KEY AUTO_INCREMENT, name TEXT NOT NULL, wins INTEGER NOT NULL DEFAULT '0', loses INTEGER NOT NULL DEFAULT '0')
            '''
        ]
        for query in queries:
            self.cursor.execute(query, ())
            self.db.commit()

    def create_game(self, **options):
        query = 'INSERT INTO games ({}) VALUES ({})'
        args = []
        args_str = []
        if not options:
            raise Exception("No arguments passed!")

        for key, val in options.items():
            args.append(val)
            args_str.append(key)

        query = query.format(", ".join(args_str), ', '.join('?' * len(args_str)))
        self.cursor.execute(query, args)
        self.db.commit()


    def update_game(self, game_id: str, **options):
        query = 'UPDATE games SET {} WHERE game_id = ?'
        args = []
        args_str = []
        if not options:
            raise Exception("No arguments passed!")
        for key, val in options.items():
            args.append(val)
            args_str.append(f"{key} = ?")
        args.append(game_id)
        query = query.format(', '.join(args_str))
        self.cursor.execute(query, args)
        self.db.commit()

    def get_game(self, **options):
        query = 'SELECT * FROM games WHERE '
        args_str = []
        args = []
        if not options:
            raise Exception("No arguments passed!")
        for key, val in options.items():
            args.append(val)
            args_str.append(f"{key} = ?")
        query += " AND ".join(args_str)
        self.cursor.execute(query, args)
        return self.cursor.fetchone()

    def get_games(self, **options):
        query = 'SELECT * FROM games'
        args_str = []
        args = []
        if options:
            query += ' WHERE '
            for key, val in options.items():
                args.append(val)
                args_str.append(f"{key} = ?")
        self.cursor.execute(query, args)
        return self.cursor.fetchall()



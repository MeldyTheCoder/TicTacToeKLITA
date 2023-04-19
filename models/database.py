import os
import sqlite3
from typing import Union
from models import exceptions

class Database:
    def __init__(self, path: Union[str, os.PathLike] = ""):
        if not os.path.exists(path):
            raise exceptions.NoDatabaseFoundException(path)

        self.db = sqlite3.connect(path)
        self.cursor = self.db.cursor()
        self.cursor.row_factory = self.__dict_factory
        self.initialize()

    def __dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def initialize(self):
        queries = [
            '''CREATE TABLE IF NOT EXISTS games 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, game_id TEXT NOT NULL, players TEXT NOT NULL, board TEXT NOT NULL, status INTEGER NOT NULL, winner INTEGER NOT NULL, last_step INTEGER NOT NULL)
            ''',

            '''CREATE TABLE IF NOT EXISTS players 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, wins INTEGER NOT NULL DEFAULT '0', loses INTEGER NOT NULL DEFAULT '0')
            '''
        ]
        for query in queries:
            self.cursor.execute(query, ())
            self.db.commit()

    def create_game(self, **options) -> int:
        query = 'INSERT INTO games ({}) VALUES ({})'
        args = []
        args_str = []
        if not options:
            raise exceptions.DatabaseNoArgumentsPassed()

        for key, val in options.items():
            args.append(val)
            args_str.append(key)

        query = query.format(", ".join(args_str), ', '.join('?' * len(args_str)))
        self.cursor.execute(query, args)
        self.db.commit()
        return self.cursor.lastrowid


    def update_game(self, game_id: str, **options):
        query = 'UPDATE games SET {} WHERE game_id = ?'
        args = []
        args_str = []
        if not options:
            raise exceptions.DatabaseNoArgumentsPassed()
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
            raise exceptions.DatabaseNoArgumentsPassed()
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





from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user



class Chore:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.chore = db_data['chore']
        self.time = db_data['time']
        self.questions = db_data['questions']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.creator = None
        self.voters = []
        self.num_votes = db_data['num_votes']
    
    @staticmethod
    def validate_chore(chore):
        is_valid = True
        if len(chore['chore']) < 1:
            flash("Chore must have a name", "chore")
            is_valid = False
        if len(chore['time']) < 1:
            flash("time cannot be left blank", "chore")
            is_valid = False
        if len(chore['questions']) < 1:
            flash("questions cannot be left blank", "chore")
            is_valid = False
        return is_valid
    
    @classmethod
    def create_chore(cls, data):
        query = "INSERT INTO chores (user_id, chore, time, questions) VALUES (%(user_id)s, %(chore)s, %(time)s, %(questions)s);"
        return connectToMySQL('chore_schema').query_db(query, data)

    @classmethod
    def get_all_chores_with_votes(cls):
        query = "SELECT chores.id, chores.user_id AS creator_id, chore, COUNT(votes.chore_id) AS num_votes \
            FROM chores LEFT JOIN votes ON votes.chore_id = chores.id GROUP BY chores.id ORDER BY num_votes DESC;"
        results = connectToMySQL('chore_schema').query_db(query)
        all_chores = []
        print(results)
        for row in results:
            chore_data = {'chore_id': row['id']}
            one_chore = cls(cls.get_one_chore(chore_data))
            creator_data = {'id': row['creator_id']}
            creator = user.User.get_user_by_id(creator_data)
            one_chore.creator = creator
            one_chore.num_votes = row['num_votes']
            all_chores.append(one_chore)
        return all_chores

    @classmethod
    def get_chores_of_creator(cls, data):
        query = "SELECT * FROM chores LEFT JOIN users ON chores.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL('chore_schema').query_db(query, data)
        creator_chores = []
        for row in results:
            one_chore = cls(row)
            creator_chores.append(one_chore)
        return creator_chores
    

    @classmethod
    def get_one_chore(cls, data):
        query = "SELECT * FROM chores WHERE id = %(chore_id)s;"
        result = connectToMySQL('chore_schema').query_db(query, data)
        if result:
                return result[0]
        return None

    @classmethod
    def edit_chore(cls, data):
        query = "UPDATE chores SET chore = %(chore)s, time = %(time)s, questions = %(questions)s WHERE id = %(id)s;"
        return connectToMySQL('chore_schema').query_db(query, data)

    @classmethod
    def delete_chore(cls, data):
        query = "DELETE FROM chores WHERE id = %(id)s;"
        return connectToMySQL('chore_schema').query_db(query, data)

    @staticmethod
    def add_vote(data):
        query = "INSERT INTO votes (user_id, chore_id) VALUES (%(user_id)s, %(chore_id)s);"
        return connectToMySQL('chore_schema').query_db(query, data)

    @staticmethod
    def subtract_vote(data):
        query = "DELETE FROM votes WHERE user_id = %(user_id)s AND chore_id = %(chore_id)s"
        return connectToMySQL('chore_schema').query_db(query, data)
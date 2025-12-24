import uuid

from bson import ObjectId
from extensions import get_db
from datetime import datetime, timezone

class User():
    @staticmethod
    def create_user(username, email, password, role='personal'):
        user = {
            "_id": str(uuid.uuid4()),
            "username": username,
            "email": email,
            "password": password,
            "role": role,          # personal или team
            "team_id": None,       # ако е team member, тук ще стои team id
            "team_role": None,     # например 'admin' или 'member'
            "created_at": datetime.now(timezone.utc)
        }
        get_db()['users'].insert_one(user)
        return user

    @staticmethod
    def find_by_username(username):
        return get_db()['users'].find_one({"username": username})

    @staticmethod
    def find_by_email(email):
        from extensions import get_db
        return get_db()['users'].find_one({"email": email})

    @staticmethod
    def to_string(user):
        return f"<User {user['username']}>"

class Team():
    @staticmethod
    def create_team(TeamName, admin_user_id):
        team = {
            "_id": str(uuid.uuid4()),
            "name": TeamName,
            "members": [
                {"user_id": admin_user_id, "role": "admin"}
            ],
            "created_at": datetime.now(timezone.utc)
        }
        get_db()['teams'].insert_one(team)
        # Update user's team info
        get_db()['users'].update_one(
            {"_id": admin_user_id},
            {"$set": {"team_id": team['_id'], "team_role": "admin"}}
        )
        return team

    @staticmethod
    def add_member(team_id, user_id, role='member'):
        # Добавяне на член към екипа
        if get_db()['teams'].find_one({"_id": team_id, "members.user_id": user_id}):
            return False

        # Обновяване на info за потребителя
        get_db()['users'].update_one(
            {"_id": user_id},
            {"$set": {"team_id": team_id, "team_role": role}}
        )
    @staticmethod
    def get_all_teams():
        teams = list(get_db().teams.find({}, {"members": 0}))
        for t in teams:
            t['_id'] = str(t['_id'])
        return teams

    @staticmethod
    def is_admin(user_id, team_id):
        team = get_db().teams.find_one({"_id": team_id})

        for m in team["members"]:
            if m["user_id"] == user_id and m["role"] in ["owner", "admin"]:
                return True
            
        return False

    @staticmethod
    def get_members(team_id):
        team = get_db()['teams'].find_one({"_id": team_id})
        if not team:
            return []
        members_info = []
        for m in team['members']:
            user = get_db()['users'].find_one({"_id": m['user_id']}, {"password": 0})
            if user:
                user_info = {
                    "user_id": user['_id'],
                    "username": user['username'],
                    "role": m['role']
                }
                members_info.append(user_info)
        return members_info
    

class Task:
    @staticmethod
    def create_task(title, description, due_date, owner_id):
        task = {
            "_id": str(uuid.uuid4()),
            "title": title,
            "description": description,
            "due_date": due_date,
            "status": "pending", 
            "owner_id": owner_id,
            "completed": False,  
            "created_at": datetime.now(timezone.utc)
        }
        get_db()['tasks'].insert_one(task)
        return task

    @staticmethod
    def get_tasks_by_user(owner_id):
        tasks = list(get_db()['tasks'].find({"owner_id": owner_id}))
        for task in tasks:
            task['_id'] = str(task['_id'])
        return tasks

    @staticmethod
    def update_task(task_id, data, owner_id):
        result = get_db()['tasks'].update_one(
            {"_id": task_id, "owner_id": owner_id},
            {"$set": data}
        )
        return result.modified_count > 0

    @staticmethod
    def delete_task(task_id, owner_id):
        result = get_db()['tasks'].delete_one(
            {"_id": task_id, "owner_id": owner_id}
        )
        return result.deleted_count > 0

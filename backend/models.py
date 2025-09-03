import uuid
from extensions import get_db
from datetime import datetime, timezone

class User():
    @staticmethod
    def create_user(username, email, password):
        user = {
            "_id": str(uuid.uuid4()),
            "username": username,
            "email": email,
            "password": password,
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
        result = get_db()['tasks'].insert_one(task)
        task['_id'] = result.inserted_id
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

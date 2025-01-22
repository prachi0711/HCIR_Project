import cv2
import json


class UserManager:
    def __init__(self):
        self.authorized_users = []
        self.load_users_from_json('face_detection/users.json')

    def add_user(self, user):
        self.authorized_users.append(user)

    def remove_user(self, user):
        self.authorized_users.remove(user)

    def get_users(self):
        return self.authorized_users

    def load_users_from_json(self, users_json):
        with open(users_json, 'r') as file:
            data = json.load(file)

        self.authorized_users = [User(user['username'], user['image']) for user in data['users']]


class User:
    def __init__(self, username, image):
        self.username = username
        self.image = cv2.imread(image)



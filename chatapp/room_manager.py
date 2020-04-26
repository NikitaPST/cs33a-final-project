class RoomManager:
    users = []

    def add_user(self, id, user, room):
        if not user or not room:
            raise Exception("User and room are required!")

        existing_entry = next((x for x in RoomManager.users 
            if x["room"] == room and x["username"] == user.username), None)

        if existing_entry is not None:
            raise Exception("User is already in the room")

        entry = {
            "id": id,
            "username": user.username,
            "room": room
        }
        RoomManager.users.append(entry)

    def remove_user(self, id):
        RoomManager.users = [x for x in RoomManager.users
            if x["id"] != id]

    def get_users_in_room(self, room):
        users = [x["username"] for x in RoomManager.users
            if x["room"] == room]
        return users
# textgame_gma/object.py

class GameObject:
    def __init__(self, name, description=''):
        self.name = name
        self.description = description

    def __str__(self):
        return f"{self.name}: {self.description}"

    def __repr__(self):
        return f"GameObject(name={self.name!r}, description={self.description!r})"

class Player(GameObject):
    def __init__(self, name, description='', health=100, inventory=None):
        super().__init__(name, description)
        self.health = health
        self.inventory = inventory if inventory is not None else []

    def __str__(self):
        inventory_str = ', '.join(item.name for item in self.inventory)
        return (f"Player(name={self.name}, description={self.description}, "
                f"health={self.health}, inventory=[{inventory_str}])")

    def __repr__(self):
        return (f"Player(name={self.name!r}, description={self.description!r}, "
                f"health={self.health!r}, inventory={self.inventory!r})")

    def add_to_inventory(self, item):
        if not isinstance(item, GameObject):
            raise TypeError("Only GameObject instances can be added to inventory.")
        self.inventory.append(item)

    def remove_from_inventory(self, item_name):
        for item in self.inventory:
            if item.name == item_name:
                self.inventory.remove(item)
                return
        raise ValueError(f"Item '{item_name}' not found in inventory.")

class ObjectManager:
    def __init__(self):
        self.objects = {}
        self.players = {}

    def add_object(self, obj):
        if not isinstance(obj, GameObject):
            raise TypeError("Only GameObject instances can be added.")
        self.objects[obj.name] = obj

    def remove_object(self, name):
        if name in self.objects:
            del self.objects[name]
        else:
            raise KeyError(f"No object found with the name '{name}'.")

    def get_object(self, name):
        return self.objects.get(name, None)

    def list_objects(self):
        return list(self.objects.values())

    def create_player(self, name, description='', health=100):
        if name in self.players:
            raise ValueError(f"Player with name '{name}' already exists.")
        player = Player(name=name, description=description, health=health)
        self.players[name] = player
        return player

    def get_player(self, name):
        return self.players.get(name, None)

    def remove_player(self, name):
        if name in self.players:
            del self.players[name]
        else:
            raise KeyError(f"No player found with the name '{name}'.")

    def list_players(self):
        return list(self.players.values())

import os
import django
from django.db.models import F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character


def create_pet(name: str, species: str):
    Pet.objects.create(
        name=name,
        species=species,
    )
    pet = Pet.objects.last()
    return f'{pet.name} is a very cute {pet.species}!'


# print(create_pet('Buddy', 'Dog'))
# print(create_pet('Whiskers', 'Cat'))
# print(create_pet('Rocky', 'Hamster'))

def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool):
    Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical,
    )
    last_artifact = Artifact.objects.last()

    return f'The artifact {last_artifact.name} is {last_artifact.age} years old!'


def rename_artifact(artifact: Artifact, new_name: str):
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts():
    Artifact.objects.all().delete()


# print(create_artifact('Ancient Sword', 'Lost Kingdom', 500, 'A legendary sword with a rich history', True))
# artifact_object = Artifact.objects.get(name='Ancient Sword')
# rename_artifact(artifact_object, 'Ancient Shield')
# print(artifact_object.name)


def show_all_locations():
    return '\n'.join(str(l) for l in Location.objects.all().order_by('-id'))


def new_capital():
    location = Location.objects.first()
    location.is_capital = True
    location.save()


def get_capitals():
    return Location.objects.all().filter(is_capital=True).values('name')


def delete_first_location():
    Location.objects.first().delete()


#
# print(show_all_locations())
# print(new_capital())
# print(get_capitals())


def apply_discount():
    for car in Car.objects.all():
        discount = sum([int(x) for x in str(car.year)]) / 100
        car.price_with_discount = float(car.price) - (float(car.price) * discount)
        car.save()


def get_recent_cars():
    return Car.objects.all().filter(year__gt=2020).values('model', 'price_with_discount')


def delete_last_car():
    Car.objects.last().delete()


# apply_discount()
# print(get_recent_cars())


def show_unfinished_tasks():
    result = []

    for task in Task.objects.all().filter(is_finished=False):
        result.append(f'Task - {task.title} needs to be done until {task.due_date}!')

    return '\n'.join(result)


def complete_odd_tasks():
    for task in Task.objects.all():
        if task.id % 2 != 0:
            task.is_finished = True
            task.save()


def encode_and_replace(text: str, task_title: str):
    decoded_text = ''.join(chr(ord(symbol) - 3) for symbol in text)
    Task.objects.all().filter(title=task_title).update(description=decoded_text)


# encode_and_replace("Zdvk#wkh#glvkhv$", "Simple Task")
# print(Task.objects.get(title='Simple Task').description)


def get_deluxe_rooms():
    result = []

    for room in HotelRoom.objects.all().filter(room_type='Deluxe'):
        if room.id % 2 == 0:
            result.append(f'Deluxe room with number {room.room_number} costs {room.price_per_night}$ per night!')

    return '\n'.join(result)


def increase_room_capacity():
    previous_room = None
    rooms = HotelRoom.objects.all().order_by('id')
    for room in rooms:
        if not room.is_reserved:
            continue

        if previous_room:
            room.capacity += previous_room
        else:
            room.capacity += room.id

        previous_room = room.capacity

    HotelRoom.objects.bulk_update(rooms, ['capacity'])


def reserve_first_room():
    room = HotelRoom.objects.first()
    room.is_reserved = True
    room.save()


def delete_last_room():
    room = HotelRoom.objects.last()
    if not room.is_reserved:
        room.delete()


# print(get_deluxe_rooms())
# reserve_first_room()
# print(HotelRoom.objects.get(room_number=401).is_reserved)

def update_characters():
    Character.objects.filter(class_name='Mage').update(
        level=F('level') + 3,
        intelligence=F('intelligence') - 7
    )
    Character.objects.filter(class_name="Warrior").update(
        hit_points=F('hit_points') / 2,
        dexterity=F('dexterity') + 4
    )

    Character.objects.filter(class_name__in=["Assassin", "Scout"]).update(
        inventory="The inventory is empty"
    )


def fuse_characters(first_character: Character, second_character: Character):
    fusion_name = f'{first_character.name} {second_character.name}'
    class_name = "Fusion"
    level = (first_character.level + second_character.level) // 2
    strength = (first_character.strength + second_character.strength) * 1.2
    dexterity = (first_character.dexterity + second_character.dexterity) * 1.4
    intelligence = (first_character.intelligence + second_character.intelligence) * 1.5
    hit_points = first_character.hit_points + second_character.hit_points

    if first_character.class_name in ["Mage", "Scout"]:
        inventory = "Bow of the Elven Lords, Amulet of Eternal Wisdom"
    else:
        inventory = "Dragon Scale Armor, Excalibur"

    Character.objects.create(
        name=fusion_name,
        class_name=class_name,
        level=level,
        strength=strength,
        dexterity=dexterity,
        intelligence=intelligence,
        hit_points=hit_points,
        inventory=inventory
    )

    first_character.delete()
    second_character.delete()


def grand_dexterity():
    Character.objects.update(dexterity=30)


def grand_intelligence():
    Character.objects.update(intelligence=40)


def grand_strength():
    Character.objects.update(strength=50)


def delete_characters():
    Character.objects.filter(inventory='The inventory is empty').delete()

# character1 = Character.objects.create(
#     name='Gandalf',
#     class_name='Mage',
#     level=10,
#     strength=15,
#     dexterity=20,
#     intelligence=25,
#     hit_points=100,
#     inventory='Staff of Magic, Spellbook',
# )
#
# character2 = Character.objects.create(
#     name='Hector',
#     class_name='Warrior',
#     level=12,
#     strength=30,
#     dexterity=15,
#     intelligence=10,
#     hit_points=150,
#     inventory='Sword of Troy, Shield of Protection',
# )
#
# fuse_characters(character1, character2)
# fusion = Character.objects.filter(class_name='Fusion').get()
#
# print(fusion.name)
# print(fusion.class_name)
# print(fusion.level)
# print(fusion.intelligence)
# print(fusion.inventory)

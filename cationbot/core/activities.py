from discord import Activity, ActivityType, Game, Streaming

games = [
    "Cat Quest",
    "Cat in the Box",
    "The Cat Games",
    "Nyan Cat: Lost In Space",
    "Counter-Strike: Global Offensive",
]

listening = [
    "Relaxing Music for Cats",
    "Nyan Cat: Theme song",
    "Deadmau5 - 50 Something cats",
    "Excision & Downling - Robo Kitty",
    "Anamanaguchi - MEOW",
    "Party Favor & Zooly - Meow",
    "Volta Bureau - Alley Cat",
    "Deadmau5 - Cat Thruster",
]

streaming = [
    "Criando whiskas com React.js",
]

watching = [
    "Tom & Jerry: The Movie",
    "Pets 2",
    "Cat's Eye",
]

activities = [
    *[Game(name=g) for g in games],
    *[Activity(type=ActivityType.watching, name=w) for w in watching],
    *[Streaming(name=s, url="https://twitch.tv") for s in streaming],
    *[Activity(type=ActivityType.listening, name=l) for l in listening],
]

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
    *[Game(name=game) for game in games],
    *[Activity(type=ActivityType.watching, name=watch) for watch in watching],
    *[Streaming(name=stream, url="https://twitch.tv") for stream in streaming],
    *[
        Activity(type=ActivityType.listening, name=listen)
        for listen in listening
    ],
]

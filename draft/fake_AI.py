import sys

var = sys.stdin.read()
sys.stdout.write("""[
    {
        "starting_planet": {
        "x": 3,
        "y": 7
        },
        "destination_planet": {
        "x": 4,
        "y": 1
        },
        "nb_ships": 12
    },
    {
        "starting_planet": {
        "x": 3,
        "y": 7
        },
        "destination_planet": {
        "x": 2,
        "y": 2
        },
        "nb_ships": 3
    }
]
""")
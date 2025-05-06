import random

# List of common first names and last names

first_names = [
    "Carol",
    "Jason",
    "Amy",
    "Nathan",
    "Alice",
    "George",
    "Katherine",
    "Aaron",
    "Harold",
    "Jacob",
    "Rachel",
    "Madison",
    "Noah",
    "Elizabeth",
    "Michael",
    "Rebecca",
    "Bryan",
    "Jeffrey",
    "Logan",
    "Ralph",
    "Kevin",
    "Teresa",
    "Willie",
    "Doris",
    "Raymond",
    "Jacqueline",
    "Ryan",
    "Carolyn",
    "Matthew",
    "Christian",
    "Alexander",
    "Frances",
    "Betty",
    "Jesse",
    "Johnny",
    "Charles",
    "Angela",
    "Andrew",
    "Mark",
    "Joshua",
    "Julia",
    "Alexis",
    "Adam",
    "Ethan",
    "Kenneth",
    "Diane",
    "Sean",
    "Marilyn",
    "Jordan",
    "Emma",
]

last_names = [
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Jones",
    "Garcia",
    "Miller",
    "Davis",
    "Rodriguez",
    "Martinez",
    "Hernandez",
    "Lopez",
    "Gonzalez",
    "Wilson",
    "Anderson",
    "Thomas",
    "Taylor",
    "Moore",
    "Jackson",
    "Martin",
    "Lee",
    "Perez",
    "Thompson",
    "White",
    "Harris",
    "Sanchez",
    "Clark",
    "Ramirez",
    "Lewis",
    "Robinson",
    "Walker",
    "Young",
    "Allen",
    "King",
    "Wright",
    "Scott",
    "Torres",
    "Nguyen",
    "Hill",
    "Flores",
    "Green",
    "Adams",
    "Nelson",
    "Baker",
    "Hall",
    "Rivera",
    "Campbell",
    "Mitchell",
    "Carter",
    "Roberts",
]


def generate(n_users, include_celebrity=False):
    # Randomly select users' first names
    selected_first_names = random.choices(first_names, k=n_users)

    # Randomly select users' last names
    selected_last_names = random.choices(last_names, k=n_users)

    # Randomly select users' unique number
    numbers = map(str, random.sample(range(10 * n_users), k=n_users))

    # Combine them into their Twitter username
    users = zip(selected_first_names, selected_last_names, numbers)
    screen_names = list(map(lambda u: f"{u[0]}_{u[1]}{u[2]}".lower(), users))

    user_followings = []
    for k in range(n_users):

        # Users can follow anyone except themselves
        possible_followings = list(range(n_users))
        possible_followings.remove(k)
        n_following = random.randint(0, len(possible_followings) - 1)

        # Select any number of people to follow
        following = random.sample(possible_followings, k=n_following)

        # If celebrity is going to be included...
        if include_celebrity:
            # If user is not the celebrity (index 0)
            # and is not already following celebrity,
            # there's a 50% chance they will follow them.
            if k != 0 and 0 not in following:
                if random.randint(0, 1):
                    following.append(0)

        user_followings.append(following)

    return {
        "users": screen_names,
        "followings": user_followings,
        "celebrity": screen_names[0] if include_celebrity else None,
    }

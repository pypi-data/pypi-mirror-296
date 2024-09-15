"""A Day at the Zoo."""

from ._story import Story

questions = {
    1: "adjective",
    2: "animal",
    3: "verb ending in -ing",
    4: "place",
    5: "adjective",
    6: "animal",
    7: "verb ending in -ing",
    8: "adjective",
    9: "food",
    10: "adjective",
    11: "animal",
    12: "adjective",
    13: "animal",
    14: "verb ending in -ing",
    15: "verb ending in -ing",
    16: "adjective",
    17: "adjective",
    18: "noun",
    19: "adjective",
}

template = """
One day, my friend and I decided to visit the zoo. We were very (1) to see all the animals.
First, we saw the (2), which was (3) in its (4).
Next, we went to the (5) exhibit where we saw a (6) that was (7). It was so (8)!

After that, we decided to have some (9) for lunch.
While eating, we saw a (10) (11) that tried to steal our (9)!
We laughed and decided to go see the (12) (13) show. The (13) did tricks like (14) and (15).
It was the most (16) part of our day.

Finally, we visited the gift shop and bought a (17) (18) as a souvenir.
It was a (19) day at the zoo, and we couldn't wait to come back again!
"""

a_day_at_the_zoo = Story(title="A Day at the Zoo", template=template, questions=questions)

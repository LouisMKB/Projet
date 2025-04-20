
from collections import Counter


def count_gender(genre_rows: list[str]) -> Counter:
    genre_counter = Counter()

    for genre_str in genre_rows:
        #print(f"Processing genre string: {genre_str}")
        if not genre_str:
            continue
        genres = genre_str.split(",")
        for g in genres:
            g = g.strip()
            if g:
                genre_counter[g] += 1

    print(f"Final genre counts: {genre_counter}")
    return genre_counter
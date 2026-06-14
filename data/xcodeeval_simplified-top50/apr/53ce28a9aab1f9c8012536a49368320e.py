from itertools import combinations
from copy import copy


def variants(items):
    for i in range(6):
        for combination in combinations(items, i):
            yield combination


def main():
    input()
    cards = {(color, int(value)) for color, value in (card for card in input().split())}
    value_counts = [0] * 6
    color_counts = {color: 0 for color in "RGBYW"}
    for color, value in cards:
        value_counts[value] += 1
        color_counts[color] += 1
    best = float("inf")
    for chosen_colors in variants("RGBYW"):
        for chosen_values in variants(range(1, 6)):
            remaining_cards = copy(cards)
            current_value_counts = value_counts[:]
            current_color_counts = copy(color_counts)
            for card in copy(remaining_cards):
                color, value = card
                if color in chosen_colors and value in chosen_values:
                    current_value_counts[value] -= 1
                    current_color_counts[color] -= 1
                    remaining_cards.remove(card)
            for _ in range(11):
                for card in copy(remaining_cards):
                    color, value = card
                    if (
                        current_value_counts[value] == 1
                        and current_color_counts[color] == 1
                        or current_value_counts[value] == 1
                        and value in chosen_values
                        or current_color_counts[color] == 1
                        and color in chosen_colors
                    ):
                        current_value_counts[value] -= 1
                        current_color_counts[color] -= 1
                        remaining_cards.remove(card)
            if not remaining_cards:
                best = min(best, len(chosen_colors) + len(chosen_values))
    print(best)


main()

from fractions import Fraction

def generate_dice_combinations():
    combinations = {}
    for i in range(2, 13):
        combinations[i] = []
        for j in range(1, 7):
            if i - j in range(1, 7):
                combinations[i].append((j, i - j))
    return combinations

def main():
    dice_combinations = generate_dice_combinations()
    for i in range(2, 13):
        total_combinations = len(dice_combinations[i])
        starting_with_six = [combo for combo in dice_combinations[i] if combo[0] == 6]
        if total_combinations > 0:
            conditional_probability = Fraction(len(starting_with_six), total_combinations)
            print(f"Dice combinations that add up to {i}: {dice_combinations[i]}")
            print(f"Conditional probability that the first die lands on 6 given the sum is {i}: {conditional_probability}")
            print()

if __name__ == "__main__":
    main()

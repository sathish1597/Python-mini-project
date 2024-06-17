import random
import time
from words import word_list  # Import the default word list


def display_hangman(attempts):
    """
    Returns the hangman diagram based on the number of wrong attempts.
    """
    stages = [
        """
           ------
           |    |
           |
           |
           |
           |
        --------
        """,
        """
           ------
           |    |
           |    O
           |
           |
           |
        --------
        """,
        """
           ------
           |    |
           |    O
           |    |
           |
           |
        --------
        """,
        """
           ------
           |    |
           |    O
           |   /|
           |
           |
        --------
        """,
        """
           ------
           |    |
           |    O
           |   /|\\
           |
           |
        --------
        """,
        """
           ------
           |    |
           |    O
           |   /|\\
           |   /
           |
        --------
        """,
        """
           ------
           |    |
           |    O
           |   /|\\
           |   / \\
           |
        --------
        """,
    ]
    return stages[min(attempts, len(stages) - 1)]


def choose_word(word_list):
    """
    Chooses a random word from the word list.
    """
    return random.choice(word_list)


def initialize_game(word):
    """
    Initializes the game state with underscores for the word,
    zero wrong attempts, and an empty list of guessed words.
    """
    return ["_"] * len(word), 0, []


def update_game_state(guess, word, display_word, guessed_words, wrong_attempts, max_attempts):
    """
    Updates the game state based on the player's guess.
    """
    guessed_words.append(guess)
    correct_guess = False

    # Check each character and update display_word accordingly
    for i, letter in enumerate(word):
        if letter == guess:
            display_word[i] = letter
            correct_guess = True

    if not correct_guess:
        wrong_attempts += 1
        print(f"Wrong! You have {max_attempts - wrong_attempts} attempts left.")

    return display_word, guessed_words, wrong_attempts


def give_hint(hint, hint_used):
    """
    Provides a hint to the player if not already used.
    """
    if hint_used:
        print("You have already used your hint!")
    else:
        print(f"Hint: {hint}")
        hint_used = True
    return hint_used


def try_again():
    """
    Asks the player if they want to play again.
    """
    while True:
        response = input("Do you want to play again? (yes/no): ").lower()
        if response == "yes":
            return True
        elif response == "no":
            print("Thanks for playing! Goodbye.")
            return False
        else:
            print("Please answer 'yes' or 'no'.")


def display_statistics(stats):
    """
    Displays the game statistics.
    """
    print("\nStatistics:")
    print(f"Games Played: {stats['games_played']}")
    print(f"Games Won: {stats['games_won']}")
    print(f"Games Lost: {stats['games_lost']}")
    if stats["games_played"] > 0:
        avg_time = stats["total_time"] / stats["games_played"]
        print(f"Average Time: {avg_time: .2f} seconds")


def sort_key(player):
    """
    Sort key function for sorting the leaderboard by the number of games won.
    """
    return player["games_won"]


def display_leaderboard(leaderboard):
    """
    Displays the leaderboard sorted by the number of games won.
    """
    print("\nLeaderboard:")
    sorted_leaderboard = sorted(leaderboard, key=sort_key, reverse=True)
    for rank, player in enumerate(sorted_leaderboard, start=1):
        avg_time = player["total_time"] / player["games_played"]
        print(f"{rank}. {player['name']} - Games Won: {player['games_won']}, Games Played: {player['games_played']}, "
              f"Average Time: {avg_time: .2f} seconds")


def hangman(word_list, stats):
    """
    Main function to run the hangman game.
    """
    chosen_word_info = choose_word(word_list)  # Choose a random word
    word = chosen_word_info["word"]
    hint = chosen_word_info["hint"]
    max_attempts = 10
    display_word, wrong_attempts, guessed_words = initialize_game(word)
    hint_used = False
    start_time = time.time()

    while wrong_attempts < max_attempts:
        print(display_hangman(wrong_attempts))  # Display hangman diagram
        print("Word: " + " ".join(display_word))  # Display the current state of the word
        guess = input("Guess the word or type 'hint' for a hint (you can use the hint only once): ").lower()

        if guess == "hint":
            hint_used = give_hint(hint, hint_used)
        elif guess.isalpha() and guess == word:  # Validate input and check if the guess matches the word
            display_word = list(word)
            stats["games_won"] += 1
            break
        elif guess.isalpha():  # Validate input
            display_word, guessed_words, wrong_attempts = update_game_state(
                guess, word, display_word, guessed_words, wrong_attempts, max_attempts)
        else:
            print("Invalid input. Please guess a word or type 'hint'.")

        if "_" not in display_word:  # Check if the word is completely guessed
            print(f"Congratulations! You guessed the word: {''.join(display_word)}")
            stats["games_won"] += 1
            break
    else:
        print(display_hangman(wrong_attempts))  # Display final hangman diagram
        print(f"Game Over! The word was: {word}")
        stats["games_lost"] += 1

    stats["games_played"] += 1
    stats["total_time"] += time.time() - start_time


def get_custom_word_list():
    """
    Prompts the player to input a custom word list.
    """
    custom_word_list = []
    while True:
        word = input("Enter a word (or 'done' to finish): ").lower()
        if word == 'done':
            break
        hint = input("Enter a hint for this word: ").lower()
        custom_word_list.append({"word": word, "hint": hint})
    return custom_word_list


# Main game loop
def main():
    playing = True
    use_custom_list = input("Do you want to add a custom word list? (yes/no): ").lower() == "yes"
    custom_word_list = get_custom_word_list() if use_custom_list else word_list

    statistics = {
        "games_played": 0,
        "games_won": 0,
        "games_lost": 0,
        "total_time": 0.0
    }
    leaderboard = []

    while playing:
        name = input("Enter your name: ")
        print(f"Welcome {name}")
        print("=====================")
        print("Try to guess the word in less than 10 attempts")
        hangman(custom_word_list, statistics)
        leaderboard.append({
            "name": name,
            "games_played": statistics["games_played"],
            "games_won": statistics["games_won"],
            "total_time": statistics["total_time"]
        })
        playing = try_again()

    display_statistics(statistics)
    display_leaderboard(leaderboard)


if __name__ == "__main__":
    main()

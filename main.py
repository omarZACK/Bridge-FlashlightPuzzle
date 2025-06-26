#!/usr/bin/env python3
"""
Bridge and Flashlight Puzzle - Main Demo
Demonstrates the puzzle classes and shows the optimal solution.
"""
from models import Person, Bridge, Flashlight, GameState, Move


def create_puzzle_setup():
    """Create the standard puzzle setup with 4 people."""
    # Create the four people with their crossing times
    you = Person("You", 1)
    lab_assistant = Person("Lab Assistant", 2)
    worker = Person("Worker", 5)
    scientist = Person("Scientist", 10)

    people = [you, lab_assistant, worker, scientist]

    # Create bridge (capacity 2, 17 minute time limit)
    bridge = Bridge(capacity=2, max_time=17)

    # Create flashlight
    flashlight = Flashlight()

    # Create game state
    game_state = GameState(bridge, flashlight, people)

    return game_state, people


def print_game_state(game_state, step_num=None):
    """Print the current game state in a readable format."""
    if step_num is not None:
        print(f"\n--- Step {step_num} ---")

    print(f"Current State: {game_state}")
    print(f"Game Won: {game_state.is_game_won()}")
    print(f"Game Over: {game_state.is_game_over()}")

    if game_state.is_game_won():
        print("🎉 Congratulations! Everyone crossed safely!")
    elif game_state.is_game_over():
        print("💀 Game Over! The zombies caught up!")


def demonstrate_optimal_solution():
    """Demonstrate the optimal solution to the puzzle."""
    print("=" * 60)
    print("BRIDGE AND FLASHLIGHT PUZZLE - OPTIMAL SOLUTION")
    print("=" * 60)

    game_state, people = create_puzzle_setup()
    you, lab_assistant, worker, scientist = people

    print("\nInitial Setup:")
    print("- You (1 min), Lab Assistant (2 min), Worker (5 min), Scientist (10 min)")
    print("- Bridge capacity: 2 people")
    print("- Time limit: 17 minutes")
    print("- Zombies arrive after 17 minutes")

    print_game_state(game_state, 0)

    # Optimal solution sequence
    moves = [
        Move([you, lab_assistant], "left_to_right"),  # You and Lab Assistant cross (2 min)
        Move([you], "right_to_left"),  # You return with flashlight (1 min)
        Move([worker, scientist], "left_to_right"),  # Worker and Scientist cross (10 min)
        Move([lab_assistant], "right_to_left"),  # Lab Assistant returns (2 min)
        Move([you, lab_assistant], "left_to_right"),  # You and Lab Assistant cross again (2 min)
    ]

    print(f"\nExecuting optimal solution:")
    total_time = 0

    for i, move in enumerate(moves, 1):
        if game_state.make_move(move):
            total_time += move.get_time_taken()
            print(f"\nMove {i}: {move}")
            print(f"Time taken: {move.get_time_taken()} minutes")
            print(f"Total time: {total_time} minutes")
            print_game_state(game_state)
        else:
            print(f"Failed to execute move {i}: {move}")
            break

    print(f"\n" + "=" * 60)
    if game_state.is_game_won():
        print(f"SUCCESS! Everyone crossed in {total_time} minutes (within the 17-minute limit)")
    else:
        print("FAILED! Could not complete the puzzle in time")
    print("=" * 60)


def demonstrate_invalid_moves():
    """Demonstrate some invalid moves to show validation."""
    print("\n" + "=" * 60)
    print("DEMONSTRATING INVALID MOVES")
    print("=" * 60)

    game_state, people = create_puzzle_setup()
    you, lab_assistant, worker, scientist = people

    # Try some invalid moves
    invalid_moves = [
        Move([lab_assistant], "left_to_right"),  # Lab Assistant doesn't have flashlight
        Move([you, lab_assistant, worker], "left_to_right"),  # Too many people (capacity = 2)
        Move([scientist], "right_to_left"),  # Scientist is not on right side
    ]

    for i, move in enumerate(invalid_moves, 1):
        print(f"\nTrying invalid move {i}: {move}")
        if game_state.can_make_move(move):
            print("✓ Move is valid")
        else:
            print("✗ Move is invalid (as expected)")


def show_available_moves():
    """Show available moves from the initial state."""
    print("\n" + "=" * 60)
    print("AVAILABLE MOVES FROM INITIAL STATE")
    print("=" * 60)

    game_state, _ = create_puzzle_setup()
    valid_moves = game_state.get_valid_moves()

    print(f"Number of valid moves: {len(valid_moves)}")
    for i, move in enumerate(valid_moves, 1):
        print(f"{i}. {move} (would take {move.calculate_time(game_state._bridge)} minutes)")


def play_interactive_game():
    """Interactive terminal-based game."""
    print("🌉" + "=" * 58 + "🌉")
    print("     BRIDGE AND FLASHLIGHT PUZZLE - INTERACTIVE GAME")
    print("🌉" + "=" * 58 + "🌉")

    print("\n📖 STORY:")
    print("You and 3 others are being chased by zombies! You need to cross")
    print("a bridge to safety. The bridge can only hold 2 people at once,")
    print("and you need the flashlight to see in the dark.")
    print("The zombies will arrive in 17 minutes!")

    print("\n👥 CHARACTERS:")
    print("• You: 1 minute to cross")
    print("• Lab Assistant: 2 minutes to cross")
    print("• Worker: 5 minutes to cross")
    print("• Scientist: 10 minutes to cross")

    print("\n📋 RULES:")
    print("• Only 2 people can cross at once")
    print("• Someone must carry the flashlight")
    print("• When 2 people cross together, they move at the slower person's speed")
    print("• The flashlight must be carried back and forth")

    # Create game setup
    game_state, people = create_puzzle_setup()
    you, lab_assistant, worker, scientist = people

    print(f"\n⏰ TIME LIMIT: {game_state._bridge.get_max_time()} minutes")
    print("Let's begin!")

    move_count = 0

    while not game_state.is_game_over():
        move_count += 1
        print(f"\n{'=' * 60}")
        print(f"MOVE #{move_count}")
        print(f"{'=' * 60}")

        # Show current state
        display_current_state(game_state)

        # Get valid moves
        valid_moves = game_state.get_valid_moves()

        if not valid_moves:
            print("No valid moves available!")
            break

        # Show available moves
        print(f"\n🎯 AVAILABLE MOVES:")
        for i, move in enumerate(valid_moves, 1):
            time_needed = move.calculate_time(game_state._bridge)
            persons_str = " + ".join([p.get_name() for p in move.get_crossing_persons()])
            direction = "→" if move.get_direction() == "left_to_right" else "←"
            print(f"{i}. {persons_str} {direction} ({time_needed} min)")

        # Get user choice
        while True:
            try:
                choice = input(f"\nChoose your move (1-{len(valid_moves)}) or 'q' to quit: ").strip()

                if choice.lower() == 'q':
                    print("Thanks for playing! 👋")
                    return

                choice_num = int(choice)
                if 1 <= choice_num <= len(valid_moves):
                    selected_move = valid_moves[choice_num - 1]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(valid_moves)}")
            except ValueError:
                print("Please enter a valid number or 'q' to quit")

        # Execute the move
        if game_state.make_move(selected_move):
            time_taken = selected_move.get_time_taken()
            persons_str = " + ".join([p.get_name() for p in selected_move.get_crossing_persons()])
            direction_word = "crossed to the right" if selected_move.get_direction() == "left_to_right" else "returned to the left"

            print(f"\n✅ {persons_str} {direction_word} in {time_taken} minutes!")
            print(f"⏱️  Total time elapsed: {game_state.get_elapsed_time()} minutes")
            print(f"⏰ Time remaining: {game_state.get_remaining_time()} minutes")
        else:
            print("❌ Failed to execute move!")

    # Game over - show results
    print(f"\n{'🏁' * 20}")
    print("GAME OVER!")
    print(f"{'🏁' * 20}")

    display_current_state(game_state)

    if game_state.is_game_won():
        print(f"\n🎉 CONGRATULATIONS! 🎉")
        print(f"You successfully got everyone across in {game_state.get_elapsed_time()} minutes!")
        print("You escaped the zombies! 🧟‍♂️💨")

        # Show move history
        print(f"\n📜 Your solution:")
        for i, move in enumerate(game_state.get_move_history(), 1):
            persons_str = " + ".join([p.get_name() for p in move.get_crossing_persons()])
            direction = "→" if move.get_direction() == "left_to_right" else "←"
            print(f"{i}. {persons_str} {direction} ({move.get_time_taken()} min)")
    else:
        print(f"\n💀 GAME OVER! 💀")
        print("The zombies caught up! You ran out of time.")
        print("Better luck next time!")

    # Ask if they want to see the optimal solution
    show_solution = input(f"\nWould you like to see the optimal solution? (y/n): ").strip().lower()
    if show_solution == 'y':
        print(f"\n{'📚' * 20}")
        print("OPTIMAL SOLUTION:")
        print(f"{'📚' * 20}")
        demonstrate_optimal_solution()


def display_current_state(game_state):
    """Display the current game state in a visual format."""
    left_side = game_state.get_left_side()
    right_side = game_state.get_right_side()
    flashlight_holder = game_state.get_flashlight_holder()

    print(f"\n🌉 BRIDGE STATUS:")
    print(f"⏱️  Time: {game_state.get_elapsed_time()}/{game_state._bridge.get_max_time()} minutes")
    print(f"⏰ Remaining: {game_state.get_remaining_time()} minutes")

    print(f"\n👥 CURRENT POSITIONS:")

    # Left side
    print("🏠 LEFT SIDE (Start):")
    if left_side:
        for person in left_side:
            flashlight_indicator = " 🔦" if person == flashlight_holder else ""
            print(f"   • {person.get_name()} ({person.get_crossing_time()} min){flashlight_indicator}")
    else:
        print("   (empty)")

    # Bridge representation
    print("   " + "=" * 20)
    print("   🌉    BRIDGE    🌉")
    print("   " + "=" * 20)

    # Right side
    print("🏰 RIGHT SIDE (Safety):")
    if right_side:
        for person in right_side:
            flashlight_indicator = " 🔦" if person == flashlight_holder else ""
            print(f"   • {person.get_name()} ({person.get_crossing_time()} min){flashlight_indicator}")
    else:
        print("   (empty)")


def show_menu():
    """Show the main menu."""
    print("🌉" + "=" * 58 + "🌉")
    print("     BRIDGE AND FLASHLIGHT PUZZLE")
    print("🌉" + "=" * 58 + "🌉")

    print("\nWhat would you like to do?")
    print("1. 🎮 Play the game")
    print("2. 📚 See the optimal solution")
    print("3. 🔍 See demo of invalid moves")
    print("4. 📋 Show available moves from start")
    print("5. ❌ Quit")

    while True:
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            choice_num = int(choice)
            if 1 <= choice_num <= 5:
                return choice_num
            else:
                print("Please enter a number between 1 and 6")
        except ValueError:
            print("Please enter a valid number")


if __name__ == "__main__":
    while True:
        choice = show_menu()

        if choice == 1:
            play_interactive_game()
        elif choice == 2:
            demonstrate_optimal_solution()
        elif choice == 3:
            demonstrate_invalid_moves()
        elif choice == 4:
            show_available_moves()
        elif choice == 5:
            print("\nThanks for playing! 👋")
            break

        input("\nPress Enter to return to menu...")
        print("\n" * 2)  # Clear screen effect



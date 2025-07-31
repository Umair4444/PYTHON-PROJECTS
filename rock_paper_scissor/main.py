import random

def play():
    options = ["Rock", "Paper", "Scissors"]
    print("Welcome to Rock, Paper, Scissors!")

    while True:
        print("\nChoose an option:")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        print("4. Quit")

        try:
            choice = int(input("Enter your choice (1-4): "))
            if choice == 4:
                print("Thanks for playing!")
                break
            if choice not in [1, 2, 3]:
                print("Invalid choice. Please try again.")
                continue
        except ValueError:
            print("Please enter a number.")
            continue

        user_choice = options[choice - 1]
        computer_choice = random.choice(options)

        print(f"\nYou chose: {user_choice}")
        print(f"Computer chose: {computer_choice}")

        if user_choice == computer_choice:
            print("It's a tie!")
        elif (user_choice == "Rock" and computer_choice == "Scissors") or \
             (user_choice == "Paper" and computer_choice == "Rock") or \
             (user_choice == "Scissors" and computer_choice == "Paper"):
            print("You win!")
        else:
            print("You lose!")

if __name__ == "__main__":
    play()

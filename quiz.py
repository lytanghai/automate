# flashcards.py

flashcards = {
    "What is the capital of France?": "Paris",
    "What is 2 + 2?": "4",
    "What is the color of the sky?": "Blue",
}

def start_quiz():
    score = 0
    for question, answer in flashcards.items():
        user_answer = input(question + " : ")
        if user_answer.lower() == answer.lower():
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect! The correct answer is {answer}.")
    
    print(f"Your score: {score}/{len(flashcards)}")



def main():
    print("Welcome to the Flashcard Quiz App!")
    start_quiz()

if __name__ == "__main__":
    main()

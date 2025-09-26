import json, random, os, datetime

QUESTIONS_FILE = "questions.json"
SCORES_FILE = "scores.json"

def load_json(fname, default):
    if os.path.exists(fname):
        try:
            with open(fname, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return default
    else:
        return default

def save_json(data, fname):
    with open(fname, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def create_sample_questions():
    if not os.path.exists(QUESTIONS_FILE):
        sample = [
            {
                "question": "What is the output of print(2 + 3 * 4)?",
                "options": ["20", "14", "24", "None of these"],
                "answer_index": 1
            },
            {
                "question": "Which data type is immutable in Python?",
                "options": ["list", "dict", "tuple", "set"],
                "answer_index": 2
            },
            {
                "question": "What does the len() function return?",
                "options": ["Number of items", "Converts to int", "Prints value", "Creates list"],
                "answer_index": 0
            }
        ]
        save_json(sample, QUESTIONS_FILE)
        print(f"Sample questions created in {QUESTIONS_FILE}")

def add_question():
    print("\n--- Add new question ---")
    q = input("Question text: ").strip()
    options = []
    for i in range(4):
        opt = input(f"Option {i+1}: ").strip()
        options.append(opt)
    while True:
        ans = input("Correct option number (1-4): ").strip()
        if ans.isdigit() and 1 <= int(ans) <= 4:
            ans_idx = int(ans)-1
            break
        else:
            print("Please enter a number 1-4.")
    data = load_json(QUESTIONS_FILE, [])
    data.append({"question": q, "options": options, "answer_index": ans_idx})
    save_json(data, QUESTIONS_FILE)
    print("Question added.\n")

def take_quiz():
    questions = load_json(QUESTIONS_FILE, [])
    if not questions:
        print("No questions found. Please add some first.")
        return
    name = input("Your name: ").strip()
    random.shuffle(questions)
    total = len(questions)
    try:
        n = int(input(f"How many questions do you want (1-{total})? ").strip())
        if n < 1 or n > total:
            n = total
    except Exception:
        n = total
    score = 0
    for i, q in enumerate(questions[:n], start=1):
        print(f"\nQ{i}. {q['question']}")
        for idx, opt in enumerate(q['options'], start=1):
            print(f"  {idx}. {opt}")
        while True:
            ans = input("Your answer (1-4): ").strip()
            if ans.isdigit() and 1 <= int(ans) <= len(q['options']):
                ans_idx = int(ans)-1
                break
            else:
                print("Enter a valid option number.")
        if ans_idx == q.get('answer_index', 0):
            print("Correct!")
            score += 1
        else:
            correct = q['options'][q.get('answer_index', 0)]
            print(f"Wrong. Correct answer: {correct}")
    print(f"\n{name}, your score: {score}/{n}")
    scores = load_json(SCORES_FILE, [])
    scores.append({"name": name, "score": score, "total": n, "date": datetime.datetime.now().isoformat()})
    save_json(scores, SCORES_FILE)
    print("Score saved.\n")

def show_scores():
    scores = load_json(SCORES_FILE, [])
    if not scores:
        print("No scores yet.")
        return
    scores_sorted = sorted(scores, key=lambda x: (x['score']/x['total']) if x['total']>0 else 0, reverse=True)
    print("\n--- High Scores ---")
    for i, s in enumerate(scores_sorted[:10], start=1):
        pct = round((s['score']/s['total']*100),2) if s['total']>0 else 0
        print(f"{i}. {s['name']} - {s['score']}/{s['total']} ({pct}%) on {s['date'][:19]}")

def main():
    create_sample_questions()
    while True:
        print("\n--- Quiz App ---")
        print("1. Take Quiz")
        print("2. Add Question")
        print("3. Show High Scores")
        print("4. Exit")
        choice = input("Choose (1-4): ").strip()
        if choice == '1':
            take_quiz()
        elif choice == '2':
            add_question()
        elif choice == '3':
            show_scores()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Enter 1-4.")

if __name__ == '__main__':
    main()
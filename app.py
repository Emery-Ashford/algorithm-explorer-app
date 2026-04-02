import gradio as gr


# =========================
# Search Algorithms
# =========================
def parse_array(arr_str):
    try:
        return [int(x.strip()) for x in arr_str.split(",") if x.strip() != ""]
    except:
        return None


def linear_search(arr, target):
    steps = []
    for i in range(len(arr)):
        steps.append(f"Step {i + 1}: check index {i}, value = {arr[i]}")
        if arr[i] == target:
            steps.append(f"Found target {target} at index {i}.")
            return "\n".join(steps)
    steps.append(f"Target {target} was not found.")
    return "\n".join(steps)


def binary_search(arr, target):
    steps = []
    low = 0
    high = len(arr) - 1
    step_num = 1

    while low <= high:
        mid = (low + high) // 2
        steps.append(
            f"Step {step_num}: low={low}, high={high}, mid={mid}, value={arr[mid]}"
        )

        if arr[mid] == target:
            steps.append(f"Found target {target} at index {mid}.")
            return "\n".join(steps)
        elif arr[mid] < target:
            steps.append(f"{arr[mid]} < {target}, search the right half.")
            low = mid + 1
        else:
            steps.append(f"{arr[mid]} > {target}, search the left half.")
            high = mid - 1

        step_num += 1

    steps.append(f"Target {target} was not found.")
    return "\n".join(steps)


def run_search(arr_str, target, algorithm):
    arr = parse_array(arr_str)
    if arr is None:
        return "Please enter valid integers separated by commas."

    try:
        target = int(target)
    except:
        return "Please enter a valid target integer."

    if algorithm == "Linear Search":
        return linear_search(arr, target)
    else:
        sorted_arr = sorted(arr)
        result = [
            f"Binary Search requires a sorted list.",
            f"Sorted array: {sorted_arr}",
            "",
        ]
        result.append(binary_search(sorted_arr, target))
        return "\n".join(result)


# =========================
# Sorting Algorithms
# =========================
def bubble_sort(arr):
    arr = arr[:]
    steps = [f"Initial array: {arr}"]
    n = len(arr)

    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        steps.append(f"Pass {i + 1}: {arr}")
        if not swapped:
            break

    steps.append(f"Sorted array: {arr}")
    return "\n".join(steps)


def selection_sort(arr):
    arr = arr[:]
    steps = [f"Initial array: {arr}"]
    n = len(arr)

    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
        steps.append(f"Pass {i + 1}: {arr}")

    steps.append(f"Sorted array: {arr}")
    return "\n".join(steps)


def insertion_sort(arr):
    arr = arr[:]
    steps = [f"Initial array: {arr}"]

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key
        steps.append(f"Pass {i}: {arr}")

    steps.append(f"Sorted array: {arr}")
    return "\n".join(steps)


def run_sort(arr_str, algorithm):
    arr = parse_array(arr_str)
    if arr is None:
        return "Please enter valid integers separated by commas."

    if algorithm == "Bubble Sort":
        return bubble_sort(arr)
    elif algorithm == "Selection Sort":
        return selection_sort(arr)
    else:
        return insertion_sort(arr)


# =========================
# Quiz
# =========================
quiz_questions = [
    {
        "question": "Which search algorithm requires a sorted list?",
        "answer": "Binary Search",
    },
    {
        "question": "Which sorting algorithm repeatedly swaps adjacent elements?",
        "answer": "Bubble Sort",
    },
    {"question": "Which algorithm checks items one by one?", "answer": "Linear Search"},
]


def check_quiz(q1, q2, q3):
    score = 0
    feedback = []

    answers = [q1, q2, q3]

    for i in range(3):
        correct = quiz_questions[i]["answer"]
        if answers[i] == correct:
            score += 1
            feedback.append(f"Q{i + 1}: Correct")
        else:
            feedback.append(f"Q{i + 1}: Incorrect. Correct answer: {correct}")

    feedback.append(f"\nFinal Score: {score}/3")
    return "\n".join(feedback)


# =========================
# Gradio UI
# =========================
with gr.Blocks() as app:
    gr.Markdown("# Algorithm Explorer App")
    gr.Markdown("Learn and test searching and sorting algorithms interactively.")

    with gr.Tab("Search Simulator"):
        gr.Markdown("## Search for a Target Number")
        search_arr = gr.Textbox(
            label="Enter numbers separated by commas", placeholder="e.g. 8, 3, 11, 2, 7"
        )
        search_target = gr.Textbox(label="Enter target number", placeholder="e.g. 7")
        search_algo = gr.Radio(
            ["Linear Search", "Binary Search"],
            label="Choose a search algorithm",
            value="Linear Search",
        )
        search_btn = gr.Button("Run Search")
        search_output = gr.Textbox(label="Search Steps", lines=18)
        search_btn.click(
            run_search,
            inputs=[search_arr, search_target, search_algo],
            outputs=search_output,
        )

    with gr.Tab("Sorting Visualizer"):
        gr.Markdown("## Visualize Sorting Step by Step")
        sort_arr = gr.Textbox(
            label="Enter numbers separated by commas", placeholder="e.g. 9, 4, 1, 6, 2"
        )
        sort_algo = gr.Radio(
            ["Bubble Sort", "Selection Sort", "Insertion Sort"],
            label="Choose a sorting algorithm",
            value="Bubble Sort",
        )
        sort_btn = gr.Button("Run Sort")
        sort_output = gr.Textbox(label="Sorting Steps", lines=18)
        sort_btn.click(run_sort, inputs=[sort_arr, sort_algo], outputs=sort_output)

    with gr.Tab("Mini Quiz"):
        gr.Markdown("## Test Your Knowledge")
        q1 = gr.Radio(
            ["Linear Search", "Binary Search"],
            label="1. Which search algorithm requires a sorted list?",
        )
        q2 = gr.Radio(
            ["Bubble Sort", "Selection Sort", "Insertion Sort"],
            label="2. Which sorting algorithm repeatedly swaps adjacent elements?",
        )
        q3 = gr.Radio(
            ["Linear Search", "Binary Search"],
            label="3. Which algorithm checks items one by one?",
        )
        quiz_btn = gr.Button("Submit Quiz")
        quiz_output = gr.Textbox(label="Quiz Result", lines=10)
        quiz_btn.click(check_quiz, inputs=[q1, q2, q3], outputs=quiz_output)

app.launch(share=True)

import os
import re
from dotenv import load_dotenv
from ollama import chat

load_dotenv()

NUM_RUNS_TIMES = 5

# TODO: Fill this in!
YOUR_SYSTEM_PROMPT = """
You are a math master. Please think step by step when you solve the problem.

Example 1:
User: Solve this problem, then give the final answer on the last line as "Answer: <number>".
what is 2^{20} (mod 10)?
Assistant: Let's solve this step by step.
1. We need to find the last digit of 2^20, which is equivalent to computing 2^20 (mod 10).
2. Let's find the pattern of powers of 2 modulo 10:
   - 2^1 = 2 (mod 10)
   - 2^2 = 4 (mod 10)
   - 2^3 = 8 (mod 10)
   - 2^4 = 16 = 6 (mod 10)
   - 2^5 = 32 = 2 (mod 10)
3. The pattern of the last digit is 2, 4, 8, 6, which repeats every 4 powers.
4. To find the last digit of 2^20, we divide the exponent 20 by the period length 4.
5. 20 / 4 = 5 with a remainder of 0.
6. A remainder of 0 means the last digit is the 4th element in the pattern, which is 6.
Answer: 6

Example 2:
User: Solve this problem, then give the final answer on the last line as "Answer: <number>".
what is 7^{100} (mod 10)?
Assistant: Let's solve this step by step.
1. We need to find the remainder of 7^100 when divided by 10.
2. Let's find the pattern of 7^n (mod 10):
       - 7^1 = 7 (mod 10)
       - 7^2 = 49 = 9 (mod 10)
       - 7^3 = 343 = 3 (mod 10)
       - 7^4 = 2401 = 1 (mod 10)
       - 7^5 = 16807 = 7 (mod 10)
3. The sequence is 7, 9, 3, 1, and it repeats every 4 powers.
4. We divide the exponent 100 by the period length 4.
5. 100 / 4 = 25 with a remainder of 0.
6. A remainder of 0 corresponds to the 4th element in the sequence, which is 1.
Answer: 1
"""


USER_PROMPT = """
Solve this problem, then give the final answer on the last line as "Answer: <number>".

what is 3^{12345} (mod 100)?
"""


# For this simple example, we expect the final numeric answer only
EXPECTED_OUTPUT = "Answer: 43"


def extract_final_answer(text: str) -> str:
    """Extract the final 'Answer: ...' line from a verbose reasoning trace.

    - Finds the LAST line that starts with 'Answer:' (case-insensitive)
    - Normalizes to 'Answer: <number>' when a number is present
    - Falls back to returning the matched content if no number is detected
    """
    matches = re.findall(r"(?mi)^\s*answer\s*:\s*(.+)\s*$", text)
    if matches:
        value = matches[-1].strip()
        # Prefer a numeric normalization when possible (supports integers/decimals)
        num_match = re.search(r"-?\d+(?:\.\d+)?", value.replace(",", ""))
        if num_match:
            return f"Answer: {num_match.group(0)}"
        return f"Answer: {value}"
    return text.strip()


def test_your_prompt(system_prompt: str) -> bool:
    """Run up to NUM_RUNS_TIMES and return True if any output matches EXPECTED_OUTPUT.

    Prints "SUCCESS" when a match is found.
    """
    for idx in range(NUM_RUNS_TIMES):
        print(f"Running test {idx + 1} of {NUM_RUNS_TIMES}")
        response = chat(
            model="llama3.1:8b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": USER_PROMPT},
            ],
            options={"temperature": 0.3},
        )
        output_text = response.message.content
        final_answer = extract_final_answer(output_text)
        if final_answer.strip() == EXPECTED_OUTPUT.strip():
            print("SUCCESS")
            return True
        else:
            print(f"Expected output: {EXPECTED_OUTPUT}")
            print(f"Actual output: {final_answer}")
    return False


if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)

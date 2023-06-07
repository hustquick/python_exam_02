import random
import string

# 生成选择题
def generate_multiple_choice(n):
    multiple_choice = []
    for i in range(n):
        question = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
        options = ["".join(random.choices(string.ascii_lowercase + string.digits, k=5)) for _ in range(4)]
        answer = random.choice(options)
        multiple_choice.append({
            "题目": question,
            "选项": options,
            "答案": answer,
        })
    return multiple_choice

# 生成判断题
def generate_true_or_false(n):
    true_or_false = []
    for i in range(n):
        question = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
        answer = random.choice([True, False])
        true_or_false.append({
            "题目": question,
            "答案": answer,
        })
    return true_or_false

# 生成题库
def generate_question_bank(n_multiple_choice, n_true_or_false):
    multiple_choice = generate_multiple_choice(n_multiple_choice)
    true_or_false = generate_true_or_false(n_true_or_false)
    return multiple_choice, true_or_false


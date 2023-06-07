import pandas as pd
import random
import string

# 生成选择题
def generate_multiple_choice(n):
    multiple_choice = []
    for i in range(n):
        question = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
        options = ["".join(random.choices(string.ascii_lowercase + string.digits, k=5)) for _ in range(4)]
        answer_index = random.randint(0, 3)
        answer = chr(ord('A') + answer_index)  # Convert answer index to letter A, B, C, or D
        options[answer_index] = answer  # Replace the actual answer with the letter
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



# 将题库写入Excel文件
def write_to_excel(multiple_choice, true_or_false, filename):
    with pd.ExcelWriter(filename) as writer:
        multiple_choice_df = pd.DataFrame(multiple_choice)
        true_or_false_df = pd.DataFrame(true_or_false)
        # Write the dataframes to separate sheets in the Excel file
        multiple_choice_df.to_excel(writer, sheet_name='选择题', index=False)
        true_or_false_df.to_excel(writer, sheet_name='判断题', index=False)

# 使用示例
multiple_choice, true_or_false = generate_question_bank(50, 50)
write_to_excel(multiple_choice, true_or_false, '题库.xlsx')


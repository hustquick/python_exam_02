import pandas as pd
import random

class ExamPaperGenerator:
    def __init__(self, filename, n_mc, n_tf):
        self.filename = filename
        self.n_mc = n_mc
        self.n_tf = n_tf
        self.mc_questions = pd.read_excel(filename, sheet_name='选择题').to_dict('records')
        self.tf_questions = pd.read_excel(filename, sheet_name='判断题').to_dict('records')
        self.papers = {}
        self.answers = {}  # 添加一个新的属性来保存学生的答案

    def generate_paper(self, student_id):
        mc_paper = random.sample(self.mc_questions, self.n_mc)
        tf_paper = random.sample(self.tf_questions, self.n_tf)
        self.papers[student_id] = {
            "选择题": mc_paper,
            "判断题": tf_paper,
            "选择题答案": [],
            "判断题答案": [],
        }

    def add_answer(self, student_id, question_type, answer):
        self.papers[student_id][f"{question_type}答案"].append(answer)

    def calculate_score(self, student_id):
        score = 0
        paper = self.papers[student_id]
        for question_type in ["选择题", "判断题"]:
            for question, answer in zip(paper[question_type], paper[f"{question_type}答案"]):
                if question["答案"] == answer:
                    score += 1
        return score

    def record_answer(self, student_id, question_type, question, answer):
        if student_id not in self.answers:
            self.answers[student_id] = {}

        if question_type not in self.answers[student_id]:
            self.answers[student_id][question_type] = {}

        self.answers[student_id][question_type][question] = answer

    def score_paper(self, student_id):
        score = 0
        paper = self.papers[student_id]
        for question_type in paper:
            for question in paper[question_type]:
                if '答案' in question and '学生答案' in question:
                    if question['答案'] == question['学生答案']:
                        score += 1
        return score


import ast
import tkinter as tk
from tkinter import messagebox
# from exam_generator import ExamGenerator
import logging


class ExamInterface:
    def __init__(self, master, generator ):
        self.master = master
        self.generator = generator

        self.student_id_label = tk.Label(master, text="学号")
        self.student_id_entry = tk.Entry(master)
        self.start_button = tk.Button(master, text="开始答题", command=self.start_exam)

        self.question_label = tk.Label(master)
        self.options_frame = tk.Frame(master)
        self.option_vars = []

        self.answer_entry = tk.Entry(self.master)
        self.option_var = tk.StringVar()  # 添加此行

        self.next_button = tk.Button(master, text="下一题", command=self.next_question)
        self.submit_button = tk.Button(master, text="完成答题", command=self.submit_exam)

        self.student_id_label.pack()
        self.student_id_entry.pack()
        self.start_button.pack()

    def start_exam(self):
        self.current_question_type = "选择题"
        self.current_question = 0
        self.student_id = self.student_id_entry.get()
        if self.student_id:
            self.generator.generate_paper(self.student_id)

            self.student_id_label.pack_forget()
            self.student_id_entry.pack_forget()
            self.start_button.pack_forget()

            self.question_label.pack()
            self.options_frame.pack()
            self.answer_entry.pack()  # 在界面上显示答案输入框
            self.next_button.pack()

            self.display_question()

    def display_question(self):
        # 清除旧的选项
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        # 获取当前题目信息
        question = self.generator.papers[self.student_id][self.current_question_type][self.current_question]

        # 显示题目
        self.question_label["text"] = f"{self.current_question + 1}. {question['题目']}"

        # 处理选项
        if self.current_question_type == '选择题':
            options = ast.literal_eval(question["选项"])  # 从字符串转换回列表
            self.option_var = tk.StringVar()
            for i, option in enumerate(options):
                rb = tk.Radiobutton(self.options_frame, text=f"{chr(65 + i)}. {option}", variable=self.option_var,
                                    value=chr(65 + i), indicatoron=0, width=20, padx=10, pady=5)

                rb.pack(fill='both')

        else:  # 判断题
            self.option_var = tk.StringVar()
            options = ['对', '错']
            for i, option in enumerate(options):
                rb = tk.Radiobutton(self.options_frame, text=option, variable=self.option_var, value=option,
                                    indicatoron=0, width=20, padx=20, pady=5)
                rb.pack(fill='both')

    def next_question(self):
        answer = self.option_var.get()
        self.generator.record_answer(self.student_id, self.current_question_type, self.current_question, answer)
        print(
            f"Student ID: {self.student_id}, Question Type: {self.current_question_type}, Question: {self.current_question}, Answer: {answer}")
        if self.current_question_type == "选择题":
            answer = self.option_var.get()
        elif self.current_question_type == "判断题":
            answer = self.answer_entry.get()
        self.generator.record_answer(self.student_id, self.current_question_type, self.current_question, answer)

        selected_option = None
        for rb in self.options_frame.winfo_children():
            if rb['variable'] == self.option_var and rb['value'] == self.option_var.get():
                selected_option = rb['text'].split('. ')[1]
                break

        logging.debug(f'Student answer: {selected_option}')  # 调试语句
        # Add some debugging prints here.
        # logging.debug(f'Current question type: {self.current_question_type}')
        # logging.debug(f'Current question: {self.current_question}')
        # logging.debug(f'Answer: {answer}')

        # If we have finished all questions of current type, switch to next type.
        if self.current_question + 1 >= len(self.generator.papers[self.student_id][self.current_question_type]):
            if self.current_question_type == "选择题":
                self.current_question_type = "判断题"
                self.current_question = 0
            else:
                # If we have finished all types of questions, show submit button.
                self.next_button.pack_forget()
                self.submit_button.pack()
                return

        # If we haven't finished current type of questions, go to next question.
        self.current_question += 1
        self.display_question()

    def submit_exam(self):
        answer = self.option_var.get()
        self.generator.record_answer(self.student_id, self.current_question_type, self.current_question, answer)
        print(
            f"Student ID: {self.student_id}, Question Type: {self.current_question_type}, Question: {self.current_question}, Answer: {answer}")
        selected_option = None
        for rb in self.options_frame.winfo_children():
            if rb['variable'] == self.option_var and rb['value'] == self.option_var.get():
                selected_option = rb['text'].split('. ')[1]
                break

        logging.debug(f'Student answer: {selected_option}')  # 调试语句
        # 评分
        score = self.generator.score_paper(self.student_id)
        messagebox.showinfo("考试结束！", f"你的分数是：{score}")

        self.master.quit()

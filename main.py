import tkinter as tk
from exam_interface import ExamInterface
from exam_paper_generator import ExamPaperGenerator

root = tk.Tk()

# 创建试卷生成器实例
generator = ExamPaperGenerator('题库.xlsx', 10, 10)

# 创建并启动考试界面
app = ExamInterface(root, generator)
root.mainloop()


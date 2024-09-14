import tkinter as tk
from PIL import Image, ImageTk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class ImageApp(tk.Tk):
    def __init__(self, gen_image_func, watch_file_path):
        super().__init__()
        self.gen_image_func = gen_image_func
        self.watch_file_path = watch_file_path
        self.image = None
        self.photo = None

        self.last_call_resize_time = time.time()

        # 创建一个标签用于显示图片
        self.label = tk.Label(self)
        self.label.pack(fill=tk.BOTH, expand=True)

        # 绑定窗口大小变化事件
        self.bind("<Configure>", self.on_resize)

        # 初始化显示图片
        self.update_image()

        # 监控文件系统
        self.event_handler = FileChangeHandler(self)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, path='.', recursive=False)
        self.observer.start()

    def update_image(self):
        # 使用 gen_image_func 生成图片
        self.image = self.gen_image_func(self.watch_file_path)
        self.display_image()

    def display_image(self):
        if self.image:
            # 获取当前窗口大小
            window_width = self.winfo_width()
            window_height = self.winfo_height()

            # 获取图片的原始尺寸
            image_width, image_height = self.image.size

            # 计算缩放比例以适应窗口
            scale = min(window_width / image_width, window_height / image_height)
            new_width = int(image_width * scale)
            new_height = int(image_height * scale)

            if new_height <= 0:
                new_height = 200
            if new_width <= 0:
                new_width = 200

            # 调整图片大小
            resized_image = self.image.resize((new_width, new_height))
            self.photo = ImageTk.PhotoImage(resized_image)

            # 更新标签显示
            self.label.config(image=self.photo)
            self.label.image = self.photo

    def on_resize(self, event):
        # 窗口大小变化时重新调整图片
        if time.time() - self.last_call_resize_time > 0.1:
            self.last_call_resize_time = time.time()
            self.display_image()

    def on_file_change(self):
        # 当文件发生变化时，更新图片
        self.update_image()

    def on_closing(self):
        # 关闭窗口时停止观察
        self.observer.stop()
        self.observer.join()
        self.destroy()

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, app):
        self.app = app

    def on_modified(self, event):
        if event.src_path.endswith(self.app.watch_file_path):
            self.app.on_file_change()

def start_real_time_watcher(gen_image_func, yaml_file_path) -> None:
    img_app = ImageApp(gen_image_func, yaml_file_path)
    img_app.protocol("WM_DELETE_WINDOW", img_app.on_closing)
    img_app.mainloop()
    return

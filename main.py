import tkinter as tk
from tkinter import ttk
import json
import keyboard
import subprocess
import os
from tkinter import filedialog
import random
import time
import threading

# 修改语言配置结构
TRANSLATIONS = {
    'title': {
        'en': 'LICHARSE 工具箱 v2.0',
        'zh': 'LICHARSE 工具箱 v2.0'
    },
    'add_tool': {
        'en': '[ INITIALIZE NEW TOOL ]',
        'zh': '[ 初始化新工具 ]'
    },
    'powered_by': {
        'en': '由您的想象力驱动',
        'zh': '由您的想象力驱动'
    },
    'system_ready': {
        'en': 'System Ready...',
        'zh': '系统就绪...'
    },
    'add_new_tool': {
        'en': '[ ADD NEW TOOL ]',
        'zh': '[ 添加新工具 ]'
    },
    'tool_name': {
        'en': '[*] TOOL NAME:',
        'zh': '[*] 工具名称:'
    },
    'select_tool_type': {
        'en': ' SELECT TOOL TYPE ',
        'zh': ' 选择工具类型 '
    },
    'file_path': {
        'en': ' FILE PATH ',
        'zh': ' 文件路径 '
    },
    'no_file': {
        'en': 'No file selected...',
        'zh': '未选择文件...'
    },
    'select_file': {
        'en': '[ SELECT FILE ]',
        'zh': '[ 选择文件 ]'
    },
    'confirm': {
        'en': '[ CONFIRM ]',
        'zh': '[ 确认 ]'
    },
    'exe_program': {
        'en': 'Direct EXE Program',
        'zh': '直接执行程序'
    },
    'script_program': {
        'en': 'Python Script',
        'zh': 'Python脚本'
    },
    'custom_command': {
        'en': 'Custom Command',
        'zh': '自定义命令'
    },
    'param_placeholder': {
        'en': 'Enter parameters (optional)',
        'zh': '输入参数（可选）'
    },
    'command_placeholder': {
        'en': 'Enter command (e.g., python -m pip install xxx)',
        'zh': '输入命令 (例如: python -m pip install xxx)'
    },
    'run_mode': {
        'en': ' RUN MODE ',
        'zh': ' 运行模式 '
    },
    'show_console': {
        'en': 'Show Console Window',
        'zh': '显示控制台窗口'
    },
    'save_success': {
        'en': 'Tool added successfully',
        'zh': '工具添加成功'
    },
    'save_error': {
        'en': 'Please fill in all required fields',
        'zh': '请填写所有必填项'
    },
    'system_hibernate': {
        'en': 'System Hibernating...',
        'zh': '系统休眠中...'
    },
    'init_launch': {
        'en': 'INITIALIZING LAUNCH SEQUENCE...',
        'zh': '初始化启动序列...'
    },
    'launch_success': {
        'en': 'PROGRAM {} LAUNCHED SUCCESSFULLY',
        'zh': '程序 {} 启动成功'
    },
    'working_dir': {
        'en': 'Working Directory (Optional)',
        'zh': '工作目录（可选）'
    },
    'startup_messages': {
        'en': [
            "INITIALIZING SYSTEM...",
            "LOADING CORE MODULES...",
            "CHECKING SECURITY PROTOCOLS...",
            "ESTABLISHING SECURE CONNECTION...",
            "SCANNING NETWORK INTERFACES...",
            "BYPASSING SECURITY...",
            "ACCESS GRANTED - WELCOME LICHARSE"
        ],
        'zh': [
            "初始化系统...",
            "加载核心模块...",
            "检查安全协议...",
            "建立安全连接...",
            "扫描网络接口...",
            "绕过安全验证...",
            "访问授权 - 欢迎 LICHARSE"
        ]
    },
    'categories': {
        'en': {
            'webshell': 'WebShell Tools',
            'info_collect': 'Information Collection',
            'exploit': 'Exploit Tools',
            'post': 'Post Exploitation',
            'other': 'Other Tools'
        },
        'zh': {
            'webshell': 'WebShell管理工具',
            'info_collect': '信息收集',
            'exploit': '漏洞利用工具',
            'post': '后渗透工具',
            'other': '其他工具'
        }
    },
    'jar_program': {
        'en': 'Java JAR Program',
        'zh': 'Java JAR程序'
    }
}

class Style:
    BG = '#000000'
    FG = '#00ff00'
    TITLE_BG = '#001100'
    ACTIVE_BG = '#003300'
    ERROR_FG = '#ff0000'
    INACTIVE_FG = '#555555'
    FONT = 'Consolas'
    
    @staticmethod
    def create_button(parent, text, command, **kwargs):
        """创建统一样式的按钮"""
        config = {
            'bg': Style.TITLE_BG,
            'fg': Style.FG,
            'font': (Style.FONT, kwargs.pop('size', 10), kwargs.pop('weight', '')),
            'relief': kwargs.pop('relief', 'solid'),
            'bd': kwargs.pop('bd', 1),
            'activebackground': Style.ACTIVE_BG,
            'activeforeground': Style.FG
        }
        config.update(kwargs)
        return tk.Button(parent, text=text, command=command, **config)
    
    @staticmethod
    def create_label(parent, text, **kwargs):
        """创建统一样式的标签"""
        config = {
            'bg': Style.BG,
            'fg': Style.FG,
            'font': (Style.FONT, kwargs.pop('size', 10))
        }
        config.update(kwargs)
        return tk.Label(parent, text=text, **config)
    
    @staticmethod
    def create_frame(parent, **kwargs):
        """创建统一样式的框架"""
        config = {'bg': Style.BG}
        config.update(kwargs)
        return tk.Frame(parent, **config)

TOOL_ICONS = {
    'exe': '⚡',
    'script': '🐍',
    'custom': '⌨️',
    'default': '📌'
}

def create_tool_button(parent, tool, command, **kwargs):
    """创建工具按钮"""
    icon = TOOL_ICONS.get(tool['type'], TOOL_ICONS['default'])
    btn = Style.create_button(
        parent,
        text=f"{icon} {tool['name']}",
        command=command,
        width=45,
        anchor='w',
        padx=10,
        **kwargs
    )
    
    def on_hover(enter):
        btn.config(bg=Style.ACTIVE_BG if enter else Style.TITLE_BG)
    
    btn.bind('<Enter>', lambda e: on_hover(True))
    btn.bind('<Leave>', lambda e: on_hover(False))
    return btn

class DraggableMixin:
    def init_drag(self, handle):
        """初始化拖动功能"""
        handle.bind('<Button-1>', self.start_move)
        handle.bind('<B1-Motion>', self.do_move)
    
    def start_move(self, event):
        self.x = event.x_root - self.winfo_x()
        self.y = event.y_root - self.winfo_y()
    
    def do_move(self, event):
        x = event.x_root - self.x
        y = event.y_root - self.y
        self.geometry(f"+{x}+{y}")

def center_window(window):
    """使窗口居中显示"""
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"+{x}+{y}")

class MatrixEffect:
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.chars = ['0', '1'] + [chr(i) for i in range(65, 91)]  # 数字和字母
        self.streams = []
        self.running = True
        
    def create_stream(self):
        x = random.randint(0, self.width - 20)
        speed = random.uniform(0.1, 0.3)
        length = random.randint(5, 15)
        return {'x': x, 'y': -length, 'speed': speed, 'length': length, 'chars': []}
        
    def update(self):
        while self.running:
            self.canvas.delete('matrix')
            
            # 创建新流
            if len(self.streams) < 10 and random.random() < 0.1:
                self.streams.append(self.create_stream())
            
            # 更新现有流
            for stream in self.streams[:]:
                stream['y'] += stream['speed']
                
                # 生成字符
                while len(stream['chars']) < stream['length']:
                    stream['chars'].append(random.choice(self.chars))
                
                # 绘制字符
                for i, char in enumerate(stream['chars']):
                    y = stream['y'] + i
                    if 0 <= y < self.height:
                        color = f'#{0:02x}ff{0:02x}' if i == 0 else '#00ff00'
                        self.canvas.create_text(
                            stream['x'], y,
                            text=char,
                            fill=color,
                            font=('Consolas', 8),
                            tags='matrix'
                        )
                
                # 移除超出屏幕的流
                if stream['y'] > self.height:
                    self.streams.remove(stream)
            
            time.sleep(0.05)

class ToolBox:
    def __init__(self):
        self.window = tk.Tk()
        self.lang = 'en'  # 默认语言
        self.window.title(TRANSLATIONS['title'][self.lang])
        self.window.geometry("600x700")
        
        # 初始化分类
        self.current_category = None
        self.tools = []  # 初始化工具列表
        
        # 设置窗口图标
        try:
            self.window.iconbitmap('icon.png')
        except:
            pass  # 如果图标文件不存在，使用默认图标
        
        # 设置窗口样式
        self.window.attributes('-topmost', True, '-alpha', 0.9)
        self.window.withdraw()
        self.window.overrideredirect(True)
        
        # 设置黑客风格
        self.window.configure(bg='#000000')
        
        # 添加标题栏（移到最顶部）
        self.title_frame = tk.Frame(self.window, bg='#001100', height=30)
        self.title_frame.pack(fill=tk.X, side=tk.TOP, pady=0)
        self.title_frame.pack_propagate(False)
        
        # Logo
        self.logo_label = tk.Label(
            self.title_frame,
            text=TRANSLATIONS['title'][self.lang],
            bg='#001100',
            fg='#00ff00',
            font=('Consolas', 12, 'bold')
        )
        self.logo_label.pack(side=tk.LEFT, padx=10)
        
        # 添加语言切换按钮
        self.create_language_button()
        
        # 关闭按钮
        close_btn = tk.Button(
            self.title_frame,
            text="×",
            command=self.window.withdraw,
            bg='#001100',
            fg='#00ff00',
            font=('Consolas', 12, 'bold'),
            relief='flat',
            bd=0,
            activebackground='#003300',
            activeforeground='#ff0000',
            width=2
        )
        close_btn.pack(side=tk.RIGHT, padx=5)
        
        # 创建主容器
        self.main_container = tk.Frame(self.window, bg='#000000')
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # 状态栏（移到标题栏下方）
        self.status_label = tk.Label(
            self.window,
            text=TRANSLATIONS['system_ready'][self.lang],
            bg='#000000',
            fg='#00ff00',
            font=('Consolas', 9),
            anchor='w'
        )
        self.status_label.pack(fill=tk.X, padx=10, pady=5)  # 放在标题栏下方
        
        # 添加ASCII艺术标题
        self.ascii_label = tk.Label(
            self.main_container,
            text=self.get_ascii_art(),
            bg='#000000',
            fg='#00ff00',
            font=('Consolas', 8),
            justify=tk.LEFT
        )
        self.ascii_label.pack(pady=10)
        
        style = ttk.Style()
        style.configure('Hack.TFrame', background='#000000')
        style.configure('Hack.TButton',
            background='#000000',
            foreground='#00ff00',
            borderwidth=1,
            relief='solid',
            font=('Consolas', 10))
        style.configure('Hack.TLabel',
            background='#000000',
            foreground='#00ff00',
            font=('Consolas', 10))
        
        # 创建左侧分类栏和右侧工具区
        self.main_paned = tk.PanedWindow(
            self.main_container,
            orient=tk.HORIZONTAL,
            bg='#000000',
            sashwidth=2,
            sashpad=1,
            showhandle=False,
            sashrelief='solid'
        )
        self.main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建左侧分类栏
        self.category_frame = Style.create_frame(self.main_paned)
        self.main_paned.add(self.category_frame, width=200)
        
        # 创建右侧工具列表区
        self.tool_container = Style.create_frame(self.main_paned)
        self.main_paned.add(self.tool_container, width=300)
        
        # 创建工具列表框架
        self.tool_frame = Style.create_frame(self.tool_container)
        self.tool_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建分类按钮
        self.create_categories()
        
        # 加载工具列表
        self.create_widgets()
        self.load_tools()
        
        # 注册快捷键 (Ctrl+Alt+T)
        keyboard.add_hotkey('ctrl+alt+t', self.toggle_window)
        
        # 使主窗口可拖动
        self.title_frame.bind('<Button-1>', self.start_move)
        self.title_frame.bind('<B1-Motion>', self.do_move)

    def create_language_button(self):
        lang_btn = tk.Button(
            self.title_frame,
            text="EN/中",
            command=self.toggle_language,
            bg='#001100',
            fg='#00ff00',
            font=('Consolas', 10, 'bold'),
            relief='flat',
            bd=0,
            activebackground='#003300',
            activeforeground='#00ff00',
            width=4
        )
        lang_btn.pack(side=tk.RIGHT, padx=5)

    def toggle_language(self):
        self.lang = 'zh' if self.lang == 'en' else 'en'
        self.update_texts()
        
        # 如果有打开的添加工具对话框，也更新它的语言
        for widget in self.window.winfo_children():
            if isinstance(widget, tk.Toplevel):
                dialog = widget.children.get('!addtooldialog')
                if dialog:
                    dialog.lang = self.lang
                    dialog.update_texts()

    def update_texts(self):
        # 更新窗口标题
        self.window.title(self.get_text('title'))
        
        # 更新标题栏
        self.logo_label.config(text=self.get_text('title'))
        
        # 更新状态栏
        self.status_label.config(text=self.get_text('system_ready'))
        
        # 更新添加工具按钮
        self.add_btn.config(text=self.get_text('add_tool'))
        
        # 更新ASCII艺术标题
        self.ascii_label.config(text=self.get_ascii_art())
        
        # 更新分类按钮文本
        categories = [
            ('webshell', '📁', TRANSLATIONS['categories'][self.lang]['webshell']),
            ('info_collect', '🔍', TRANSLATIONS['categories'][self.lang]['info_collect']),
            ('exploit', '⚡', TRANSLATIONS['categories'][self.lang]['exploit']),
            ('post', '🔧', TRANSLATIONS['categories'][self.lang]['post']),
            ('other', '📌', TRANSLATIONS['categories'][self.lang]['other'])
        ]
        
        # 更新分类按钮
        for btn, cat_id, icon in self.category_buttons:
            btn.config(text=f"{icon} {TRANSLATIONS['categories'][self.lang][cat_id]}")
        
        # 平滑切换效果
        def fade_text(widget, new_text, steps=10):
            original_fg = widget.cget('fg')
            for i in range(steps):
                alpha = 1 - (i / steps)
                color = f'#{int(alpha*255):02x}ff{int(alpha*255):02x}'
                widget.config(fg=color)
                self.window.update()
                time.sleep(0.01)
            widget.config(text=new_text)
            for i in range(steps):
                alpha = i / steps
                color = f'#{int(alpha*255):02x}ff{int(alpha*255):02x}'
                widget.config(fg=color)
                self.window.update()
                time.sleep(0.01)
            widget.config(fg=original_fg)
        
        # 对重要文本应用淡入淡出效果
        fade_text(self.logo_label, self.get_text('title'))
        fade_text(self.status_label, self.get_text('system_ready'))
        
        # 刷新工具列表
        self.refresh_tool_list()

    def create_widgets(self):
        # 创建工具列表容器
        self.tool_frame = tk.Frame(self.main_container, bg='#000000')
        self.tool_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 添加工具按钮
        self.add_btn = tk.Button(
            self.main_container,
            text=TRANSLATIONS['add_tool'][self.lang],
            command=self.add_tool,
            bg='#001100',
            fg='#00ff00',
            font=('Consolas', 10, 'bold'),
            relief='solid',
            bd=1,
            activebackground='#003300',
            activeforeground='#00ff00'
        )
        self.add_btn.pack(pady=10)

    def add_tool(self):
        dialog = AddToolDialog(self.window, self)
        
    def load_tools(self):
        try:
            with open('tools.json', 'r', encoding='utf-8') as f:
                self.tools = json.load(f)
                self.refresh_tool_list()
        except FileNotFoundError:
            self.tools = []

    def save_tools(self):
        with open('tools.json', 'w', encoding='utf-8') as f:
            json.dump(self.tools, f, ensure_ascii=False, indent=2)

    def refresh_tool_list(self):
        for widget in self.tool_frame.winfo_children():
            widget.destroy()
        
        # 筛选当前分类的工具
        filtered_tools = [
            tool for tool in self.tools 
            if tool.get('category', 'other') == self.current_category
        ] if self.current_category else self.tools
        
        for i, tool in enumerate(filtered_tools):
            # 创建工具容器
            tool_frame = Style.create_frame(self.tool_frame)
            tool_frame.pack(fill=tk.X, pady=2)
            
            # 创建主内容框架
            content_frame = Style.create_frame(tool_frame)
            content_frame.pack(fill=tk.X, padx=1)
            
            # 创建工具信息区
            info_frame = Style.create_frame(content_frame)
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # 工具名称和图标
            name_frame = Style.create_frame(info_frame)
            name_frame.pack(fill=tk.X, pady=2)
            
            # 工具类型图标
            type_indicators = {
                'exe': '⚡ GUI应用',
                'script': '🐍 命令行',
                'custom': '⌨️ 命令行'
            }
            indicator = type_indicators.get(tool['type'], '📌')
            
            # 工具名称按钮
            tool_btn = Style.create_button(
                name_frame,
                text=f"{tool['name']}",
                command=lambda t=tool: self.run_tool(t),
                bg='#000000',
                fg='#00ffff',  # 荧光蓝色
                font=(Style.FONT, 10),
                relief='flat',
                bd=0,
                anchor='w',
                padx=5
            )
            tool_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # 工具类型标签
            tk.Label(
                name_frame,
                text=indicator,
                bg='#000000',
                fg='#666666',  # 暗灰色
                font=(Style.FONT, 9)
            ).pack(side=tk.RIGHT, padx=5)
            
            # 创建底部信息栏
            bottom_frame = Style.create_frame(info_frame)
            bottom_frame.pack(fill=tk.X)
            
            # 添加工具路径/命令信息
            path_text = tool.get('params', '') if tool['type'] == 'custom' else tool.get('path', '')
            tk.Label(
                bottom_frame,
                text=path_text,
                bg='#000000',
                fg='#444444',  # 更暗的灰色
                font=(Style.FONT, 8)
            ).pack(side=tk.LEFT, padx=5)
            
            # 创建右侧控制区
            control_frame = Style.create_frame(content_frame)
            control_frame.pack(side=tk.RIGHT, fill=tk.Y)
            
            # 运行按钮
            run_btn = Style.create_button(
                control_frame,
                text="运行",
                command=lambda t=tool: self.run_tool(t),
                bg='#000000',
                fg='#00ffff',
                font=(Style.FONT, 9),
                relief='flat',
                bd=0,
                width=6
            )
            run_btn.pack(side=tk.LEFT, padx=5)
            
            # 删除按钮
            del_btn = Style.create_button(
                control_frame,
                text="×",
                command=lambda idx=i: self.delete_tool(idx),
                bg='#000000',
                fg='#666666',
                font=(Style.FONT, 9),
                relief='flat',
                bd=0,
                width=2
            )
            del_btn.pack(side=tk.RIGHT, padx=2)
            
            # 添加荧光边框效果
            def create_border(parent, color='#00ffff'):
                tk.Frame(parent, bg=color, height=1).pack(side=tk.TOP, fill=tk.X)
                tk.Frame(parent, bg=color, height=1).pack(side=tk.BOTTOM, fill=tk.X)
            
            create_border(tool_frame)

    def delete_tool(self, index):
        self.update_status(f"Removing {self.tools[index]['name']}...")
        del self.tools[index]
        self.save_tools()
        self.refresh_tool_list()

    def update_status(self, message):
        self.status_label.config(text=f"[*] {message}")
        self.window.after(2000, lambda: self.status_label.config(text="System Ready..."))

    def toggle_window(self):
        if self.window.state() == 'withdrawn':
            self.window.deiconify()
            self.window.update_idletasks()
            
            # 居中显示
            width = self.window.winfo_width()
            height = self.window.winfo_height()
            x = (self.window.winfo_screenwidth() // 2) - (width // 2)
            y = (self.window.winfo_screenheight() // 2) - (height // 2)
            self.window.geometry(f'+{x}+{y}')
            
            # 添加启动动画效果
            self.show_startup_animation()
        else:
            self.update_status(TRANSLATIONS['system_hibernate'][self.lang])
            self.window.after(500, self.window.withdraw)

    def show_startup_animation(self):
        messages = TRANSLATIONS['startup_messages'][self.lang]
        
        def show_message(index=0):
            if index < len(messages):
                msg = messages[index]
                # 添加进度条效果
                progress = "=" * (index + 1) + ">" + "." * (len(messages) - index - 1)
                formatted_msg = f"[{progress}] {msg}"
                
                # 添加打字机效果
                self.status_label.config(text="")
                for i in range(len(formatted_msg)):
                    self.status_label.config(
                        text=formatted_msg[:i+1] + "█"
                    )
                    self.window.update()
                    time.sleep(0.02)
                
                # 随机添加一些"黑客"效果
                if random.random() < 0.3:
                    for _ in range(3):
                        self.status_label.config(
                            text=formatted_msg + random.choice(["█", "▓", "▒", "░"])
                        )
                        self.window.update()
                        time.sleep(0.1)
                
                self.window.after(300, lambda: show_message(index + 1))
        
        show_message()

    def run_tool(self, tool):
        self.update_status(TRANSLATIONS['init_launch'][self.lang])
        time.sleep(0.3)
        
        try:
            if tool['type'] == 'custom':
                # 自定义命令
                command = tool['params']
                working_dir = tool.get('working_dir', '')
                
                if tool.get('show_console', True):
                    subprocess.Popen(
                        command,
                        shell=True,
                        creationflags=subprocess.CREATE_NEW_CONSOLE,
                        cwd=working_dir if working_dir else None
                    )
                else:
                    subprocess.Popen(
                        command,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        cwd=working_dir if working_dir else None
                    )
            elif tool['type'] == 'script':
                # Python脚本
                cmd = ['python', tool['path']]
                if tool.get('show_console', True):
                    subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
                else:
                    subprocess.Popen(cmd)
            elif tool['type'] == 'jar':
                # JAR程序
                cmd = ['java', '-jar', tool['path']]
                if tool.get('show_console', True):
                    subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
                else:
                    subprocess.Popen(cmd)
            else:
                # EXE程序
                if tool.get('show_console', True):
                    subprocess.Popen(tool['path'], creationflags=subprocess.CREATE_NEW_CONSOLE)
                else:
                    subprocess.Popen(tool['path'])
            
            self.update_status(TRANSLATIONS['launch_success'][self.lang].format(tool['name']))
            self.window.after(1000, self.window.withdraw)
            
        except Exception as e:
            self.update_status(f"Error: {str(e)}")

    def start_move(self, event):
        self.x = event.x_root - self.window.winfo_x()
        self.y = event.y_root - self.window.winfo_y()

    def do_move(self, event):
        x = event.x_root - self.x
        y = event.y_root - self.y
        self.window.geometry(f"+{x}+{y}")

    def get_ascii_art(self):
        """获取 ASCII 艺术标题"""
        return """
╔══════════════════════════════════════════════════╗
║    ██╗     ██╗ ██████╗██╗  ██╗ █████╗ ██████╗    ║
║    ██║     ██║██╔════╝██║  ██║██╔══██╗██╔══██╗   ║
║    ██║     ██║██║     ███████║███████║██████╔╝   ║
║    ██║     ██║██║     ██╔══██║██╔══██║██╔══██╗   ║
║    ███████╗██║╚██████╗██║  ██║██║  ██║██║  ██║   ║
║    ╚══════╝╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ║
║                                                  ║
║              LICHARSE 工具箱 v2.0                 ║
║                由您的想象力驱动                    ║
╚══════════════════════════════════════════════════╝
"""

    def get_text(self, key):
        """获取当前语言的文本"""
        return TRANSLATIONS[key][self.lang]

    def create_categories(self):
        """创建分类按钮"""
        self.category_buttons = []  # 保存按钮引用以便后续更新
        categories = [
            ('webshell', '📁'),
            ('info_collect', '🔍'),
            ('exploit', '⚡'),
            ('post', '🔧'),
            ('other', '📌')
        ]
        
        for cat_id, icon in categories:
            cat_frame = Style.create_frame(self.category_frame)
            cat_frame.pack(fill=tk.X, pady=1)
            
            btn = Style.create_button(
                cat_frame,
                text=f"{icon} {TRANSLATIONS['categories'][self.lang][cat_id]}",
                command=lambda c=cat_id: self.switch_category(c),
                bg='#000000',
                fg='#00ffff',
                font=(Style.FONT, 9),
                relief='flat',
                bd=0,
                anchor='w',
                padx=10,
                width=25
            )
            btn.pack(fill=tk.X)
            self.category_buttons.append((btn, cat_id, icon))  # 保存按钮和相关信息
            
            # 添加荧光边框
            def create_border(parent, color='#00ffff'):
                tk.Frame(parent, bg=color, height=1).pack(side=tk.TOP, fill=tk.X)
                tk.Frame(parent, bg=color, height=1).pack(side=tk.BOTTOM, fill=tk.X)
            
            create_border(cat_frame)
    
    def switch_category(self, category):
        """切换分类"""
        self.current_category = category
        self.refresh_tool_list()

class AddToolDialog:
    def __init__(self, parent, toolbox):
        self.dialog = tk.Toplevel(parent)
        self.toolbox = toolbox
        self.lang = toolbox.lang
        
        # 设置对话框样式
        self.dialog.configure(bg='#000000')
        self.dialog.overrideredirect(True)  # 隐藏标准窗口边框
        self.dialog.geometry("500x800")
        
        # 标题栏
        self.title_frame = tk.Frame(self.dialog, bg='#001100', height=35)
        self.title_frame.pack(fill=tk.X, side=tk.TOP, pady=0)
        self.title_frame.pack_propagate(False)
        
        # 标题文本
        self.title_label = tk.Label(
            self.title_frame,
            text=TRANSLATIONS['add_new_tool'][self.lang],
            bg='#001100',
            fg='#00ff00',
            font=('Consolas', 10, 'bold')
        )
        self.title_label.pack(side=tk.LEFT, padx=10)
        
        # 关闭按钮
        close_btn = tk.Button(
            self.title_frame,
            text="×",
            command=self.dialog.destroy,
            bg='#001100',
            fg='#00ff00',
            font=('Consolas', 12, 'bold'),
            relief='flat',
            bd=0,
            activebackground='#003300',
            activeforeground='#ff0000',
            width=2
        )
        close_btn.pack(side=tk.RIGHT, padx=5)
        
        # 绑定拖动事件到标题栏
        self.title_frame.bind('<Button-1>', self.start_move)
        self.title_frame.bind('<B1-Motion>', self.do_move)
        
        # 创建主框架来容纳所有内容
        main_frame = tk.Frame(self.dialog, bg='#000000')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 工具名称
        name_frame = tk.Frame(main_frame, bg='#000000')
        name_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            name_frame,
            text=TRANSLATIONS['tool_name'][self.lang],
            bg='#000000',
            fg='#00ff00',
            font=('Consolas', 10)
        ).pack(side=tk.LEFT)
        
        self.name_entry = tk.Entry(
            name_frame,
            bg='#001100',
            fg='#00ff00',
            insertbackground='#00ff00',
            font=('Consolas', 10),
            relief='solid',
            bd=1
        )
        self.name_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # 工具类型选择
        self.type_frame = tk.LabelFrame(
            main_frame,
            text=" [ SELECT TOOL TYPE ] ",
            bg='#000000',
            fg='#00ffff',
            font=('Consolas', 10, 'bold'),
            bd=1,
            relief='solid',
            padx=10,
            pady=10
        )
        self.type_frame.pack(fill=tk.X, pady=10)
        
        # 添加荧光边框
        tk.Frame(self.type_frame, bg='#00ffff', height=1).pack(side=tk.TOP, fill=tk.X)
        tk.Frame(self.type_frame, bg='#00ffff', height=1).pack(side=tk.BOTTOM, fill=tk.X)

        self.type_var = tk.StringVar(value="exe")
        self.radio_frames = []

        types = [
            (TRANSLATIONS['exe_program'][self.lang], "exe", "⚡"),
            (TRANSLATIONS['script_program'][self.lang], "script", "🐍"),
            (TRANSLATIONS['jar_program'][self.lang], "jar", "☕"),
            (TRANSLATIONS['custom_command'][self.lang], "custom", "⌨️")
        ]

        for text, value, icon in types:
            radio_frame = self.create_type_radio(self.type_frame, text, value, icon)
            self.radio_frames.append(radio_frame)
        
        # 文件选择区域
        self.file_frame = tk.LabelFrame(
            main_frame,
            text=TRANSLATIONS['file_path'][self.lang],
            bg='#000000',
            fg='#00ff00',
            font=('Consolas', 10),
            bd=1,
            relief='solid',
            padx=10,
            pady=10
        )
        self.file_frame.pack(fill=tk.X, pady=10)
        
        self.path_label = tk.Label(
            self.file_frame,
            text=TRANSLATIONS['no_file'][self.lang],
            bg='#000000',
            fg='#555555',
            font=('Consolas', 9),
            wraplength=350
        )
        self.path_label.pack(fill=tk.X)
        
        self.select_btn = tk.Button(
            self.file_frame,
            text=TRANSLATIONS['select_file'][self.lang],
            command=self.choose_file,
            bg='#001100',
            fg='#00ff00',
            font=('Consolas', 10),
            relief='solid',
            bd=1,
            activebackground='#003300',
            activeforeground='#00ff00'
        )
        self.select_btn.pack(pady=10)
        
        # 运行模式
        self.mode_frame = tk.LabelFrame(
            main_frame,
            text=TRANSLATIONS['run_mode'][self.lang],
            bg='#000000',
            fg='#00ff00',
            font=('Consolas', 10),
            bd=1,
            relief='solid',
            padx=5,
            pady=5
        )
        self.mode_frame.pack(fill=tk.X, pady=10)
        
        self.show_console = tk.BooleanVar(value=True)
        tk.Checkbutton(
            self.mode_frame,
            text=TRANSLATIONS['show_console'][self.lang],
            variable=self.show_console,
            bg='#000000',
            fg='#00ff00',
            selectcolor='#001100',
            activebackground='#000000',
            activeforeground='#00ff00',
            font=('Consolas', 10)
        ).pack(pady=5)
        
        # 添加分类选择
        self.category_frame = tk.LabelFrame(
            main_frame,
            text=" TOOL CATEGORY ",
            bg='#000000',
            fg='#00ff00',
            font=('Consolas', 10),
            bd=1,
            relief='solid',
            padx=10,
            pady=10
        )
        self.category_frame.pack(fill=tk.X, pady=10)
        
        # 创建下拉框容器
        dropdown_frame = tk.Frame(self.category_frame, bg='#000000')
        dropdown_frame.pack(fill=tk.X, pady=5)
        
        # 创建分类图标标签
        self.category_icon = tk.Label(
            dropdown_frame,
            text='📁',
            bg='#000000',
            fg='#00ffff',
            font=('Consolas', 10)
        )
        self.category_icon.pack(side=tk.LEFT, padx=5)
        
        # 创建下拉选择框
        self.category_var = tk.StringVar(value="other")
        categories = [
            ('webshell', '📁', 'WebShell管理工具'),
            ('info_collect', '🔍', '信息收集'),
            ('exploit', '⚡', '漏洞利用工具'),
            ('post', '🔧', '后渗透工具'),
            ('other', '📌', '其他工具')
        ]
        
        # 创建自定义样式的组合框
        self.category_combo = ttk.Combobox(
            dropdown_frame,
            textvariable=self.category_var,
            values=[cat[2] for cat in categories],
            state='readonly',
            font=('Consolas', 10),
            width=30
        )
        self.category_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # 创建分类映射
        self.category_mapping = {cat[2]: (cat[0], cat[1]) for cat in categories}
        
        # 绑定选择事件
        def on_category_select(event):
            selected_text = self.category_combo.get()
            cat_id, icon = self.category_mapping[selected_text]
            self.category_var.set(cat_id)
            self.category_icon.config(text=icon)
        
        self.category_combo.bind('<<ComboboxSelected>>', on_category_select)
        
        # 设置下拉框样式
        style = ttk.Style()
        style.configure(
            'TCombobox',
            fieldbackground='#001100',
            background='#000000',
            foreground='#00ffff',
            selectbackground='#003300',
            selectforeground='#00ffff',
            arrowcolor='#00ffff'
        )
        
        # 参数输入框（仅用于自定义命令）
        self.param_frame = tk.LabelFrame(
            main_frame,
            text=" COMMAND ",
            bg='#000000',
            fg='#00ffff',
            font=('Consolas', 10),
            bd=1,
            relief='solid',
            padx=10,
            pady=10
        )
        
        # 添加荧光边框
        tk.Frame(self.param_frame, bg='#00ffff', height=1).pack(side=tk.TOP, fill=tk.X)
        tk.Frame(self.param_frame, bg='#00ffff', height=1).pack(side=tk.BOTTOM, fill=tk.X)
        
        self.param_entry = tk.Entry(
            self.param_frame,
            bg='#001100',
            fg='#555555',
            insertbackground='#00ffff',
            font=('Consolas', 10),
            relief='solid',
            bd=1
        )
        self.param_entry.insert(0, TRANSLATIONS['command_placeholder'][self.lang])
        self.param_entry.bind('<FocusIn>', self.on_entry_click)
        self.param_entry.bind('<FocusOut>', self.on_focus_out)
        self.param_entry.pack(fill=tk.X, expand=True, pady=5)
        
        # 工作目录框架（仅用于自定义命令）
        self.workdir_frame = tk.LabelFrame(
            main_frame,
            text=" WORKING DIRECTORY ",
            bg='#000000',
            fg='#00ffff',
            font=('Consolas', 10),
            bd=1,
            relief='solid',
            padx=10,
            pady=10
        )
        
        # 添加荧光边框
        tk.Frame(self.workdir_frame, bg='#00ffff', height=1).pack(side=tk.TOP, fill=tk.X)
        tk.Frame(self.workdir_frame, bg='#00ffff', height=1).pack(side=tk.BOTTOM, fill=tk.X)
        
        self.workdir_entry = tk.Entry(
            self.workdir_frame,
            bg='#001100',
            fg='#00ffff',
            insertbackground='#00ffff',
            font=('Consolas', 10),
            relief='solid',
            bd=1
        )
        self.workdir_entry.pack(fill=tk.X, expand=True, pady=5)
        
        # 选择工作目录按钮
        self.select_workdir_btn = Style.create_button(
            self.workdir_frame,
            text="[ SELECT DIRECTORY ]",
            command=self.choose_workdir,
            bg='#001100',
            fg='#00ffff',
            font=(Style.FONT, 10),
            relief='flat',
            bd=0
        )
        self.select_workdir_btn.pack(pady=5)
        
        # 底部按钮
        button_frame = tk.Frame(main_frame, bg='#000000')
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
        
        self.confirm_btn = Style.create_button(
            button_frame,
            text=TRANSLATIONS['confirm'][self.lang],
            command=self.save_tool,
            size=14,
            weight='bold',
            width=25,
            height=2,
            bg='#001100',
            fg='#00ff00'
        )
        self.confirm_btn.pack(pady=10)
        
        # 绑定类型变更事件
        self.type_var.trace_add('write', self.on_type_change)
        
        # 初始化变量
        self.file_path = None
        
        # 设置窗口位置为居中
        self.center_window()

    def start_move(self, event):
        """开始拖动窗口"""
        self.x = event.x_root - self.dialog.winfo_x()
        self.y = event.y_root - self.dialog.winfo_y()

    def do_move(self, event):
        """拖动窗口"""
        x = event.x_root - self.x
        y = event.y_root - self.y
        self.dialog.geometry(f"+{x}+{y}")

    def choose_file(self):
        selected_type = self.type_var.get()
        
        # 文件类型配置
        file_types = {
            'exe': [("EXE Files", "*.exe")],
            'script': [("Python Files", "*.py"), ("Batch Files", "*.bat")],
            'jar': [("JAR Files", "*.jar")],
            'param': [("All Files", "*.*")]
        }
        
        # 使用标准文件选择对话框
        if selected_type in file_types:
            self.file_path = filedialog.askopenfilename(
                title=TRANSLATIONS['select_file'][self.lang],
                filetypes=file_types[selected_type]
            )
            
            if self.file_path:
                self.path_label.config(text=self.file_path, fg='#00ffff')

    def save_tool(self):
        if not self.name_entry.get():
            self.show_error(TRANSLATIONS['save_error'][self.lang])
            return
            
        if self.type_var.get() != 'custom' and not self.file_path:
            self.show_error(TRANSLATIONS['save_error'][self.lang])
            return
            
        if self.type_var.get() == 'custom' and (
            not self.param_entry.get() or 
            self.param_entry.get() == TRANSLATIONS['command_placeholder'][self.lang]
        ):
            self.show_error(TRANSLATIONS['save_error'][self.lang])
            return
        
        # 获取参数（仅用于自定义命令）
        params = ""
        if self.type_var.get() == 'custom':
            params = self.param_entry.get()
        
        tool = {
            "name": self.name_entry.get(),
            "type": self.type_var.get(),
            "path": self.file_path if self.type_var.get() != 'custom' else "",
            "params": params,
            "show_console": self.show_console.get(),
            "working_dir": self.workdir_entry.get() if self.type_var.get() == 'custom' else "",
            "category": self.category_var.get()
        }
        
        self.toolbox.tools.append(tool)
        self.toolbox.save_tools()
        self.toolbox.refresh_tool_list()
        self.show_success(TRANSLATIONS['save_success'][self.lang])
        self.dialog.after(1000, self.dialog.destroy)

    def update_texts(self):
        self.title_label.config(text=TRANSLATIONS['add_new_tool'][self.lang])
        self.tool_name_label.config(text=TRANSLATIONS['tool_name'][self.lang])
        self.type_frame.config(text=TRANSLATIONS['select_tool_type'][self.lang])
        self.file_frame.config(text=TRANSLATIONS['file_path'][self.lang])
        self.select_btn.config(text=TRANSLATIONS['select_file'][self.lang])
        self.confirm_btn.config(text=TRANSLATIONS['confirm'][self.lang])
        self.path_label.config(text=TRANSLATIONS['no_file'][self.lang] if not self.file_path else self.file_path)
        
        # 更新单选按钮
        types = [
            (TRANSLATIONS['exe_program'][self.lang], "exe", "⚡"),
            (TRANSLATIONS['script_program'][self.lang], "script", "🐍"),
            (TRANSLATIONS['jar_program'][self.lang], "jar", "☕"),
            (TRANSLATIONS['custom_command'][self.lang], "custom", "⌨️")
        ]
        
        # 更新所有单选按钮的文本
        for rb, (text, value, icon) in zip(self.radio_frames, types):
            rb.config(text=f"{icon} {text}")

    def on_entry_click(self, event):
        """当用户点击输入框时，如果显示的是占位文本就清除"""
        if self.param_entry.get() == TRANSLATIONS['param_placeholder'][self.lang]:
            self.param_entry.delete(0, tk.END)
            self.param_entry.config(fg='#00ff00')

    def on_focus_out(self, event):
        """当输入框失去焦点时，如果为空就显示占位文本"""
        if not self.param_entry.get():
            self.param_entry.insert(0, TRANSLATIONS['param_placeholder'][self.lang])
            self.param_entry.config(fg='#555555')

    def show_error(self, message):
        """显示错误消息"""
        error_label = tk.Label(
            self.dialog,
            text=f"[!] {message}",
            bg='#000000',
            fg='#ff0000',
            font=('Consolas', 10)
        )
        error_label.pack(pady=5)
        self.dialog.after(2000, error_label.destroy)

    def show_success(self, message):
        """显示成功消息"""
        success_label = tk.Label(
            self.dialog,
            text=f"[+] {message}",
            bg='#000000',
            fg='#00ff00',
            font=('Consolas', 10)
        )
        success_label.pack(pady=5)
        self.dialog.after(2000, success_label.destroy)

    def on_type_change(self, *args):
        """当工具类型改变时调用"""
        selected_type = self.type_var.get()
        
        # 隐藏所有可选框
        self.param_frame.pack_forget()
        self.workdir_frame.pack_forget()
        self.file_frame.pack_forget()
        self.mode_frame.pack_forget()
        self.category_frame.pack_forget()
        
        # 根据不同类型显示不同的组件
        if selected_type == 'custom':
            # 自定义命令：显示命令输入和工作目录
            self.param_frame.pack(fill=tk.X, pady=10)
            self.param_entry.delete(0, tk.END)
            self.param_entry.insert(0, TRANSLATIONS['command_placeholder'][self.lang])
            self.param_entry.config(fg='#555555')
            
            self.workdir_frame.pack(fill=tk.X, pady=10)
            self.mode_frame.pack(fill=tk.X, pady=10)
            self.category_frame.pack(fill=tk.X, pady=10)
            
        else:  # exe, script, jar 等类型
            # 其他类型：只显示文件选择
            self.file_frame.pack(fill=tk.X, pady=10)
            self.mode_frame.pack(fill=tk.X, pady=10)
            self.category_frame.pack(fill=tk.X, pady=10)
            
            # 更新文件选择按钮文本
            self.select_btn.config(text=TRANSLATIONS['select_file'][self.lang])

    def choose_workdir(self):
        workdir = filedialog.askdirectory(
            title=TRANSLATIONS['working_dir'][self.lang]
        )
        if workdir:
            self.workdir_entry.delete(0, tk.END)
            self.workdir_entry.insert(0, workdir)

    def center_window(self):
        # 获取屏幕分辨率
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        
        # 获取窗口大小
        window_width = self.dialog.winfo_width()
        window_height = self.dialog.winfo_height()
        
        # 计算窗口左上角的位置
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        
        # 设置窗口位置
        self.dialog.geometry(f"+{x}+{y}")

    def create_type_radio(self, frame, text, value, icon):
        """创建美化的单选按钮"""
        radio_frame = tk.Frame(frame, bg='#000000')
        radio_frame.pack(fill=tk.X, pady=2)
        
        def on_select():
            self.type_var.set(value)
            # 更新所有单选按钮的样式
            for rb in self.radio_frames:
                if rb == radio_frame:
                    rb.config(bg='#001100')
                    for child in rb.winfo_children():
                        child.config(bg='#001100', fg='#00ffff')
                else:
                    rb.config(bg='#000000')
                    for child in rb.winfo_children():
                        child.config(bg='#000000', fg='#00ff00')
        
        # 图标
        icon_label = tk.Label(
            radio_frame,
            text=icon,
            bg='#000000',
            fg='#00ff00',
            font=('Consolas', 12)
        )
        icon_label.pack(side=tk.LEFT, padx=5)
        
        # 文本
        text_label = tk.Label(
            radio_frame,
            text=text,
            bg='#000000',
            fg='#00ff00',
            font=('Consolas', 10)
        )
        text_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 绑定点击事件
        radio_frame.bind('<Button-1>', lambda e: on_select())
        icon_label.bind('<Button-1>', lambda e: on_select())
        text_label.bind('<Button-1>', lambda e: on_select())
        
        # 添加悬停效果
        def on_enter(e):
            if self.type_var.get() != value:
                radio_frame.config(bg='#001100')
                icon_label.config(bg='#001100')
                text_label.config(bg='#001100')
        
        def on_leave(e):
            if self.type_var.get() != value:
                radio_frame.config(bg='#000000')
                icon_label.config(bg='#000000')
                text_label.config(bg='#000000')
        
        radio_frame.bind('<Enter>', on_enter)
        radio_frame.bind('<Leave>', on_leave)
        icon_label.bind('<Enter>', on_enter)
        icon_label.bind('<Leave>', on_leave)
        text_label.bind('<Enter>', on_enter)
        text_label.bind('<Leave>', on_leave)
        
        return radio_frame

if __name__ == "__main__":
    app = ToolBox()
    app.window.mainloop()
def create_categories(self):
    """创建赛博朋克风格的分类选择器"""
    self.category_buttons = []
    
    # 创建分类标题
    title_frame = tk.Frame(self.category_frame, bg='#000000')
    title_frame.pack(fill=tk.X, pady=(0, 5))
    
    tk.Label(
        title_frame,
        text="[ TOOL CATEGORY ]",
        bg='#000000',
        fg='#00ff00',
        font=('Consolas', 12, 'bold')
    ).pack(side=tk.LEFT, padx=10)
    
    # 添加装饰性扫描线
    scan_line = tk.Frame(self.category_frame, height=2, bg='#00ff00')
    scan_line.pack(fill=tk.X, pady=2)
    
    def animate_scan_line():
        scan_line.config(bg='#003300')
        self.window.after(500, lambda: scan_line.config(bg='#00ff00'))
        self.window.after(1000, animate_scan_line)
    
    animate_scan_line()
    
    # 创建下拉框容器
    dropdown_frame = tk.Frame(self.category_frame, bg='#000000', bd=1, relief='solid')
    dropdown_frame.pack(fill=tk.X, pady=5, padx=10)
    
    # 创建分类图标标签
    self.category_icon = tk.Label(
        dropdown_frame,
        text='📌',  # 默认图标
        bg='#000000',
        fg='#00ffff',
        font=('Consolas', 12)
    )
    self.category_icon.pack(side=tk.LEFT, padx=5)
    
    # 创建自定义下拉框
    class CyberCombobox(ttk.Combobox):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.option_add('*TCombobox*Listbox.font', ('Consolas', 10))
            self.option_add('*TCombobox*Listbox.background', '#001100')
            self.option_add('*TCombobox*Listbox.foreground', '#00ffff')
            self.option_add('*TCombobox*Listbox.selectBackground', '#002200')
            self.option_add('*TCombobox*Listbox.selectForeground', '#ffffff')
    
    # 创建样式
    style = ttk.Style()
    style.configure(
        'Cyber.TCombobox',
        fieldbackground='#001100',
        background='#001100',
        foreground='#00ffff',
        arrowcolor='#00ffff',
        selectbackground='#002200',
        selectforeground='#ffffff',
        borderwidth=1,
        relief='solid',
        padding=5
    )
    
    # 设置下拉框样式
    style.map('Cyber.TCombobox',
        fieldbackground=[('readonly', '#001100'), ('active', '#002200')],
        selectbackground=[('readonly', '#002200')],
        selectforeground=[('readonly', '#ffffff')],
        background=[('readonly', '#001100'), ('active', '#002200')],
        foreground=[('readonly', '#00ffff'), ('active', '#ffffff')]
    )
    
    # 创建分类列表
    categories = [
        ('webshell', '📁', TRANSLATIONS['categories'][self.lang]['webshell']),
        ('info_collect', '🔍', TRANSLATIONS['categories'][self.lang]['info_collect']),
        ('exploit', '⚡', TRANSLATIONS['categories'][self.lang]['exploit']),
        ('post', '🔧', TRANSLATIONS['categories'][self.lang]['post']),
        ('other', '📌', TRANSLATIONS['categories'][self.lang]['other'])
    ]
    
    # 创建下拉框
    self.category_combo = CyberCombobox(
        dropdown_frame,
        values=[f"{icon} {text}" for _, icon, text in categories],
        state='readonly',
        style='Cyber.TCombobox',
        font=('Consolas', 10),
        width=30
    )
    self.category_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    
    # 设置默认值
    default_text = f"📌 {TRANSLATIONS['categories'][self.lang]['other']}"
    self.category_combo.set(default_text)
    
    # 创建分类映射
    self.category_mapping = {f"{icon} {text}": (cat_id, icon) for cat_id, icon, text in categories}
    
    # 绑定选择事件
    def on_select(event):
        selected = self.category_combo.get()
        cat_id, icon = self.category_mapping[selected]
        self.current_category = cat_id
        self.category_icon.config(text=icon)
        
        # 添加选择动画效果
        def flash():
            self.category_icon.config(fg='#ffffff')
            self.window.after(100, lambda: self.category_icon.config(fg='#00ffff'))
        flash()
        
        # 刷新工具列表
        self.refresh_tool_list()
    
    self.category_combo.bind('<<ComboboxSelected>>', on_select)
    
    # 创建装饰性边框
    def create_cyber_border(widget):
        # 上边框
        top_frame = tk.Frame(widget, height=2, bg='#00ffff')
        top_frame.pack(side=tk.TOP, fill=tk.X)
        
        # 下边框
        bottom_frame = tk.Frame(widget, height=2, bg='#00ffff')
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 左边装饰
        left_decor = tk.Label(
            widget,
            text="[",
            bg='#000000',
            fg='#00ffff',
            font=('Consolas', 12)
        )
        left_decor.place(x=0, y=10)
        
        # 右边装饰
        right_decor = tk.Label(
            widget,
            text="]",
            bg='#000000',
            fg='#00ffff',
            font=('Consolas', 12)
        )
        right_decor.place(relx=1, y=10, anchor='ne')
        
        return [top_frame, bottom_frame, left_decor, right_decor]
    
    # 添加边框和装饰
    border_elements = create_cyber_border(dropdown_frame)
    
    # 添加悬停效果
    def on_enter(e):
        for element in border_elements[:2]:
            element.config(bg='#00ffaa')
        self.category_icon.config(fg='#00ffaa')
        for element in border_elements[2:]:
            element.config(fg='#00ffaa')
        dropdown_frame.config(bg='#001100')  # 改变容器背景色
    
    def on_leave(e):
        for element in border_elements[:2]:
            element.config(bg='#00ffff')
        self.category_icon.config(fg='#00ffff')
        for element in border_elements[2:]:
            element.config(fg='#00ffff')
        dropdown_frame.config(bg='#000000')  # 恢复容器背景色
    
    # 绑定悬停事件
    dropdown_frame.bind('<Enter>', on_enter)
    dropdown_frame.bind('<Leave>', on_leave)
    self.category_combo.bind('<Enter>', on_enter)
    self.category_combo.bind('<Leave>', on_leave)
    
    # 添加底部状态显示
    status_frame = tk.Frame(self.category_frame, bg='#000000')
    status_frame.pack(fill=tk.X, pady=(5, 0))
    
    tk.Label(
        status_frame,
        text="[ STATUS: ACTIVE ]",
        bg='#000000',
        fg='#00ff00',
        font=('Consolas', 8)
    ).pack(side=tk.RIGHT, padx=5) 
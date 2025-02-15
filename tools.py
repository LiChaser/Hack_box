import os
import subprocess

class ToolRunner:
    @staticmethod
    def run_cmd(tool, show_console=True):
        """在指定目录打开CMD"""
        try:
            directory = tool['path']
            if not os.path.isdir(directory):
                return False, "Directory does not exist"
            
            cmd = f'start cmd /K "cd /d "{directory}""'
            subprocess.Popen(cmd, shell=True)
            return True, None
        except Exception as e:
            return False, str(e)

    @staticmethod
    def run_tool(tool, show_console=True):
        """运行工具的通用方法"""
        if tool['type'] == 'custom':
            return ToolRunner.run_custom_command(tool, show_console)
        elif tool['type'] == 'script':
            return ToolRunner.run_script(tool, show_console)
        elif tool['type'] == 'jar':
            return ToolRunner.run_jar(tool, show_console)
        elif tool['type'] == 'cmd':
            return ToolRunner.run_cmd(tool, show_console)
        else:
            return ToolRunner.run_exe(tool, show_console) 
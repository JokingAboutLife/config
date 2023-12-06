import os
import subprocess
import shutil
import argparse


def remove_gtk4_theme_link(system_gtk4_theme_dir):
    for item in os.scandir(system_gtk4_theme_dir):
        print(item.path)
        if item.is_symlink():
            os.unlink(item.path)
        elif item.is_dir():
            shutil.rmtree(item.path)
        elif item.is_file():
            os.remove(item.path)


def make_gtk4_theme_link(system_gtk4_theme_dir, current_theme_gtk4_dir):
    for item in os.scandir(current_theme_gtk4_dir):
        tmp_result = subprocess.run(['ln', '-s', item.path, system_gtk4_theme_dir], capture_output=True, text=True)
        if tmp_result.returncode:
            print('%s 建立软连接错误 %s' % (item.path, tmp_result.stderr))
        else:
            print(item.path)


if __name__ == '__main__':
    USER_HOME_DIR = os.environ['HOME']
    GTK4_DIR_NAME = 'gtk-4.0'
    SYSTEM_GTK4_THEME_DIR = USER_HOME_DIR + "/.config/" + GTK4_DIR_NAME
    THEME_DIR = USER_HOME_DIR + '/.themes/'

    parser = argparse.ArgumentParser(description='帮助')
    parser.add_argument('-u', '--uninstall', action='store_true', required=False, help='卸载 GTK4 主题')
    args = parser.parse_args()
    # print(args.uninstall)
    
    if args.uninstall:
        print('--------------- 清空 .config/gtk-4.0 文件夹 ---------------'.center(50, '-'))
        remove_gtk4_theme_link(SYSTEM_GTK4_THEME_DIR)
        print('--------------- 结束 ---------------'.center(50, '-'))
    else:
        TMP_RESULT = subprocess.run('gsettings get org.gnome.desktop.interface gtk-theme',
                                    shell=True, capture_output=True, text=True, check=False)
        if TMP_RESULT.returncode:
            print('获取 GTK 主题失败，%s' % TMP_RESULT.stderr)
        else:
            theme_name = TMP_RESULT.stdout.strip().replace("'", "")
            current_gtk_theme_dir = THEME_DIR + theme_name
            THEME_EXISTS = os.path.exists(current_gtk_theme_dir)
            if not THEME_EXISTS:
                print('%s 主题目录不存在' % current_gtk_theme_dir)
                exit(1)
            GTK4_THEME_EXISTS = False
            for item in os.scandir(current_gtk_theme_dir):
                if item.is_dir() and GTK4_DIR_NAME == item.name:
                    GTK4_THEME_EXISTS = True
                    break
            if not GTK4_THEME_EXISTS:
                    print('不存在 GTK4 主题文件夹')
                    exit(1)
            # 清空 .config/gtk-4.0 的文件
            print('--------------- 清空 .config/gtk-4.0 文件夹 ---------------'.center(50, '-'))
            remove_gtk4_theme_link(SYSTEM_GTK4_THEME_DIR)
            
            # 将当前主题的 gtk-4.0 文件夹中的文件软链接到 .config/gtk-4.0 文件夹中
            print('--------------- 开始设置 GTK4 主题的软链接 ---------------'.center(50, '-'))
            current_theme_gtk4_dir = current_gtk_theme_dir + "/" + GTK4_DIR_NAME
            make_gtk4_theme_link(SYSTEM_GTK4_THEME_DIR, current_theme_gtk4_dir)
            print('--------------- 结束 ---------------'.center(50, '-'))

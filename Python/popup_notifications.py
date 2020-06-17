import platform, os

def push(title, message):
    plt = platform.system()
    if plt == 'Darwin':
        command = f'''
        osascript -e 'diplay notification "{message}" with title "{title}"
        '''
    elif plt == 'Linux':
        command = f'''
        notify-send "{title}" "{message}"
        '''
    elif plt == 'Windows':
        win10toast.ToastNotifier().show_toast(title, message)
        return
    else:
        return
    
    os.system(command)


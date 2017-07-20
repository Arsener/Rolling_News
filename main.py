import mongoDB
import main_console
import time

console = main_console.Console()
while True:
    web_list = ['新浪','网易','腾讯','凤凰','搜狐']
    console.mlti_thread(web_list)
    time.sleep(60)
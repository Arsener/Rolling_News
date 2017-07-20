import mongoDB
import main_console
import time

console = main_console.Console()
while True:
    web_list = ['Sina','NetEase','Tencent','ifeng','sohu']
    console.mlti_thread(web_list)
    time.sleep(60)
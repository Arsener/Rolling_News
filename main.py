import MongoDB
import main_console

console = main_console.Console()
url_pool = console.construct_url_pic(['Sina', 'NetEase', 'sohu'])
console.mlti_thread(url_pool)

# MongoDB.MongoDB.store('Sina',[{'title':'pp'}])

# print(MongoDB.MongoDB.get_latest('Sina'))
# print(type(MongoDB.MongoDB.get_latest('Sina')))
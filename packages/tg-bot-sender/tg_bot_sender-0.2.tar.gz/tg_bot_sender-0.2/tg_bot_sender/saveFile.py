import os
from datetime import datetime
import json 

def saveFile(pushName, gatherTasks) -> None:
    if not os.path.isdir(f'{pushName}'):
        os.mkdir(f'{pushName}')

    with open(f'{pushName}/{datetime.now()}data.json', 'w', encoding='utf-8') as f:
        json.dump(gatherTasks, f, ensure_ascii=False, indent=4)
        print('end')
        
if __name__ == '__main__':
    pass
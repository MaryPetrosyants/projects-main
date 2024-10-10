
import sys
from task_manager import TaskManager
from task_storage_to_json import TaskStorageToJson
def main():
    storage = TaskStorageToJson('tasks.json')
    manager = TaskManager(storage)
    command=sys.argv[1]
    if command == 'add':
        print(manager.add_task(" ".join(sys.argv[2:])))
    elif command == 'delete':
        task_id = int(sys.argv[2])
        print(manager.delete_task(task_id))
    elif command == 'list':
        task_list = manager.list_tasks()
        for i, task in enumerate(task_list):
            print (task_list[i])

if __name__ == "__main__":
    main()


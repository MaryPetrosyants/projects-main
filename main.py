
from task_manager import TaskManager
from task_storage_to_json import TaskStorageToJson
from task_storage_to_sqllite import StorageToSqllite
import argparse


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    parser.add_argument('-n', '--name', nargs='?')
    parser.add_argument('-i', '--id', type=int,  nargs='?')
    parser.add_argument('-nn', '--new_name', nargs='?')
    parser.add_argument('-ns', '--new_status', nargs='?')
    return parser


def main():
   # storage = StorageToSqllite('tasks.db')
    # manager = TaskManager(storage)
    parser = createParser()
    args = parser.parse_args()
    with TaskStorageToJson('tasks.json') as storage:
        manager = TaskManager(storage)
        match args.command:
            case 'add':
                name = args.name
                manager.add_task(name)
                print(f"Task {name} add")
            case 'delete':
                id = args.id
                manager.delete_task(id)
                print(f"Task {id} delete")
            case 'list':
                task_list = manager.list_tasks()
                for i, _ in enumerate(task_list):
                    print(task_list[i])
            case 'update':
                id = args.id
                new_name = args.new_name
                new_status = args.new_status
                manager.update_task(id, new_name, new_status)
                print(f'Task {id} update')

            case _:
                print("not correct comand")


if __name__ == "__main__":
    main()

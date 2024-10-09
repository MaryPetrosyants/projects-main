
import sys
from task_manager import TaskManager

def main():
    manager = TaskManager()
    command=sys.argv[1]
    if command == 'add':
        print(manager.add_task(" ".join(sys.argv[2:])))
    elif command == 'delete':
        task_id = int(sys.argv[2])
        print(manager.delete_task(task_id))
    elif command == 'list':
        task_list = manager.list_tasks()
        for task in task_list:
            print(task)

if __name__ == "__main__":
    main()


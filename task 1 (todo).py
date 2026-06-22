import json
import os


class TodoModel:
    def __init__(self, storage_file="tasks_db.json"):
        self.storage_file = storage_file
        self.tasks = self._load()

    def _load(self):
        if not os.path.exists(self.storage_file):
            return []
        try:
            with open(self.storage_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def _save(self):
        with open(self.storage_file, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def add_task(self, task_name):
        next_id = self.tasks[-1]["id"] + 1 if self.tasks else 1
        task = {"id": next_id, "task": task_name}
        self.tasks.append(task)
        self._save()
        return task

    def get_all_tasks(self):
        return self.tasks


class TodoView:
    @staticmethod
    def display_menu():
        print("\n--- To-Do List ---")
        print("1. Add task")
        print("2. View tasks")
        print("3. Exit")
        return input("Choose an option (1-3): ").strip()

    @staticmethod
    def get_task_input():
        return input("Task description: ").strip()

    @staticmethod
    def show_tasks(tasks):
        if not tasks:
            print("\nNo tasks yet.")
            return

        print("\n--- Your Tasks ---")
        for index, task in enumerate(tasks, start=1):
            print(f"{index}. [{task['id']}] {task['task']}")

    @staticmethod
    def show_message(message):
        print(f"\n{message}")


def main():
    model = TodoModel()
    view = TodoView()

    while True:
        choice = view.display_menu()

        if choice == "1":
            task_name = view.get_task_input()
            if task_name:
                new_task = model.add_task(task_name)
                view.show_message(f"Added: '{new_task['task']}'")
            else:
                view.show_message("Task can't be empty.")

        elif choice == "2":
            view.show_tasks(model.get_all_tasks())

        elif choice == "3":
            view.show_message("Bye!")
            break

        else:
            view.show_message("Not a valid option, try again.")


if __name__ == "__main__":
    main()

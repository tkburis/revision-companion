import time
from PyInquirer import prompt
from util import Utility
from prompt_toolkit.validation import Validator, ValidationError
from rich import print
from rich.table import Table
from rich.progress import track
from sys import exit
from os import system, name


def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


class NumItemsValidator(Validator):
    def validate(self, x):
        x = x.text
        len_x = len(x)
        if x.isnumeric():
            x = int(x)
            if x < 1:
                raise ValidationError(message='Please make sure your number is greater than 1',
                                      cursor_position=len_x)
        else:
            raise ValidationError(message='Please make sure you are entering a number',
                                  cursor_position=len_x)


class Application:
    def __init__(self):
        self.utility = Utility(items_file_name='items.txt')

    def start(self):
        self.main_menu()

    def main_menu(self):
        get_rev_items_prompt = 'Get my revision items for today'
        edit_items_prompt = 'Edit my revision items'
        exit_prompt = 'Exit program'
        questions = [
            {
                'type': 'list',
                'name': 'main_menu',
                'message': 'What would you like to do?',
                'choices': [
                    get_rev_items_prompt,
                    edit_items_prompt,
                    exit_prompt
                ]
            }
        ]
        answers = prompt(questions)
        if answers['main_menu'] == get_rev_items_prompt:
            self.revise()
        elif answers['main_menu'] == edit_items_prompt:
            self.edit_items()
        elif answers['main_menu'] == exit_prompt:
            exit()

    def revise(self):
        utility = self.utility
        questions = [
            {'type': 'input',
             'name': 'num_items_menu',
             'message': 'How many items would you like to revise?',
             'default': '2',
             'validate': NumItemsValidator}
        ]
        answers = prompt(questions)
        num_items = int(answers['num_items_menu'])
        items = utility.get_session_items(num_items)
        print('[blue]Here are your items for today:[/]')
        if items:
            for item in items:
                print(f'• [bold red]{item}[/]')
        else:
            print('[italic purple]No items...[/]')
        self.exit_or_menu()

    def edit_items(self):
        self.print_all_items()
        add_new_item_prompt = 'Add a new item'
        remove_item_prompt = 'Remove an item'
        back_main_prompt = 'Back to main menu'
        questions = [
            {
                'type': 'list',
                'name': 'edit_menu',
                'message': 'What would you like to do?',
                'choices': [
                    add_new_item_prompt,
                    remove_item_prompt,
                    back_main_prompt
                ]
            }
        ]
        answers = prompt(questions)
        if answers['edit_menu'] == add_new_item_prompt:
            self.add_new_item()
        elif answers['edit_menu'] == remove_item_prompt:
            self.remove_item()
        elif answers['edit_menu'] == back_main_prompt:
            clear()
            self.main_menu()

    def add_new_item(self):
        utility = self.utility
        questions = [
            {'type': 'input',
             'name': 'add_item_menu',
             'message': 'What would you like to add?'
             }
        ]
        answers = prompt(questions)
        item_to_add = answers['add_item_menu']
        utility.insert_new_item(item_to_add)
        print('[green]Done[/]')
        time.sleep(1)
        clear()
        self.edit_items()

    def remove_item(self):
        utility = self.utility
        questions = [
            {'type': 'checkbox',
             'name': 'remove_item_menu',
             'message': 'Which would you like to remove?',
             'choices': [{'name': k} for k, v in utility.get_all_items().items()]
             }
        ]
        answers = prompt(questions)
        items_to_remove = answers['remove_item_menu']
        for item in track(items_to_remove, description='Removing...'):
            utility.remove_item(item)
        print('[green]Done[/]')
        time.sleep(1)
        clear()
        self.edit_items()

    def print_all_items(self):
        utility = self.utility
        all_items = utility.get_all_items()
        print('[green]Here are your items:[/]')

        table = Table(title='Revision Items')
        table.add_column('Name', justify='left', style='cyan')
        table.add_column('Miss Value', justify='left', style='red')

        if all_items:
            for item_name, value in all_items.items():
                table.add_row(item_name, str(value['miss']))
            print(table)
        else:
            print("[italic purple]No items...[/]")

    def exit_or_menu(self):
        exit_prompt = 'Exit the program'
        return_prompt = 'Return to main menu'
        questions = [
            {
                'type': 'list',
                'name': 'end_menu',
                'message': 'What now?',
                'choices': [
                    return_prompt,
                    exit_prompt
                ]
            }
        ]
        answers = prompt(questions)
        if answers['end_menu'] == exit_prompt:
            exit()
        elif answers['end_menu'] == return_prompt:
            clear()
            self.main_menu()


if __name__ == "__main__":
    app = Application()
    app.start()

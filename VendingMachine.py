# VENDING MACHINE

###########################################################################################################################

# Imports
from rich.console import Console
from rich.panel import Panel
from rich.style import Style
from rich.table import Table
from rich.table import Column, Table
from rich.progress import track
from rich.progress import Progress
from rich.text import Text
from rich.markup import escape
from rich import box
import pygame
import time
import sys
import random

###########################################################################################################################

# Console Instance - 
console = Console()

# Vending Machine header
print()
label = """
 █ █ ██▀ █▄ █ █▀▄ █ █▄ █ ▄▀▀    █▄ ▄█ ▄▀▄ ▄▀▀ █▄█ █ █▄ █ ██▀ 
 ▀▄▀ █▄▄ █ ▀█ █▄▀ █ █ ▀█ ▀▄█    █ ▀ █ █▀█ ▀▄▄ █ █ █ █ ▀█ █▄▄ 
"""

label_panel = Panel.fit(label, subtitle= "☛ [italic] Snack Time, Your Way, Everyday![/] ☚ ", style="bold gold3", box=box.DOUBLE)
console.print(label_panel, justify="center")
print()

# Animated greeting
def greet(greeting, delay=0.02):
    for char in greeting:
        console.print(Text(char, style="cyan1"), end='')
        time.sleep(delay)

greeting = "ᴡᴇʟᴄᴏᴍᴇ! ᴛᴀᴋᴇ ᴀ ʟᴏᴏᴋ ᴀᴛ ᴛʜᴇ sᴇʟᴇᴄᴛɪᴏɴ.".center(console.width)
greet(greeting)  
print("\n")  

### MAIN PROGRAM ########################################################################################################################

class VendingMachine:
    def __init__(self):
        self.item = {
            'CHIPS': [
                {'CODE': 'A1', 'PRODUCT': 'Doritos Sweet Chili Pepper', 'PRICE': 3.95, 'STOCK': 4},
                {'CODE': 'A2', 'PRODUCT': 'Nova Homestyle BBQ Flavor', 'PRICE': 2.75, 'STOCK': 4},
                {'CODE': 'A3', 'PRODUCT': 'Piattos Cheese Flavored', 'PRICE': 3.55, 'STOCK': 4},
                {'CODE': 'A4', 'PRODUCT': 'Takis Blue Heat', 'PRICE': 3.95, 'STOCK': 4}],
            'SNACKS': [
                {'CODE': 'B1', 'PRODUCT': 'Combos Pepperoni Pizza Chips', 'PRICE': 3.95, 'STOCK': 4},
                {'CODE': 'B2', 'PRODUCT': 'Breadpan Toasted Garlic', 'PRICE': 5.00, 'STOCK': 4}, 
                {'CODE': 'B3', 'PRODUCT': "Snyder's Mini Pretzels", 'PRICE': 5.30, 'STOCK': 4},
                {'CODE': 'B4', 'PRODUCT': 'Goldfish Crackers', 'PRICE': 5.90, 'STOCK': 4}],
            'DRINKS': [
                {'CODE': 'C1', 'PRODUCT': "Masafi Alkaline Water", 'PRICE': 1.95, 'STOCK': 4},
                {'CODE': 'C2', 'PRODUCT': 'Nescafe Chilled Latte', 'PRICE': 2.50, 'STOCK': 4},
                {'CODE': 'C3', 'PRODUCT': 'Coca-Cola Cherry', 'PRICE': 2.40, 'STOCK': 4},
                {'CODE': 'C4', 'PRODUCT': 'Fanta Orange', 'PRICE': 7.00, 'STOCK': 4}
            ]
        }
        self.balance = 0.0
        self.console = Console()

### MENU ########################################################################################################################

    def menu(self):
            table = Table(header_style= "yellow", box= box.DOUBLE_EDGE, style="yellow")

            table.add_column("ITEM CODE", justify="center", no_wrap=True)
            table.add_column("PRODUCT", justify="center", no_wrap=True)
            table.add_column("PRICE", justify="center", no_wrap=True)
            table.add_column("STOCK", justify="center", no_wrap=True)
            
            for category, items in self.item.items():
                table.add_row("", "[bold]" + category + "[/bold]", "", "", style="navy_blue on light_cyan1")
                table.add_row()
                for item in items:
                    table.add_row(
                        f"[cyan]{item['CODE']}[/]",
                        f"[pale_green1]{item['PRODUCT']}[/]",
                        f"[deep_sky_blue1]{item['PRICE']:.2f}[/]",
                        f"[gold3]{item['STOCK']}[/]"
                    )
                table.add_row(end_section=True)

            self.console.print(table, justify="center")
            self.console.print()
            self.console.rule(style="bold")

### USER BALANCE ########################################################################################################################

    def display_balance(self):
        self.console.print(f"[chartreuse1]ᴄᴜʀʀᴇɴᴛ ʙᴀʟᴀɴᴄᴇ[/chartreuse1] : [bold]${self.balance:.2f}[/]\n", justify="center")

### CONDITION WHEN PAYMENT IS 0 ########################################################################################################################

    def insert_money(self, amount):
        if amount > 0:
            self.balance += amount
            self.display_balance()
        else:
            self.console.print("⚠️  [red]ɪɴᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ. ᴘʟᴇᴀsᴇ ɪɴsᴇʀᴛ ᴀ ᴘᴏsɪᴛɪᴠᴇ ᴀᴍᴏᴜɴᴛ.[/]", justify="center")
    
### ITEM PURCHASE ########################################################################################################################

    def selected_items(self):
        selected_items = []
        self.menu()  
        print()

        while True:
            item_code_prompt = "ᴇɴᴛᴇʀ ᴛʜᴇ ɪᴛᴇᴍ ᴄᴏᴅᴇ || ᴛʏᴘᴇ 'ᴅᴏɴᴇ' ᴛᴏ ꜰɪɴɪꜱʜ : "
            self.console.print(" " * 39 + item_code_prompt, style="bold cyan1", end="")
            code = self.console.input("").upper()

            if code == 'DONE':
                break

            selected_category = None

            found_item = False
            for category_name, category_items in self.item.items():
                for item in category_items:
                    if item['CODE'] == code and item['STOCK'] > 0:
                        selected_items.append(item)
                        item['STOCK'] -= 1
                        product_name = escape(item['PRODUCT'])
                        self.console.print(f"[green]sᴇʟᴇᴄᴛᴇᴅ[/] [gold3]►[/] [bold]{item['PRODUCT']}[/]\n", justify="center")
                        self.update_stock(item['CODE'], item['STOCK'])
                        selected_category = category_name
                        found_item = True
                        break

            if not found_item:
                self.console.print("⚠️  [red]ɪɴᴠᴀʟɪᴅ ᴄᴏᴅᴇ ᴏʀ ɪᴛᴇᴍ ᴏᴜᴛ ᴏꜰ sᴛᴏᴄᴋ.[/red]", justify="center")
            
            if selected_items:
                cancel_item = self.console.print("ᴡᴀɴᴛ ᴛᴏ ᴄᴀɴᴄᴇʟ ᴛʜɪs ɪᴛᴇᴍ? (ʏᴇs/ɴᴏ):", justify="center")
                cancel_choice = self.console.input(cancel_item).lower()

                if cancel_choice == 'yes':
                    removed_item = selected_items.pop()
                    self.console.print(f"[red]ᴄᴀɴᴄᴇʟʟᴇᴅ[/] [gold3]►[/] [bold]{removed_item['PRODUCT']}[/]\n", justify="center")
                    self.update_stock(removed_item['CODE'], removed_item['STOCK'])

            if selected_category is not None:
                self.suggest_items(selected_category)

        return selected_items

### SUGGESTION FEATURE ########################################################################################################################

    def suggest_items(self, category):
        suggestions = []

        # Define suggestions based on the category
        if category == 'DRINKS':
            suggestions = self.item['SNACKS'] + self.item['CHIPS']
        elif category == 'SNACKS':
            suggestions = self.item['DRINKS'] + self.item['CHIPS']
        elif category == 'CHIPS':
            suggestions = self.item['DRINKS'] + self.item['SNACKS']

        # Randomized suggestions
        random.shuffle(suggestions)

        # Print a single suggestion if available
        if suggestions:
            self.console.print(f"[dark_orange]🙋 ʏᴏᴜ ᴍɪɢʜᴛ ᴀʟsᴏ ʟɪᴋᴇ :[/]", justify="center")
            suggested_item = suggestions[0]
            self.console.print(f"[bold]{suggested_item['PRODUCT']}[/bold] - ${suggested_item['PRICE']:.2f}\n", justify="center")
        else:
            self.console.print("ɴᴏ sᴜɢɢᴇsᴛɪᴏɴs ᴀᴠᴀɪʟᴀʙʟᴇ ꜰᴏʀ ᴛʜɪs ᴄᴀᴛᴇɢᴏʀʏ.", justify="center")


### STOCK UPDATE #######################################################################################################################

    def update_stock(self, code, new_stock):
            self.console.print(f"[dark_orange]sᴛᴏᴄᴋ ᴜᴘᴅᴀᴛᴇᴅ[/] : [cyan]{code}[/] - [gold3]{new_stock}[/]\n", justify="center")    

### RECEIPT AND PAYMENT #######################################################################################################################

    def make_payment(self):
        # Dispensing animation
        print()
        for i in track(range(20), description="[magenta]                                ᴅɪsᴘᴇɴsɪɴɢ[/]"):
            time.sleep(0.02) 

        self.console.print("\n+⁌┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉⁍+", justify="center", style="gold3")
        self.console.print("sᴇʟᴇᴄᴛᴇᴅ ɪᴛᴇᴍs :\n", justify="center", style="bold cyan1")
        total_price = sum(item['PRICE'] for item in self.selected_items)

        for item in self.selected_items:
            self.console.print(f"[bold]{item['PRODUCT']}[/] - ${item['PRICE']:.2f}", justify="center")

        self.console.print("⁌┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉⁍", justify="center", style="gold3")
        self.console.print(f"ᴛᴏᴛᴀʟ :  [bold]${total_price:.2f}[/]", justify="center", style="bold cyan1")

        self.console.print("+⁌┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉⁍+", justify="center", style="gold3")
        while self.balance < total_price:
            amount = self.console.input(" " * 51 + "[bold cyan1]ɪɴsᴇʀᴛ ᴍᴏɴᴇʏ ᴛᴏ ᴘᴀʏ : $[/]")
            self.insert_money(float(amount))

            if self.balance < total_price:
                remaining_amount = total_price - self.balance
                self.console.print(f"⚠️  [red]ɪɴsᴜꜰꜰɪᴄɪᴇɴᴛ ꜰᴜɴᴅs [/]|| [red]ʏᴏᴜ ɴᴇᴇᴅ ᴀɴ ᴀᴅᴅɪᴛɪᴏɴᴀʟ ${remaining_amount:.2f}[/]", justify="center")

        change = self.balance - total_price
        self.console.print(f"""[green]ᴘᴀʏᴍᴇɴᴛ sᴜᴄᴄᴇssꜰᴜʟ! ᴛʜᴀɴᴋ ʏᴏᴜ ꜰᴏʀ ʏᴏᴜʀ ᴘᴜʀᴄʜᴀsᴇ![/] 
[cyan1]ʏᴏᴜʀ ᴄʜᴀɴɢᴇ : [bold]${change:.2f}[/]""", justify="center", style="bold")
        print()


###########################################################################################################################

if __name__ == "__main__":
    vending_machine = VendingMachine()

    vending_machine.selected_items = vending_machine.selected_items()

    vending_machine.make_payment()
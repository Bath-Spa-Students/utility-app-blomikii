# VENDING MACHINE

# Imports
from rich.console import Console
from rich.progress import track
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box
import random
import time
import sys

##################################################################################################################################################################

# Create an instance of Rich's console library to access it
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
def greet(greeting):
    for letter in greeting:
        console.print(Text(letter, style="cyan1"), end='') # end='' prints the letters in the same line
        time.sleep(0.02) # Used to print the letters with a fixed delay

greeting = "ᴡᴇʟᴄᴏᴍᴇ! ᴛᴀᴋᴇ ᴀ ʟᴏᴏᴋ ᴀᴛ ᴛʜᴇ sᴇʟᴇᴄᴛɪᴏɴ.".center(console.width) # --> Justify parameter is not suitable and will print the letters in separate lines
greet(greeting)  
print("\n")  

###  01 MAIN PROGRAM ################################################################################################################################################

class VendingMachine: # Encapsulate all methods
    def __init__(self): # Initializing attributes
        self.item = { 
            'CHIPS': [ # Triple nested data structures to declare the categories and their items
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
        self.balance = 0.0 # User's funds
        self.console = Console() # Accessing rich library inside the class

### 02 MENU ########################################################################################################################################################

    def menu(self):
            table = Table(header_style= "yellow", box= box.DOUBLE_EDGE, style="yellow")

            table.add_column("ITEM CODE", justify="center", no_wrap=True)
            table.add_column("PRODUCT", justify="center", no_wrap=True)
            table.add_column("PRICE", justify="center", no_wrap=True)
            table.add_column("STOCK", justify="center", no_wrap=True)
            
            for category, items in self.item.items(): # Loops through the categories and their items
                table.add_row("", "[bold]" + category + "[/bold]", "", "", style="navy_blue on light_cyan1")
                table.add_row()
                for item in items: # Loops through the items in each category and prints them
                    table.add_row(
                        f"[cyan]{item['CODE']}[/]",
                        f"[pale_green1]{item['PRODUCT']}[/]",
                        f"[deep_sky_blue1]{item['PRICE']:.2f}[/]",
                        f"[gold3]{item['STOCK']}[/]"
                    )
                table.add_row(end_section=True) # Adds a line to separate the item categories

            self.console.print(table, justify="center")
            self.console.print()
            self.console.rule(style="bold") # console.rule draws a horizontal line | useful for sectioning the terminal

### 03 STOCK UPDATE ###############################################################################################################################################

    def update_stock(self, code, new_stock):
            self.console.print(f"[dark_orange]sᴛᴏᴄᴋ ᴜᴘᴅᴀᴛᴇᴅ[/] : [cyan]{code}[/] - [gold3]{new_stock}[/]\n", justify="center")    

### 04 USER BALANCE ###############################################################################################################################################

    def display_balance(self):
        self.console.print(f"[chartreuse1]ᴄᴜʀʀᴇɴᴛ ʙᴀʟᴀɴᴄᴇ[/chartreuse1] : [bold]${self.balance:.2f}[/]\n", justify="center") # Displays the user's current funds

### 05 SUGGESTION FEATURE ##########################################################################################################################################

    def suggest_items(self, category):
        suggestions = []

        # Suggestions are based on the selected item's category to avoid repetition
        if category == 'DRINKS':
            suggestions = self.item['SNACKS'] + self.item['CHIPS']
        elif category == 'SNACKS':
            suggestions = self.item['DRINKS'] + self.item['CHIPS']
        elif category == 'CHIPS':
            suggestions = self.item['DRINKS'] + self.item['SNACKS']

        # Randomized suggestions
        random.shuffle(suggestions)

        if suggestions:
            self.console.print(f"[dark_orange]🙋 ʏᴏᴜ ᴍɪɢʜᴛ ᴀʟsᴏ ʟɪᴋᴇ :[/]", justify="center")
            suggested_item = suggestions[0] # This is randomized by the random function used
            self.console.print(f"[bold]{suggested_item['PRODUCT']}[/bold] - ${suggested_item['PRICE']:.2f}\n", justify="center")
        else:
            self.console.print("ɴᴏ sᴜɢɢᴇsᴛɪᴏɴs ᴀᴠᴀɪʟᴀʙʟᴇ ꜰᴏʀ ᴛʜɪs ᴄᴀᴛᴇɢᴏʀʏ.", justify="center")
    
### 06 ITEM PURCHASE ###############################################################################################################################################

    def selected_items(self):
        selected_items = [] # Starting with an empty list | Selected items are placed here later on
        self.menu() # Display the menu 
        print()

        while True:
            item_code_prompt = "ᴇɴᴛᴇʀ ᴛʜᴇ ɪᴛᴇᴍ ᴄᴏᴅᴇ || ᴛʏᴘᴇ 'ᴅᴏɴᴇ' ᴛᴏ ꜰɪɴɪꜱʜ : "
            self.console.print(" " * 39 + item_code_prompt, style="bold cyan1", end="")
            code = self.console.input().upper() # Entered item code is converted into uppercase to avoid input issues

            if code == 'DONE': 
                break

            selected_category = None # Indicates that no category has been selected yet | This is meant for product suggestions

            found_item = False 

            for category_name, category_items in self.item.items():
                for item in category_items:
                    if item['CODE'] == code and item['STOCK'] > 0:
                        selected_items.append(item) # Selected items are added to the empty list (selected_items=[])
                        item['STOCK'] -= 1 # Stock is updated and deducted by 1
                        self.console.print(f"[green]sᴇʟᴇᴄᴛᴇᴅ[/] [gold3]►[/] [bold]{item['PRODUCT']}[/]\n", justify="center")
                        self.update_stock(item['CODE'], item['STOCK']) # Calls the method and displays updated item stock
                        selected_category = category_name # selected_category is now updated with the selected item's category
                        found_item = True
                        break

            if not found_item:
                self.console.print("⚠️  [red]ɪɴᴠᴀʟɪᴅ ᴄᴏᴅᴇ ᴏʀ ɪᴛᴇᴍ ᴏᴜᴛ ᴏꜰ sᴛᴏᴄᴋ.[/red]", justify="center")

            if selected_category is not None: # Displays the suggestion based on the selected item's category
                self.suggest_items(selected_category)

        return selected_items

### 07 CONDITION WHEN PAYMENT IS 0 OR LESS ########################################################################################################################
    
    def insert_money(self, amount):
        if amount > 0:
            self.balance += amount # User's inputted money is added to the balance from self.balance
            self.display_balance() # Calls the method to display user's current balance
        else:
            self.console.print("⚠️  [red]ɪɴᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ. ᴘʟᴇᴀsᴇ ɪɴsᴇʀᴛ ᴀ ᴘᴏsɪᴛɪᴠᴇ ᴀᴍᴏᴜɴᴛ.[/]", justify="center")

### 08 RECEIPT AND PAYMENT ########################################################################################################################################

    def make_payment(self):
        # Dispensing animation
        print()
        for i in track(range(20), description="[magenta]                                ᴅɪsᴘᴇɴsɪɴɢ[/]"): # Justify argument was not applicable, so spaces were added instead
            time.sleep(0.02) 

        self.console.print("\n+⁌┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉⁍+", justify="center", style="gold3")
        self.console.print("sᴇʟᴇᴄᴛᴇᴅ ɪᴛᴇᴍs :\n", justify="center", style="bold cyan1")
       
        for item in self.selected_items: # All purchased items are printed
            self.console.print(f"[bold]{item['PRODUCT']}[/] - ${item['PRICE']:.2f}", justify="center")

        self.console.print("⁌┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉⁍", justify="center", style="gold3")

        total_price = sum(item['PRICE'] for item in self.selected_items) # Calculates the total of all purchased items

        self.console.print(f"ᴛᴏᴛᴀʟ :  [bold]${total_price:.2f}[/]", justify="center", style="bold cyan1") 
        self.console.print("+⁌┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉⁍+", justify="center", style="gold3")
        
        while self.balance < total_price: # Checking payment validity
            amount = self.console.input(" " * 52 + "[bold cyan1]ɪɴsᴇʀᴛ ᴍᴏɴᴇʏ ᴛᴏ ᴘᴀʏ : $[/]")
            self.insert_money(float(amount))

            if self.balance < total_price:
                remaining_amount = total_price - self.balance # To inform the user of their remaining charges
                self.console.print(f"⚠️  [red]ɪɴsᴜꜰꜰɪᴄɪᴇɴᴛ ꜰᴜɴᴅs [/]|| [red]ʏᴏᴜ ɴᴇᴇᴅ ᴀɴ ᴀᴅᴅɪᴛɪᴏɴᴀʟ ${remaining_amount:.2f}[/]", justify="center") 

        change = self.balance - total_price
        self.console.print(f"""[green]ᴘᴀʏᴍᴇɴᴛ sᴜᴄᴄᴇssꜰᴜʟ! ᴛʜᴀɴᴋ ʏᴏᴜ ꜰᴏʀ ʏᴏᴜʀ ᴘᴜʀᴄʜᴀsᴇ![/] 
[cyan1]ʏᴏᴜʀ ᴄʜᴀɴɢᴇ : [bold]${change:.2f}[/]""", justify="center", style="bold")
        print()


### 09 EXECUTING ###################################################################################################################################################

vending_machine= VendingMachine()
vending_machine.selected_items = vending_machine.selected_items()
vending_machine.make_payment()


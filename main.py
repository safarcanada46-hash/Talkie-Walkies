import time
import os

# ANSI color codes for colorful output
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

# Game state
money = 0
carry_capacity = 3
oven_speed = 2.0  # seconds per pizza
worker = False
worker_income_rate = 5  # seconds per $1 if worker active
pizzas_in_oven = 0
last_oven_time = time.time()
last_worker_time = time.time()
pizzas_carried = 0
level = 1
deliveries = 0
experience = 0
exp_to_next_level = 100

# Upgrade costs
carry_upgrade_cost = 10
oven_upgrade_cost = 20
worker_cost = 50

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_status():
    print(f"{Colors.CYAN}=== TERMINAL ARCADE IDLE SIMULATOR ==={Colors.RESET}")
    print(f"{Colors.GREEN}Money: 💰{money}{Colors.RESET}")
    print(f"{Colors.YELLOW}Level: {level} (Exp: {experience}/{exp_to_next_level}){Colors.RESET}")
    print(f"{Colors.BLUE}Carry Capacity: {carry_capacity}{Colors.RESET}")
    print(f"{Colors.RED}Oven Speed: {oven_speed}s per pizza{Colors.RESET}")
    print(f"{Colors.MAGENTA}Worker: {'Active' if worker else 'Inactive'}{Colors.RESET}")
    print(f"{Colors.WHITE}Pizzas in Oven: {pizzas_in_oven}{Colors.RESET}")
    print(f"{Colors.WHITE}Pizzas Carried: {pizzas_carried}/{carry_capacity}{Colors.RESET}")
    print()

def update_game():
    global pizzas_in_oven, last_oven_time, money, last_worker_time
    current_time = time.time()
    
    # Update oven
    if current_time - last_oven_time >= oven_speed:
        pizzas_in_oven += 1
        last_oven_time = current_time
    
    # Update worker income
    if worker and current_time - last_worker_time >= worker_income_rate:
        money += 1
        last_worker_time = current_time

def go_to_oven():
    global pizzas_carried, pizzas_in_oven
    clear_screen()
    print(f"{Colors.RED}=== OVEN ZONE ==={Colors.RESET}")
    print("The oven is hot and ready!")
    available = min(carry_capacity - pizzas_carried, pizzas_in_oven)
    if available > 0:
        pizzas_carried += available
        pizzas_in_oven -= available
        print(f"You picked up {available} pizza(s)!")
    else:
        print("No pizzas available or you're at carry capacity.")
    input("Press Enter to return to main menu...")

def go_to_delivery():
    global pizzas_carried, money, deliveries, experience
    clear_screen()
    print(f"{Colors.BLUE}=== DELIVERY ZONE ==={Colors.RESET}")
    print("Customers are waiting!")
    if pizzas_carried > 0:
        earned = pizzas_carried * 1  # $1 per pizza
        money += earned
        deliveries += pizzas_carried
        experience += pizzas_carried * 10  # 10 exp per delivery
        print(f"You delivered {pizzas_carried} pizza(s) and earned 💰{earned}!")
        pizzas_carried = 0
    else:
        print("You have no pizzas to deliver.")
    input("Press Enter to return to main menu...")

def open_shop():
    global money, carry_capacity, oven_speed, worker
    while True:
        clear_screen()
        print(f"{Colors.GREEN}=== SHOP ==={Colors.RESET}")
        print(f"Money: 💰{money}")
        print()
        print("Upgrades:")
        print(f"1. Increase Carry Capacity (+1) - 💰{carry_upgrade_cost}")
        print(f"2. Upgrade Oven Speed (-0.5s) - 💰{oven_upgrade_cost}")
        print(f"3. Hire Worker (Auto-income) - 💰{worker_cost}")
        print("4. Back to Main Menu")
        print()
        choice = input("Choose an upgrade: ")
        
        if choice == '1':
            if money >= carry_upgrade_cost:
                money -= carry_upgrade_cost
                carry_capacity += 1
                carry_upgrade_cost += 5  # Increase cost
                print("Carry capacity upgraded!")
            else:
                print("Not enough money!")
        elif choice == '2':
            if money >= oven_upgrade_cost:
                money -= oven_upgrade_cost
                oven_speed = max(0.5, oven_speed - 0.5)
                oven_upgrade_cost += 10  # Increase cost
                print("Oven speed upgraded!")
            else:
                print("Not enough money!")
        elif choice == '3':
            if not worker and money >= worker_cost:
                money -= worker_cost
                worker = True
                print("Worker hired! Auto-income activated.")
            elif worker:
                print("Worker already hired!")
            else:
                print("Not enough money!")
        elif choice == '4':
            break
        else:
            print("Invalid choice.")
        input("Press Enter to continue...")

def check_level_up():
    global level, experience, exp_to_next_level, carry_capacity, oven_speed
    while experience >= exp_to_next_level:
        experience -= exp_to_next_level
        level += 1
        exp_to_next_level += 50
        carry_capacity += 1
        oven_speed = max(0.5, oven_speed - 0.2)
        print(f"{Colors.YELLOW}LEVEL UP! You are now level {level}!{Colors.RESET}")
        print("Bonuses: +1 Carry Capacity, -0.2s Oven Speed")

# Main game loop
while True:
    update_game()
    check_level_up()
    clear_screen()
    print_status()
    print("What would you like to do?")
    print("1. Go to Oven (Pick up pizzas)")
    print("2. Go to Delivery Point (Deliver pizzas)")
    print("3. Open Shop (Buy upgrades)")
    print("4. Exit Game")
    print()
    choice = input("Enter your choice: ")
    
    if choice == '1':
        go_to_oven()
    elif choice == '2':
        go_to_delivery()
    elif choice == '3':
        open_shop()
    elif choice == '4':
        print("Thanks for playing!")
        break
    else:
        print("Invalid choice. Try again.")
        time.sleep(1)

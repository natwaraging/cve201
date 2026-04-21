import math

def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("❌ Please enter a valid number.")

def concrete_calculator_pro():
    print("\n" + "="*40)
    print("     CONCRETE MIXTURE CALCULATOR (PRO V2) ")
    print("="*40)

    # 1. Get dimensions and check for valid input
    width = get_float_input("📏 Width (meters): ")
    length = get_float_input("📏 Length (meters): ")
    depth = get_float_input("📏 Thickness/Height (meters): ")
    waste_percent = get_float_input("⚠️ Extra allowance for waste (%): ")

    # 2. Select mixing ratio
    print("\nSelect mixing ratio (Cement:Sand:Stone):")
    print("1. [1:1.5:3] - General structure (beams, columns)")
    print("2. [1:2:4]   - Flooring, pavements")
    print("3. [1:3:5]   - Lean concrete, leveling")

    choice = input("Choose number (1-3) [default is 2]: ")
    if choice == '1':
        ratio = (1, 1.5, 3)
    elif choice == '3':
        ratio = (1, 3, 5)
    else:
        ratio = (1, 2, 4)

    # 3. Calculate volumes
    net_volume = width * length * depth
    total_volume = net_volume * (1 + (waste_percent / 100))

    # Standard multiplier for dry volume (1.54 accounts for shrinkage and voids)
    dry_volume = total_volume * 1.54
    sum_ratio = sum(ratio)

    # 4. Calculate materials
    cement_m3 = (ratio[0] / sum_ratio) * dry_volume
    sand_m3 = (ratio[1] / sum_ratio) * dry_volume
    stone_m3 = (ratio[2] / sum_ratio) * dry_volume

    # One 50kg cement bag = approx 0.035 m³
    cement_bags = math.ceil(cement_m3 / 0.035)
    # Water estimation: 1 cement bag uses about 25 liters water at 0.5 W/C ratio
    water_liters = cement_bags * 25

    # 5. Display result
    print("\n" + "📊 Calculation Summary".center(40, "="))
    print(f"Net concrete volume:           {net_volume:>8.2f} m³")
    print(f"Required volume (+{waste_percent}%): {total_volume:>8.2f} m³")
    print(f"Selected ratio:             {ratio[0]}:{ratio[1]}:{ratio[2]}")
    print("-" * 40)
    print(f"✅ Cement (50kg bags):      {cement_bags:>8}")
    print(f"✅ Sand:                   {sand_m3:>8.2f} m³")
    print(f"✅ Stone (3/4”):           {stone_m3:>8.2f} m³")
    print(f"✅ Water (approx):         {water_liters:>8.2f} liters")
    print("=" * 40)
    print("*Note: 1 m³ = 1 cubic meter")

if __name__ == "__main__":
    concrete_calculator_pro()
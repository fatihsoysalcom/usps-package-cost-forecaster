import math

# --- Simplified USPS-like Rules (for demonstration purposes) ---
# These values are illustrative and may not reflect exact current USPS rules.
# The purpose is to demonstrate the *concept* of applying rules to predict costs.

DIMENSIONAL_DIVISOR = 166  # Common for domestic US shipments (cubic inches)
OVERSIZE_LENGTH_LIMIT = 60 # inches (e.g., packages over this length might incur a surcharge)
OVERSIZE_GIRTH_LIMIT = 108 # inches (Length + Girth > this limit might incur surcharge)
OVERSIZE_SURCHARGE_AMOUNT = 15.00 # USD, illustrative additional cost
WEIGHT_DISCREPANCY_THRESHOLD_PERCENT = 0.10 # 10% tolerance for declared vs actual weight
WEIGHT_DISCREPANCY_SURCHARGE_AMOUNT = 10.00 # USD, illustrative additional cost

def calculate_girth(width, height):
    """Calculates the girth of a package."""
    # Girth = (2 * Width) + (2 * Height)
    return (2 * width) + (2 * height)

def calculate_dimensional_weight(length, width, height, divisor):
    """
    Calculates the dimensional weight of a package.
    Used when a package is light but bulky; carriers charge based on the greater of actual or dimensional weight.
    """
    volume = length * width * height
    return math.ceil(volume / divisor) # USPS often rounds up to the next whole pound

def get_package_details(prompt_prefix):
    """Helper to get package dimensions and weight from user."""
    print(f"\n--- Enter {prompt_prefix} Package Details (in inches and pounds) ---")
    length = float(input(f"Enter {prompt_prefix} Length: "))
    width = float(input(f"Enter {prompt_prefix} Width: "))
    height = float(input(f"Enter {prompt_prefix} Height: "))
    weight = float(input(f"Enter {prompt_prefix} Weight: "))
    return length, width, height, weight

def analyze_package_costs():
    """
    Analyzes declared and actual package details to predict potential surcharges.
    """
    print("--- USPS Surcharge Predictor Tool ---")
    print("This tool helps identify potential unexpected costs based on simplified USPS-like rules.")

    # Get declared package details, as entered when creating a shipping label
    declared_length, declared_width, declared_height, declared_weight = get_package_details("DECLARED")

    # Get actual package details, which might be measured by the carrier and differ from declared
    actual_length, actual_width, actual_height, actual_weight = get_package_details("ACTUAL")

    potential_surcharges = []
    total_surcharges = 0.0

    print("\n--- Analysis Results ---")

    # 1. Check for Weight Discrepancy Surcharge
    # If actual weight significantly exceeds declared weight, a surcharge might apply.
    if actual_weight > declared_weight * (1 + WEIGHT_DISCREPANCY_THRESHOLD_PERCENT):
        potential_surcharges.append(
            f"Weight Discrepancy Surcharge: ${WEIGHT_DISCREPANCY_SURCHARGE_AMOUNT:.2f} "
            f"(Actual weight {actual_weight:.2f} lbs significantly exceeds declared {declared_weight:.2f} lbs)"
        )
        total_surcharges += WEIGHT_DISCREPANCY_SURCHARGE_AMOUNT

    # 2. Calculate Actual Billable Weight (considering Dimensional Weight)
    # Carriers like USPS charge based on the greater of actual weight or dimensional weight.
    actual_dimensional_weight = calculate_dimensional_weight(
        actual_length, actual_width, actual_height, DIMENSIONAL_DIVISOR
    )
    actual_billable_weight = max(actual_weight, actual_dimensional_weight)

    if actual_dimensional_weight > actual_weight:
        potential_surcharges.append(
            f"Dimensional Weight Impact: Billable weight increased from {actual_weight:.2f} lbs "
            f"to {actual_dimensional_weight:.2f} lbs due to package bulkiness. "
            f"(This isn't a surcharge, but increases the base shipping cost.)"
        )

    # 3. Check for Oversize Surcharge
    # Packages exceeding certain length or combined length+girth limits incur surcharges.
    actual_girth = calculate_girth(actual_width, actual_height)
    length_plus_girth = actual_length + actual_girth

    if actual_length > OVERSIZE_LENGTH_LIMIT:
        potential_surcharges.append(
            f"Oversize Surcharge (Length): ${OVERSIZE_SURCHARGE_AMOUNT:.2f} "
            f"(Actual length {actual_length:.2f} inches exceeds {OVERSIZE_LENGTH_LIMIT} inches)"
        )
        total_surcharges += OVERSIZE_SURCHARGE_AMOUNT
    
    if length_plus_girth > OVERSIZE_GIRTH_LIMIT:
        # This is a separate rule, so it can be added even if length also triggered a surcharge.
        potential_surcharges.append(
            f"Oversize Surcharge (Length+Girth): ${OVERSIZE_SURCHARGE_AMOUNT:.2f} "
            f"(Actual Length+Girth {length_plus_girth:.2f} inches exceeds {OVERSIZE_GIRTH_LIMIT} inches)"
        )
        total_surcharges += OVERSIZE_SURCHARGE_AMOUNT


    print(f"\nDeclared Package Details: L:{declared_length:.2f} W:{declared_width:.2f} H:{declared_height:.2f} Weight:{declared_weight:.2f} lbs")
    print(f"Actual Package Details:   L:{actual_length:.2f} W:{actual_width:.2f} H:{actual_height:.2f} Weight:{actual_weight:.2f} lbs")
    print(f"Actual Billable Weight: {actual_billable_weight:.2f} lbs (used for base shipping cost calculation)")

    if potential_surcharges:
        print("\n--- POTENTIAL SURCHARGES IDENTIFIED! ---")
        for surcharge in potential_surcharges:
            print(f"- {surcharge}")
        print(f"\nEstimated Total Surcharges: ${total_surcharges:.2f}")
        print("ACTION REQUIRED: Adjust package details or consider alternative shipping options to avoid these costs.")
    else:
        print("\nNo immediate surcharges identified based on actual vs. declared details and current rules.")
        print("Your package details seem consistent with declared values and within standard limits.")

    print("\nNote: These rules and amounts are illustrative. Always refer to official carrier guidelines.")

if __name__ == "__main__":
    analyze_package_costs()

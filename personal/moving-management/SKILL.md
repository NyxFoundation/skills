---
name: moving-management
description: Comprehensive workflow for planning and executing residential moves, including inventory management, cost estimation, waste disposal, and vendor communication.
tags: [moving, inventory, waste-disposal, logistics]
---

# Moving Management Workflow

This skill governs the end-to-end process of residential relocation, focusing on minimizing friction through structured inventory, proactive waste management, and precise communication with moving companies.

## 1. Inventory & Classification
The primary objective is to move from a \"raw list\" to a \"disposition list\".

### Classification Categories
- **Keep (Bring)**: Items to be transported by the moving company.
- **Dispose (Waste/Sell)**: Items to be removed before the move.
- **Deferred**: Items with a specific date-based disposition (e.g., \"Pickup by X on Y date\").

### Disposition Strategies
- **Recycle Shop**: Fast removal, potential cash back (Electronic appliances, electronics).
- **Municipal Waste (粗大ゴミ)**: Fixed cost, requires appointment (Furniture, mattresses).
- **P2P / Giveaway (Jimoty)**: High effort, zero/low cost (Pianos, large furniture).
- **Specific Arrangement**: Third-party pickup (Bicycles, specific shared items).

## 2. Logistics & Cost Estimation
When calculating costs for long-distance moves (e.g., Tokyo $\to$ Toyama), use the following dimensions:

### Cost Drivers
- **Distance**: Total mileage.
- **Timing**:
  - *Peak Season (March-April)*: $1.5\text{x} \sim 1.7\text{x}$ multiplier.
  - *Off-Peak (May-February)*: Baseline rates.
- **Volume**:
  - *Single (Light)*: Minimal boxes, small appliances.
  - *Single (Heavy)*: Multiple large items (desk, shelf, large fridge).
  - *2-Person Equivalent*: Large furniture, multiple appliances, high box count.
  - *Sizing Requirement*: Moving companies require exact dimensions (W x D x H) for all large items to avoid surcharges.

### Estimation Range
- For \"Single-Heavy\" to \"2-Person\" long-distance moves in off-peak, budget $\approx \text{¥80,000} \sim \text{¥140,000}$ depending on the specific plan.

## 3. Cost Calculation Models (Bottom-Up)
When the user asks for \"cost-based\" (原価ベース) estimations, do not rely solely on market averages. Use a bottom-up calculation including:

### Direct Cash Outlay (Cash-out Cost)
- **Personnel**: 
  - Standard: ¥15,000/person/day.
  - Long-haul (12-15h): ¥18,000-20,000/person/day.
- **Vehicle**:
  - Own-fleet (Standard): ¥8,000-10,000/day (Depreciation + Maintenance).
  - Rental (Small/Low-cap): ¥50,000/day.
- **Variable Costs**:
  - Highway Tolls (Return trip).
  - Fuel (Distance / Fuel Efficiency * Price).
  - Packing Materials/Protection.

### Opportunity Cost (The \"Hidden\" Cost)
Moving companies value their assets by what they *could* have earned elsewhere.
- **Urban Opportunity Cost**: A truck + crew can typically handle 2-3 small moves per day in Tokyo (~¥90,000 total revenue). 
- **Long-haul Trade-off**: Dedicating a vehicle to a long-distance move for one day loses this urban revenue. This \"Opportunity Cost\" (機会原価) is often the primary driver of quotes for long-distance moves.

### Final Calculation Logic
`Estimated Quote = (Direct Cash Outlay + Opportunity Cost) * (1 + Profit Margin)`
- Typical Profit Margin: ~15%.
- The \"Reasonable Bottom Line\" for long-distance moves is often the `Cash Outlay + Opportunity Cost`.

## 4. Moving Company Communication Checklist
To avoid \"surprise charges\" on moving day, ensure the following are communicated during the quote:

### Item Details
- **Special Handling**: TV, Monitors (require specific padding), Bicycles (rack space), Large Furniture (desk, shelf).
- **Small Appliances**: 60L fridge (require defrosting/water drain 24h before), air purifiers.
- **Fragile Items**: Explicitly label glassware/ceramics to ensure dedicated padding/boxes.

### Site Conditions
- **Origin (Current)**: Floor, elevator availability/size, parking for truck, stair width.
- **Destination (New)**: Floor, elevator availability/size, parking for truck, road width (truck access).

### Service Options
- **Free-Date (フリー便)**: Lower cost, flexible timing.
- **Materials**: Request free cardboard boxes (e.g., Sakai provides up to 50).
- **Packing**: DIY vs. Professional.

## 5. Critical Timelines (T-Minus)
- **T-30 Days**: Start getting multiple quotes (Comparison is key).
- **T-14 Days**: Reserve municipal waste collection (粗大ゴミ) as slots fill up.
- **T-7 Days**: Confirm specific pickup times for third-party arrangements.
- **T-0**: Move day.

### Item-specific Logic
- **Bedding/Curtains**: Often forgotten in lists; verify if replacing at destination or transporting.
- **Perishables**: Clear fridge logic (consume/discard by T-1).
- **Electronics**: Pack peripherals (cables, remotes) in designated boxes to avoid loss.

## Pitfalls & Lessons
- **The \"Sizing\" Gap**: Don't assume a \"Single Pack\" (Kago-sha) can fit large furniture. Exact dimensions are critical to prevent last-minute quote spikes.
- **Waste Lead Time**: Municipal waste in Japan often requires $\ge 2$ weeks' notice. Do not wait until the last week.
- **Bicycle Logistics**: Confirm whether the moving truck has a dedicated rack or if the bike should be disassembled/packed.
- **Cash Outlay vs. Opportunity Cost**: Avoid assuming that a self-owned truck costs nothing. The \"Opportunity Cost\" of not doing 2-3 smaller urban moves is a major part of the professional quote logic.

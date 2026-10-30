#!/usr/bin/env python3
"""
Spot Instance GPU Training Budget Estimator 2026.
Calculates gross hours, checkpointing overhead, usable compute, and effective hourly rates for ML projects.
"""
import argparse

def estimate_spot_budget(budget, hourly_rate, overhead_pct):
    gross_hours = budget / hourly_rate if hourly_rate > 0 else 0.0
    overhead_hours = gross_hours * (overhead_pct / 100.0)
    usable_hours = gross_hours - overhead_hours
    effective_rate = budget / usable_hours if usable_hours > 0 else 0.0
    return {
        "budget": budget,
        "hourly_rate": hourly_rate,
        "overhead_pct": overhead_pct,
        "gross_hours": gross_hours,
        "overhead_hours": overhead_hours,
        "usable_hours": usable_hours,
        "effective_rate": effective_rate
    }

def main():
    parser = argparse.ArgumentParser(description="Spot Instance GPU Budget Estimator")
    parser.add_argument("--budget", type=float, default=500.0, help="Total allocated compute budget in USD (default: $500.00)")
    parser.add_argument("--hourly-rate", type=float, default=0.35, help="Spot instance rate in USD/hr (default: $0.35)")
    parser.add_argument("--overhead-pct", type=float, default=5.0, help="Checkpointing & resumption overhead percentage (default: 5.0%%)")
    args = parser.parse_args()

    res = estimate_spot_budget(args.budget, args.hourly_rate, args.overhead_pct)
    print(f"Allocated Budget:        ${res['budget']:.2f}")
    print(f"Spot Hourly Rate:        ${res['hourly_rate']:.2f}/hr")
    print(f"Gross Compute Hours:     {res['gross_hours']:.2f} hrs")
    print(f"Resumption Overhead:    {res['overhead_hours']:.2f} hrs ({args.overhead_pct:.1f}%)")
    print(f"Net Usable Compute:      {res['usable_hours']:.2f} hrs")
    print(f"Effective Rate:          ${res['effective_rate']:.4f}/usable-hr")

if __name__ == "__main__":
    main()

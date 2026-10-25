"""
STM32 Timer Prescaler (PSC) and Auto-Reload Register (ARR) Calculator.

Formula:
    f_out = f_clk / ((PSC + 1) * (ARR + 1))

Note on STM32 Clock Tree (RM0008 / RM0090):
    If the APB prescaler (PPRE1/PPRE2) is > 1, the hardware timer input clock
    is automatically doubled: f_clk = 2 * f_PCLK.

Usage Examples:
    python3 scripts/stm32_timer_calc.py --clk 72000000 --freq 50
    python3 scripts/stm32_timer_calc.py --clk 168000000 --freq 20000 --bits 32
    python3 scripts/stm32_timer_calc.py 72000000 1000
"""

import argparse
import math
import sys
from typing import List, Tuple


def solve_timer(
    f_clk: int,
    f_target: float,
    timer_bits: int = 16,
    top_n: int = 5,
) -> List[Tuple[float, int, int, float, float]]:
    """
    Find optimal (PSC, ARR) integer pairs minimizing frequency error
    and maximizing PWM duty-cycle resolution (highest ARR).
    """
    if f_clk <= 0:
        raise ValueError("Timer input clock (f_clk) must be > 0 Hz.")
    if f_target <= 0:
        raise ValueError("Target frequency (f_target) must be > 0 Hz.")
    if f_target > f_clk:
        raise ValueError("Target frequency cannot exceed timer input clock (f_clk).")

    max_arr = (1 << timer_bits) - 1
    candidates = []

    for psc in range(65536):
        divider = (psc + 1) * f_target
        arr_exact = (f_clk / divider) - 1.0
        if arr_exact < 0:
            break
        arr = round(arr_exact)
        if 0 <= arr <= max_arr:
            f_actual = f_clk / ((psc + 1) * (arr + 1))
            error_pct = abs(f_actual - f_target) / f_target * 100.0
            pwm_res_bits = math.log2(arr + 1)
            # Sort key: lowest relative error first, then highest ARR (best PWM resolution)
            candidates.append((error_pct, -arr, psc, arr, f_actual, pwm_res_bits))

    candidates.sort()
    return [
        (err, psc, arr, f_act, res_bits)
        for err, _, psc, arr, f_act, res_bits in candidates[:top_n]
    ]


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calculate optimal STM32 timer PSC and ARR register values."
    )
    parser.add_argument(
        "pos_args",
        nargs="*",
        type=float,
        help="Optional positional arguments: [f_clk_hz] [target_freq_hz]",
    )
    parser.add_argument(
        "--clk",
        type=int,
        default=None,
        help="Timer input clock frequency in Hz (default: 72000000)",
    )
    parser.add_argument(
        "--freq",
        type=float,
        default=None,
        help="Target update/PWM frequency in Hz (default: 50.0)",
    )
    parser.add_argument(
        "--bits",
        type=int,
        choices=[16, 32],
        default=16,
        help="Timer counter width in bits: 16 or 32 (default: 16)",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="Number of top solutions to display (default: 5)",
    )
    return parser.parse_args(argv)


def main() -> int:
    args = parse_args(sys.argv[1:])

    f_clk = args.clk if args.clk is not None else (
        int(args.pos_args[0]) if len(args.pos_args) >= 1 else 72_000_000
    )
    f_target = args.freq if args.freq is not None else (
        float(args.pos_args[1]) if len(args.pos_args) >= 2 else 50.0
    )

    try:
        results = solve_timer(f_clk, f_target, timer_bits=args.bits, top_n=args.top)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if not results:
        print(
            f"No valid (PSC, ARR) combination found for f_target={f_target} Hz "
            f"with a {args.bits}-bit timer at f_clk={f_clk} Hz.",
            file=sys.stderr,
        )
        return 1

    print(
        f"Target: {f_target:g} Hz | Timer Clock: {f_clk / 1e6:.3f} MHz "
        f"({args.bits}-bit Timer)"
    )
    print("-" * 78)
    print(
        f"{'PSC':<8} | {'ARR':<12} | {'Actual Freq (Hz)':<18} | "
        f"{'Error (%)':<12} | {'PWM Res (bits)'}"
    )
    print("-" * 78)

    for err, psc, arr, f_act, res_bits in results:
        print(
            f"{psc:<8} | {arr:<12} | {f_act:<18.4f} | "
            f"{err:<12.6f} | {res_bits:.2f} bits"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())

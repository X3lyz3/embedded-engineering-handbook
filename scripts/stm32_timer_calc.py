"""
STM32 Timer Prescaler (PSC) and Auto-Reload Register (ARR) Calculator.
Formula: f_out = f_clk / ((PSC + 1) * (ARR + 1))
Usage:   python3 stm32_timer_calc.py <f_clk_hz> <target_freq_hz>
Example: python3 stm32_timer_calc.py 72000000 50
"""
import sys

def solve_timer(f_clk: int, f_target: float, max_arr: int = 65535):
    results = []
    for psc in range(65536):
        arr_float = (f_clk / ((psc + 1) * f_target)) - 1
        arr = round(arr_float)
        if 0 <= arr <= max_arr:
            f_actual = f_clk / ((psc + 1) * (arr + 1))
            error_pct = abs(f_actual - f_target) / f_target * 100.0
            results.append((error_pct, -arr, psc, arr, f_actual))
    
    results.sort()
    return results[:5]

if __name__ == "__main__":
    f_clk = int(sys.argv[1]) if len(sys.argv) > 1 else 72_000_000
    f_target = float(sys.argv[2]) if len(sys.argv) > 2 else 50.0

    print(f"Target: {f_target} Hz | Timer Clock: {f_clk / 1e6:.2f} MHz (16-bit Timer)")
    print("-" * 65)
    print(f"{'PSC':<8} | {'ARR':<8} | {'Actual Freq (Hz)':<18} | {'Error (%)'}")
    print("-" * 65)

    for err, _, psc, arr, f_act in solve_timer(f_clk, f_target):
        print(f"{psc:<8} | {arr:<8} | {f_act:<18.4f} | {err:.6f}%")

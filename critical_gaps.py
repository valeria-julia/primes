def find_critical_gaps(p_limit):
    primes = [n for n in range(2, p_limit + 1) if all(n % i != 0 for i in range(2, int(n**0.5) + 1))]
    covered = set()
    # Речник за активните празнини: {gap_value: {"p_start": p, "steps": 0}}
    active_gaps = {}
    history = [] # Записваме само изчистените празнини за анализ

    for i, p in enumerate(primes):
        if p < 3: continue
        double_p = 2 * p
        covered.add(double_p)
        
        # 1. Директно изчистване, ако double_p е било gap
        if double_p in active_gaps:
            data = active_gaps.pop(double_p)
            history.append({"gap": double_p, "p_start": data["p_start"], "p_end": p, "life": data["steps"]})

        # 2. Сумиране с предходни
        current_gap_values = set(active_gaps.keys())
        for j in range(i - 1, -1, -1):
            s = p + primes[j]
            if s in covered or s in current_gap_values: break
            if s % 2 == 0: covered.add(s)

        # 3. Регистриране на нови празнини
        if i > 0:
            prev_double = 2 * primes[i-1]
            for x in range(prev_double + 2, double_p, 2):
                if x not in covered and x not in active_gaps:
                    active_gaps[x] = {"p_start": p, "steps": 0}

        # 4. Опит за изчистване и увеличаване на "живота"
        cleared_this_step = []
        for gap, data in active_gaps.items():
            p1_idx, p0_idx = i, i - 1
            is_cleared = False
            while p0_idx >= 0 and p1_idx < len(primes):
                current_sum = primes[p1_idx] + primes[p0_idx]
                if current_sum == gap:
                    is_cleared = True; break
                elif current_sum > gap: p0_idx -= 1
                else: break
            
            if is_cleared:
                cleared_this_step.append(gap)
                history.append({"gap": gap, "p_start": data["p_start"], "p_end": p, "life": data["steps"]})
            else:
                data["steps"] += 1 # Увеличаваме живота, ако оцелее
                
        for gap in cleared_this_step:
            del active_gaps[gap]

    # Сортиране по продължителност на живота (life)
    critical = sorted(history, key=lambda x: x['life'], reverse=True)
    return critical[:10] # Връщаме топ 10 най-упорити празнини
    # return history

# Тест до P=1000
top_gaps = find_critical_gaps(1000)
print(f"{'GAP':<8} | {'P_START':<10} | {'P_CLEAR':<10} | {'LIFE (STEPS)'}")
print("-" * 45)
for g in top_gaps:
    print(f"{g['gap']:<8} \t {g['p_start']:<10} \t {g['p_end']:<10} \t {g['life']}")

def process_primes_with_immediate_clear(p_limit):
    # 1. Генериране на прости числа
    primes = [n for n in range(2, p_limit + 1) if all(n % i != 0 for i in range(2, int(n**0.5) + 1))]
    
    covered = set()
    active_gaps = [] # Списък от речници {"gap": x, "p1_idx": i}

    for i, p in enumerate(primes):
        # Винаги добавяме 2*p към покритите
        double_p = 2 * p
        covered.add(double_p)
        
        # Ако double_p е било в списъка с празнини, го махаме (директно изчистване)
        active_gaps = [g for g in active_gaps if g["gap"] != double_p]

        # 2. Сумиране с предходни (STOP при вече покрито или gap)
        # Използваме списък от самите стойности на празнините за бърза проверка
        current_gap_values = {g["gap"] for g in active_gaps}
        
        for j in range(i - 1, -1, -1):
            s = p + primes[j]
            if s in covered or s in current_gap_values:
                break
            if s % 2 == 0:
                covered.add(s)

        # 3. Регистрация на нови празнини между предишното и текущото 2*p
        if i > 0:
            prev_double = 2 * primes[i-1]
            for x in range(prev_double + 2, double_p, 2):
                if x not in covered and x not in current_gap_values:
                    active_gaps.append({"gap": x, "p1_idx": i, "prime": primes[i]})
                    current_gap_values.add(x)

        # 4. Опит за ИЗЧИСТВАНЕ на активните празнини с текущото p като p1 или p0
        remaining_gaps = []
        for item in active_gaps:
            gap = item["gap"]
            p1_idx, p0_idx = i, i - 1
            is_cleared = False
            
            # Логика за балансиране (движение на p1 и p0)
            while p0_idx >= 0 and p1_idx < len(primes):
                current_sum = primes[p1_idx] + primes[p0_idx]
                if current_sum == gap:
                    covered.add(gap)
                    is_cleared = True
                    break
                elif current_sum > gap:
                    p0_idx -= 1
                else:
                    # В този контекст p1 е ограничено до текущото p, 
                    # за да не "предсказваме" бъдещи изчиствания
                    break 
            
            if not is_cleared:
                remaining_gaps.append(item)
        active_gaps = remaining_gaps
    return [{"gap":g["gap"], "prime":g["prime"]} for g in active_gaps]
    # return sorted([g["gap"] for g in active_gaps])

# Тест за p=30
final_unresolved_gaps = process_primes_with_immediate_clear(30)
print(f"Останали неизчистени празнини: {final_unresolved_gaps}")

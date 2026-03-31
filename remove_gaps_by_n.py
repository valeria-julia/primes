def process_primes_pipeline(p_limit, pass2=True):
    primes = [n for n in range(2, p_limit + 1) if all(n % i != 0 for i in range(2, int(n**0.5) + 1))]
    covered = set()
    active_gaps = [] # Списък от обекти {"gap": val, "p1_idx": idx}
    doubles = set()
    for i, p in enumerate(primes):
        if p < 3: continue
        n=0
        # --- PASS 1: Директно покритие (2*p) ---
        # 100 - 6 1000 - 6 10000 - 18 100000 - 30 1000000 - 32
        # 100 - 6 1000 - 20 10000 - 36 100000 - 70 1000000 - 114
        double_p =  2*p - 2*n
        # print(p, double_p)
        covered.add(double_p)
        doubles.add(p)
        # Премахваме веднага, ако 2*p е било в списъка с празнини
        active_gaps = [g for g in active_gaps if g["gap"] != double_p]
        # print(active_gaps)
        
        # --- PASS 2: Бързо сумиране (p + p_prev) със STOP ---
        # Тези суми попълват 'covered', което предотвратява създаването на нови празнини
        current_gap_vals = {g["gap"] for g in active_gaps}
        for j in range(i - 1, -1, -1):
            s = p + primes[j]
            if s in covered or s in current_gap_vals:
                break
            if s % 2 == 0:
                covered.add(s)

        
        # --- РЕГИСТРАЦИЯ: Генериране на нови празнини ---
        # Изпълнява се само между PASS 2 и PASS 3
        if i > 0:
            prev_double = 2 * primes[i-1]
            for x in range(prev_double + 2, double_p, 2):
                if x not in covered and x not in current_gap_vals:
                    active_gaps.append({"gap": x, "p1_idx": i, "prime": primes[i]})

        if pass2==True: 
            # --- PASS 3: Опит за изчистване на ОЦЕЛЕЛИТЕ празнини (Балансирано търсене) ---
            # Взима само това, което е останало в active_gaps след първите два паса
            remaining = []
            for item in active_gaps:
                gap = item["gap"]
                # Логика за Pass 3 (тук p1_idx е фиксиран на текущото p)
            
                p1_idx, p0_idx = i, i - 1
            
                is_cleared = False
                while p0_idx >= 0:
                    current_sum = primes[p1_idx] + primes[p0_idx]
                    if current_sum == gap:
                        covered.add(gap)
                        is_cleared = True
                        break
                    elif current_sum > gap:
                        p0_idx -= 1
                    else: break
            
                if not is_cleared:
                    remaining.append(item)
        
            active_gaps = remaining

    # print((active_gaps))
    # print(sorted([g["prime"] for g in active_gaps]))
    # print(sorted([g["gap"] for g in active_gaps]))
    return active_gaps
    

# Тест
pass3_gaps = process_primes_pipeline(100, False)
print(f"Останали празнини след pass 3: {len(pass3_gaps)}")

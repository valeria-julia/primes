# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
def check_total_net_balance(p_limit):
    # Бързо генериране на прости числа (Sieve of Eratosthenes)
    sieve = [True] * (p_limit + 1)
    for p in range(2, int(p_limit**0.5) + 1):
        if sieve[p]:
            for i in range(p * p, p_limit + 1, p):
                sieve[i] = False
    primes = [p for p in range(2, p_limit + 1) if sieve[p]]
    
    covered = set()
    active_gaps = set()
    total_created = 0
    total_closed = 0
    
    for i, p in enumerate(primes):
        if p < 3: continue
        
        # 1. Затваряне чрез 2*p (Директно покритие)
        double_p = 2 * p
        if double_p in active_gaps:
            active_gaps.remove(double_p)
            total_closed += 1
        covered.add(double_p)

        # 2. Покриване чрез суми (p + p_prev)
        for j in range(i - 1, -1, -1):
            s = p + primes[j]
            if s in covered or s in active_gaps:
                break
            if s % 2 == 0:
                covered.add(s)

        # 3. Опит за затваряне на останалите празнини (Балансирано търсене)
        cleared_this_step = set()
        for gap in active_gaps:
            p1_idx, p0_idx = i, i - 1
            while p0_idx >= 0 and p1_idx < len(primes):
                current_sum = primes[p1_idx] + primes[p0_idx]
                if current_sum == gap:
                    cleared_this_step.add(gap)
                    covered.add(gap)
                    total_closed += 1
                    break
                elif current_sum > gap:
                    p0_idx -= 1
                else:
                    break
        active_gaps -= cleared_this_step

        # 4. Регистриране на нови празнини
        if i > 0:
            prev_double = 2 * primes[i-1]
            for x in range(prev_double + 2, double_p, 2):
                if x not in covered and x not in active_gaps:
                    active_gaps.add(x)
                    total_created += 1
                    
    # Общият баланс е разликата между всички затворени и всички създадени празнини
    return total_closed - total_created

# 10 0 100 6 1000 16 10000 28 100000 50 1000000 81 10000000 135
# Бърза проверка за p=1000
net_result = check_total_net_balance(100)
print(f"Total Net Balance up to p=1000: {net_result}")

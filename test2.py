def transact_price(arr):
    tmp_min = float("inf")
    global_max = -float("inf")
    for p in arr:
        tmp_min = min(tmp_min, p)
        global_max = max(global_max, p - tmp_min)
    return global_max

def sum_to_target(arr, target):
    h = set()
    for n in arr:
        if target-n in h:
            return True
        h.add(n)
    return False

if __name__ == "__main__":
    test_arr1 = [150, 100]
    target=300

    print(sum_to_target(test_arr1, target))
    print(sum_to_target([150, 150], target))

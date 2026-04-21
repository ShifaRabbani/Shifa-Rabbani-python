def leader_val(arr):
    result = []
    r_max = arr[-1]

    for i in range(len(arr)-1 , -1 , -1):
        if arr[i] >= r_max:
            result.append(arr[i])
            r_max = arr[i]
    result.reverse()
    return result
result = [16,15,23,2]
print(leader_val(result))
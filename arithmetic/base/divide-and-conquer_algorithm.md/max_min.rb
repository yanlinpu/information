
def max_min(a, low, high, min, max)
    if low == high
        max = min = a[low]
        [min, max]
    elsif low+1 == high
        if a[low] > a[high]
            max, min = a[low], a[high]
        else
            max, min = a[high], a[low]
        end
        [min, max]
    else
        mid = (low + high) / 2
        min1, max1 = max_min(a, low, mid, min, max)
        min2, max2 = max_min(a, mid+1, high, min, max)
        min, max = min1, max2
        min = min2 if min1 > min2
        max = max1 if max1 > max2    
        [min, max]
    end
end
arr = [2,4,2,1,99999,2,32,34,23,4,123,-77,3,3]
min, max = max_min([2,4,2,1,99999,2,32,34,23,4,123,-77,3,3], 0, arr.size-1, arr.first, arr.first)
puts min
puts max



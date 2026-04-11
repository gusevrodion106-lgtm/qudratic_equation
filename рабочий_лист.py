def count_sum(index, a):
    summ = 0
    for i in range(index):
        summ += (a[index] - a[i])
    return summ

t = int(input())
for _ in range(t):
    n, x = [int(x) for x in input().split()]
    a = [int(x) for x in input().split()]
    a.sort()
    hui = count_sum(n - 1, a)
    otv = 0
    if x > hui:
        otv = a[-1]
        while hui < x:
            hui += n
            otv += 1
        if hui > x:
            otv -= 1
        print(otv)
        continue
    
    

        

    








     




        

    




        
    








    


                
                





    

    







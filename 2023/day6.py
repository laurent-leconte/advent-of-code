import math

time =[55, 99, 97, 93]
distance =[401, 1485, 2274, 1405]

def solve(t,d):
    delta = math.sqrt(t*t -4*d)
    tmin = math.ceil((t-delta)/2)
    tmax = math.floor((t+delta)/2)
    return (tmax - tmin + 1)

def part1():
    results = 1
    for t,d in zip(time, distance):
        results *= solve(t, d)
    print(results)

def part2():
    t = 55999793
    d = 401148522741405
    print(solve(t,d))

if __name__ == "__main__":
    part1()
    part2()


def aggregate():
    series = []
    def aggregater(func):
        def inner(a):
            series.append(a) # 'series' can be retrieved in inner
            return sum(series) / len(series)
        return inner
    return aggregater


@aggregate()
def mean(a):
    pass


array = [i for i in range(1, 6)]
for i in array:
    print(mean(i))

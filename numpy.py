from collections.abc import Sequence


class NumPy:
    def __init__(self, iterable=None):
        if not isinstance(iterable, Sequence):
            raise TypeError('Not a sequence or an iterable.')
        self._array = [[i for i in iterable]] if iterable else []
        self._row = 1
        self._col = len(self._array[0])

    def __repr__(self):
        return f'NumPy({self._build_array()})'

    @property
    def shape(self):
        return (self._row, self._col)

    @shape.setter
    def shape(self, args):
        row, col = args
        if row * col != self._row * self._col:
            raise ValueError(f'Invalid shape: ({row}, {col})')
        self._row, self._col = row, col

    def _build_array(self, transpose=False):
        row, col = self._row, self._col
        if not transpose:
            return [[r*col + c for c in range(col)] for r in range(row)]
        return [[c+r*col for r in range(row)] for c in range(col)]

    def transpose(self):
        return self._build_array(True)


if __name__ == '__main__':
    n = NumPy(range(8))
    print(n)
    n.shape = 2, 4
    print(n.shape)
    print(n)
    print(n.transpose())

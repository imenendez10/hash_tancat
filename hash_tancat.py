# Estats d'una posició de la taula (hash tancat). NO canvieu aquests valors.
LLIURE = "L"
OCUPAT = "O"
ESBORRAT = "B"


class MyHashMap:
    """Taula de hash tancada amb amb sondeig linial"""

    def __init__(self, cap=13):
        self._table = [[None, None, LLIURE]for i in range(cap)]   # m posicions, inicialment buides
        self._n = 0                  # nombre de claus desades

    def _hash_function(self, key):
        return key % len(self._table)          # h(x) = x % m

    def _find(self,key):
        inici = self._hash_function(key)
        tamaño = len(self._table)

        for i in range(tamaño):
            j = (inici+i)%tamaño
            posicion = self._table[j]

            if posicion[2]==LLIURE:
                return None

            if posicion[2]==OCUPAT and posicion[0]==key:
                return j
        return None
    
    

    def put(self, key: int, value: int) -> None:

        inicio = self._hash_function(key)
        tamaño = len(self._table)
        primera_disponible = None

        for i in range(tamaño):
            j = (inicio + i) % tamaño
            posicion = self._table[j]

            if posicion[2] == OCUPAT and posicion[0] == key:
                posicion[1] = value
                return

            if posicion[2] == ESBORRAT:
                if primera_disponible is None:
                    primera_disponible = j

            elif posicion[2] == LLIURE:
                if primera_disponible is None:
                    primera_disponible = j
                break

        if primera_disponible is not None:
            self._table[primera_disponible] = [key, value, OCUPAT]
            self._n += 1
        else:
            self._resize(2 * tamaño - 1)
            self.put(key, value)
            return

        if self._n > len(self._table) // 2:
            self._resize(2 * len(self._table) - 1)


    def get(self, key: int) -> int:
        j = self._find(key)

        if j is not None:
            return self._table[j][1]

        return -1

    def remove(self, key: int) -> None:
        j = self._find(key)

        if j is not None:
            self._table[j] = [None, None, ESBORRAT]
            self._n -= 1

    def _resize(self, c):
        tabla_antigua = self._table

        self._table = [[None, None, LLIURE] for i in range(c)]
        self._n = 0

        for posicion in tabla_antigua:
            if posicion[2] == OCUPAT:
                self.put(posicion[0], posicion[1])

    def __len__(self):
        return self._n
# Importare le funzioni e i metodi utili
import datetime
from dataclasses import dataclass

# Creare la classe Situazione
@dataclass
class Situazione:
    localita: str
    data: datetime.date
    umidita: int

    # Definire il metodo __eq__
    def __eq__(self, other):
        return self.localita == other.localita and self.data == other.data

    # Definire il metodo __hash__
    def __hash__(self):
        return hash((self.localita, self.data))
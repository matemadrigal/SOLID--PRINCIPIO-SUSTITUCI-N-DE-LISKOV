

from __future__ import annotations
from abc import ABC, abstractmethod


class Vehicle(ABC):

    def __init__(self, max_speed: float) -> None:
        if max_speed <= 0:
            raise ValueError("max_speed debe ser > 0")
        self._max_speed = float(max_speed)
        self._speed = 0.0

    @property
    def speed(self) -> float:
        return self._speed

    @property
    def max_speed(self) -> float:
        return self._max_speed

    @abstractmethod
    def accelerate(self, delta: float) -> None:
        """Incrementa la velocidad respetando el contrato."""

    @abstractmethod
    def brake(self, delta: float) -> None:
        """Reduce la velocidad respetando el contrato."""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(speed={self.speed:.1f}, max={self.max_speed:.1f})"


# ============ Subclases que CUMPLEN el contrato ============

class Car(Vehicle):
    def accelerate(self, delta: float) -> None:
        if delta <= 0:
            raise ValueError("delta de aceleración debe ser > 0")
        self._speed = min(self.max_speed, self.speed + delta)

    def brake(self, delta: float) -> None:
        if delta <= 0:
            raise ValueError("delta de frenado debe ser > 0")
        self._speed = min(self.max_speed, self.speed + delta)

    def brake(self, delta: float) -> None:
        if delta <= 0:
            raise ValueError("delta de frenado debe ser > 0")
        self._speed = max(0.0, self.speed - delta)


class Bicycle(Vehicle):

    PER_STEP_CAP = 5.0  # m/s por paso de aceleración

    def accelerate(self, delta: float) -> None:
        if delta <= 0:
            raise ValueError("delta de aceleración debe ser > 0")
        # Limita cuánto puede acelerar en un 'paso':
        effective = min(delta, self.PER_STEP_CAP)
        self._speed = min(self.max_speed, self.speed + effective)

    def brake(self, delta: float) -> None:
        if delta <= 0:
            raise ValueError("delta de frenado debe ser > 0")
        self._speed = max(0.0, self.speed - delta)


class ElectricScooter(Vehicle):
    RAMP_RATIO = 0.15  # como máximo acelera un 15% de su velocidad máxima por paso

    def accelerate(self, delta: float) -> None:
        if delta <= 0:
            raise ValueError("delta de aceleración debe ser > 0")
        cap = self.max_speed * self.RAMP_RATIO
        effective = min(delta, cap)
        self._speed = min(self.max_speed, self.speed + effective)

    def brake(self, delta: float) -> None:
        if delta <= 0:
            raise ValueError("delta de frenado debe ser > 0")
        self._speed = max(0.0, self.speed - delta)


# ============ Verificación del LSP ============

def lsp_check(vehicle: Vehicle) -> bool:
    # Estado inicial
    assert vehicle.speed >= 0
    assert vehicle.max_speed > 0
    assert vehicle.speed <= vehicle.max_speed

    # Acelerar dentro del límite
    s0 = vehicle.speed
    vehicle.accelerate(10)
    assert vehicle.speed >= s0
    assert 0 <= vehicle.speed <= vehicle.max_speed

    # Frenar parcialmente
    s1 = vehicle.speed
    vehicle.brake(3)
    assert vehicle.speed <= s1
    assert vehicle.speed >= 0

    # Frenazo extremo: nunca negativo
    vehicle.brake(10**6)
    assert vehicle.speed == 0

    # Acelerar por encima del máximo: queda clamp al tope
    vehicle.accelerate(vehicle.max_speed * 2)
    assert vehicle.speed <= vehicle.max_speed


    return True


def demo() -> None:
    """Pequeña demo y validación LSP."""
    fleet: list[Vehicle] = [
        Car(max_speed=200),
        Bicycle(max_speed=40),
        ElectricScooter(max_speed=25),
    ]

    print("Vehículos iniciales:")
    for v in fleet:
        print(" ", v)

    print("\nComprobando LSP en cada vehículo...")
    for v in fleet:
        ok = lsp_check(v)
        print(f"  {v.__class__.__name__}: LSP OK -> {ok}")

    print("\nEstado final tras pruebas:")
    for v in fleet:
        print(" ", v)


if __name__ == "__main__":
    demo()


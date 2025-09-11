from random import randint, random

class Cuadrilla:
    def __init__(self, dimensiones: int = 10, dificultad: int = 1) -> None:
        self.dimensiones = dimensiones
        self.grid = [['0' for _ in range(dimensiones)] for _ in range(dimensiones)]
        self.punto_objetivo()
        
        try: 
            self.crear_obstaculos_dinamicos(dificultad)
        except ValueError as e:
            print(e)
    def punto_objetivo(self) -> None:
        x = randint(0, self.dimensiones - 1)
        y = randint(0, self.dimensiones - 1)
        self.grid[y][x] = 'U'  # Representa el punto objetivo con 'U'
    
    def crear_obstaculos_dinamicos(self, dificultad: int = 1) -> None:

        if dificultad < 1 or dificultad > 3:
            raise ValueError("La dificultad debe estar entre 1 y 4.")
        
        valores = dificultad * (self.dimensiones**2) // 6
        
        for _ in range(valores):
            x = randint(0, self.dimensiones - 1)
            y = randint(0, self.dimensiones - 1)
            
            while self.grid[y][x] != '0':
                x = randint(0, self.dimensiones - 1)
                y = randint(0, self.dimensiones - 1)

            if self.grid[y][x] == '0':  # Solo coloca un obstáculo si la celda está vacía
                self.grid[y][x] = 'X'  # Representa un obstáculo con 'X'
    
    def cambiar_muros(self) -> None:
        for i in range(self.dimensiones):
            for j in range(self.dimensiones):
                if self.grid[i][j] == 'X' and random() < 0.3:  # 30% de probabilidad de cambiar
                    self.grid[i][j] = '0'  # Cambia a espacio vacío
                elif self.grid[i][j] == '0' and random() < 0.4:  # 10% de probabilidad de cambiar
                    self.grid[i][j] = 'X'  # Cambia a obstáculo
        

    def __str__(self) -> None:
        string = ""
        
        for fila in self.grid:
            string += "  ".join(str(celda) for celda in fila)
            string += "\n"
        
        return string


    
        
from aplicacion.dto.LibroDTO import LibroCrearDTO
from dominio.entidades.Libro import Libro
from dominio.puertos.IRepoLibro import IRepoLibro
from typing import List, Optional
import uuid

class GestionarLibros:
    def __init__(self, repositorio_libro: IRepoLibro):
        self.repositorio_libro = repositorio_libro

    def crear_libro(self, datos_libro: LibroCrearDTO) -> Libro:
        nuevo_libro = Libro(**datos_libro.model_dump())
        return self.repositorio_libro.guardar(nuevo_libro)

    def obtener_todos_los_libros(self) -> List[Libro]:
        return self.repositorio_libro.obtener_todos()
    
    def obtener_libro_por_id(self, libro_id: uuid.UUID) -> Optional[Libro]:
        return self.repositorio_libro.obtener_por_id(libro_id)
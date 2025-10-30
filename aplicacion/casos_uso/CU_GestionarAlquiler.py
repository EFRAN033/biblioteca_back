from aplicacion.dto.AlquilerDTO import AlquilerSolicitudDTO
from dominio.entidades.Alquiler import Alquiler
from dominio.puertos.IRepoAlquiler import IRepoAlquiler
from dominio.puertos.IRepoLibro import IRepoLibro # Necesitamos el repo de libros
from datetime import datetime, timedelta
import uuid

class GestionarAlquiler:
    def __init__(self, repo_alquiler: IRepoAlquiler, repo_libro: IRepoLibro):
        self.repo_alquiler = repo_alquiler
        self.repo_libro = repo_libro

    def solicitar_prestamo(self, datos_solicitud: AlquilerSolicitudDTO, usuario_id: uuid.UUID) -> Alquiler:
        
        libro = self.repo_libro.obtener_por_id(datos_solicitud.libro_id)
        if not libro:
            raise ValueError("El libro solicitado no existe.")

       
        if libro.ejemplares_disponibles <= 0:
            raise ValueError("No hay ejemplares disponibles de este libro.")


        libro.ejemplares_disponibles -= 1
        self.repo_libro.guardar(libro) 

       
        fecha_fin = datetime.utcnow() + timedelta(days=15) 
        nuevo_alquiler = Alquiler(
            libro_id=libro.id,
            usuario_id=usuario_id,
            fecha_fin=fecha_fin
        )
        return self.repo_alquiler.guardar(nuevo_alquiler)
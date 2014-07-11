__author__ = 'nickbortolotti'

import logging
import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

#Funcionalidad de Mensajes
class Mensaje(messages.Message):
    message = messages.StringField(1)

class ColeccionMensajes(messages.Message):
    items = messages.MessageField(Mensaje, 1, repeated=True)

almacen = ColeccionMensajes(items=[
    Mensaje(message='Hola'),
    Mensaje(message='Hola Mundo'),
    Mensaje(message='Hola Mundo LatAm'),
])

@endpoints.api(name='mensaje', version='v1')
class ManejarMensaje(remote.Service):
    id_mensaje = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.IntegerField(1, variant=messages.Variant.INT32))

    @endpoints.method(id_mensaje, Mensaje,
                      path='mensajes/{id}', http_method='GET',
                      name='mensajes.getMensaje')
    def mensaje_get(self, request):
        try:
            logging.info(almacen.items[request.id])
            return almacen.items[request.id]
        except (IndexError, TypeError):
            raise endpoints.NotFoundException('No existe el mensaje %s' % (request.id,))

application = endpoints.api_server([ManejarMensaje])
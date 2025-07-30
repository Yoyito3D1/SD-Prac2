# Documentación

## 1. Introducción

El sistema implementa un Shard Master, encargado de gestionar la asignación de claves a diferentes servidores en un sistema distribuido de almacenamiento de clave-valor. El objetivo del sistema es garantizar una distribución eficiente y equilibrada de las claves entre los servidores, al mismo tiempo que proporciona tolerancia a fallos y escalabilidad.

## 2. Arquitectura del Sistema

El sistema consta de dos componentes principales: ShardMasterService y ShardMasterServicer.

- **ShardMasterService**: Esta clase implementa la lógica del Shard Master. Gestiona la membresía de los servidores, la asignación de claves y la redistribución de claves. Utiliza un diccionario compartido (`node_dict`) para almacenar los rangos de claves asignados a cada servidor. Los métodos `join` y `leave` agregan y eliminan servidores respectivamente, recalculando la asignación de claves en cada caso. El método `query` devuelve el servidor responsable de una clave dada. El método `recalculate_shards` calcula los rangos de claves para cada servidor en función del número total de servidores. El método `redistribute_keys` redistribuye las claves cuando un servidor se une o abandona el sistema.

- **ShardMasterServicer**: Esta clase actúa como servidor gRPC para el Shard Master. Implementa los métodos gRPC definidos en el protocolo del Shard Master. Delega la lógica real al ShardMasterService.

## 3. Versión Definitiva y Cumplimiento de Objetivos

La versión definitiva del sistema proporciona una implementación funcional de un Shard Master con capacidad para agregar y eliminar servidores, consultar la asignación de claves y redistribuir claves cuando los servidores se unen o abandonan. El sistema tiene como objetivo lograr tanto escalabilidad vertical como horizontal.

- **Escalabilidad Vertical**: El sistema se puede escalar verticalmente mediante la adición de más recursos (por ejemplo, CPU, memoria) al servidor del Shard Master. A medida que aumenta el número de servidores o claves, el Shard Master puede manejar la carga adicional mediante una ampliación de recursos.

- **Escalabilidad Horizontal**: El sistema se puede escalar horizontalmente mediante la adición de más servidores KVStore. El Shard Master distribuye las claves entre múltiples servidores para equilibrar la carga. La adición de nuevos servidores desencadena la redistribución de claves, lo que garantiza una distribución equilibrada de las claves.

## 4. Respuestas a las Preguntas

1. **¿El sistema está diseñado para ser escalable verticalmente, horizontalmente o ambas? Justifica tu respuesta.**

El sistema está diseñado para ser escalable tanto vertical como horizontalmente. La escalabilidad vertical se logra al permitir que el servidor del Shard Master maneje una carga creciente mediante la adición de más recursos. Por otro lado, la escalabilidad horizontal se logra distribuyendo las claves entre múltiples servidores KVStore, lo que permite al sistema manejar un mayor número de claves y solicitudes de clientes. El Shard Master gestiona la asignación y redistribución de claves cuando se agregan o eliminan servidores, lo que garantiza un equilibrio eficiente de la carga.

---

*Nota: El resto de la documentación se omitió por no contener información adicional solicitada en las preguntas.*
# Sistema de inventario bajo arquitectura de micro-servicios

El diseño de grandes aplicaciones para empresas está evolucionando de arquitecturas [monolíticas](https://tallerbd.wikispaces.com/Arquitectura+Monol%C3%ADtica.)  a  arquitecturas  basadas  en  [microservicios](https://es.wikipedia.org/wiki/Arquitectura_de_microservicios).  Estas  son  particularmente adecuadas  para  ejecutarse  en  entornos [cloud](https://es.wikipedia.org/wiki/Computación_en_la_nube)  porque  cada  servicio  puede  ser desarrollado,  desplegado  y  gestionado  individualmente,  lo  que  permite  un  control mucho más detallado y un alto grado de **escalabilidad**.
 
Basado en un ejemplo concreto, en este proyecto se desarrollará un sistema para la gestión de inventario bajo arquitectura de microservicios, mostrando los desafíos de ésta en un entorno de intranet pero que puede ser facilmente acoplado a un entorno cloud.

El sistema de inventario estará conformado por 7 servicios, cada uno desarrollado bajo la filosofia [Rest](https://es.wikipedia.org/wiki/Transferencia_de_Estado_Representacional) y siguiendo las buenas practicas recomendadas [**AQUI**](https://elbauldelprogramador.com/buenas-practicas-para-el-diseno-de-una-api-restful-pragmatica/).

A continuación los servicios web que conforman al sistema de inventario:

## Ubicación [ver codigo](https://github.com/carloscercado/microservicios/tree/master/servicio-ubicacion)

Este servicio manejar toda la informacion referente al espacio fisico de la organizacion donde funcionará el sistema de inventario. Desde aqui se gestionaran los almacenes, los estantes, los cubiculos, las organizaciones entre otras cosas.

## Productos [ver codigo](https://github.com/carloscercado/microservicios/tree/master/servicio-productos)

Este servicio maneja toda la informacion referente a los productos con los que trabajan en la organizacion, sus detalles, las categorias, los tamaños y sus fechas de vencimientos respectivas.

## Usuarios [ver codigo](https://github.com/carloscercado/microservicios/tree/master/servicio-auth)

Este servicio gestiona la integridad y confidencialidad de la informacion que se maneja en el sistema, permite manejar los usuarios y sus datos, las cuentas de usuario y el control de acceso.

## Compras [ver codigo](#)

Este servicio maneja todo lo referente a los procesos de compra, el cual permite dar entrada de los productos a la organizacion. Este servicio gestiona los proveedores, las compras y sus respectivos detalles, permite dar reportes de gastos y varios indicadores en apoyo a la toma de decisiones.

## Salidas [ver codigo](#)

Este servicio maneja toda la informacion referente a las salidas del inventario. Gestiona los clientes, los pedidos y sus respectivos detalles, las donaciones, los prestamos y permite dar reportes e indicadores en apoyo a la toma de decisiones.

## Gerencia [ver codigo](#)

Este servicio permite consumir la informacion que se maneja en todo el sistema para efectos gerencias, informacion sobre el comportamiento de la organizacion con respecto al uso del dinero hacia el inventario. Informacion inteligente que apoye en gran medida a la toma de decisiones.

## Gateway [ver codigo](#)

 Este servicio tendra como finalidad servir de puerta de enlace entre todos los servicios web. Sera el [EndPoint](https://en.wikipedia.org/wiki/Endpoint_interface) comun para el Frontend. Conectara todas los servicios web y los ubicara con un enrrutador para permitir una rapida escalabilidad.

 Este servicio sera realizado basado en las especificaciones definidas [**AQUI**](http://microservices.io/patterns/apigateway.html)



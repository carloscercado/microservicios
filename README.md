# Sistema de inventario bajo arquitectura de micro-servicios

El diseño de grandes aplicaciones para empresas está evolucionando de arquitecturas [monolíticas](https://tallerbd.wikispaces.com/Arquitectura+Monol%C3%ADtica.)  a  arquitecturas  basadas  en  [microservicios](https://es.wikipedia.org/wiki/Arquitectura_de_microservicios).  Estas  son  particularmente adecuadas  para  ejecutarse  en  entornos [cloud](https://es.wikipedia.org/wiki/Computación_en_la_nube)  porque  cada  servicio  puede  ser desarrollado,  desplegado  y  gestionado  individualmente,  lo  que  permite  un  control mucho más detallado y un alto grado de **escalabilidad**.
 
Basado en un ejemplo concreto, en este proyecto se desarrollará un sistema para la gestión de inventario bajo la arquitectura de microservicios, mostrando los desafíos de ésta en un entorno de intranet pero que puede ser facilmente acoplado a entorno cloud.

El sistema de inventario estará conformado por 6 servicios, cada uno desarrollado bajo la filosofia [Rest](https://es.wikipedia.org/wiki/Transferencia_de_Estado_Representacional) y siguiendo las buenas practicas recomendadas [**AQUI**](https://elbauldelprogramador.com/buenas-practicas-para-el-diseno-de-una-api-restful-pragmatica/).

A continuación los servicios web que conforman al sistema de inventario:

## Ubicación [ir](https://github.com/carloscercado/microservicios/tree/master/ubicacion)

Este servicio tendra como objetivo manejar toda la informacion referente al espacio fisico de la organizacion donde funcionará el sistema de inventario. Desde aqui se gestionaran los almacenes, los estantes, los cubiculos, las organizaciones entre otras cosas.

## Productos [ir](https://github.com/carloscercado/microservicios/tree/master/productos)

Este servicio tendra como objetivo manejar toda la informacion referente al los productos con los que se trabajan en la organizacion, sus detalles, las categorias, los tamaños y sus fechas de vencimientos.
 



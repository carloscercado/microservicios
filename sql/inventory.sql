/*
*  ************************************************************
*/
--Referente a las zonas fisicas donde se ubican los productos
CREATE TABLE empresa (
    id int PRIMARY KEY,
    nombre text NOT NULL,
    direccion text NOT NULL,
    estado varchar(20) NOT NULL,
    ciudad varchar(20) NOT NULL,
    telefono varchar(20),
    correo text,
    rif varchar(30) NOT NULL
);


ALTER TABLE public.empresa OWNER TO ubicacion;


CREATE TABLE almacen (
    id int PRIMARY KEY,
    nombre varchar(30) NOT NULL,
    direccion text NOT NULL,
    telefono varchar(20),
    empresa int  NOT NULL references empresa(id)
);

ALTER TABLE public.almacen OWNER TO ubicacion;

CREATE TABLE estante (
    id int PRIMARY KEY,
    nombre varchar(20) NOT NULL,
    almacen int NOT NULL references almacen(id)
);


ALTER TABLE public.estante OWNER TO ubicacion;

CREATE TABLE cubiculo (
    id int PRIMARY KEY,
    nombre varchar(20) NOT NULL,
    estante int NOT NULL references estante(id)
);

ALTER TABLE public.cubiculo OWNER TO ubicacion;

/*
*  ************************************************************
*/
-- Referentes a los productos y su conformacion

CREATE TABLE categoria (
    id int PRIMARY KEY,
    categoria varchar(20) NOT NULL
);

ALTER TABLE public.categoria OWNER TO producto;

CREATE TABLE insumo (
    id int PRIMARY KEY,
    nombre varchar(60) NOT NULL,
    marca varchar(20) NOT NULL,
    minimo int DEFAULT 10 NOT NULL,
    maximo int DEFAULT 100 NOT NULL,
    perecedero boolean NOT NULL,
    categoria int NOT NULL references categoria(id),
    cantidad int DEFAULT 0 NOT NULL,
    codigo varchar(20) NOT NULL UNIQUE
);


ALTER TABLE public.insumo OWNER TO producto;


CREATE TABLE perece (
    id int PRIMARY KEY,
    insumo int NOT NULL references insumo(id),
    fecha date NOT NULL
);


ALTER TABLE public.perece OWNER TO producto;

/*
*  ************************************************************
*/
-- Referente a las cuentas de usuario

CREATE TABLE persona (
    id int PRIMARY KEY,
    nombre text NOT NULL,
    apellido text NOT NULL,
    cedula text NOT NULL,
    sexo varchar(20) NOT NULL,
    cargo text NOT NULL,
    telefono varchar(20)
);


ALTER TABLE public.persona OWNER TO usuarios;


CREATE TABLE cuenta (
    id int PRIMARY KEY,
    usuario text NOT NULL,
    clave text NOT NULL,
    rol text NOT NULL,
    pregunta text NOT NULL,
    respuesta text NOT NULL,
    ultima_coneccion timestamp without time zone,
    persona int NOT NULL references persona(id)
);

ALTER TABLE public.cuenta OWNER TO usuarios;


/*
*  ************************************************************
*/
-- Referente a las compras


CREATE TABLE proveedor (
    id int PRIMARY KEY,
    nombre text NOT NULL,
    direccion text NOT NULL,
    estado varchar(20) NOT NULL,
    ciudad varchar(20) NOT NULL,
    telefono varchar(20),
    correo text,
    rif varchar(30) NOT NULL UNIQUE
);


ALTER TABLE public.proveedor OWNER TO compras;

CREATE TABLE compra (
    id int PRIMARY KEY,
    fecha date DEFAULT (now())::date NOT NULL,
    estado boolean DEFAULT true NOT NULL,
    cuenta int NOT NULL references cuenta(id),
    orden varchar(20) NOT NULL,
    factura varchar(20) NOT NULL,
    proveedor int NOT NULL references proveedor(id)
);


ALTER TABLE public.compra OWNER TO compras;

CREATE TABLE detalle_compra (
    id int PRIMARY KEY,
    insumo int NOT NULL references insumo(id),
    cantidad int NOT NULL,
    estado boolean DEFAULT true,
    registrados int DEFAULT 0,
    precio numeric(10,2) NOT NULL,
    devuelto int DEFAULT 0,
    compra int NOT NULL references compra(id)
);


ALTER TABLE public.detalle_compra OWNER TO compras;

CREATE TABLE unidad (
    id int PRIMARY KEY,
    detalle int NOT NULL references detalle_compra(id),
    cubiculo int NOT NULL,
    estado boolean DEFAULT true,
    codigo varchar(20) DEFAULT 'SIN SERIAL'::varchar UNIQUE
);


ALTER TABLE public.unidad OWNER TO compras;


/*
*  ************************************************************
*/
-- Referente a las salidas


CREATE TABLE cliente (
    id int PRIMARY KEY,
    nombre varchar(20) NOT NULL,
    descripcion text DEFAULT 'NINGUNA'::text,
    telefono varchar(20),
    correo text
);

ALTER TABLE public.cliente OWNER TO salidas;


CREATE TABLE pedido (
    id int PRIMARY KEY,
    fecha date DEFAULT (now())::date,
    cliente int NOT NULL references cliente(id),
    cuenta int NOT NULL references cuenta(id),
    estado boolean DEFAULT true,
    recibido date
);


ALTER TABLE public.pedido OWNER TO salidas;

CREATE TABLE detalle_pedido (
    id int PRIMARY KEY,
    insumo int NOT NULL references unidad(id),
    cantidad int NOT NULL,
    estado boolean DEFAULT true,
    pedido int NOT NULL references pedido(id)
);


ALTER TABLE public.detalle_pedido OWNER TO salidas;


/*
*  ************************************************************
*/
-- Referente a los indiadores en apoyo a la toma de desiciones

CREATE TABLE indicador (
    id int PRIMARY KEY,
    nombre varchar(20) NOT NULL,
    eficiente int NOT NULL,
    critico int NOT NULL,
    eficiencia text NOT NULL,
    criticidad text NOT NULL,
    aceptable text NOT NULL,
    frecuencia int DEFAULT 30
);


ALTER TABLE public.indicador OWNER TO gerencia;

CREATE TABLE comportamiento (
    id int PRIMARY KEY,
    indicador int NOT NULL references indicador(id),
    valor int NOT NULL,
    observacion text NOT NULL,
    fecha date DEFAULT (now())::date
);


ALTER TABLE public.comportamiento OWNER TO gerencia;

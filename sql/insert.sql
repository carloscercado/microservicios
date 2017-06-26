insert into empresa (id, nombre,direccion,estado,ciudad,telefono,correo,rif) 
values(1,'UPTOS','CARRETERA CUMANA-CUMANACOA','SUCRE','CUMANA','(293)416-4458',NULL,'J45637289');

insert into almacen (id, nombre, direccion, telefono, empresa)
values (1, 'ALMACEN 1', 'ZONA 4, PERIMETRAL CRUCE CON CALLE ADJUNTA', '(293)454-6567',1),
(2, 'ALMACEN 2', 'ZONA 4, PERIMETRAL CRUCE CON CALLE ADJUNTA', '(293)454-6567',1),
(3, 'ALMACEN 2', 'ZONA 4, PERIMETRAL CRUCE CON CALLE ADJUNTA', '(293)454-6567',1);

insert into estante (id, nombre, almacen)
values(1,'ESTANTE 1-1',1),
(2,'ESTANTE 1-2',1),
(3,'ESTANTE 1-3',1),
(4,'ESTANTE 2-1',2),
(5,'ESTANTE 2-2',2),
(6,'ESTANTE 2-3',2),
(7,'ESTANTE 3-1',3),
(8,'ESTANTE 3-2',3),
(9,'ESTANTE 3-3',3);

insert into cubiculo (id, nombre, estante)
values (1, 'CUBICULO 1-1',1),
 (2, 'CUBICULO 1-2',1),
 (3, 'CUBICULO 1-3',1),
 (4, 'CUBICULO 2-1',2),
 (5, 'CUBICULO 2-2',2),
 (6, 'CUBICULO 2-3',2),
 (7, 'CUBICULO 3-1',3),
 (8, 'CUBICULO 3-2',3),
 (9, 'CUBICULO 3-3',3);

 insert into categoria (id, categoria) values (1,'MEDICINA'),
 (2,'LIMPIEZA'),(3,'OFICINA'),(4,'ELECTRONICOS');

 insert into insumo (id,nombre, marca, perecedero, categoria, codigo)
 values (1,'MAUSE','GENIUS',FALSE, 4,'040040010'),
 (2,'TECLADO','GENIUS',FALSE, 4,'040040012'),
 (3,'MONITOR','GENIUS',FALSE, 4,'040040013'),
  (4,'SPRAY LIMPIATODO','HOME',TRUE,2,'140040012'),
 (5,'CLORO','ACNE',TRUE, 2,'140040013'),
  (6,'SUAVISANTE','SUAVITEL',TRUE, 2,'140040014');

  insert into perece (id,insumo, fecha)
  values (1,4,now()),
  (2,5, now()),
  (3,6, now());
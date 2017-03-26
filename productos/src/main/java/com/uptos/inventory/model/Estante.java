package com.uptos.inventory.model;



import java.util.HashSet;
import java.util.Set;

/**
 * Estante generated by hbm2java
 */
public class Estante  implements java.io.Serializable {


     private int id;
     private Almacen almacen;
     private String nombre;
     private Set cubiculos = new HashSet(0);

    public Estante() {
    }

	
    public Estante(int id, Almacen almacen, String nombre) {
        this.id = id;
        this.almacen = almacen;
        this.nombre = nombre;
    }
    public Estante(int id, Almacen almacen, String nombre, Set cubiculos) {
       this.id = id;
       this.almacen = almacen;
       this.nombre = nombre;
       this.cubiculos = cubiculos;
    }
   
    public int getId() {
        return this.id;
    }
    
    public void setId(int id) {
        this.id = id;
    }
    public Almacen getAlmacen() {
        return this.almacen;
    }
    
    public void setAlmacen(Almacen almacen) {
        this.almacen = almacen;
    }
    public String getNombre() {
        return this.nombre;
    }
    
    public void setNombre(String nombre) {
        this.nombre = nombre;
    }
    public Set getCubiculos() {
        return this.cubiculos;
    }
    
    public void setCubiculos(Set cubiculos) {
        this.cubiculos = cubiculos;
    }




}



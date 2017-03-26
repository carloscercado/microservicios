package com.uptos.inventory.model;



import java.util.HashSet;
import java.util.Set;

/**
 * Cliente generated by hbm2java
 */
public class Cliente  implements java.io.Serializable {


     private int id;
     private String nombre;
     private String descripcion;
     private String telefono;
     private String correo;
     private Set pedidos = new HashSet(0);

    public Cliente() {
    }

	
    public Cliente(int id, String nombre) {
        this.id = id;
        this.nombre = nombre;
    }
    public Cliente(int id, String nombre, String descripcion, String telefono, String correo, Set pedidos) {
       this.id = id;
       this.nombre = nombre;
       this.descripcion = descripcion;
       this.telefono = telefono;
       this.correo = correo;
       this.pedidos = pedidos;
    }
   
    public int getId() {
        return this.id;
    }
    
    public void setId(int id) {
        this.id = id;
    }
    public String getNombre() {
        return this.nombre;
    }
    
    public void setNombre(String nombre) {
        this.nombre = nombre;
    }
    public String getDescripcion() {
        return this.descripcion;
    }
    
    public void setDescripcion(String descripcion) {
        this.descripcion = descripcion;
    }
    public String getTelefono() {
        return this.telefono;
    }
    
    public void setTelefono(String telefono) {
        this.telefono = telefono;
    }
    public String getCorreo() {
        return this.correo;
    }
    
    public void setCorreo(String correo) {
        this.correo = correo;
    }
    public Set getPedidos() {
        return this.pedidos;
    }
    
    public void setPedidos(Set pedidos) {
        this.pedidos = pedidos;
    }




}



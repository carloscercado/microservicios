package com.uptos.inventory.model;




/**
 * DetallePedido generated by hbm2java
 */
public class DetallePedido  implements java.io.Serializable {


     private int id;
     private Pedido pedido;
     private Unidad unidad;
     private int cantidad;
     private Boolean estado;

    public DetallePedido() {
    }

	
    public DetallePedido(int id, Pedido pedido, Unidad unidad, int cantidad) {
        this.id = id;
        this.pedido = pedido;
        this.unidad = unidad;
        this.cantidad = cantidad;
    }
    public DetallePedido(int id, Pedido pedido, Unidad unidad, int cantidad, Boolean estado) {
       this.id = id;
       this.pedido = pedido;
       this.unidad = unidad;
       this.cantidad = cantidad;
       this.estado = estado;
    }
   
    public int getId() {
        return this.id;
    }
    
    public void setId(int id) {
        this.id = id;
    }
    public Pedido getPedido() {
        return this.pedido;
    }
    
    public void setPedido(Pedido pedido) {
        this.pedido = pedido;
    }
    public Unidad getUnidad() {
        return this.unidad;
    }
    
    public void setUnidad(Unidad unidad) {
        this.unidad = unidad;
    }
    public int getCantidad() {
        return this.cantidad;
    }
    
    public void setCantidad(int cantidad) {
        this.cantidad = cantidad;
    }
    public Boolean getEstado() {
        return this.estado;
    }
    
    public void setEstado(Boolean estado) {
        this.estado = estado;
    }




}



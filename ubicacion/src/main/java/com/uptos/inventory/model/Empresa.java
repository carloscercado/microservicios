package com.uptos.inventory.model;


import java.util.HashSet;
import java.util.Set;
import javax.json.Json;
import javax.json.JsonObject;
import javax.json.JsonObjectBuilder;

/**
 *
 * @author Carlos Cercado
 * @email cercadocarlos@gmail.com
 */
public class Empresa  implements java.io.Serializable {


     private Integer id;
     private String nombre;
     private String direccion;
     private String estado;
     private String ciudad;
     private String telefono;
     private String correo;
     private String rif;

    public Empresa() {
    }

    public Empresa(Integer id)
    {
        this.id = id;
    }

    
	
    public Empresa(Integer id, String nombre, String direccion, String estado, String ciudad, String rif) {
        this.id = id;
        this.nombre = nombre;
        this.direccion = direccion;
        this.estado = estado;
        this.ciudad = ciudad;
        this.rif = rif;
    }

   
    public Integer getId() {
        return this.id;
    }
    
    public void setId(Integer id) {
        this.id = id;
    }
    public String getNombre() {
        return this.nombre;
    }
    
    public void setNombre(String nombre) {
        this.nombre = nombre;
    }
    public String getDireccion() {
        return this.direccion;
    }
    
    public void setDireccion(String direccion) {
        this.direccion = direccion;
    }
    public String getEstado() {
        return this.estado;
    }
    
    public void setEstado(String estado) {
        this.estado = estado;
    }
    public String getCiudad() {
        return this.ciudad;
    }
    
    public void setCiudad(String ciudad) {
        this.ciudad = ciudad;
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
    public String getRif() {
        return this.rif;
    }
    
    public void setRif(String rif) {
        this.rif = rif;
    }


    public void toUpper()
    {
        this.nombre = this.nombre.toUpperCase();
        this.ciudad = this.ciudad.toUpperCase();
        this.correo = this.correo.toUpperCase();
        this.direccion = this.direccion.toUpperCase();
        this.estado = this.estado.toUpperCase();
    }

    public JsonObject validate()
    {
        JsonObjectBuilder res = Json.createObjectBuilder();

        if (this.direccion == null)
        {
            res.add("direccion", "no puede ser null");
        }

        if (this.nombre == null)
        {
            res.add("nombre", "no puede ser null");
        }
        
        if (this.ciudad == null)
        {
            res.add("ciudad", "no puede ser null");
        }
        
        if (this.correo == null)
        {
            res.add("correo", "no puede ser null");
        }
        
        if (this.estado == null)
        {
            res.add("estado", "no puede ser null");
        }

       

        JsonObject values = res.build();
        return (values.size() == 0) ? null : values;

    }


}



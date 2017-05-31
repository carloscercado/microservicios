package com.uptos.inventory.model;

import com.uptos.inventory.dao.EstanteDAO;
import javax.json.Json;
import javax.json.JsonObject;
import javax.json.JsonObjectBuilder;

/**
 *
 * @author Carlos Cercado
 * @email cercadocarlos@gmail.com
 */
public class Cubiculo  implements java.io.Serializable {


     private int id;
     private Estante estante;
     private String nombre;

    public Cubiculo() {
    }

    public Cubiculo(int id, Estante estante, String nombre) {
       this.id = id;
       this.estante = estante;
       this.nombre = nombre;
    }
   
    public int getId() {
        return this.id;
    }
    
    public void setId(int id) {
        this.id = id;
    }
    public Estante getEstante() {
        return this.estante;
    }
    
    public void setEstante(Estante estante) {
        this.estante = estante;
    }
    public String getNombre() {
        return this.nombre;
    }
    
    public void setNombre(String nombre) {
        this.nombre = nombre;
    }
    
    public void toUpper()
    {
        this.nombre = this.nombre.toUpperCase();
    }

    public JsonObject validate()
    {
        JsonObjectBuilder res = Json.createObjectBuilder();

        if (this.nombre == null)
        {
            res.add("nombre", "no puede ser null");
        }

        
        if (this.estante.getId() == null)
        {
            res.add("estante", "no puede ser null");
        } else
        {
            EstanteDAO db = new EstanteDAO();
            Estante emp = db.get("from Estante em where em.id=" + this.estante.getId());
            if (emp == null)
            {
                res.add("estante", "no existe");
            } else
            {
                this.estante = emp;
            }
        }

        JsonObject values = res.build();
        return (values.size() == 0) ? null : values;

    }




}



package com.uptos.inventory.model;

import com.uptos.inventory.dao.AlmacenDAO;
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
public class Estante implements java.io.Serializable
{

    private Integer id;
    private Almacen almacen;
    private String nombre;

    public Estante()
    {
    }

    public Estante(Integer id)
    {
        this.id = id;
    }

    
    public Estante(Integer id, Almacen almacen, String nombre)
    {
        this.id = id;
        this.almacen = almacen;
        this.nombre = nombre;
    }

    public Estante(Almacen almacen, String nombre)
    {
        this.almacen = almacen;
        this.nombre = nombre;
    }

    public Integer getId()
    {
        return this.id;
    }

    public void setId(Integer id)
    {
        this.id = id;
    }

    public Almacen getAlmacen()
    {
        return this.almacen;
    }

    public void setAlmacen(Almacen almacen)
    {
        this.almacen = almacen;
    }

    public String getNombre()
    {
        return this.nombre;
    }

    public void setNombre(String nombre)
    {
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

        if (this.almacen.getId() == null)
        {
            res.add("almacen", "no puede ser null");
        } else
        {
            AlmacenDAO db = new AlmacenDAO();
            Almacen emp = db.get("from Almacen em where em.id=" + this.almacen.getId());
            if (emp == null)
            {
                res.add("almacen", "no existe");
            } else
            {
                this.almacen = emp;
            }
        }

        JsonObject values = res.build();
        return (values.size() == 0) ? null : values;

    }

}

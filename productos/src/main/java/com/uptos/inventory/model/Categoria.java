package com.uptos.inventory.model;

import java.util.Date;
import javax.json.Json;
import javax.json.JsonObject;
import javax.json.JsonObjectBuilder;

public class Categoria implements java.io.Serializable
{

    private int id;
    private String categoria;

    public Categoria()
    {
    }

    public Categoria(int id, String categoria)
    {
        this.id = id;
        this.categoria = categoria;
    }

    public int getId()
    {
        return this.id;
    }

    public void setId(int id)
    {
        this.id = id;
    }

    public String getCategoria()
    {
        return this.categoria;
    }

    public void setCategoria(String categoria)
    {
        this.categoria = categoria;
    }

    public void toUpper()
    {
        this.categoria = this.categoria.toUpperCase();
    }
    
    public JsonObject validate()
    {
        JsonObjectBuilder res = Json.createObjectBuilder();
      
        if (this.categoria == null)
        {
            res.add("categoria", "no puede ser null");
        } 

        JsonObject values = res.build();
        return (values.size() == 0) ? null : values;

    }
}

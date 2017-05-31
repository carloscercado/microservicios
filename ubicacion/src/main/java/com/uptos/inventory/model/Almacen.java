package com.uptos.inventory.model;

import com.uptos.inventory.dao.EmpresaDAO;
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
public class Almacen implements java.io.Serializable
{

    private Integer id;
    private Empresa empresa;
    private String nombre;
    private String direccion;
    private String telefono;

    public Almacen()
    {
    }

    public Almacen(Integer id)
    {
        this.id = id;
    }
    
    

    public Almacen(Integer id, Empresa empresa, String nombre, String direccion)
    {
        this.id = id;
        this.empresa = empresa;
        this.nombre = nombre;
        this.direccion = direccion;
    }

    public Almacen(Empresa empresa, String nombre, String direccion, String telefono)
    {
        this.empresa = empresa;
        this.nombre = nombre;
        this.direccion = direccion;
        this.telefono = telefono;
    }

    public Integer getId()
    {
        return this.id;
    }

    public void setId(Integer id)
    {
        this.id = id;
    }

    public Empresa getEmpresa()
    {
        return this.empresa;
    }

    public void setEmpresa(Empresa empresa)
    {
        this.empresa = empresa;
    }

    public String getNombre()
    {
        return this.nombre;
    }

    public void setNombre(String nombre)
    {
        this.nombre = nombre;
    }

    public String getDireccion()
    {
        return this.direccion;
    }

    public void setDireccion(String direccion)
    {
        this.direccion = direccion;
    }

    public String getTelefono()
    {
        return this.telefono;
    }

    public void setTelefono(String telefono)
    {
        this.telefono = telefono;
    }

    public void toUpper()
    {
        this.nombre = this.nombre.toUpperCase();
        this.direccion = this.direccion.toUpperCase();
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
        if (this.empresa.getId() == null)
        {
            res.add("empresa", "no puede ser null");
        } else
        {
            EmpresaDAO db = new EmpresaDAO();
            Empresa emp = db.get("from Empresa em where em.id=" + this.empresa.getId());
            if(emp == null)
            {
                res.add("empresa", "no existe");
            }else
            {
                this.empresa = emp;
            }
        }

        JsonObject values = res.build();
        return (values.size() == 0) ? null : values;

    }

}

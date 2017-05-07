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

    private int id;
    private Empresa empresa;
    private String nombre;
    private String direccion;
    private String telefono;
    private Set estantes = new HashSet(0);

    public Almacen()
    {
    }

    public Almacen(int id, Empresa empresa, String nombre, String direccion)
    {
        this.id = id;
        this.empresa = empresa;
        this.nombre = nombre;
        this.direccion = direccion;
    }

    public Almacen(int id, Empresa empresa, String nombre, String direccion, String telefono, Set estantes)
    {
        this.id = id;
        this.empresa = empresa;
        this.nombre = nombre;
        this.direccion = direccion;
        this.telefono = telefono;
        this.estantes = estantes;
    }

    public int getId()
    {
        return this.id;
    }

    public void setId(int id)
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

    public Set getEstantes()
    {
        return this.estantes;
    }

    public void setEstantes(Set estantes)
    {
        this.estantes = estantes;
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

        EmpresaDAO db = new EmpresaDAO();
        this.empresa = db.get("from Empresa em where em.id=" + this.empresa.getId());
        if (this.empresa == null)
        {
            res.add("empresa", "no existe");
        }

        JsonObject values = res.build();
        return (values.size() == 0) ? null : values;

    }

}

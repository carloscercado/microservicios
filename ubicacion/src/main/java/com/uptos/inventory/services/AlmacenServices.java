package com.uptos.inventory.services;

import com.google.gson.Gson;
import javax.json.Json;
import javax.json.JsonObject;
import javax.ws.rs.Consumes;
import javax.ws.rs.FormParam;
import javax.ws.rs.GET;
import com.uptos.inventory.config.Error;
import com.uptos.inventory.dao.AlmacenDAO;
import com.uptos.inventory.model.Almacen;
import com.uptos.inventory.model.Empresa;
import java.util.List;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

/**
 *
 * @author Carlos Cercado
 * @email cercadocarlos@gmail.com
 */
@Path("almacenes")
public class AlmacenServices
{

    @GET
    @Produces(MediaType.APPLICATION_JSON)
    public Response get()
    {
        AlmacenDAO db = new AlmacenDAO();
        List<Almacen> lista = db.read("from Almacen al join fetch al.empresa");
        if (lista.size() > 0)
        {
            Gson gson = new Gson();
            String salida = gson.toJson(lista);
            return Response.ok(salida).build();
        }
        return Response.status(Response.Status.NO_CONTENT).build();
    }

    @GET
    @Path("/empresa/{empresa}")
    @Produces(MediaType.APPLICATION_JSON)
    public Response getByCompany(@PathParam("empresa") int id)
    {
        AlmacenDAO db = new AlmacenDAO();
        List<Almacen> lista = db.read("from Almacen al join fetch al.empresa em where em.id="+id);
        if (lista.size() > 0)
        {
            Gson gson = new Gson();
            String salida = gson.toJson(lista);
            return Response.ok(salida).build();
        }
        return Response.status(Response.Status.NO_CONTENT).build();
    }

    @GET
    @Path("/{id}")
    @Produces(MediaType.APPLICATION_JSON)
    public Response get(@PathParam("id") int id)
    {
        AlmacenDAO db = new AlmacenDAO();
        Almacen obj = db.get("from Almacen idi join fetch idi.empresa where idi.id=" + id);
        if (obj != null)
        {
            return Response.ok(obj).build();
        }
        return Response.status(Response.Status.NO_CONTENT).build();
    }

    @POST
    @Produces(MediaType.APPLICATION_JSON)
    @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
    public Response post(@FormParam("nombre") String nombre,
            @FormParam("direccion") String direccion,
            @FormParam("telefono") String telefono,
            @FormParam("empresa") Integer empresa)
    {
        Empresa emp = new Empresa(empresa);
        Almacen obj = new Almacen(emp, nombre, direccion, telefono);
        if (obj.validate() == null)
        {
            AlmacenDAO db = new AlmacenDAO();
            obj.toUpper();
            Almacen res = db.create(obj);
            if (res != null)
            {
                return Response.status(Response.Status.CREATED).entity(res).build();
            } else
            {
                JsonObject json = Json.createObjectBuilder()
                        .add("error", Error.getDataBase(Error.NO_SAVE))
                        .add("developerMessage", "problemas con la persistencia")
                        .add("userMessage", "problemas al registrar").build();
                return Response.status(Response.Status.INTERNAL_SERVER_ERROR).entity(json).build();
            }
        } else
        {
            JsonObject json = Json.createObjectBuilder()
                    .add("error", Error.getBadData(Error.BAD_OTHER_DATA))
                    .add("developerMessage", "algunos datos son incorrectos")
                    .add("details", obj.validate())
                    .add("userMessage", "Problemas al registrar").build();
            return Response.status(Response.Status.BAD_REQUEST).entity(json).build();
        }
    }

}

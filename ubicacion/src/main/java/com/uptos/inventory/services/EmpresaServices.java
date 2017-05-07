package com.uptos.inventory.services;

import com.google.gson.Gson;
import javax.json.Json;
import javax.json.JsonObject;
import javax.ws.rs.Consumes;
import javax.ws.rs.FormParam;
import javax.ws.rs.GET;
import com.uptos.inventory.config.Error;
import com.uptos.inventory.dao.EmpresaDAO;
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
@Path("empresas")
public class EmpresaServices
{

    @GET
    @Produces(MediaType.APPLICATION_JSON)
    public Response get()
    {
        EmpresaDAO db = new EmpresaDAO();
        List<Empresa> lista = db.read("from Empresa");
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
        EmpresaDAO db = new EmpresaDAO();
        Empresa obj = db.get("from Empresa idi where idi.id=" + id);
        if (obj != null)
        {
            return Response.ok(obj).build();
        }
        return Response.status(Response.Status.NO_CONTENT).build();
    }

    @POST
    @Produces(MediaType.APPLICATION_JSON)
    @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
    public Response post(@FormParam("name") String nombre)
    {
        Empresa obj = new Empresa();
        obj.setNombre(nombre);
        if (obj.validate() == null)
        {
            EmpresaDAO db = new EmpresaDAO();
            obj.toUpper();
            Empresa res = db.create(obj);
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

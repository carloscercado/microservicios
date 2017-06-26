package com.uptos.inventory.services;

import com.google.gson.Gson;
import com.uptos.inventory.dao.CategoriaDAO;
import com.uptos.inventory.model.Categoria;
import java.util.List;
import javax.json.Json;
import javax.json.JsonObject;
import javax.ws.rs.*;
import javax.ws.rs.core.*;
import javax.ws.rs.core.MediaType;
import com.uptos.inventory.config.Error;
/**
 *
 * @author Carlos Cercado
 * @email cercadocarlos@gmail.com
 */
@Path("categorias")
public class CategoriaServices 
{
    @GET
    @Produces(MediaType.APPLICATION_JSON)
    public Response get()
    {
        CategoriaDAO db = new CategoriaDAO();
        List<Categoria> lista = db.read("from Categoria");
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
    public Response getByID(@PathParam ("id") Integer id)
    {
        CategoriaDAO db = new CategoriaDAO();
        Categoria lista = db.get("from Categoria cat where cat.id="+id);
        if (lista != null)
        {
            Gson gson = new Gson();
            String salida = gson.toJson(lista);
            return Response.ok(salida).build();
        }
        return Response.status(Response.Status.NO_CONTENT).build();
    }
    
    @POST
    @Produces(MediaType.APPLICATION_JSON)
    public Response post(@FormParam("categoria") String categoria)
    {
        Categoria obj = new Categoria(0, categoria);
        if (obj.validate() == null)
        {
            obj.toUpper();
            CategoriaDAO dao = new CategoriaDAO();
            Categoria res =  dao.create(obj);
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
                    .add("error", Error.getBadData(Error.BAD_DATA))
                    .add("developerMessage", "algunos datos son incorrectos")
                    .add("details", obj.validate())
                    .add("userMessage", "Problemas al registrar").build();
            return Response.status(Response.Status.BAD_REQUEST).entity(json).build();
        }
    }


}

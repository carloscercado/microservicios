package com.uptos.inventory.services;

import com.google.gson.Gson;
import com.uptos.inventory.dao.CategoriaDAO;
import com.uptos.inventory.dao.InsumoDAO;
import com.uptos.inventory.model.Categoria;
import com.uptos.inventory.model.Insumo;
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
@Path("insumos")
public class InsumoServices
{

    @GET
    @Produces(MediaType.APPLICATION_JSON)
    public Response get()
    {
        InsumoDAO db = new InsumoDAO();
        List<Insumo> lista = db.read("from Insumo ins join fetch ins.categoria");
        if (lista.size() > 0)
        {
            Gson gson = new Gson();
            String salida = gson.toJson(lista);
            return Response.ok(salida).build();
        }
        return Response.status(Response.Status.NO_CONTENT).build();
    }

    @GET
    @Path("/categoria/{id}")
    @Produces(MediaType.APPLICATION_JSON)
    public Response getByCategoria(@PathParam("id") Integer categoria)
    {
        InsumoDAO db = new InsumoDAO();
        List<Insumo> lista = db.read("from Insumo ins join fetch ins.categoria cat where cat.id=" + categoria);
        if (lista.size() > 0)
        {
            Gson gson = new Gson();
            lista.stream().forEach(x -> x.setCategoria(null));
            String salida = gson.toJson(lista);
            return Response.ok(salida).build();
        }
        return Response.status(Response.Status.NO_CONTENT).build();
    }

    @GET
    @Path("/{id}")
    @Produces(MediaType.APPLICATION_JSON)
    public Response getByID(@PathParam("id") Integer id)
    {
        InsumoDAO db = new InsumoDAO();
        Insumo lista = db.get("from Insumo ins join fetch ins.categoria cat where ins.id=" + id);
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
    public Response post(@FormParam("nombre") String nombre, @FormParam("marca") String marca,
            @FormParam("perecedero") String perece, @FormParam("codigo") String codigo,
            @FormParam("categoria") int categoria, @FormParam("fecha") String fecha)
    {
        CategoriaDAO dbcate = new CategoriaDAO();
        Categoria cate = dbcate.get("from Categoria cate where cate.id=" + categoria);
        boolean perecedero = (perece.equals("true")) ? true : false;
        Insumo obj = new Insumo(cate, nombre, marca, perecedero, codigo, fecha);
        if (obj.validate() == null)
        {
            obj.toUpper();
            InsumoDAO dao = new InsumoDAO();
            Insumo res = (obj.isPerecedero()) ? dao.create(obj, obj.getVencimiento()) : dao.create(obj);
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

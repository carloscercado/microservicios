package com.uptos.inventory.services;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import javax.json.Json;
import javax.json.JsonObject;
import javax.ws.rs.Consumes;
import javax.ws.rs.FormParam;
import javax.ws.rs.GET;
import com.uptos.inventory.config.Error;
import com.uptos.inventory.dao.CubiculoDAO;
import com.uptos.inventory.model.Cubiculo;
import java.lang.reflect.Type;
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
@Path("cubiculos")
public class CubiculoServices
{

    @GET
    @Produces(MediaType.APPLICATION_JSON)
    public Response get()
    {
        CubiculoDAO db = new CubiculoDAO();
        List<Cubiculo> lista = db.read("from Cubiculo cu join fetch cu.estante es "
                + "join fetch es.almacen");
        if (lista.size() > 0)
        {
            Type fooType = new TypeToken<List<Cubiculo>>()
            {
            }.getType();

            Gson gson = new Gson();
            lista.stream().forEach(x ->
            {
                x.getEstante().getAlmacen().setEmpresa(null);
            });
            String salida = gson.toJson(lista, fooType);
            return Response.ok(salida).build();
        }
        return Response.status(Response.Status.NO_CONTENT).build();
    }

    @GET
    @Path("/estante/{estante}")
    @Produces(MediaType.APPLICATION_JSON)
    public Response getByCompany(@PathParam("estante") int id)
    {
        CubiculoDAO db = new CubiculoDAO();
        List<Cubiculo> lista = db.read("from Cubiculo cu join fetch cu.estante es "
                + "join fetch es.almacen where es.id=" + id);
        if (lista.size() > 0)
        {
            Type fooType = new TypeToken<List<Cubiculo>>()
            {
            }.getType();

            Gson gson = new Gson();
            lista.stream().forEach(x ->
            {
                x.getEstante().getAlmacen().setEmpresa(null);
            });
            String salida = gson.toJson(lista, fooType);
            return Response.ok(salida).build();
        }
        return Response.status(Response.Status.NO_CONTENT).build();
    }

    @GET
    @Path("/{id}")
    @Produces(MediaType.APPLICATION_JSON)
    public Response get(@PathParam("id") int id)
    {
        CubiculoDAO db = new CubiculoDAO();
        Cubiculo obj = db.get("from Cubiculo cu join fetch cu.estante es "
                + "join fetch es.almacen where cu.id=" + id);
        if (obj != null)
        {
            Type fooType = new TypeToken<List<Cubiculo>>()
            {
            }.getType();
            Gson gson = new Gson();
            obj.getEstante().getAlmacen().setEmpresa(null);

            String salida = gson.toJson(obj, fooType);
            return Response.ok(salida).build();
        }
        return Response.status(Response.Status.NO_CONTENT).build();
    }

    @POST
    @Produces(MediaType.APPLICATION_JSON)
    @Consumes(MediaType.APPLICATION_FORM_URLENCODED)
    public Response post(@FormParam("name") String nombre)
    {
        Cubiculo obj = new Cubiculo();
        obj.setNombre(nombre);
        if (obj.validate() == null)
        {
            CubiculoDAO db = new CubiculoDAO();
            obj.toUpper();
            Cubiculo res = db.create(obj);
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

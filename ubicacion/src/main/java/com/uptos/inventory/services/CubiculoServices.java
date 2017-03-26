package com.uptos.inventory.services;

import com.uptos.inventory.dao.CubiculoDAO;
import com.uptos.inventory.model.Cubiculo;
import java.util.List;
import javax.ws.rs.*;
import javax.ws.rs.core.*;
import javax.ws.rs.core.MediaType;

/**
 *
 * @author Carlos Cercado
 * @email cercadocarlos@gmail.com
 */
@Path("cubiculos")
public class CubiculoServices 
{
    @GET
    @Path("/")
    @Produces(MediaType.APPLICATION_JSON)
    public Response get()
    {
        GenericEntity<List<Cubiculo>> lista = new GenericEntity<List<Cubiculo>>(CubiculoDAO.getAll())
        {
        };
        if (((List) lista.getEntity()).size() > 0)
        {
            return Response.ok(lista).build();
        }
        return Response.status(Response.Status.NO_CONTENT).build();
    }

}

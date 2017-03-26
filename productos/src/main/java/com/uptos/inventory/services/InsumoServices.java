package com.uptos.inventory.services;

import com.uptos.inventory.dao.InsumoDAO;
import com.uptos.inventory.model.Insumo;
import java.util.List;
import javax.ws.rs.*;
import javax.ws.rs.core.*;
import javax.ws.rs.core.MediaType;

/**
 *
 * @author Carlos Cercado
 * @email cercadocarlos@gmail.com
 */
@Path("insumos")
public class InsumoServices 
{
    @GET
    @Path("/")
    @Produces(MediaType.APPLICATION_JSON)
    public Response get()
    {
        GenericEntity<List<Insumo>> lista = new GenericEntity<List<Insumo>>(InsumoDAO.getAll())
        {
        };
        if (((List) lista.getEntity()).size() > 0)
        {
            return Response.ok(lista).build();
        }
        return Response.status(Response.Status.NO_CONTENT).build();
    }

}

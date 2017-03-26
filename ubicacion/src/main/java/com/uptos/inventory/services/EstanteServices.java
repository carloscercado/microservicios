package com.uptos.inventory.services;

import com.uptos.inventory.dao.EstanteDAO;
import com.uptos.inventory.model.Estante;
import java.util.List;
import javax.ws.rs.*;
import javax.ws.rs.core.*;
import javax.ws.rs.core.MediaType;

/**
 *
 * @author Carlos Cercado
 * @email cercadocarlos@gmail.com
 */
@Path("estantes")
public class EstanteServices 
{
    @GET
    @Path("/")
    @Produces(MediaType.APPLICATION_JSON)
    public Response get()
    {
        GenericEntity<List<Estante>> lista = new GenericEntity<List<Estante>>(EstanteDAO.getAll())
        {
        };
        if (((List) lista.getEntity()).size() > 0)
        {
            return Response.ok(lista).build();
        }
        return Response.status(Response.Status.NO_CONTENT).build();
    }

}

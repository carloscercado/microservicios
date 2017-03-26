package com.uptos.inventory.services;

import com.uptos.inventory.dao.AlmacenDAO;
import com.uptos.inventory.model.Almacen;
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
public class AlmacenServices 
{
    @GET
    @Path("/")
    @Produces(MediaType.APPLICATION_JSON)
    public Response get()
    {
        GenericEntity<List<Almacen>> lista = new GenericEntity<List<Almacen>>(AlmacenDAO.getAll())
        {
        };
        if (((List) lista.getEntity()).size() > 0)
        {
            return Response.ok(lista).build();
        }
        return Response.status(Response.Status.NO_CONTENT).build();
    }

}

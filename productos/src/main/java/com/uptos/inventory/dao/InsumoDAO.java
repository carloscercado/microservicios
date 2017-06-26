package com.uptos.inventory.dao;

import com.uptos.inventory.config.HibernateUtil;
import com.uptos.inventory.model.Insumo;
import com.uptos.inventory.model.Perece;
import java.util.Date;
import org.hibernate.Session;

/**
 *
 * @author Carlos Cercado
 * @email cercadocarlos@gmail.com
 */
public class InsumoDAO implements Crud<Insumo>
{

    public Insumo create(Insumo obj, Date vencimiento)
    {
        Session sesion = null;
        Insumo salida = null;
        try
        {
            sesion = HibernateUtil.getSesion().openSession();
            sesion.beginTransaction();
            sesion.save(obj);
            
            sesion.getTransaction().commit();
            sesion.beginTransaction();
            PereceDAO pere = new PereceDAO();
            Perece perece2 = new Perece(0, obj, vencimiento);
            pere.create(perece2);
            sesion.getTransaction().commit();
            salida = obj;
        } catch (Exception ex)
        {
            System.out.println(ex.getMessage());
            sesion.getTransaction().rollback();
            salida = null;
        } finally
        {
            if (sesion != null)
            {
                sesion.close();
            }
        }
        return salida;
    }
}

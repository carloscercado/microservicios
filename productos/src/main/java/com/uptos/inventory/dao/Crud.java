package com.uptos.inventory.dao;

import com.uptos.inventory.config.HibernateUtil;
import java.util.List;
import org.hibernate.Session;

/**
 *
 * @author Carlos Cercado
 * @email cercadocarlos@gmail.com
 */
public interface Crud<T>
{

    default List<T> read(String hql)
    {
        Session sesion = null;//
        List<T> lista = null;
        try
        {
            sesion = HibernateUtil.getSesion().openSession();
            sesion.beginTransaction();
            lista = sesion.createQuery(hql).list();
            sesion.getTransaction().commit();
        } catch (Exception ex)
        {
            System.out.println("XXXXXXXXXXXXX:::  "+ex.getMessage());
            sesion.getTransaction().rollback();
        } finally
        {
            if (sesion != null)
            {
                sesion.close();
            }
            return lista;
        }
    }

    default T create(T obj)
    {
        Session sesion = null;
        T salida = null;
        try
        {
            sesion = HibernateUtil.getSesion().openSession();
            sesion.beginTransaction();
            sesion.save(obj);
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

    default T update(T obj)
    {
        Session sesion = null;
        T salida = null;
        try
        {
            sesion = HibernateUtil.getSesion().openSession();
            sesion.beginTransaction();
            sesion.update(obj);
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
    default T get(String hql)
    {
        Session sesion = null;//
        T obj = null;
        try
        {
            sesion = HibernateUtil.getSesion().openSession();
            sesion.beginTransaction();
            obj = (T) sesion.createQuery(hql).list().get(0);
            sesion.getTransaction().commit();
        } catch (Exception ex)
        {
            System.err.println(ex.getMessage());
            sesion.getTransaction().rollback();
        } finally
        {
            if (sesion != null)
            {
                sesion.close();
            }
            return obj;
        }
    }
}

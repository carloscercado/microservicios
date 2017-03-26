package com.uptos.inventory.dao;

import com.uptos.inventory.config.MyBatisUtil;
import com.uptos.inventory.model.Almacen;
import java.util.List;
import org.apache.ibatis.session.SqlSession;
import com.uptos.inventory.mapper.AlmacenMapper;

/**
 *
 * @author Carlos Cercado
 * @email cercadocarlos@gmail.com
 */
public class AlmacenDAO
{

    public static boolean save(Almacen obj)
    {
        SqlSession sesion = null;
        boolean estado = false;
        try
        {
            sesion = MyBatisUtil.getSesion().openSession();
            AlmacenMapper map = sesion.getMapper(AlmacenMapper.class);
            map.insert(obj);
            sesion.commit();
            estado = true;
        } catch (Exception e)
        {
            System.out.println(e.getMessage());
            sesion.rollback();
            estado = false;
        } finally
        {
            if (sesion != null)
            {
                sesion.close();
            }
        }
        return estado;
    }
    
    public static Almacen findById(int id)
    {
        SqlSession sesion = null;
        Almacen obj = null;
        try
        {
            sesion = MyBatisUtil.getSesion().openSession();
            AlmacenMapper map = sesion.getMapper(AlmacenMapper.class);
            obj = map.getById(id);
            sesion.commit();
        } catch (Exception e)
        {
            sesion.rollback();
            obj = null;
        } finally
        {
            if (sesion != null)
            {
                sesion.close();
            }
        }
        return obj;

    }

    public static List<Almacen> getAll()
    {
        SqlSession sesion = null;
        List<Almacen> objs = null;
        try
        {
            sesion = MyBatisUtil.getSesion().openSession();
            AlmacenMapper map = sesion.getMapper(AlmacenMapper.class);
            objs = map.getAll();
            sesion.commit();
        } catch (Exception e)
        {
            sesion.rollback();
            objs = null;
        } finally
        {
            if (sesion != null)
            {
                sesion.close();
            }
        }
        return objs;

    }

    public static List<Almacen> getAllByCategory(int categoria)
    {
        SqlSession sesion = null;
        List<Almacen> objs = null;
        try
        {
            sesion = MyBatisUtil.getSesion().openSession();
            AlmacenMapper map = sesion.getMapper(AlmacenMapper.class);
            objs = map.getAllByCategory(categoria);
            sesion.commit();
        } catch (Exception e)
        {
            sesion.rollback();
            objs = null;
        } finally
        {
            if (sesion != null)
            {
                sesion.close();
            }
        }
        return objs;

    }
}

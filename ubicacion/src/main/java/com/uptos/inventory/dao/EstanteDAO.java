package com.uptos.inventory.dao;

import com.uptos.inventory.config.MyBatisUtil;
import com.uptos.inventory.model.Estante;
import java.util.List;
import org.apache.ibatis.session.SqlSession;
import com.uptos.inventory.mapper.EstanteMapper;

/**
 *
 * @author Carlos Cercado
 * @email cercadocarlos@gmail.com
 */
public class EstanteDAO
{

    public static boolean save(Estante obj)
    {
        SqlSession sesion = null;
        boolean estado = false;
        try
        {
            sesion = MyBatisUtil.getSesion().openSession();
            EstanteMapper map = sesion.getMapper(EstanteMapper.class);
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
    
    public static Estante findById(int id)
    {
        SqlSession sesion = null;
        Estante obj = null;
        try
        {
            sesion = MyBatisUtil.getSesion().openSession();
            EstanteMapper map = sesion.getMapper(EstanteMapper.class);
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

    public static List<Estante> getAll()
    {
        SqlSession sesion = null;
        List<Estante> objs = null;
        try
        {
            sesion = MyBatisUtil.getSesion().openSession();
            EstanteMapper map = sesion.getMapper(EstanteMapper.class);
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

    public static List<Estante> getAllByCategory(int categoria)
    {
        SqlSession sesion = null;
        List<Estante> objs = null;
        try
        {
            sesion = MyBatisUtil.getSesion().openSession();
            EstanteMapper map = sesion.getMapper(EstanteMapper.class);
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

package com.uptos.inventory.dao;

import com.uptos.inventory.config.MyBatisUtil;
import com.uptos.inventory.mapper.InsumoMapper;
import com.uptos.inventory.model.Insumo;
import java.util.List;
import org.apache.ibatis.session.SqlSession;

/**
 *
 * @author Carlos Cercado
 * @email cercadocarlos@gmail.com
 */
public class InsumoDAO
{

    public static boolean save(Insumo obj)
    {
        SqlSession sesion = null;
        boolean estado = false;
        try
        {
            sesion = MyBatisUtil.getSesion().openSession();
            InsumoMapper map = sesion.getMapper(InsumoMapper.class);
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
    
    public static Insumo findById(int id)
    {
        SqlSession sesion = null;
        Insumo obj = null;
        try
        {
            sesion = MyBatisUtil.getSesion().openSession();
            InsumoMapper map = sesion.getMapper(InsumoMapper.class);
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

    public static List<Insumo> getAll()
    {
        SqlSession sesion = null;
        List<Insumo> objs = null;
        try
        {
            sesion = MyBatisUtil.getSesion().openSession();
            InsumoMapper map = sesion.getMapper(InsumoMapper.class);
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

    public static List<Insumo> getAllByCategory(int categoria)
    {
        SqlSession sesion = null;
        List<Insumo> objs = null;
        try
        {
            sesion = MyBatisUtil.getSesion().openSession();
            InsumoMapper map = sesion.getMapper(InsumoMapper.class);
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

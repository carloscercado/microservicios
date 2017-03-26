package com.uptos.inventory.dao;

import com.uptos.inventory.config.MyBatisUtil;
import com.uptos.inventory.model.Cubiculo;
import java.util.List;
import org.apache.ibatis.session.SqlSession;
import com.uptos.inventory.mapper.CubiculoMapper;

/**
 *
 * @author Carlos Cercado
 * @email cercadocarlos@gmail.com
 */
public class CubiculoDAO
{

    public static boolean save(Cubiculo obj)
    {
        SqlSession sesion = null;
        boolean estado = false;
        try
        {
            sesion = MyBatisUtil.getSesion().openSession();
            CubiculoMapper map = sesion.getMapper(CubiculoMapper.class);
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
    
    public static Cubiculo findById(int id)
    {
        SqlSession sesion = null;
        Cubiculo obj = null;
        try
        {
            sesion = MyBatisUtil.getSesion().openSession();
            CubiculoMapper map = sesion.getMapper(CubiculoMapper.class);
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

    public static List<Cubiculo> getAll()
    {
        SqlSession sesion = null;
        List<Cubiculo> objs = null;
        try
        {
            sesion = MyBatisUtil.getSesion().openSession();
            CubiculoMapper map = sesion.getMapper(CubiculoMapper.class);
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

    public static List<Cubiculo> getAllByCategory(int categoria)
    {
        SqlSession sesion = null;
        List<Cubiculo> objs = null;
        try
        {
            sesion = MyBatisUtil.getSesion().openSession();
            CubiculoMapper map = sesion.getMapper(CubiculoMapper.class);
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

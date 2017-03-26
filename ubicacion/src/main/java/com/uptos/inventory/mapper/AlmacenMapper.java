package com.uptos.inventory.mapper;

import com.uptos.inventory.model.Almacen;
import java.util.List;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Options;
import org.apache.ibatis.annotations.Select;

/**
 *
 * @author Carlos Cercado
 * @email cercadocarlos@gmail.com
 */
public interface AlmacenMapper
{

    String getById = "select * from insumo where id=#{id}";
    String insert = "insert into insumo (nombre) values(#{nombre})";
    String getAll = "select * from insumo";
    String getAllByCategory = "select * from insumo where categoria=#{categoria}";

    @Select(getById)
    public Almacen getById(int id) throws Exception;

    @Select(getAll)
    public List<Almacen> getAll() throws Exception;

    @Select(getAllByCategory)
    public List<Almacen> getAllByCategory(int categoria) throws Exception;

    @Insert(insert)
    @Options(useGeneratedKeys = true)
    public void insert(Almacen obj) throws Exception;
}

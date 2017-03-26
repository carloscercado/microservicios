package com.uptos.inventory.mapper;

import com.uptos.inventory.model.Insumo;
import java.util.List;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Options;
import org.apache.ibatis.annotations.Select;

/**
 *
 * @author Carlos Cercado
 * @email cercadocarlos@gmail.com
 */
public interface InsumoMapper
{

    String getById = "select * from insumo where id=#{id}";
    String insert = "insert into insumo (nombre) values(#{nombre})";
    String getAll = "select * from insumo";
    String getAllByCategory = "select * from insumo where categoria=#{categoria}";

    @Select(getById)
    public Insumo getById(int id) throws Exception;

    @Select(getAll)
    public List<Insumo> getAll() throws Exception;

    @Select(getAllByCategory)
    public List<Insumo> getAllByCategory(int categoria) throws Exception;

    @Insert(insert)
    @Options(useGeneratedKeys = true)
    public void insert(Insumo obj) throws Exception;
}

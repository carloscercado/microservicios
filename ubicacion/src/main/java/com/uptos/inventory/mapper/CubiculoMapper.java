package com.uptos.inventory.mapper;

import com.uptos.inventory.model.Cubiculo;
import java.util.List;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Options;
import org.apache.ibatis.annotations.Select;

/**
 *
 * @author Carlos Cercado
 * @email cercadocarlos@gmail.com
 */
public interface CubiculoMapper
{

    String getById = "select * from insumo where id=#{id}";
    String insert = "insert into insumo (nombre) values(#{nombre})";
    String getAll = "select * from insumo";
    String getAllByCategory = "select * from insumo where categoria=#{categoria}";

    @Select(getById)
    public Cubiculo getById(int id) throws Exception;

    @Select(getAll)
    public List<Cubiculo> getAll() throws Exception;

    @Select(getAllByCategory)
    public List<Cubiculo> getAllByCategory(int categoria) throws Exception;

    @Insert(insert)
    @Options(useGeneratedKeys = true)
    public void insert(Cubiculo obj) throws Exception;
}

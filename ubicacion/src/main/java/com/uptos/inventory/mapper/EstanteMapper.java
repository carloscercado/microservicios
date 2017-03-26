package com.uptos.inventory.mapper;

import com.uptos.inventory.model.Estante;
import java.util.List;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Options;
import org.apache.ibatis.annotations.Select;

/**
 *
 * @author Carlos Cercado
 * @email cercadocarlos@gmail.com
 */
public interface EstanteMapper
{

    String getById = "select * from insumo where id=#{id}";
    String insert = "insert into insumo (nombre) values(#{nombre})";
    String getAll = "select * from insumo";
    String getAllByCategory = "select * from insumo where categoria=#{categoria}";

    @Select(getById)
    public Estante getById(int id) throws Exception;

    @Select(getAll)
    public List<Estante> getAll() throws Exception;

    @Select(getAllByCategory)
    public List<Estante> getAllByCategory(int categoria) throws Exception;

    @Insert(insert)
    @Options(useGeneratedKeys = true)
    public void insert(Estante obj) throws Exception;
}

package com.uptos.inventory.config;

import java.io.InputStream;
import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;

public class MyBatisUtil
{

    private static SqlSessionFactory sqlSessionFactory;

    static
    {

        try
        {
            String resource = "config.xml";
            InputStream inputStream = Resources.getResourceAsStream(resource);
            sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
        } catch (Exception e)
        {

            System.err.println("MYBATIS ERROR::::::" + e.getMessage());
        }
    }

    public static SqlSessionFactory getSesion()
    {
        return sqlSessionFactory;
    }

}

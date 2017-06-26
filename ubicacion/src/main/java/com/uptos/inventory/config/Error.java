package com.uptos.inventory.config;

public class Error
{
    public static final String WITH_OUT_AUTHORIZATION = "01";
    public static final String CREDENTIAL_FALSE = "02";
    public static final String CREDENTIAL_EXPIRED = "03";
    public static final String PASSWORD_SHORT = "04";
    public static final String BAD_USERNAME = "05";
    public static final String BAD_DATA = "06";
    public static final String BAD_OTHER_DATA = "07";
    public static final String NO_SAVE = "08";
    public static final String NO_EXIST = "09";
    
    public static String getCredential(String error)
    {
        return "0"+error;
    }
    
    public static String getBadData (String error)
    {
        return "1"+error;
    }
    
    public static String getDataBase(String error)
    {
        return "2"+error;
    }
}

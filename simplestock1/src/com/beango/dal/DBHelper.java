package com.beango.dal;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteDatabase.CursorFactory;
import android.database.sqlite.SQLiteOpenHelper;

public class DBHelper extends SQLiteOpenHelper {
	private final static int VERSION = 1;  
	
    private final static String DB_NAME = "wlstock.s3db";  
    private final static String TABLE_NAME = "mystock";  
    private final static String CREATE_TBL = "create table mystock(pkid integer primary key autoincrement, stockno text, stocktype text)";  
    private SQLiteDatabase db;  
    
	//SQLiteOpenHelper�������Ҫ��һ�����캯��  
    public DBHelper(Context context, String name, CursorFactory factory,int version) {  
        //����ͨ��super ���ø���Ĺ��캯��  
        super(context, name, factory, version);  
    }  
      
    //���ݿ�Ĺ��캯������������������  
    public DBHelper(Context context, String name, int version){  
        this(context, name, null, version);  
    }  
      
    //���ݿ�Ĺ��캯��������һ�������ģ� ���ݿ����ֺͰ汾�Ŷ�д����  
    public DBHelper(Context context){  
        this(context, DB_NAME, null, VERSION);  
    }  
    
	@Override
	public void onCreate(SQLiteDatabase db) {
		this.db = db;  
        System.out.println("Create Database");  
        //db.execSQL(CREATE_TBL);   
	}

	@Override
	public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
		System.out.println("update Database"); 
	}

	//���뷽��  
    public void insert(ContentValues values){  
        //��ȡSQLiteDatabaseʵ��  
        SQLiteDatabase db = getWritableDatabase();  
        //�������ݿ���  
        db.insert(TABLE_NAME, null, values);  
        db.close();  
    }  
      
    //��ѯ����  
    public Cursor query(){  
    	System.out.println("query Database");
        SQLiteDatabase db = getReadableDatabase();  
        //��ȡCursor  
        Cursor c = db.query(TABLE_NAME, null, null, null, null, null, null, null);  
        return c;  
          
    }  
      
    //����Ψһ��ʶ_id  ��ɾ������  
    public void delete(int id){  
        SQLiteDatabase db = getWritableDatabase();  
        db.delete(TABLE_NAME, "_id=?", new String[]{String.valueOf(id)});  
    }  
      
      
    //�������ݿ������  
    public void update(ContentValues values, String whereClause, String[]whereArgs){  
        SQLiteDatabase db = getWritableDatabase();  
        db.update(TABLE_NAME, values, whereClause, whereArgs);  
    }  
      
    //�ر����ݿ�  
    public void close(){  
        if(db != null){  
            db.close();  
        }  
    }  
}

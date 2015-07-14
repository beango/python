package com.beango.dal;

public class MyStockDTO {
	private int pkid; 
	private String stockno; 
	private String stockname; 
	public String getStockname() {
		return stockname;
	}
	public void setStockname(String stockname) {
		this.stockname = stockname;
	}
	private String stocktype;	
	
	public int getPkid() {
		return pkid;
	}
	public void setPkid(int pkid) {
		this.pkid = pkid;
	}
	public String getStockno() {
		return stockno;
	}
	public void setStockno(String stockno) {
		this.stockno = stockno;
	}
	public String getStocktype() {
		return stocktype;
	}
	public void setStocktype(String stocktype) {
		this.stocktype = stocktype;
	} 
}

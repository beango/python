package com.beango.dal;

public class MyStockExDTO extends MyStockDTO {
private double newprice;
private double delayprice;
private double delayrate;
public double getNewprice() {
	return newprice;
}
public void setNewprice(double newprice) {
	this.newprice = newprice;
}
public double getDelayprice() {
	return delayprice;
}
public void setDelayprice(double delayprice) {
	this.delayprice = delayprice;
}
public double getDelayrate() {
	return delayrate;
}
public void setDelayrate(double delayrate) {
	this.delayrate = delayrate;
}
}

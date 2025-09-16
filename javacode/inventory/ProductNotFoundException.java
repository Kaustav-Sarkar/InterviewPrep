package javacode.inventory;

public class ProductNotFoundException extends Exception {
    @Override
    public String getMessage() {
        System.out.println("over ridden exception");
        return super.getMessage();
    }
}

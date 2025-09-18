package LLD.javacode.inventory;

public interface Purchasable {

    double getPrice();

    String getSku();

    default String someMethod() {
        System.out.println("This is default method of interface");
        return "Hello World";
    }
}

package LLD.javacode.inventory;

public class Ebook extends DigitalProduct {
    private String author;

    Ebook(String name, double price, String author) {
        super(name, price);
        this.author = author;
    }

    public String getSku() {
        return "EBK-" + super.getName();
    }

    public void validate() {
        System.out.println("validating ebook");
    }

}
package javacode.inventory;

abstract class DigitalProduct implements Purchasable {
    private String name;
    private double price;

    DigitalProduct(String name, double price) {
        if (name.length() < 100) {
            this.name = name;
        } else {
            throw new IllegalArgumentException("Name Cannot be greater than 100 characters");
        }
        if (price > 0) {
            this.price = price;
        } else {
            throw new IllegalArgumentException("Price Cannot be less than 0");
        }
    }

    public double getPrice() {
        return this.price;
    }

    public String getName() {
        return this.name;
    }

    public abstract void validate();

}

package LLD.javacode.inventory;

public class GameKey extends DigitalProduct {
    private String platform;

    GameKey(String name, double price, String platform) {
        super(name, price);
        this.platform = platform;
    }

    public String getSku() {
        return "GMK-" + this.getName();
    }

    public void validate() {
        System.out.println("validating gamekey");
    }

}
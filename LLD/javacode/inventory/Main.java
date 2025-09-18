package LLD.javacode.inventory;

import java.util.List;
import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        Inventory<DigitalProduct> inventory = new Inventory<>();
        List<GameKey> gameKeys = new ArrayList<>();
        List<Ebook> eBooks = new ArrayList<>();
        gameKeys.add(new GameKey("Hogwarts Legacy", 2700, "Steam"));
        gameKeys.add(new GameKey("AC Valhalla", 4000, "Epic Games"));

        eBooks.add(new Ebook("Atomic Habits", 599, "James Clear"));
        eBooks.add(new Ebook("Harry Potter", 199, "JK Rowling"));

        for (var ebook : eBooks) {
            inventory.addProduct(ebook);
        }
        for (var gameKey : gameKeys) {
            inventory.addProduct(gameKey);
        }

        try {
            System.out.println(inventory.getAllProductSkus());
            System.out.println(inventory.getAllProducts());
            System.out.println("\n\n Trying to get atomic habits");
            System.out.println(inventory.getProductBySku("EBK-Atomic Habits"));
            System.out.println("\n\n Trying to get Ac Valhalla");
            System.out.println(inventory.getProductBySku("GMK-AC Valhalla"));
            System.out.println("\n\n Trying to get Invalid SKU");
            System.out.println(inventory.getProductBySku("GMK-AC Valhalla2"));
        } catch (Exception e) {
            System.out.println(e);
        }
    }
}

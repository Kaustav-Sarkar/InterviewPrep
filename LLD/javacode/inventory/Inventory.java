package LLD.javacode.inventory;

import java.util.Map;
import java.util.HashMap;
import java.util.List;
import java.util.ArrayList;

public class Inventory<T extends DigitalProduct> {
    private Map<String, T> inventory = new HashMap<>();

    void addProduct(T product) {
        inventory.put(product.getSku(), product);
    }

    T getProductBySku(String Sku) throws ProductNotFoundException {
        try {
            if (inventory.get(Sku) == null) {
                throw new ProductNotFoundException();
            }
        } catch (Exception e) {
            System.out.println("Product not found");
            throw (e);
        }
        return inventory.get(Sku);

    }

    public List<String> getAllProductSkus() {
        List<String> skus = new ArrayList<>();
        this.inventory.forEach((sku, product) -> skus.add(sku));
        return skus;
    }

    public List<DigitalProduct> getAllProducts() {
        List<DigitalProduct> products = new ArrayList<>();
        this.inventory.forEach((sku, product) -> products.add(product));
        return products;
    }
}

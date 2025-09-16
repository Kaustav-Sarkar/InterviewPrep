package javacode.sample;

public class Car {
    private String color;
    private int year;

    Car(String color, int year) {
        this.color = color;
        this.year = year;
    }

    Car() {
        System.out.println("Color and Year is not set");
    }

    public String getColor() {
        return this.color;
    }

    public int getYear() {
        return this.year;
    }
}

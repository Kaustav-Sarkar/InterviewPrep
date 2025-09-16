package javacode.sample;

public class Main {
    public static void main(String args[]) {
        Car myCar = new Car("red", 2024);
        System.out.println(myCar.getColor());
        System.out.println(myCar.getYear());
        System.out.println(myCar.toString());

        ElectricCar myElectricCar = new ElectricCar("green", 2025, 100);
        System.out.println(myElectricCar.toString());
    }
}
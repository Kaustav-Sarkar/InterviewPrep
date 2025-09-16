package javacode.sample;

public class ElectricCar extends Car {
    private int batteryCapacity;

    ElectricCar(int batteryCapacity) {
        super();
        this.batteryCapacity = batteryCapacity;

    }

    ElectricCar(String color, int year, int batteryCapacity) {
        super(color, year);
        this.batteryCapacity = batteryCapacity;
    }

    public int getBatteryCapacity() {
        return this.batteryCapacity;
    }

    @Override
    public String toString() {
        return String.format("Color %s, year %s, batteryCapacity %s", this.getColor(), this.getYear(),
                this.getBatteryCapacity());
    }
}

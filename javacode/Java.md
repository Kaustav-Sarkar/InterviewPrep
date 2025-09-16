# Java Interview Quick Reference

## Fundamentals

* **Entry Point**: `public static void main(String[] args)`
* **8 Primitives**: `byte`, `short`, `int`, `long`, `float`, `double`, `boolean`, `char`.
* **Control Flow**: `for`/`while` loops.
  * `break`: Exits the entire loop.
  * `continue`: Skips the current iteration.
* **Strings are objects**, not primitives.

---

## OOP Pillars

* **Encapsulation**: `private` fields with `public` getters/setters to protect and control access to data.
* **Inheritance**: `extends` keyword for "is-a" relationships. Use `super()` to call parent constructor.
* **Polymorphism**: A subclass provides its own implementation of a parent method. Use `@Override`.
* **Abstraction**: Hide complex implementation, showing only essential features.

---

## `abstract class` vs. `interface`

* **`abstract class`**: A blueprint for closely related classes.
  * Use for "is-a" relationships (`Car` is-a `Vehicle`).
  * Can have instance variables (state) and constructors.
  * A class can `extend` only **one** abstract class.
* **`interface`**: A contract for capabilities.
  * Use for "can-do" relationships (`Bird` can-do `Flyable`).
  * Cannot have instance variables or constructors. Variables are `public static final`.
  * A class can `implement` **multiple** interfaces.

---

## Advanced Concepts

* **Collections Framework**:
  * `List`: Ordered, allows duplicates (`ArrayList`).
  * `Set`: Unordered, unique elements (`HashSet`).
  * `Map`: Key-value pairs (`HashMap`).
* **Generics**: Type safety for collections, e.g., `List<String>`.
* **Exception Handling**:
  * `try-catch-finally` block to handle errors.
  * `throw` to signal an error.
  * Create custom exceptions by extending `Exception`.
  * Use `IllegalArgumentException` for bad method arguments.

---

## "Default" Features

* **Default Access Modifier**: No keyword (`public`, `private`) means the class/method is **package-private**.
* **Default Constructor**: If a class has no constructors, the compiler creates a public no-argument one.
* **Default Methods**: In an `interface`, the `default` keyword lets you provide a method implementation.

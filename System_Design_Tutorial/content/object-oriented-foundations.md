# Object-Oriented Foundations

Welcome to the foundation of Low-Level Design! Before we can talk about design patterns or building complex systems like a Parking Lot or an Elevator, we absolutely must master the four pillars of Object-Oriented Programming (OOP).

Many developers can recite the definitions of these pillars, but they struggle to apply them practically. Today, we aren't just memorizing definitions; we are understanding *why* these concepts were invented and exactly how they solve massive software engineering headaches.

## Encapsulation

Encapsulation is the practice of bundling data (attributes) and the methods that operate on that data into a single unit (a class), and crucially, **restricting direct access to some of the object's components.**

### The "Why" Behind Encapsulation
Imagine a Bank Account. If the `balance` variable is public, any part of the codebase can execute `account.balance = 1000000;`.
Why is this terrible?
1. **No Validation:** Someone could set the balance to a negative number.
2. **No Auditing:** We have no way to log *who* changed the balance.
3. **Tight Coupling:** If we later decide the balance should be stored in cents instead of dollars, we break every piece of code that accessed `balance` directly.

Encapsulation forces other code to use a method, like `deposit(amount)`.

### Real-World Analogy
Think of a vending machine. The money and the snacks inside are **encapsulated**. You cannot just reach in and grab a snack or change the coin counter. You must interact with the vending machine through its public interface (the buttons and the coin slot). The vending machine validates your input (did you put in enough money?) before dispensing the item.

```java
public class BankAccount {
    // Hidden data
    private double balance;

    // Public method to control access
    public void deposit(double amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("Deposit amount must be positive");
        }
        this.balance += amount; // We can add auditing logs here later without breaking external code!
    }
}
```

## Abstraction

Abstraction means hiding the complex implementation details and showing only the essential features of the object. While encapsulation hides *data*, abstraction hides *complexity*.

### The "Why" Behind Abstraction
Software is infinitely complex. If a developer had to understand how a hard drive stores magnetic bits just to save a text file, nothing would ever get built. Abstraction provides a simple interface over a complex subsystem.

### Real-World Analogy
Think of driving a car. You interact with the steering wheel, the accelerator, and the brake pedal. This is the **abstraction**. You don't need to know the thermodynamics of the internal combustion engine, the gear ratios in the transmission, or how the fuel injector works to drive to the grocery store.

In code, abstraction is usually achieved via Interfaces or Abstract Classes.

```java
// The Abstraction
public interface Database {
    void save(String data);
}

// The Complex Implementation
public class PostgresDatabase implements Database {
    public void save(String data) {
        // 1. Establish TCP connection
        // 2. Authenticate
        // 3. Begin transaction
        // 4. Write to WAL (Write-Ahead Log)
        // 5. Commit transaction
    }
}
```
If your system relies on the `Database` interface, you can swap `PostgresDatabase` for `MongoDatabase` tomorrow, and the rest of your system won't even notice.

> [!NOTE]
> **Teacher FAQ:** *What's the difference between Encapsulation and Abstraction?*
> Encapsulation is about **protection and state management** (hiding the variables). Abstraction is about **simplifying the interface** (hiding the logic).

## Inheritance vs Composition

This is perhaps the most debated topic in Object-Oriented Design. Both are ways to reuse code, but they behave very differently.

### Inheritance (The "Is-A" Relationship)
Inheritance is when a class derives from a parent class, absorbing all its data and behaviors.
*Example: A `Dog` IS-A `Animal`.*

**The Danger of Inheritance:**
Inheritance creates extreme coupling. If you change the base class, you immediately affect all child classes. This often leads to the "Fragile Base Class" problem.
Also, what if you have a `Bird` class that inherits from `Animal`, and you add a `fly()` method to `Bird`? Now you have a `Penguin` that inherits from `Bird`. Penguins can't fly. You are forced to override `fly()` to throw an exception, violating design principles.

### Composition (The "Has-A" Relationship)
Composition is when a class contains instances of other classes to achieve functionality.
*Example: A `Car` HAS-A `Engine`.*

Instead of `Penguin` inheriting from a `FlyingAnimal`, we give classes capabilities.

### Why Composition is Usually Better
Modern software engineering strongly favors **Composition over Inheritance**. It provides incredible flexibility at runtime.

| Feature | Inheritance | Composition |
|---------|-------------|-------------|
| **Relationship** | "Is-a" | "Has-a" / "Uses-a" |
| **Coupling** | Very tight (Compile-time) | Loose (Runtime) |
| **Flexibility** | Cannot change parent at runtime | Can swap components at runtime |
| **Testing** | Hard to mock parent classes | Easy to mock injected dependencies |

```java
// Composition Approach
public class Duck {
    private FlyBehavior flyBehavior; // Interface
    private QuackBehavior quackBehavior; // Interface

    public Duck(FlyBehavior fb, QuackBehavior qb) {
        this.flyBehavior = fb;
        this.quackBehavior = qb;
    }

    public void performFly() {
        flyBehavior.fly();
    }
}
// We can easily create a RubberDuck by injecting a NoFly behavior and a Squeak behavior, without complex inheritance trees!
```

## Polymorphism

Polymorphism literally means "many forms". In programming, it is the ability of different objects to respond to the same method call in their own specific way.

### The "Why" Behind Polymorphism
Polymorphism allows you to write extremely clean, extensible code. Without polymorphism, you would need massive `if/else` or `switch` statements every time you wanted to perform an action on different types of objects.

### Real-World Analogy
Imagine a movie director on a set yelling "Action!".
- The actor starts crying.
- The camera operator starts recording.
- The lighting technician turns on the spotlights.

The director sent **one command** ("Action!"), but each person (object) interpreted that command differently based on their role. The director doesn't need to know *how* the camera works; they just know the camera understands the "Action!" command.

### Polymorphism in Action
```java
List<Shape> shapes = new ArrayList<>();
shapes.add(new Circle());
shapes.add(new Square());
shapes.add(new Triangle());

// NO if/else needed! The exact draw() method called is determined at runtime.
for (Shape shape : shapes) {
    shape.draw();
}
```

> [!TIP]
> **Pro Tip for Interviews:**
> If an interviewer asks you to design a system with many different types of a core entity (e.g., Different types of notifications: SMS, Email, Push), immediately reach for Polymorphism + Composition. Create an interface `NotificationSender`, implement it for each type, and have your main class iterate through them. This proves you understand extensible LLD.

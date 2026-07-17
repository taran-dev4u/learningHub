# Design Patterns For LLD

Welcome to the toolkit of a Senior Engineer. Design Patterns are proven, repeatable solutions to commonly occurring problems in software design. They are not code; they are templates.

If you don't use design patterns, you will constantly reinvent the wheel, and your wheel will probably be a square. In this masterclass, we will cover the five most important patterns you need for Low-Level Design interviews and production systems.

## Factory Pattern

The Factory Pattern is a Creational Pattern. It provides an interface for creating objects in a superclass, but allows subclasses to alter the type of objects that will be created.

### The "Why" Behind Factory Pattern
Imagine you are writing a ride-sharing app (like Uber). Initially, you only have `Car` objects. You sprinkle `new Car()` everywhere in your codebase.
Six months later, the business wants to add `Bike` and `Scooter`. Now you have to hunt down every `new Car()` and replace it with a massive `if/else` block based on the ride type.
The Factory Pattern centralizes this creation logic.

### Real-World Analogy
Think of a car manufacturing plant. When a customer orders a vehicle, they don't go to the assembly line and bolt the doors on. They go to the dealership (the Factory) and say "I want a Sedan". The factory handles the complex creation process and hands them the keys.

```java
public class VehicleFactory {
    public static Vehicle getVehicle(String type) {
        if (type.equals("CAR")) {
            return new Car();
        } else if (type.equals("BIKE")) {
            return new Bike();
        }
        throw new IllegalArgumentException("Unknown vehicle type");
    }
}
```

## Strategy Pattern

The Strategy Pattern is a Behavioral Pattern. It defines a family of algorithms, encapsulates each one, and makes them interchangeable.

### The "Why" Behind Strategy Pattern
Let's say you are building a navigation app (like Google Maps). You need to calculate a route.
First, you write a route for cars. Then you add logic for walking. Then for public transit. Your `RouteCalculator` class is now 5,000 lines long and completely unmaintainable.
The Strategy pattern lets you pull those algorithms out into their own classes.

### How it Works
1. Define a `RouteStrategy` interface with a `calculate()` method.
2. Create `CarStrategy`, `WalkStrategy`, and `BusStrategy` classes that implement it.
3. The main `Navigator` class holds a reference to a `RouteStrategy` and delegates the calculation to it.

> [!TIP]
> **Interview Tip:** If you hear the words "sort", "filter", "calculate", or "discount" in an interview, immediately consider the Strategy Pattern.

## Observer Pattern

The Observer Pattern is a Behavioral Pattern. It lets you define a subscription mechanism to notify multiple objects about any events that happen to the object they're observing.

### The "Why" Behind Observer Pattern
Imagine an auction system. When the current bid changes, the system needs to update the web UI, send an SMS to the previous highest bidder, and update the database.
If the `BidManager` directly calls all three of these systems, it is tightly coupled to them. What if we want to add an email notification later?
The Observer Pattern decouples the "Subject" (the bid) from the "Observers" (the UI, SMS, Database).

### Real-World Analogy
A YouTube channel. You (the Observer) click the "Subscribe" button on a channel (the Subject). When the channel posts a new video, YouTube automatically notifies you and a million other subscribers. The channel doesn't need to know your name or email address; it just knows you implement the `Subscriber` interface.

## Decorator Pattern

The Decorator Pattern is a Structural Pattern. It lets you attach new behaviors to objects by placing these objects inside special wrapper objects that contain the behaviors.

### The "Why" Behind Decorator Pattern
Suppose you are designing a coffee shop POS system. You have a `Coffee` class. Then someone wants milk, so you create `CoffeeWithMilk`. Then they want sugar: `CoffeeWithMilkAndSugar`. Before you know it, you have 100 classes for every possible combination of condiments (Class Explosion).
The Decorator Pattern lets you wrap the base `Coffee` object with multiple decorators (`Milk`, `Sugar`, `Caramel`) at runtime.

| Pattern | Type | Primary Use Case |
|---------|------|------------------|
| **Factory** | Creational | Centralizing object creation |
| **Strategy** | Behavioral | Swapping algorithms at runtime |
| **Observer** | Behavioral | Event-driven pub/sub communication |
| **Decorator** | Structural | Adding features without sub-classing |

## State Pattern

The State Pattern is a Behavioral Pattern. It lets an object alter its behavior when its internal state changes. It appears as if the object changed its class.

### The "Why" Behind State Pattern
Remember the State Diagram from our UML masterclass? The State Pattern is how you implement that diagram in code.
Instead of a giant `switch` statement checking `if (state == PAID)` in every method, you create a class for each state (`PaidState`, `ShippedState`). The main object delegates all actions to its current State object.

> [!NOTE]
> **Teacher FAQ:** *Isn't the Strategy Pattern and State Pattern the same thing?*
> Structurally, they are very similar (both use composition and delegation). However, the intent is different. **Strategy** is about the *client* choosing an algorithm (e.g., the user selects "Walk" or "Drive"). **State** is about an object autonomously transitioning itself from one state to another (e.g., an Order goes from "Paid" to "Shipped" without the client knowing the details).

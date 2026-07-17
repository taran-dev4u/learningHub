# Design Principles

Welcome to the architectural rules of the road. Once you understand Object-Oriented Programming, the next step is writing *good* Object-Oriented code. Code that doesn't break when requirements change. Code that other developers can read and extend without fear.

This is where Design Principles come in. They are language-agnostic philosophies that guide how you structure your logic. In this masterclass, we will dive deep into SOLID, DRY, KISS, and YAGNI.

## SOLID Principles

SOLID is an acronym introduced by Robert C. Martin (Uncle Bob). It represents five principles that, when combined, make it easy for a programmer to develop software that is easy to maintain and extend.

### 1. Single Responsibility Principle (SRP)
**Definition:** A class should have one, and only one, reason to change.
**The "Why":** If a class handles user authentication, database connections, and email sending, a change to the email provider might accidentally break the authentication logic.

**Analogy:** A Swiss Army Knife is great for camping, but in a professional kitchen, you want a specialized Chef's Knife, a specialized Spatula, and a specialized Peeler.

```java
// Bad: Multiple reasons to change
public class User {
    public void saveUserToDatabase() { ... }
    public void sendWelcomeEmail() { ... }
    public void generateInvoice() { ... }
}

// Good: Single responsibility
public class UserRepository { public void saveUser(User user) { ... } }
public class EmailService { public void sendEmail(User user) { ... } }
```

### 2. Open/Closed Principle (OCP)
**Definition:** Software entities (classes, modules, functions) should be open for extension, but closed for modification.
**The "Why":** You should be able to add new functionality without touching existing, tested code. Touching existing code risks introducing new bugs into features that already work perfectly.

**Analogy:** Think of a game console (like a PlayStation). The console itself is closed for modification (you don't unscrew it and solder new chips to play a new game). But it is open for extension (you just insert a new game disc).

### 3. Liskov Substitution Principle (LSP)
**Definition:** Objects of a superclass shall be replaceable with objects of its subclasses without breaking the application.
**The "Why":** If a function expects a `Bird`, and you pass it a `Penguin` (which inherits from `Bird`), the function shouldn't crash just because it calls `fly()`.

> [!CAUTION]
> **Common Violation:** Throwing a `NotImplementedException` in an overridden method is a massive red flag that you are violating the Liskov Substitution Principle. If the child class can't perform the action, the inheritance tree is flawed.

### 4. Interface Segregation Principle (ISP)
**Definition:** No client should be forced to depend on methods it does not use.
**The "Why":** Fat interfaces cause unnecessary coupling. If you have an `IWorker` interface with `work()` and `eat()`, and you create a `RobotWorker`, the robot shouldn't be forced to implement `eat()`.

**Solution:** Split `IWorker` into `IWorkable` and `IFeedable`.

### 5. Dependency Inversion Principle (DIP)
**Definition:** High-level modules should not depend on low-level modules. Both should depend on abstractions (interfaces).
**The "Why":** You want your core business logic to be completely decoupled from infrastructure details (like which database or message queue you use).

| Principle | Core Concept | Biggest Benefit |
|-----------|--------------|-----------------|
| **SRP** | One job per class | High cohesion, easier testing |
| **OCP** | Add features via new code | Prevents regression bugs |
| **LSP** | Predictable subclasses | Safe polymorphism |
| **ISP** | Small, focused interfaces | Prevents forced implementation |
| **DIP** | Depend on interfaces | Loose coupling, swappable tech |

## DRY Principle

**DRY = Don't Repeat Yourself.**

**The "Why":** Every piece of knowledge must have a single, unambiguous, authoritative representation within a system. If you copy-paste code, and a bug is found in that logic, you have to remember to fix it in 15 different places. You will inevitably forget one, leading to production issues.

**How to apply it:** If you see the same 5 lines of code in three different methods, extract them into a private helper method or a shared utility class.

## KISS Principle

**KISS = Keep It Simple, Stupid.**

**The "Why":** Complexity is the enemy of maintainability. Engineers often fall into the trap of "clever" code. They write one-line lambda expressions that do the work of 20 lines, but take 2 hours to decipher.

> [!TIP]
> **Teacher's Advice:** Code is read 10x more than it is written. Write your code so that a junior developer joining the team tomorrow can understand it without asking you questions.

## YAGNI Principle

**YAGNI = You Aren't Gonna Need It.**

**The "Why":** This is a core tenet of Extreme Programming. Do not build features, abstractions, or database columns "just in case" you might need them in the future.
Predicting the future in software engineering usually fails. If you build a complex plugin architecture for a feature the business *might* want next year, you are wasting time, adding bloat, and increasing the maintenance burden today. Build only what is needed for the current requirements.

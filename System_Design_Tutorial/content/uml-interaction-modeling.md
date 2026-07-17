# UML & Interaction Modeling

Welcome to the visual language of system design. Unified Modeling Language (UML) is the industry standard for mapping out software architecture and Low-Level Design (LLD).

Why do we need diagrams? Because human brains process visual information 60,000 times faster than text. Handing a developer a 40-page requirements document is a recipe for disaster. Handing them a Class Diagram and a Sequence Diagram gets them coding accurately in minutes.

In this masterclass, we will cover the four most critical diagrams you must master for Low-Level Design interviews and real-world architecture.

## Class Diagrams

A Class Diagram is the structural blueprint of your system. It shows the classes, their attributes, their methods, and most importantly, how they relate to one another.

### The "Why" Behind Class Diagrams
Before writing thousands of lines of code, you need to ensure your Object-Oriented principles (Inheritance, Composition) are sound. It is much easier to erase a line on a whiteboard than to refactor 50 classes.

### Key Components
- **Class Box:** Divided into three sections: Class Name, Attributes, Methods.
- **Visibility Modifiers:** `+` (Public), `-` (Private), `#` (Protected).
- **Relationships:**
  - **Inheritance (Is-A):** Solid line with a hollow arrow pointing to the parent.
  - **Composition (Strict Has-A):** Solid line with a filled diamond. If the parent dies, the child dies (e.g., `Building` has `Rooms`).
  - **Aggregation (Loose Has-A):** Solid line with a hollow diamond. The child can exist independently of the parent (e.g., `University` has `Professors`).

> [!TIP]
> **Interview Strategy:** Start your LLD interviews by drawing a fast Class Diagram. Identify the core entities (e.g., for a Parking Lot: `ParkingLot`, `Level`, `ParkingSpot`, `Vehicle`, `Ticket`).

## Sequence Diagrams

While Class Diagrams show the *structure* (static view), Sequence Diagrams show the *behavior* (dynamic view). They illustrate how objects interact over time to fulfill a specific use case.

### The "Why" Behind Sequence Diagrams
If a user clicks "Checkout", what exactly happens? Who calls who? Does the API Gateway call Auth first, or Payment? Sequence diagrams map out the exact chronological flow of messages between objects or microservices.

### Key Components
- **Actors/Objects:** Represented as boxes at the top.
- **Lifelines:** The dashed vertical line dropping down from an object, representing its lifespan.
- **Messages:** Solid arrows for synchronous calls (waiting for a response), dashed arrows for return messages.
- **Activation Boxes:** Thin rectangles on the lifeline showing when an object is actively processing.

### Analogy
Think of a Sequence Diagram like a movie script. It dictates exactly who speaks, when they speak, and who they are speaking to, from the beginning of the scene to the end.

## Activity Diagrams

Activity Diagrams are the Object-Oriented equivalent of flowcharts. They model the flow of control from one activity to another.

### The "Why" Behind Activity Diagrams
When a business process has complex branching logic, parallel execution, or loops, Class and Sequence diagrams struggle to show it clearly. Activity diagrams excel at showing business workflows.

### Key Components
- **Initial Node:** A solid black circle where the flow begins.
- **Action/Activity:** Rounded rectangles representing a step in the process.
- **Decision Node:** A diamond shape representing an `if/else` branch (e.g., "Is payment successful?").
- **Fork/Join:** Heavy black bars representing parallel execution (e.g., sending an email AND generating an invoice at the same time).
- **Final Node:** A solid circle surrounded by a hollow circle.

| Diagram Type | View Type | Best Used For |
|--------------|-----------|---------------|
| **Class** | Static | Defining data structures and OOP relationships |
| **Sequence**| Dynamic | Showing the exact API or method call order for a use case |
| **Activity**| Dynamic | Mapping out complex business logic and conditional flows |

## State Diagrams

State Diagrams (or State Machine Diagrams) show the different states an object can be in and how it transitions between them based on events.

### The "Why" Behind State Diagrams
Some objects have complex lifecycles where their behavior changes drastically depending on their current state. If you don't model this, you end up with massive, buggy `switch` statements scattered throughout your code.

### Real-World Example
Consider an `Order` in an e-commerce system:
1. **State:** `CREATED` -> Event: `pay()` -> Transitions to `PAID`
2. **State:** `PAID` -> Event: `ship()` -> Transitions to `SHIPPED`
3. **State:** `SHIPPED` -> Event: `deliver()` -> Transitions to `DELIVERED`

> [!WARNING]
> **Common Beginner Mistake:**
> Don't draw a State Diagram for everything. Only draw them for objects that have distinct, complex states (like an Order, a Vending Machine, or a TCP Connection). A `User` object usually doesn't need a state diagram if their state is just "active" or "inactive".

# Architecture Diagrams & Communication

## Overview
Welcome to the core visual language of System Design! You can have the most brilliant architecture in the world, but if you cannot draw it clearly on a whiteboard, you will fail the interview. 

An interviewer uses your whiteboard (or digital drawing tool) to judge your seniority. Junior engineers draw chaotic spaghetti diagrams. Senior engineers structure their drawings deliberately to tell a story.

In this masterclass, we will cover the industry-standard diagrams, what level of detail you should use, and exactly how to layout your whiteboard for maximum points.

---

## C4 model levels

When drawing diagrams, you need to know *what altitude* you are flying at. The **C4 Model** (Context, Containers, Components, Code) is the industry standard for visualizing software architecture.

In a 45-minute interview, you will almost exclusively use **Level 1** and **Level 2**.

| Level | Name | Description | Interview Use Case |
| :--- | :--- | :--- | :--- |
| **Level 1** | System Context | Shows the system as a single black box interacting with users and external systems. | The first 5 minutes to confirm requirements. |
| **Level 2** | Containers | Zooms into the black box. Shows the major applications, databases, and microservices (e.g., Web App, Redis, PostgreSQL). | **This is the core "High Level Design" (HLD).** You will spend 70% of the interview here. |
| **Level 3** | Components | Zooms into a single container to show its internal controllers and services. | Only used if the interviewer specifically asks you to "Deep Dive" into a complex service. |
| **Level 4** | Code | UML classes and code structures. | **Never draw this** unless explicitly asked in a low-level design interview. |

> [!TIP]
> **Teacher's Secret:** Never start drawing a Level 2 Container diagram until the interviewer explicitly agrees with your Level 1 Context diagram. "Before I break this down, does this high-level flow look correct to you?"

---

## UML class and sequence diagrams

### Sequence Diagrams
Sequence diagrams are incredibly powerful in System Design interviews. They do not show *where* things are; they show *when* things happen.

Think of a Sequence Diagram like a movie script. It reads top-to-bottom and shows the exact order of API calls between a Client, a Server, and a Database.

**When to use it:** Use sequence diagrams when discussing **Authentication (OAuth)**, **Payment Processing (Stripe)**, or any multi-step protocol where order and failure handling matter.

### UML Class Diagrams
Class diagrams show the static structure of the code (Objects, Attributes, Methods, and Inheritance).

> [!WARNING]
> **Beginner Mistake:** Do not draw UML Class diagrams in a standard System Design (Distributed Systems) interview! They are meant for Object-Oriented Design (OOD) interviews (e.g., "Design a Parking Lot"). If you start drawing UML classes when asked to "Design Twitter", you are answering the wrong question.

---

## Activity and state diagrams

### State Diagrams (State Machines)
A State Diagram shows all the possible states an object can be in and what triggers the change.

Think of an Uber Ride. It is not just "active" or "inactive".
- `Rider Searching` -> `Driver Assigned` -> `Driver Arriving` -> `Trip in Progress` -> `Trip Completed`.

**When to use it:** If you are designing Uber, an Order Processing system (Amazon), or a Job Scheduler, drawing a quick State Machine on the whiteboard instantly proves you understand the complex business logic edge cases.

### Activity Diagrams
These are essentially advanced flowcharts. They show conditional logic (If X happens, go here. If Y happens, go there). While useful, they are often too slow to draw in an interview setting. Stick to Sequence Diagrams for flow.

---

## Whiteboard layout strategy

The physical (or digital) layout of your whiteboard is just as important as the boxes you draw.

If you run out of space and start drawing arrows backwards across your own diagram, the interviewer will get confused and you will lose points.

### The "Left-to-Right" Rule
Always draw data flowing from **Left to Right**.
1. **Far Left:** The Clients (Mobile App, Web Browser, external sensors).
2. **Middle Left:** The Entry Points (Load Balancers, API Gateways, CDN).
3. **Middle Right:** The Application Logic (Microservices, Message Queues).
4. **Far Right:** The Data Layer (Databases, Caches, Object Storage).

### The "Top-to-Bottom" Rule (For Deep Dives)
Leave the bottom 30% of your whiteboard empty. When the interviewer asks you to deep-dive into a specific bottleneck (e.g., "How does the Newsfeed generation work?"), use that bottom space to draw a zoomed-in component diagram. Do not erase your main HLD!

> [!NOTE]
> **Pro-Tip:** If using an iPad or digital whiteboard (like Excalidraw), use color coding. Draw data flow arrows in **Green**, and failure/retry arrows in **Red**. This makes your diagram instantly readable without you having to explain every line.

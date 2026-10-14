# stack-website-nav

A modern, interactive computer science visualizer and educational engine demonstrating **Web Browser History Navigation** using the **Stack (LIFO - Last In, First Out)** data structure alongside **3 distinct architectural approaches**.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Flask-black.svg)](https://flask.palletsprojects.com/)
[![Data Structures](https://img.shields.io/badge/data_structures-Stack%20%7C%20DLL%20%7C%20Array-emerald.svg)](#2-the-3-architectural-approaches)
[![Frontend](https://img.shields.io/badge/frontend-Vanilla%20HTML5%20%2F%20CSS3%20%2F%20JS-orange.svg)](#4-web-visualizer-features)
[![Theme Support](https://img.shields.io/badge/theme-Light%20%26%20Dark%20Mode-violet.svg)](#4-web-visualizer-features)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 1. Problem Statement & Real-World Motivation

In modern web browsers (Chrome, Firefox, Safari, Edge), page history is fundamental to browsing. Every browser provides:
- **Back Button**: Returns to previously visited pages.
- **Forward Button**: Moves forward to pages from which the user previously moved back.
- **Visiting a New Page**: When a user navigates to a new page from an intermediate history state, the entire **forward history is permanently cleared / severed**.

### The Core LIFO Principle
A **Stack** follows the **Last In, First Out (LIFO)** principle: the most recently pushed item is always the first one popped. This precisely matches the behavior of the browser's Back button—the page you visited last is the page you return to first.

### The Canonical Demonstration Flow
The project demonstrates the definitive 7-step browser history sequence:

$$\text{Page A} \longrightarrow \text{Page B} \longrightarrow \text{Page C} \longrightarrow \text{Page D} \longrightarrow \text{Back} \longrightarrow \text{Back} \longrightarrow \text{Page E}$$

```
Step 1: Visit Page A  -->  Current: [Page A] | Back: []           | Forward: []
Step 2: Visit Page B  -->  Current: [Page B] | Back: [A]          | Forward: []
Step 3: Visit Page C  -->  Current: [Page C] | Back: [A, B]       | Forward: []
Step 4: Visit Page D  -->  Current: [Page D] | Back: [A, B, C]    | Forward: []
Step 5: Click Back    -->  Current: [Page C] | Back: [A, B]       | Forward: [D]
Step 6: Click Back    -->  Current: [Page B] | Back: [A]          | Forward: [D, C]
Step 7: Visit Page E  -->  Current: [Page E] | Back: [A, B]       | Forward: []  <-- CLEARED!
```

> **Critical LIFO Moment (Step 7)**:
> Visiting `Page E` pushes the current page (`Page B`) onto the Back Stack. Because a new branch of history has begun, the entire Forward Stack (`[Page D, Page C]`) is **completely discarded**.

---

## 2. The 3 Architectural Approaches

This project implements and compares **three architectural models** for browser history:

```
+-----------------------------------------------------------------------------------+
|                            THREE ARCHITECTURAL MODELS                             |
+-----------------------------------------------------------------------------------+
|  1. TWO STACKS (LIFO)      |  2. DOUBLY LINKED LIST    |  3. SINGLE DYNAMIC ARRAY |
|                            |                           |                          |
|  [Back Stack]  [Fwd Stack] |  [A] <==> [B] <==> [C]   |  [ A | B | C | D | E ]   |
|     |  ^          |  ^     |            ^              |            ^             |
|     v  |          v  |     |      (current_node)       |     (current_index = 1)  |
|    Push/Pop      Push/Pop  |                           |                          |
|                            |  Forward: current.next    |  Forward: slice array    |
|  Forward: .clear()         |  Sever: current.next=None |  history = history[:idx] |
+-----------------------------------------------------------------------------------+
```

### Approach 1: Two Stacks (Industry Standard / LIFO Focus)
- **Data Structure**: Two separate LIFO stacks: `back_stack` and `forward_stack`, plus a `current_page` variable.
- **Operations**:
  - `visit(url)`: Push `current_page` to `back_stack`, set `current_page = url`, clear `forward_stack` (`O(1)`).
  - `back()`: Push `current_page` to `forward_stack`, pop top from `back_stack` into `current_page` (`O(1)`).
  - `forward()`: Push `current_page` to `back_stack`, pop top from `forward_stack` into `current_page` (`O(1)`).
  - `peek()`: Inspect top of `back_stack` or `forward_stack` without removing (`O(1)`).
- **Pros**: Perfectly mirrors the conceptual model, minimal memory overhead, zero pointer chasing.

### Approach 2: Doubly Linked List with Pointer
- **Data Structure**: Bidirectional nodes with `prev`, `next`, and `data` pointers, tracked by a `current_node` reference.
- **Operations**:
  - `visit(url)`: Sever existing forward nodes by setting `current_node.next = None`, create a new node linked to `current_node`, and advance `current_node`. Orphaned nodes are automatically garbage collected.
  - `back()`: Move `current_node = current_node.prev` (`O(1)`).
  - `forward()`: Move `current_node = current_node.next` (`O(1)`).
- **Pros**: True non-contiguous list scaling; no reallocations or array copying when branching new history.

### Approach 3: Single Dynamic Array with Index Pointer
- **Data Structure**: A single Python list / dynamic array (`history`) with an integer pointer (`current_index`).
- **Operations**:
  - `visit(url)`: Truncate all elements past `current_index` via array slicing (`history = history[:current_index + 1]`), append `url`, and set `current_index = len(history) - 1`.
  - `back()`: Decrement `current_index -= 1` (`O(1)`).
  - `forward()`: Increment `current_index += 1` (`O(1)`).
- **Pros**: Direct random access ($O(1)$ by index), superior cache locality, zero pointer overhead.

---

## 3. Comprehensive Complexity & Comparison Matrix

| Feature / Metric | 1. Two Stacks (LIFO) | 2. Doubly Linked List | 3. Single Dynamic Array |
| :--- | :--- | :--- | :--- |
| **Primary Data Structure** | Two LIFO Stacks (`Array / List`) | Bidirectional Node Chain | Contiguous Array + Pointer |
| **Visit Page Time** | **$O(1)$** | **$O(1)$** | **$O(K)$** (slicing forward tranche) |
| **Back Button Time** | **$O(1)$** | **$O(1)$** | **$O(1)$** |
| **Forward Button Time** | **$O(1)$** | **$O(1)$** | **$O(1)$** |
| **Peek / Current Access** | **$O(1)$** | **$O(1)$** | **$O(1)$** |
| **Space Complexity** | **$O(N)$** | **$O(N)$** | **$O(N)$** |
| **Memory Overhead** | Low (two arrays) | High (`prev` + `next` pointers per node) | Minimal (contiguous array) |
| **Forward Severing Method** | `forward_stack.clear()` | `current_node.next = None` | `history = history[:current_index + 1]` |
| **Cache Locality** | High | Low (scattered heap nodes) | Maximum (contiguous memory) |
| **Random Access** | No (LIFO sequential only) | No (traversal required) | Yes ($O(1)$ arbitrary jumps) |
| **Ideal Real-World Use** | Embedded / standard browser engines | In-memory document revision histories | Tab session restoring & indexed history |

---

## 4. Web Visualizer Features

The web interface is engineered with a developer-grade design system:

- **Unified Side-by-Side Comparison**: View all 3 architectural models updating simultaneously in real time.
- **Top Navigation Bridge Bar**: Dedicated viewport showing current active page and directional pop flows (`Pop on Back` $\leftarrow$ `Current` $\rightarrow$ `Pop on Forward`).
- **High-Contrast Stack Visualizer**:
  - Numbered stack index pills (`#1`, `#2`, `#3`) showing stack depth.
  - High-contrast, bold typography preventing truncation or squishing.
  - Distinct `TOP` badges (Blue accent for Back Stack pop target, Rose accent for Forward Stack pop target).
- **Website History Carousel**: Horizontal tab strip showing chronological visits with manual scroll controls (`<` and `>`), maintaining clean page layouts without expanding the window.
- **Canonical Stepper Walkthrough**:
  - Interactive stepper for the canonical sequence: `A -> B -> C -> D -> Back -> Back -> E`.
  - Auto-Play mode with speed controls and explanatory step callouts.
- **Interactive Browser Mockup**: Working address bar with quick-visit chips (`Page A-E`, `google.com`, `github.com`), active tab, and dynamic Back/Forward enabled states.
- **Dark Mode & Light Mode**: Complete theme support with tailored HSL tokens and seamless CSS transitions.
- **Clean SVG Iconography**: Strict zero-emoji policy; uses crisp SVG icons throughout the interface.
- **Live Audit Log**: Real-time event log tracking every stack push, pop, severed node, and array slice.

---

## 5. Project Structure

```
stack-website-nav/
│
├── browser_engine.py      # Core data structures (TwoStacksBrowser, DoublyLinkedListBrowser, ArrayBrowser, Coordinator)
├── main.py                # Flask server, REST APIs, and CLI demo runner
├── test_engine.py         # Automated unit test suite verifying all 3 data structures
├── requirements.txt       # Project dependencies (Flask)
├── .gitignore             # Git ignore patterns for Python, virtual environments, and editors
├── README.md              # Comprehensive documentation and complexity reference
│
├── templates/
│   └── index.html         # Web visualizer markup with semantic layout
│
└── static/
    ├── css/
    │   └── style.css      # Design system, Light/Dark tokens, and responsive 2-column stack layout
    └── js/
        └── app.js         # Interactive DOM controller, stepper engine, and API synchronization
```

---

## 6. Getting Started

### Prerequisites
- **Python 3.8+** installed on your system.

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Aristo-A/stack-website-nav.git
   cd stack-website-nav
   ```

2. **(Optional) Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 7. How to Run

### Option A: Interactive Web Visualizer (Recommended)

Start the local Flask server:
```bash
python main.py
```

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

### Option B: Terminal CLI Walkthrough

Run the complete canonical walkthrough directly inside your terminal with color-coded table output:
```bash
python main.py --cli
```

### Option C: Automated Unit Tests

Execute the automated test suite verifying edge cases, LIFO properties, and the canonical demonstration flow:
```bash
python test_engine.py
```

Expected output:
```
All canonical flow assertions PASSED!
```

---

## 8. REST API Specification

The Flask server provides a clean JSON API for headless automation or frontend integration:

| Method | Endpoint | Description | Request Body |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/state` | Returns full synchronized state of all 3 engines | None |
| `POST` | `/api/action` | Executes a browser navigation action | `{"action": "visit", "url": "Page A"}` <br> `{"action": "back"}` <br> `{"action": "forward"}` <br> `{"action": "reset"}` |
| `GET` | `/api/demo_steps` | Returns array of predefined canonical walkthrough steps | None |
| `POST` | `/api/demo/step` | Advances to a specific step in the canonical demo | `{"step_index": 0}` |

---

## 9. License

This project is licensed under the [MIT License](LICENSE).

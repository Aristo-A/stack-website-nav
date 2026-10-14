"""
Browser Navigation Data Structures
-----------------------------------
Implements 3 core approaches for browser navigation history:
1. Two Stacks (Back Stack + Forward Stack)
2. Doubly Linked List + Pointer
3. Single Dynamic Array + Index Pointer

Demonstrates Stack LIFO operations (Push, Pop, Peek) and time/space complexity.
"""

from typing import Dict, Any, List, Optional


# ==============================================================================
# Approach 1: Two Stacks (Array/List based)
# ==============================================================================
class TwoStacksBrowser:
    """
    Browser history navigation implemented using two stacks:
    - back_stack: stores pages visited before the current page (LIFO)
    - forward_stack: stores pages ahead after pressing Back (LIFO)
    - current_page: currently active web page
    """
    def __init__(self, initial_page: Optional[str] = None):
        self.back_stack: List[str] = []
        self.forward_stack: List[str] = []
        self.current_page: Optional[str] = initial_page
        self.last_operation: str = "Initialized"
        self.operation_details: str = f"Started with {'empty page' if not initial_page else initial_page}"

    def visit(self, url: str) -> Dict[str, Any]:
        """
        Visits a new page:
        1. Push current page to back_stack (if current_page exists).
        2. Set current_page to new url.
        3. Clear forward_stack completely (cannot go forward after visiting new page).
        Time Complexity: O(1) push, O(K) or O(1) clear where K = forward history
        Space Complexity: O(1) additional per visit
        """
        cleared_count = len(self.forward_stack)
        if self.current_page is not None:
            self.back_stack.append(self.current_page)  # Push to Back Stack
        
        self.current_page = url
        self.forward_stack.clear()  # Forward history is cleared!
        
        self.last_operation = "VISIT"
        self.operation_details = (
            f"PUSH '{self.back_stack[-1] if self.back_stack else 'None'}' to Back Stack. "
            f"Set current page to '{url}'. "
            f"CLEARED Forward Stack ({cleared_count} pages removed)."
        )
        return self.get_state()

    def back(self) -> Dict[str, Any]:
        """
        Navigates back:
        1. Push current page to forward_stack.
        2. Pop top page from back_stack and make it current_page.
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if not self.can_go_back():
            self.last_operation = "BACK (FAILED)"
            self.operation_details = "Back Stack is empty! Cannot go back."
            return self.get_state()

        # Push current to forward stack
        if self.current_page is not None:
            self.forward_stack.append(self.current_page)
        
        # Pop top from back stack
        previous_page = self.back_stack.pop()
        self.current_page = previous_page

        self.last_operation = "BACK"
        self.operation_details = (
            f"PUSH '{self.forward_stack[-1]}' to Forward Stack. "
            f"POP '{previous_page}' from Back Stack to Current Page."
        )
        return self.get_state()

    def forward(self) -> Dict[str, Any]:
        """
        Navigates forward:
        1. Push current page to back_stack.
        2. Pop top page from forward_stack and make it current_page.
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if not self.can_go_forward():
            self.last_operation = "FORWARD (FAILED)"
            self.operation_details = "Forward Stack is empty! Cannot go forward."
            return self.get_state()

        if self.current_page is not None:
            self.back_stack.append(self.current_page)

        next_page = self.forward_stack.pop()
        self.current_page = next_page

        self.last_operation = "FORWARD"
        self.operation_details = (
            f"PUSH '{self.back_stack[-1]}' to Back Stack. "
            f"POP '{next_page}' from Forward Stack to Current Page."
        )
        return self.get_state()

    def peek_back(self) -> Optional[str]:
        """Peek top of back stack without removing it."""
        return self.back_stack[-1] if self.back_stack else None

    def peek_forward(self) -> Optional[str]:
        """Peek top of forward stack without removing it."""
        return self.forward_stack[-1] if self.forward_stack else None

    def can_go_back(self) -> bool:
        return len(self.back_stack) > 0

    def can_go_forward(self) -> bool:
        return len(self.forward_stack) > 0

    def reset(self):
        self.back_stack.clear()
        self.forward_stack.clear()
        self.current_page = None
        self.last_operation = "RESET"
        self.operation_details = "All stacks cleared and state reset."

    def get_state(self) -> Dict[str, Any]:
        return {
            "approach": "Two Stacks",
            "current_page": self.current_page,
            "back_stack": list(self.back_stack),
            "forward_stack": list(self.forward_stack),
            "can_back": self.can_go_back(),
            "can_forward": self.can_go_forward(),
            "peek_back": self.peek_back(),
            "peek_forward": self.peek_forward(),
            "back_count": len(self.back_stack),
            "forward_count": len(self.forward_stack),
            "last_operation": self.last_operation,
            "operation_details": self.operation_details,
            "complexity": {
                "time": "O(1) Push/Pop/Peek",
                "space": "O(N) Total history items"
            }
        }


# ==============================================================================
# Approach 2: Doubly Linked List + Pointer
# ==============================================================================
class DLLNode:
    """Node in Doubly Linked List representing a visited page."""
    def __init__(self, url: str):
        self.url: str = url
        self.prev: Optional['DLLNode'] = None
        self.next: Optional['DLLNode'] = None

    def to_dict(self, is_current: bool = False) -> Dict[str, Any]:
        return {
            "url": self.url,
            "has_prev": self.prev is not None,
            "has_next": self.next is not None,
            "prev_url": self.prev.url if self.prev else None,
            "next_url": self.next.url if self.next else None,
            "is_current": is_current
        }


class DoublyLinkedListBrowser:
    """
    Browser history navigation implemented using a Doubly Linked List:
    - current_node: pointer to the active node in the list
    - head: first page visited
    """
    def __init__(self, initial_page: Optional[str] = None):
        self.head: Optional[DLLNode] = None
        self.current_node: Optional[DLLNode] = None
        self.last_operation: str = "Initialized"
        self.operation_details: str = f"Started with {'empty page' if not initial_page else initial_page}"
        if initial_page:
            self.visit(initial_page)

    def visit(self, url: str) -> Dict[str, Any]:
        """
        Visits a new page:
        1. Create new DLLNode(url).
        2. Sever link to current_node.next (any existing forward nodes are pruned).
        3. Link current_node.next = new_node, new_node.prev = current_node.
        4. Advance current_node pointer to new_node.
        Time Complexity: O(1)
        Space Complexity: O(1) new node allocation
        """
        new_node = DLLNode(url)
        severed_count = 0

        if self.current_node is None:
            self.head = new_node
            self.current_node = new_node
            self.last_operation = "VISIT (HEAD)"
            self.operation_details = f"Created root HEAD node '{url}'."
        else:
            # Count severed forward nodes
            temp = self.current_node.next
            while temp:
                severed_count += 1
                temp = temp.next

            # Sever forward link & attach new node
            if self.current_node.next:
                self.current_node.next.prev = None  # Detach forward chain
            
            self.current_node.next = new_node
            new_node.prev = self.current_node
            self.current_node = new_node

            self.last_operation = "VISIT"
            self.operation_details = (
                f"Severed {severed_count} forward node(s). "
                f"Linked '{new_node.prev.url}' <--> '{new_node.url}'. "
                f"Advanced current pointer to '{url}'."
            )

        return self.get_state()

    def back(self) -> Dict[str, Any]:
        """
        Navigates back:
        1. Shift current_node = current_node.prev.
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if not self.can_go_back():
            self.last_operation = "BACK (FAILED)"
            self.operation_details = "Cannot go back: current_node.prev is None (at Head)."
            return self.get_state()

        prev_url = self.current_node.url
        self.current_node = self.current_node.prev
        self.last_operation = "BACK"
        self.operation_details = f"Shifted pointer backward: '{prev_url}' <-- '{self.current_node.url}'"
        return self.get_state()

    def forward(self) -> Dict[str, Any]:
        """
        Navigates forward:
        1. Shift current_node = current_node.next.
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if not self.can_go_forward():
            self.last_operation = "FORWARD (FAILED)"
            self.operation_details = "Cannot go forward: current_node.next is None (at Tail)."
            return self.get_state()

        prev_url = self.current_node.url
        self.current_node = self.current_node.next
        self.last_operation = "FORWARD"
        self.operation_details = f"Shifted pointer forward: '{prev_url}' --> '{self.current_node.url}'"
        return self.get_state()

    def can_go_back(self) -> bool:
        return self.current_node is not None and self.current_node.prev is not None

    def can_go_forward(self) -> bool:
        return self.current_node is not None and self.current_node.next is not None

    def reset(self):
        self.head = None
        self.current_node = None
        self.last_operation = "RESET"
        self.operation_details = "Doubly Linked List cleared."

    def get_nodes_list(self) -> List[Dict[str, Any]]:
        nodes = []
        curr = self.head
        while curr:
            is_curr = (curr == self.current_node)
            nodes.append(curr.to_dict(is_current=is_curr))
            curr = curr.next
        return nodes

    def get_state(self) -> Dict[str, Any]:
        nodes = self.get_nodes_list()
        current_url = self.current_node.url if self.current_node else None
        
        # Calculate back and forward elements for equivalent comparison
        back_items = []
        forward_items = []
        found_curr = False
        for n in nodes:
            if n["url"] == current_url and n["is_current"]:
                found_curr = True
                continue
            if not found_curr:
                back_items.append(n["url"])
            else:
                forward_items.append(n["url"])

        return {
            "approach": "Doubly Linked List",
            "current_page": current_url,
            "nodes": nodes,
            "back_stack": back_items,  # Equivalent representation
            "forward_stack": forward_items,  # Equivalent representation
            "can_back": self.can_go_back(),
            "can_forward": self.can_go_forward(),
            "last_operation": self.last_operation,
            "operation_details": self.operation_details,
            "complexity": {
                "time": "O(1) Step Traversal & Insertion",
                "space": "O(N) (prev + next pointer overhead)"
            }
        }


# ==============================================================================
# Approach 3: Single Dynamic Array + Index Pointer
# ==============================================================================
class ArrayBrowser:
    """
    Browser history navigation implemented using a Single Dynamic Array:
    - history: list of strings [url0, url1, url2...]
    - current_index: pointer index to the active page
    """
    def __init__(self, initial_page: Optional[str] = None):
        self.history: List[str] = []
        self.current_index: int = -1
        self.last_operation: str = "Initialized"
        self.operation_details: str = f"Started with {'empty page' if not initial_page else initial_page}"
        if initial_page:
            self.visit(initial_page)

    def visit(self, url: str) -> Dict[str, Any]:
        """
        Visits a new page:
        1. Truncate array history up to current_index: history = history[:current_index + 1]
        2. Append new url: history.append(url)
        3. current_index += 1
        Time Complexity: O(K) slice where K = pruned forward items, amortized O(1) append
        Space Complexity: O(1) contiguous memory
        """
        prior_len = len(self.history)
        if self.current_index >= 0:
            # Prune forward entries
            self.history = self.history[:self.current_index + 1]
        else:
            self.history = []

        severed_count = prior_len - len(self.history)
        self.history.append(url)
        self.current_index = len(self.history) - 1

        self.last_operation = "VISIT"
        self.operation_details = (
            f"Truncated {severed_count} forward element(s). "
            f"Appended '{url}' at index [{self.current_index}]."
        )
        return self.get_state()

    def back(self) -> Dict[str, Any]:
        """
        Navigates back:
        1. Decrement current_index by 1.
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if not self.can_go_back():
            self.last_operation = "BACK (FAILED)"
            self.operation_details = "Cannot go back: current_index is at 0 (first element)."
            return self.get_state()

        self.current_index -= 1
        self.last_operation = "BACK"
        self.operation_details = f"Decremented index to [{self.current_index}] -> '{self.history[self.current_index]}'"
        return self.get_state()

    def forward(self) -> Dict[str, Any]:
        """
        Navigates forward:
        1. Increment current_index by 1.
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if not self.can_go_forward():
            self.last_operation = "FORWARD (FAILED)"
            self.operation_details = "Cannot go forward: current_index is at history end."
            return self.get_state()

        self.current_index += 1
        self.last_operation = "FORWARD"
        self.operation_details = f"Incremented index to [{self.current_index}] -> '{self.history[self.current_index]}'"
        return self.get_state()

    def can_go_back(self) -> bool:
        return self.current_index > 0

    def can_go_forward(self) -> bool:
        return self.current_index >= 0 and self.current_index < len(self.history) - 1

    def reset(self):
        self.history.clear()
        self.current_index = -1
        self.last_operation = "RESET"
        self.operation_details = "Dynamic Array history cleared."

    def get_state(self) -> Dict[str, Any]:
        curr_page = self.history[self.current_index] if (0 <= self.current_index < len(self.history)) else None
        back_items = self.history[:self.current_index] if self.current_index > 0 else []
        forward_items = self.history[self.current_index + 1:] if (0 <= self.current_index < len(self.history) - 1) else []

        return {
            "approach": "Single Dynamic Array",
            "current_page": curr_page,
            "history_array": list(self.history),
            "current_index": self.current_index,
            "back_stack": back_items,
            "forward_stack": forward_items,
            "can_back": self.can_go_back(),
            "can_forward": self.can_go_forward(),
            "last_operation": self.last_operation,
            "operation_details": self.operation_details,
            "complexity": {
                "time": "O(1) Index Move, O(K) Slice on Visit",
                "space": "O(N) Contiguous memory"
            }
        }


# ==============================================================================
# Unified Coordinator (Synchronizes all 3 approaches together)
# ==============================================================================
class BrowserNavigationCoordinator:
    """Coordinates all three approaches simultaneously for direct comparison."""
    def __init__(self):
        self.two_stacks = TwoStacksBrowser()
        self.doubly_linked_list = DoublyLinkedListBrowser()
        self.dynamic_array = ArrayBrowser()
        self.history_log: List[Dict[str, Any]] = []

    def perform_action(self, action: str, url: Optional[str] = None) -> Dict[str, Any]:
        action = action.lower()
        if action == "visit" and url:
            s1 = self.two_stacks.visit(url)
            s2 = self.doubly_linked_list.visit(url)
            s3 = self.dynamic_array.visit(url)
            log_entry = {
                "action": "VISIT",
                "param": url,
                "summary": f"Visited page '{url}'"
            }
        elif action == "back":
            s1 = self.two_stacks.back()
            s2 = self.doubly_linked_list.back()
            s3 = self.dynamic_array.back()
            log_entry = {
                "action": "BACK",
                "param": None,
                "summary": f"Clicked Back button (to '{s1['current_page']}')"
            }
        elif action == "forward":
            s1 = self.two_stacks.forward()
            s2 = self.doubly_linked_list.forward()
            s3 = self.dynamic_array.forward()
            log_entry = {
                "action": "FORWARD",
                "param": None,
                "summary": f"Clicked Forward button (to '{s1['current_page']}')"
            }
        elif action == "reset":
            self.two_stacks.reset()
            self.doubly_linked_list.reset()
            self.dynamic_array.reset()
            self.history_log.clear()
            return self.get_full_state()
        else:
            raise ValueError(f"Unknown action: {action}")

        self.history_log.append(log_entry)
        return self.get_full_state()

    def get_full_state(self) -> Dict[str, Any]:
        return {
            "two_stacks": self.two_stacks.get_state(),
            "doubly_linked_list": self.doubly_linked_list.get_state(),
            "dynamic_array": self.dynamic_array.get_state(),
            "history_log": list(self.history_log),
            "current_page": self.two_stacks.current_page
        }

    def run_canonical_demo(self) -> List[Dict[str, Any]]:
        """
        Runs the canonical demo flow:
        A -> B -> C -> D -> Back -> Back -> E
        Returns sequence of states at each step.
        """
        self.perform_action("reset")
        steps = [
            ("visit", "Page A"),
            ("visit", "Page B"),
            ("visit", "Page C"),
            ("visit", "Page D"),
            ("back", None),
            ("back", None),
            ("visit", "Page E")
        ]
        results = []
        for act, param in steps:
            state = self.perform_action(act, param)
            results.append({
                "step": f"{act.upper()} {param or ''}".strip(),
                "state": state
            })
        return results

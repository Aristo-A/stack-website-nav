"""
Unit tests to verify equivalence of all 3 browser navigation approaches.
Flow: A -> B -> C -> D -> Back -> Back -> E
"""

from browser_engine import BrowserNavigationCoordinator, TwoStacksBrowser, DoublyLinkedListBrowser, ArrayBrowser


def test_canonical_flow():
    coord = BrowserNavigationCoordinator()
    
    # 1. Visit A
    coord.perform_action("visit", "A")
    state = coord.get_full_state()
    assert state["two_stacks"]["current_page"] == "A"
    assert state["two_stacks"]["back_stack"] == []
    assert state["two_stacks"]["forward_stack"] == []
    assert state["doubly_linked_list"]["current_page"] == "A"
    assert state["dynamic_array"]["current_page"] == "A"

    # 2. Visit B
    coord.perform_action("visit", "B")
    state = coord.get_full_state()
    assert state["two_stacks"]["current_page"] == "B"
    assert state["two_stacks"]["back_stack"] == ["A"]
    assert state["doubly_linked_list"]["current_page"] == "B"
    assert state["dynamic_array"]["current_page"] == "B"

    # 3. Visit C
    coord.perform_action("visit", "C")
    state = coord.get_full_state()
    assert state["two_stacks"]["current_page"] == "C"
    assert state["two_stacks"]["back_stack"] == ["A", "B"]

    # 4. Visit D
    coord.perform_action("visit", "D")
    state = coord.get_full_state()
    assert state["two_stacks"]["current_page"] == "D"
    assert state["two_stacks"]["back_stack"] == ["A", "B", "C"]
    assert state["two_stacks"]["forward_stack"] == []

    # 5. Back 1 (to C)
    coord.perform_action("back")
    state = coord.get_full_state()
    assert state["two_stacks"]["current_page"] == "C"
    assert state["two_stacks"]["back_stack"] == ["A", "B"]
    assert state["two_stacks"]["forward_stack"] == ["D"]
    assert state["doubly_linked_list"]["current_page"] == "C"
    assert state["dynamic_array"]["current_page"] == "C"

    # 6. Back 2 (to B)
    coord.perform_action("back")
    state = coord.get_full_state()
    assert state["two_stacks"]["current_page"] == "B"
    assert state["two_stacks"]["back_stack"] == ["A"]
    assert state["two_stacks"]["forward_stack"] == ["D", "C"]
    assert state["doubly_linked_list"]["current_page"] == "B"
    assert state["dynamic_array"]["current_page"] == "B"

    # 7. Visit E (Forward stack must be CLEARED!)
    coord.perform_action("visit", "E")
    state = coord.get_full_state()
    assert state["two_stacks"]["current_page"] == "E"
    assert state["two_stacks"]["back_stack"] == ["A", "B"]
    assert state["two_stacks"]["forward_stack"] == []
    assert state["doubly_linked_list"]["current_page"] == "E"
    assert [n["url"] for n in state["doubly_linked_list"]["nodes"]] == ["A", "B", "E"]
    assert state["dynamic_array"]["current_page"] == "E"
    assert state["dynamic_array"]["history_array"] == ["A", "B", "E"]
    assert state["dynamic_array"]["current_index"] == 2

    print("All canonical flow assertions PASSED!")


if __name__ == "__main__":
    test_canonical_flow()

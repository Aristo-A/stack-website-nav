"""
Browser Navigation History Simulator & Visualizer
==================================================
Demonstrates Stack Data Structure (LIFO) and 3 core approaches:
1. Two Stacks (Back Stack + Forward Stack)
2. Doubly Linked List + Pointer
3. Single Dynamic Array + Index Pointer

Supports both Web Visualizer (Flask server) and CLI demo.
"""

import sys
import argparse
import mimetypes
from flask import Flask, render_template, jsonify, request
from browser_engine import BrowserNavigationCoordinator

# Fix Windows Registry issue where .css MIME type is mistakenly set to 'text/plain'
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('application/javascript', '.js')

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
coordinator = BrowserNavigationCoordinator()

# Canonical demo steps definition with pedagogical explanations
DEMO_STEPS = [
    {
        "step_num": 1,
        "action": "visit",
        "url": "Page A",
        "description": "Visit initial page A",
        "explanation": "Page A becomes the current active page. Back stack is empty since no prior history exists."
    },
    {
        "step_num": 2,
        "action": "visit",
        "url": "Page B",
        "description": "Visit page B",
        "explanation": "Page A is PUSHED onto the Back Stack. Current page becomes B. Forward stack remains empty."
    },
    {
        "step_num": 3,
        "action": "visit",
        "url": "Page C",
        "description": "Visit page C",
        "explanation": "Page B is PUSHED onto the Back Stack [A, B]. Current page becomes C."
    },
    {
        "step_num": 4,
        "action": "visit",
        "url": "Page D",
        "description": "Visit page D",
        "explanation": "Page C is PUSHED onto the Back Stack [A, B, C]. Current page is now D (deepest page visited)."
    },
    {
        "step_num": 5,
        "action": "back",
        "url": None,
        "description": "Click Back (1st time)",
        "explanation": "Current page D is PUSHED to Forward Stack [D]. Page C is POPPED from Back Stack and becomes current."
    },
    {
        "step_num": 6,
        "action": "back",
        "url": None,
        "description": "Click Back (2nd time)",
        "explanation": "Current page C is PUSHED to Forward Stack [D, C]. Page B is POPPED from Back Stack [A] and becomes current."
    },
    {
        "step_num": 7,
        "action": "visit",
        "url": "Page E",
        "description": "Visit NEW page E",
        "explanation": "CRITICAL LIFO MOMENT: Current page B is pushed to Back Stack [A, B]. Page E becomes current. The Forward Stack [D, C] is COMPLETELY CLEARED/SEVERED!"
    }
]

demo_current_step_index = 0


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/state", methods=["GET"])
def get_state():
    return jsonify(coordinator.get_full_state())


@app.route("/api/action", methods=["POST"])
def perform_action():
    data = request.get_json() or {}
    action = data.get("action", "")
    url = data.get("url", None)
    
    try:
        new_state = coordinator.perform_action(action, url)
        return jsonify({
            "success": True,
            "state": new_state
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400


@app.route("/api/demo_steps", methods=["GET"])
def get_demo_steps():
    return jsonify({
        "steps": DEMO_STEPS,
        "current_step_index": demo_current_step_index
    })


@app.route("/api/demo/step", methods=["POST"])
def step_demo():
    global demo_current_step_index
    data = request.get_json() or {}
    direction = data.get("direction", "next")  # "next", "prev", or "reset"

    if direction == "reset":
        demo_current_step_index = 0
        coordinator.perform_action("reset")
        return jsonify({
            "step_index": 0,
            "completed": False,
            "state": coordinator.get_full_state()
        })

    if direction == "next":
        if demo_current_step_index >= len(DEMO_STEPS):
            return jsonify({
                "step_index": demo_current_step_index,
                "completed": True,
                "state": coordinator.get_full_state()
            })
        
        step_info = DEMO_STEPS[demo_current_step_index]
        coordinator.perform_action(step_info["action"], step_info["url"])
        demo_current_step_index += 1
        
        return jsonify({
            "step_index": demo_current_step_index,
            "last_step": step_info,
            "completed": demo_current_step_index >= len(DEMO_STEPS),
            "state": coordinator.get_full_state()
        })

    return jsonify({"error": "Invalid direction"}), 400


def run_cli_demo():
    """Print an interactive ASCII walkthrough in the terminal."""
    cli_coord = BrowserNavigationCoordinator()
    print("=" * 80)
    print("BROWSER NAVIGATION SIMULATOR - STACK (LIFO) DEMO")
    print("Canonical Flow: A -> B -> C -> D -> Back -> Back -> E")
    print("=" * 80)

    for step in DEMO_STEPS:
        print(f"\n>>> STEP {step['step_num']}: {step['description']}")
        print(f"Explanation: {step['explanation']}")
        cli_coord.perform_action(step["action"], step["url"])
        state = cli_coord.get_full_state()
        
        ts = state["two_stacks"]
        dll = state["doubly_linked_list"]
        arr = state["dynamic_array"]

        print(f"  [1. Two Stacks]         Back: {ts['back_stack']} | Current: [{ts['current_page']}] | Forward: {ts['forward_stack']}")
        print(f"  [2. Doubly Linked List] Nodes: {[n['url'] for n in dll['nodes']]} | Current: [{dll['current_page']}]")
        print(f"  [3. Dynamic Array]      Array: {arr['history_array']} | Index: {arr['current_index']} ('{arr['current_page']}')")
        print("-" * 80)

    print("\nDEMO COMPLETED!")
    print("Summary of Complexity:")
    print("1. Two Stacks:          Time: O(1) ops        | Space: O(N)")
    print("2. Doubly Linked List:  Time: O(1) ops        | Space: O(N)")
    print("3. Dynamic Array:       Time: O(1) move/O(K) | Space: O(N)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Browser Navigation Simulator")
    parser.add_argument("--cli", action="store_true", help="Run demonstration in terminal CLI mode")
    parser.add_argument("--port", type=int, default=5000, help="Port to run Flask web visualizer")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host interface")
    args = parser.parse_args()

    if args.cli:
        run_cli_demo()
    else:
        print(f"Starting Browser Navigation Web Visualizer at http://{args.host}:{args.port}")
        app.run(host=args.host, port=args.port, debug=False)

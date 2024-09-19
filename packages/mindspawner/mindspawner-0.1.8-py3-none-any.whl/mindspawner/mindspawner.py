import socketio
import numpy as np
import json

class MindSpawner:
    def __init__(self, user_id, agent_id=None):
        self.sio = socketio.Client()
        self.user_id = user_id
        self.agent_id = agent_id
        self.server_url = 'https://mindspawner-90819a099a6f.herokuapp.com/'
        self.last_data = {
            'input': None,
            'output': None,
            'evaluation': None
        }
        self.output_flag = 0  # New flag to track how long we waited for fresh output
        self.wait_for_output = True  # Option to either wait for fresh output or use old output
        self.received_first_output = False  # Track if the first output has been received

        # Event handler for connecting to the server
        @self.sio.event
        def connect():
            print("[P2A library] Connected to the MindSpawner server")

        # Event handler for disconnecting from the server
        @self.sio.event
        def disconnect():
            print("[P2A library] Disconnected from the MindSpawner server")

        # Event handler for receiving agent response
        @self.sio.on('response')
        def on_response(data):
            print(f"Received data: {data}")  # Log the full response for debugging
            if data['type'] == 'getOutput':
                if data['flag'] == 'success':
                    print(f"Successful response: {data}")
                    if isinstance(data['action'], str):
                        try:
                            data['action'] = json.loads(data['action'])  # Deserialize the string action
                        except json.JSONDecodeError as e:
                            print(f"Error parsing action: {e}")
                            data['action'] = None
                    self.last_data['output'] = data['action']
                    self.output_flag = 0  # Reset flag when new output is received
                    self.received_first_output = True  # Set flag that first output is received
                    print(f"Received action from agent: {data['action']}")
                else:
                    print(f"Error or system error in response: {data}")

    def connect(self):
        """Connects to the MindSpawner server."""
        self.sio.connect(self.server_url, wait_timeout=5)

    def disconnect(self):
        """Disconnects from the server."""
        self.sio.disconnect()

    def specify_agent(self, agent_id):
        """Specify the agent by ID."""
        self.agent_id = agent_id
        print(f"[P2A library] Agent ID set to: {self.agent_id}")

    def get_agent_action(self, input_data):
        """Send state input to the agent and get action output."""
        
        # Helper function to convert ndarray to list
        def convert_to_serializable(data):
            if isinstance(data, np.ndarray):
                return data.tolist()  # Convert ndarray to list
            elif isinstance(data, dict):
                # Recursively convert nested dicts
                return {key: convert_to_serializable(value) for key, value in data.items()}
            elif isinstance(data, list):
                # Recursively convert lists
                return [convert_to_serializable(item) for item in data]
            else:
                return data

        # Convert input_data to be JSON serializable (convert ndarrays)
        input_data = convert_to_serializable(input_data)

        if self.agent_id:
            # Reset output to ensure we wait for a fresh response
            self.last_data['output'] = None

            # Convert Python input to a string compatible with Node.js/JavaScript
            converted_input = self.convert_python_input(input_data)

            self.last_data['input'] = converted_input

            self.sio.emit('agent', {
                'type': 'getOutput',
                'input': converted_input,
                'auth': {
                    'userId': self.user_id,
                    'agentId': self.agent_id
                }
            })

            waited = 0

            # Ensure we wait for the first output, regardless of wait_for_output value
            while not self.received_first_output:
                self.sio.sleep(0.01)
                self.output_flag += 1

            # After the first output, decide based on the wait_for_output setting
            if self.wait_for_output:
                # Wait for fresh output for each action request
                while self.last_data['output'] is None:
                    self.sio.sleep(0.01)
                    self.output_flag += 1
            else:
                # Skip waiting if not waiting for each fresh output after the first
                print(f"Using old output after first action")

            # Log how long we waited for new output
            print(f"Waited {self.output_flag} iterations for new output.")

            # Return only the output, not the flag
            return self.last_data['output']
        else:
            print("[P2A library] Agent ID is not set.")
            return None

    def convert_python_input(self, input_data):
        """Convert Python input to a format that Node.js/JavaScript can understand."""
        try:
            # First, serialize the Python input to JSON
            json_input = json.dumps(input_data)

            # Replace Python-specific values with their JavaScript equivalents
            # 'True' -> 'true', 'False' -> 'false', 'None' -> 'null'
            json_input = json_input.replace("True", "true").replace("False", "false").replace("None", "null")

            return json_input
        except Exception as e:
            print(f"[P2A library] Error converting input data: {e}")
            return None

    def send_evaluation(self, evaluation_score):
        """Send the evaluation of the agent's performance."""
        if self.agent_id:
            self.last_data['evaluation'] = evaluation_score
            self.sio.emit('agent', {
                'type': 'logPerformanceData',
                'input': self.last_data['input'],
                'output': self.last_data['output'],
                'evaluation': evaluation_score,
                'auth': {
                    'userId': self.user_id,
                    'agentId': self.agent_id
                }
            })
            print(f"[P2A library] Sent evaluation: {evaluation_score}")
        else:
            print("[P2A library] Agent ID is not set.")

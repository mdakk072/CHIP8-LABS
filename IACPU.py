import torch
import torch.nn as nn
import torch.optim as optim
from CPU import CPU
from Keypad import Keypad
from Display import Display
import pandas as pd

class IACPU(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(17, 17)
        self.fc2 = nn.Linear(17, 11)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

net = IACPU()
display=Display()
keypad=Keypad(display=display)
cpu=CPU(display,keypad)
cpu.load_random_rom()
optimizer = optim.SGD(net.parameters(), lr=0.01)
criterion = nn.MSELoss()

for epoch in range(1000):
    input_state=cpu.get_state()
    cpu.cycle() # générer des données d'entrée avec votre classe CPU
    output_state=cpu.get_state()

    # Convertir les états en tenseurs PyTorch
    v_input = input_state['V']
    v_output = output_state['V']
    stack_input = input_state['stack']
    stack_output = output_state['stack']
    keys_input = input_state['pressed_keys']
    keys_output = output_state['pressed_keys']
    # Convertir les états en tenseurs PyTorch
    max_list_len = 10
    input_list = input_state['V'] + [input_state['I']] + input_state['pressed_keys'] + [0] * (max_list_len - len(input_state['stack'])) + input_state['stack'] + [0] * (max_list_len - len(input_state['pressed_keys']))
    output_list = output_state['V'] + [output_state['I']] + output_state['pressed_keys'] + [0] * (max_list_len - len(output_state['stack'])) + output_state['stack'] + [0] * (max_list_len - len(output_state['pressed_keys']))
    input_tensor = torch.tensor(input_list, dtype=torch.float32)
    df = pd.DataFrame(input_state)

    output_tensor = torch.tensor(output_list, dtype=torch.float32)

    


    optimizer.zero_grad()
    net_output = net(input_tensor)
    loss = criterion(net_output, output_tensor)
    loss.backward()
    optimizer.step()

    if epoch % 100 == 0:
        print(f"Epoch {epoch}: Loss = {loss.item()}")

# Test final
input_data = cpu.generate_input_data()
v_input = input_data['V']
keys_input = input_data['pressed_keys']
stack_input = input_data['stack']
input_tensor = torch.cat((torch.tensor(v_input, dtype=torch.float32), 
                          torch.tensor([input_data['I']], dtype=torch.float32), 
                          torch.tensor(keys_input, dtype=torch.float32), 
                          torch.tensor(stack_input, dtype=torch.float32)), dim=0)
output_tensor = net(input_tensor)
predicted_output = output_tensor.detach().numpy()

# Mettre les sorties prédites dans votre CPU
v_output = predicted_output[:16]
I_output = predicted_output[16]
keys_output = predicted_output[17:26]
stack_output = predicted_output[26:]
#cpu.set_state({'V': v_output, 'I': I_output, 'pressed_keys': keys_output, 'stack': stack_output})

# Afficher l'état de sortie prédit sous forme de dataframe pandas
df = pd.DataFrame(cpu.get_state())
print(df)

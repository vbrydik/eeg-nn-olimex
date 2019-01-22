# eeg_nn_olimex

EEG signals recognition system using neural networks for Olimex EEG SMT.
The neural network though is restricted to have only 3 layers (no more, no less).

Tested on Windows.

## Usage

A simple example on how to use it (or type 'help' in a program):

   	collectdata - collects data from serial port and creates a dataset:
      collectdata [profile] [dataset_name] [num_of_samples]
    
      train - trains a model on chosen datasets:
      train [profile] [model_name] [num_of_sets] [[dataset], [...], ...]
    
      predict - reads data from serial port and predicts according to a model:
      predict [profile] [model_name]
    
      print_models - prints profiles models:
      print_models [profile]
    
      print_datasets - prints profiles datasets:
      print_datasets [profile]
    
      print_config - prints out a config file:
      print_config
    
      set_port - choosing serial port from which to read:
      set_port [port]
    
      set_rate - sets baud rate of a serial port:
      set_rate [rate]
    
      set_epochs - sets neural networks epochs number (while training)
      set_epochs [n]
    
      set_layer - sets neural networks [n]umber of neurons on a [l]ayer
      set_layer [l] [n]
    
      set_batchsize - sets neural networks batch size
      set_batchsize [n]
    
# Config

Config file is divided into two groups: 

* NeuralNetworkData:
   - batch_size
   - epochs       
   - hl1_neurons  *- number of neurons in first hidden layer*
   - hl2_neurons  *- number of neurons in second hidden layer*
   - hl3_neurons  *- number of neurons in third hidden layer*
   - inputs       *- number of inputs neural network exects (or just input neurons)*
   
Note: number of *inputs* is decided by (number_of_channels_on_a_helmet * 10)

* SerialData:
   - port
   - baud_rate
   - data_len     *- number of channels*
 

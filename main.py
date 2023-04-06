import matplotlib.pyplot as plt
import matplotlib.animation as animation
import snap7
import logging
import csv
import datetime

# configura o logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# cria uma figura e um eixo
fig, ax = plt.subplots()

# inicializa o gráfico com alguns dados aleatórios
x = []
y = []
line, = ax.plot(x, y)

# endereço IP do CLP S7-1200
plc = snap7.client.Client()
plc.connect('192.168.0.20', 0, 1)

# update dos dados do CLP
def update_data():
    try:
        db_number = 11
        start_address = 0
        data_type = snap7.types.S7WLReal
        byte_count = 4
        data = plc.read_area(snap7.types.Areas.DB, db_number, start_address, byte_count)
        value = snap7.util.get_real(data, 0)
        logging.info(f'Valor lido: {value}')
        return value
    except Exception as e:
        logging.error(f'Erro ao atualizar dados do PLC: {e}')
    
# cria um arquivo CSV para registrar os valores lidos
with open('valores.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['data', 'hora', 'valor'])

    # função de atualização do gráfico
    def update(data):
        try:
            value = update_data()
            now = datetime.datetime.now()
            writer.writerow([now.date(), now.time(), value])
            # adiciona um novo ponto aos dados
            x.append(len(x) + 1)
            y.append(value)

            # atualiza o gráfico
            line.set_data(x, y)
            ax.relim()
            ax.autoscale_view()



        except Exception as e:
            logging.error(f'Erro ao atualizar o gráfico: {e}')

    # cria a animação
    ani = animation.FuncAnimation(fig, update, interval=1000, cache_frame_data=False)

    # mostra o gráfico
    plt.show()

plc.disconnect()


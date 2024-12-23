from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.window import Time
from pyflink.datastream.functions import SourceFunction, FlatMapFunction, ReduceFunction
from pyflink.common.typeinfo import Types
import socket

class SocketSourceFunction(SourceFunction):
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.running = True

    def run(self, ctx):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.hostname, self.port))
            server_socket.listen(5)
            client_socket, addr = server_socket.accept()
            with client_socket:
                while self.running:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    ctx.collect(data.decode('utf-8'))

    def cancel(self):
        self.running = False

class SensorFlatMapFunction(FlatMapFunction):
    def flat_map(self, value, collector):
        import json
        event = json.loads(value)
        for entity in event.get('entities', []):
            collector.collect((entity.get('type', ''), 1))

class SensorReduceFunction(ReduceFunction):
    def reduce(self, value1, value2):
        return (value1[0], value1[1] + value2[1])

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    custom_source = SourceFunction("org.apache.flink.streaming.api.functions.source.SocketTextStreamFunction")
    ds = env.add_source(custom_source, type_info=Types.ROW(Types.STRING()))

    # ソケットストリームソースを作成
    hostname = "localhost"
    port = 9001
    socket_stream = env.add_source(SocketSourceFunction(hostname, port), Types.STRING())

    # Process event stream
    processed_data_stream = (socket_stream
                             .flat_map(SensorFlatMapFunction(), output_type=Types.TUPLE([Types.STRING(), Types.INT()]))
                             .key_by(lambda x: x[0])
                             .time_window(Time.seconds(60))
                             .reduce(SensorReduceFunction(), output_type=Types.TUPLE([Types.STRING(), Types.INT()])))

    # Print the results with a single thread, rather than in parallel
    processed_data_stream.print().set_parallelism(1)
    env.execute("Socket Window NgsiEvent")

if __name__ == '__main__':
    main()

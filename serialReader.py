import serial


class SerialReader:
    def open(self, port, baudrate=57600, state_sync=b'\xa5Z'):
        self.PORT = port
        self.BAUD_RATE = baudrate
        self.STATE_SYNC = state_sync

        self.Serial = serial.Serial(self.PORT, self.BAUD_RATE)
        self.Serial.flushInput()
        self.Serial.flushOutput()

    def read(self, n_packages):
        sync = False

        version = []
        count = []
        data = []
        switch = []

        for i in range(n_packages):
            if not sync:
                sync_data = []
                while True:
                    sync_buffer = self.Serial.read()
                    sync_data += sync_buffer
                    if bytes(sync_data[-2:]) == self.STATE_SYNC:
                        sync = True
                        break

            buffer = self.Serial.read(17)

            v = buffer[0]
            version.append(v)

            c = buffer[1]
            count.append(c)

            d = []
            d.append(int.from_bytes(
                buffer[2:4], byteorder='big', signed=False))
            d.append(int.from_bytes(
                buffer[4:6], byteorder='big', signed=False))
            d.append(int.from_bytes(
                buffer[6:8], byteorder='big', signed=False))
            d.append(int.from_bytes(
                buffer[8:10], byteorder='big', signed=False))
            d.append(int.from_bytes(
                buffer[10:12], byteorder='big', signed=False))
            d.append(int.from_bytes(
                buffer[12:14], byteorder='big', signed=False))
            data.append(d)

            s = buffer[14]
            switch.append(s)

            if buffer[15:17] != self.STATE_SYNC:
                sync = False
                continue

        return version, count, data, switch

    def close(self):
        self.Serial.close()

from Pyro4 import expose

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))
        text = self.read_input()
        step = len(text) / len(self.workers)

        # map
        mapped = []
        for i in xrange(0, len(self.workers)):
            mapped.append(self.workers[i].mymap(text[i * step : i * step + step], 3))

        print 'Map finished: ', mapped

        # reduce
        reduced = self.myreduce(mapped)
        print("Reduce finished: " + str(reduced))

        # output
        self.write_output(reduced)

        print("Job Finished")

    @staticmethod
    @expose
    def mymap(text, shift):
        result = ""
        for i in range(len(text)):
         char = text[i]
         if (char.isupper()):
             result += chr((ord(char) - 65 + shift) % 26 + 65)
         elif (char.islower()):
             result += chr((ord(char) - 97 + shift) % 26 + 97)
         else: 
                result += char

        return result

    @staticmethod
    @expose
    def myreduce(mapped):
        output = ""
        for x in mapped:
            output += x.value
        return output

    def read_input(self):
        with open(self.input_file_name, 'r') as f:
            text = f.read() # read full text
        return text

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(str(output))
        f.write('\n')
        f.close()
        
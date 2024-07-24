import threading
import random
import time
import matplotlib.pyplot as plt

class VectorSum:
    def __init__(self, size, num_threads):
        self.size = size
        self.num_threads = num_threads
        self.vector = self._generate_random_vector()
    
    def _generate_random_vector(self):
        return [random.randint(1, 100) for _ in range(self.size)]
    
    def _sum_vector(self):
        return sum(self.vector)
    
    def _sum_vector_with_threads(self):
        total_sum = [0] * self.num_threads
        threads = []

        def partial_sum(start, end, index):
            total_sum[index] = sum(self.vector[start:end])

        chunk_size = self.size // self.num_threads
        for i in range(self.num_threads):
            start = i * chunk_size
            end = (i + 1) * chunk_size if i != self.num_threads - 1 else self.size
            thread = threading.Thread(target=partial_sum, args=(start, end, i))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return sum(total_sum)
    
    def measure_sequential_time(self):
        start_time = time.time()
        total_sum = self._sum_vector()
        end_time = time.time()
        return end_time - start_time, total_sum
    
    def measure_parallel_time(self):
        start_time = time.time()
        total_sum = self._sum_vector_with_threads()
        end_time = time.time()
        return end_time - start_time, total_sum

class ExecutionTimeGraph:
    def __init__(self, vector_sizes, num_threads_list):
        self.vector_sizes = vector_sizes
        self.num_threads_list = num_threads_list
    
    def generate_graph(self):
        for size in self.vector_sizes:
            times = []
            vector_sum = VectorSum(size, 1)
            for num_threads in self.num_threads_list:
                vector_sum.num_threads = num_threads
                par_time, _ = vector_sum.measure_parallel_time()
                times.append(par_time)
            
            plt.plot(self.num_threads_list, times, label=f'Vector Size = {size}')
        
        plt.xlabel('Number of Threads')
        plt.ylabel('Execution Time (s)')
        plt.legend()
        plt.title('Execution Time vs Number of Threads')
        plt.show()


def main():
    vector_size = int(input("Enter the size of the vector: "))
    num_threads = int(input("Enter the number of threads: "))
    
    vector_sum = VectorSum(vector_size, num_threads)
    
    seq_time, seq_sum = vector_sum.measure_sequential_time()
    print(f"Sequential Sum: {seq_sum}, Time: {seq_time:.4f} seconds")
    
    par_time, par_sum = vector_sum.measure_parallel_time()
    print(f"Parallel Sum with {num_threads} threads: {par_sum}, Time: {par_time:.4f} seconds")
    
    assert seq_sum == par_sum, "Sequential and Parallel sums do not match!"

    # Generate the execution time graph
    vector_sizes = [10**4, 10**5, 10**6]
    num_threads_list = [1, 2, 4, 8, 16, 32]
    graph = ExecutionTimeGraph(vector_sizes, num_threads_list)
    graph.generate_graph()


if __name__ == "__main__":
    main()

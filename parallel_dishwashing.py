"""
Parallel Dishwashing System - Pipeline Architecture
====================================================
This module implements a multi-threaded, parallel dishwashing process
using a pipeline pattern where different workers handle different stages
concurrently.

Author: Cassion Group
Date: February 2026
"""

import time
import random
import threading
from queue import Queue, Empty
from typing import List, Dict


class Dish:
    """Represents a single dish to be processed."""
    
    def __init__(self, dish_id: int, dish_type: str):
        """
        Initialize a dish object.
        
        Args:
            dish_id: Unique identifier for the dish
            dish_type: Type of dish (plate, bowl, utensil)
        """
        self.dish_id = dish_id
        self.dish_type = dish_type
        self.status = "dirty"
        
    def __repr__(self):
        return f"Dish({self.dish_id}, {self.dish_type}, {self.status})"


class ParallelDishwasher:
    """
    Parallel implementation of the dishwashing process using pipeline architecture.
    Multiple workers process different stages concurrently.
    """
    
    def __init__(self, num_dishes: int, num_workers: int = 4):
        """
        Initialize the parallel dishwasher.
        
        Args:
            num_dishes: Number of dishes to process
            num_workers: Number of worker threads (default 4, one per stage)
        """
        self.num_dishes = num_dishes
        self.num_workers = num_workers
        self.dishes = self._generate_dishes()
        
        # Thread-safe queues for each stage
        # These are the critical sections that require synchronization
        self.queue_1 = Queue()  # Pre-rinse queue
        self.queue_2 = Queue()  # Wash queue
        self.queue_3 = Queue()  # Dry queue
        self.queue_4 = Queue()  # Store queue
        self.completed_dishes = []
        
        # Synchronization primitives
        self.completion_lock = threading.Lock()
        self.stop_event = threading.Event()
        
    def _generate_dishes(self) -> List[Dish]:
        """Generate a list of dirty dishes with random types."""
        dish_types = ["plate", "bowl", "utensil"]
        dishes = []
        for i in range(self.num_dishes):
            dish_type = random.choice(dish_types)
            dishes.append(Dish(i + 1, dish_type))
        return dishes
    
    def _simulate_processing_time(self) -> float:
        """
        Simulate realistic processing time for a stage.
        Returns a random value between 0.1 and 0.3 seconds.
        """
        return random.uniform(0.1, 0.3)
    
    def worker_pre_rinse(self) -> None:
        """
        Worker thread for Stage 1: Pre-rinse and scrape dishes.
        Continuously processes dishes from queue_1 and passes to queue_2.
        """
        while not self.stop_event.is_set():
            try:
                # Critical section: dequeue operation
                dish = self.queue_1.get(timeout=0.1)
                
                # Process the dish
                time.sleep(self._simulate_processing_time())
                dish.status = "pre-rinsed"
                
                # Critical section: enqueue to next stage
                self.queue_2.put(dish)
                
                # Signal completion of this item
                self.queue_1.task_done()
                
            except Empty:
                continue
    
    def worker_wash(self) -> None:
        """
        Worker thread for Stage 2: Wash dishes.
        Continuously processes dishes from queue_2 and passes to queue_3.
        """
        while not self.stop_event.is_set():
            try:
                # Critical section: dequeue operation
                dish = self.queue_2.get(timeout=0.1)
                
                # Process the dish
                time.sleep(self._simulate_processing_time())
                dish.status = "washed"
                
                # Critical section: enqueue to next stage
                self.queue_3.put(dish)
                
                # Signal completion of this item
                self.queue_2.task_done()
                
            except Empty:
                continue
    
    def worker_dry(self) -> None:
        """
        Worker thread for Stage 3: Dry dishes.
        Continuously processes dishes from queue_3 and passes to queue_4.
        """
        while not self.stop_event.is_set():
            try:
                # Critical section: dequeue operation
                dish = self.queue_3.get(timeout=0.1)
                
                # Process the dish
                time.sleep(self._simulate_processing_time())
                dish.status = "dried"
                
                # Critical section: enqueue to next stage
                self.queue_4.put(dish)
                
                # Signal completion of this item
                self.queue_3.task_done()
                
            except Empty:
                continue
    
    def worker_store(self) -> None:
        """
        Worker thread for Stage 4: Sort and store dishes.
        Continuously processes dishes from queue_4 and marks them as complete.
        """
        while not self.stop_event.is_set():
            try:
                # Critical section: dequeue operation
                dish = self.queue_4.get(timeout=0.1)
                
                # Process the dish
                time.sleep(self._simulate_processing_time())
                dish.status = "stored"
                
                # Critical section: add to completed list
                with self.completion_lock:
                    self.completed_dishes.append(dish)
                
                # Signal completion of this item
                self.queue_4.task_done()
                
            except Empty:
                continue
    
    def process_parallel(self) -> Dict[str, float]:
        """
        Process all dishes in parallel using pipeline architecture.
        
        Returns:
            Dictionary containing execution time and throughput metrics
        """
        print(f"\n{'='*60}")
        print(f"PARALLEL DISHWASHING PROCESS (PIPELINE)")
        print(f"{'='*60}")
        print(f"Processing {self.num_dishes} dishes in parallel...")
        print(f"Workers: 4 concurrent threads (one per stage)")
        print(f"Architecture: Pipeline with synchronized queues")
        print(f"{'='*60}\n")
        
        start_time = time.time()
        
        # Create worker threads for each stage
        threads = [
            threading.Thread(target=self.worker_pre_rinse, name="PreRinse-Worker"),
            threading.Thread(target=self.worker_wash, name="Wash-Worker"),
            threading.Thread(target=self.worker_dry, name="Dry-Worker"),
            threading.Thread(target=self.worker_store, name="Store-Worker")
        ]
        
        # Start all worker threads
        print("Starting worker threads...")
        for thread in threads:
            thread.daemon = True
            thread.start()
            print(f"  - {thread.name} started")
        
        print("\nFeeding dishes into pipeline...")
        
        # Feed all dishes into the first queue
        for idx, dish in enumerate(self.dishes, 1):
            if idx % 20 == 0 or idx == 1:
                print(f"  Queued dish {idx}/{self.num_dishes}")
            self.queue_1.put(dish)
        
        print("\nWaiting for pipeline to complete...")
        
        # Wait for all queues to be empty and all work to be done
        self.queue_1.join()
        self.queue_2.join()
        self.queue_3.join()
        self.queue_4.join()
        
        # Signal workers to stop
        self.stop_event.set()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join(timeout=1.0)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Calculate metrics
        dishes_completed = len(self.completed_dishes)
        throughput = dishes_completed / elapsed_time
        avg_time_per_dish = elapsed_time / dishes_completed if dishes_completed > 0 else 0
        
        # Display results
        print(f"\n{'='*60}")
        print(f"PARALLEL RESULTS")
        print(f"{'='*60}")
        print(f"Total execution time: {elapsed_time:.2f} seconds")
        print(f"Dishes processed: {dishes_completed}")
        print(f"Throughput: {throughput:.2f} dishes/second")
        print(f"Average time per dish: {avg_time_per_dish:.3f} seconds")
        print(f"Pipeline efficiency: {(dishes_completed/self.num_dishes)*100:.1f}%")
        print(f"{'='*60}\n")
        
        return {
            "execution_time": elapsed_time,
            "throughput": throughput,
            "avg_time_per_dish": avg_time_per_dish,
            "dishes_processed": dishes_completed
        }


def main():
    """Main function to run the parallel dishwashing simulation."""
    # Set random seed for reproducibility
    random.seed(42)
    
    # Initialize and run parallel dishwasher
    num_dishes = 100
    num_workers = 4
    dishwasher = ParallelDishwasher(num_dishes, num_workers)
    results = dishwasher.process_parallel()
    
    return results


if __name__ == "__main__":
    main()

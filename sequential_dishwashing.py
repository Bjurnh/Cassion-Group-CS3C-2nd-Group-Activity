"""
Sequential Dishwashing System
==============================
This module implements a single-threaded, sequential dishwashing process
where one worker handles all stages of the workflow from start to finish.

Author: Cassion Group
Date: February 2026
"""

import time
import random
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


class SequentialDishwasher:
    """
    Sequential implementation of the dishwashing process.
    One worker processes all stages sequentially.
    """
    
    def __init__(self, num_dishes: int):
        """
        Initialize the sequential dishwasher.
        
        Args:
            num_dishes: Number of dishes to process
        """
        self.num_dishes = num_dishes
        self.dishes = self._generate_dishes()
        self.total_time = 0
        
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
    
    def pre_rinse(self, dish: Dish) -> None:
        """
        Stage 1: Pre-rinse and scrape the dish.
        
        Args:
            dish: Dish object to process
        """
        time.sleep(self._simulate_processing_time())
        dish.status = "pre-rinsed"
    
    def wash(self, dish: Dish) -> None:
        """
        Stage 2: Wash the dish.
        
        Args:
            dish: Dish object to process
        """
        time.sleep(self._simulate_processing_time())
        dish.status = "washed"
    
    def dry(self, dish: Dish) -> None:
        """
        Stage 3: Dry the dish.
        
        Args:
            dish: Dish object to process
        """
        time.sleep(self._simulate_processing_time())
        dish.status = "dried"
    
    def store(self, dish: Dish) -> None:
        """
        Stage 4: Sort and store the dish.
        
        Args:
            dish: Dish object to process
        """
        time.sleep(self._simulate_processing_time())
        dish.status = "stored"
    
    def process_sequential(self) -> Dict[str, float]:
        """
        Process all dishes sequentially through all stages.
        
        Returns:
            Dictionary containing execution time and throughput metrics
        """
        print(f"\n{'='*60}")
        print(f"SEQUENTIAL DISHWASHING PROCESS")
        print(f"{'='*60}")
        print(f"Processing {self.num_dishes} dishes sequentially...")
        print(f"Worker: Single worker handling all stages")
        print(f"{'='*60}\n")
        
        start_time = time.time()
        
        # Process each dish through all stages before moving to the next
        for idx, dish in enumerate(self.dishes, 1):
            if idx % 10 == 0 or idx == 1:
                print(f"Processing dish {idx}/{self.num_dishes}...")
            
            # Each dish goes through all stages sequentially
            self.pre_rinse(dish)
            self.wash(dish)
            self.dry(dish)
            self.store(dish)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Calculate metrics
        throughput = self.num_dishes / elapsed_time
        avg_time_per_dish = elapsed_time / self.num_dishes
        
        # Display results
        print(f"\n{'='*60}")
        print(f"SEQUENTIAL RESULTS")
        print(f"{'='*60}")
        print(f"Total execution time: {elapsed_time:.2f} seconds")
        print(f"Dishes processed: {self.num_dishes}")
        print(f"Throughput: {throughput:.2f} dishes/second")
        print(f"Average time per dish: {avg_time_per_dish:.3f} seconds")
        print(f"{'='*60}\n")
        
        return {
            "execution_time": elapsed_time,
            "throughput": throughput,
            "avg_time_per_dish": avg_time_per_dish,
            "dishes_processed": self.num_dishes
        }


def main():
    """Main function to run the sequential dishwashing simulation."""
    # Set random seed for reproducibility
    random.seed(42)
    
    # Initialize and run sequential dishwasher
    num_dishes = 100
    dishwasher = SequentialDishwasher(num_dishes)
    results = dishwasher.process_sequential()
    
    return results


if __name__ == "__main__":
    main()

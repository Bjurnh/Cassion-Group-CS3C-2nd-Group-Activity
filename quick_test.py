"""
Quick Test - Benchmark with reduced dataset
"""
import random
from sequential_dishwashing import SequentialDishwasher
from parallel_dishwashing import ParallelDishwasher

def quick_test():
    """Run a quick test with fewer dishes"""
    print("\n" + "="*60)
    print("QUICK PERFORMANCE TEST")
    print("="*60)
    
    num_dishes = 20  # Reduced for quick testing
    random.seed(42)
    
    # Sequential
    print("\nRunning Sequential...")
    seq = SequentialDishwasher(num_dishes)
    seq_result = seq.process_sequential()
    
    # Parallel
    print("\nRunning Parallel...")
    random.seed(42)
    par = ParallelDishwasher(num_dishes, 4)
    par_result = par.process_parallel()
    
    # Results
    speedup = seq_result["execution_time"] / par_result["execution_time"]
    print(f"\n{'='*60}")
    print(f"QUICK TEST RESULTS")
    print(f"{'='*60}")
    print(f"Sequential: {seq_result['execution_time']:.2f}s")
    print(f"Parallel:   {par_result['execution_time']:.2f}s")
    print(f"Speedup:    {speedup:.2f}x")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    quick_test()

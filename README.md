# Cassion-Group-CS3C-2nd-Group-Activity

 Parallel Computing Challenge - Restaurant Dishwashing System

## Project Overview
This project demonstrates the application of parallel computing principles to optimize a real-world bottleneck: the sequential dishwashing process in restaurants.

### Team Information
- **Project**: Analog-to-Digital Parallel Challenge
- **Real-World Bottleneck**: Restaurant Dishwashing Station
- **Parallel Strategy**: Hybrid Task-Data Parallelism (Pipeline Architecture)
- **Implementation Language**: Python 3.x

---

## Real-World Problem

### The Bottleneck
In small to medium-sized restaurants, dishwashing represents a critical operational bottleneck during peak service hours. Currently, a single worker handles the entire workflow sequentially:

1. **Pre-rinse and scraping** - Removing food debris
2. **Loading** - Organizing dishes into washer
3. **Washing** - Running the dishwasher cycle
4. **Drying** - Air or towel drying
5. **Sorting and stacking** - Organizing by type
6. **Storage** - Returning to designated locations

### Why It Matters
During dinner rush (6-9 PM), dishes accumulate faster than one person can process them through all stages. This creates:
- Service delays when kitchen runs out of clean dishes
- Worker fatigue from constant task-switching
- Underutilized equipment (washer idle during drying, etc.)
- Customer dissatisfaction due to slower service
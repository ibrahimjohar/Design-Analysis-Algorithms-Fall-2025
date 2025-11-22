import random
import os

class InputGenerator:
    @staticmethod
    def generate_points_dataset(filename, num_points, complexity="medium"):
        #generate random points dataset
        if complexity == "low":
            max_val = 100
        elif complexity == "medium":
            max_val = 1000
        else:  #high
            max_val = 10000
        
        points = []
        for _ in range(num_points):
            x = random.randint(0, max_val)
            y = random.randint(0, max_val)
            points.append((x, y))
        
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        with open(filename, 'w') as f:
            for point in points:
                f.write(f"{point[0]},{point[1]}\n")
        
        print(f"Generated {filename} with {num_points} points")
        return points
    
    @staticmethod
    def generate_integers_dataset(filename, num_integers, complexity="medium"):
        #generate random integers dataset
        if complexity == "low":
            max_digits = 10
        elif complexity == "medium":
            max_digits = 50
        else:  #high
            max_digits = 100
        
        integers = []
        num_pairs = num_integers // 2
        for _ in range(num_pairs):
            digits1 = random.randint(max_digits - 5, max_digits)
            digits2 = random.randint(max_digits - 5, max_digits)
            
            num1 = random.randint(10**(digits1-1), 10**digits1 - 1)
            num2 = random.randint(10**(digits2-1), 10**digits2 - 1)
            
            integers.append((num1, num2))
        
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        with open(filename, 'w') as f:
            for pair in integers:
                f.write(f"{pair[0]},{pair[1]}\n")
        
        print(f"Generated {filename} with {num_pairs} integer pairs")
        return integers
    
    @staticmethod
    def generate_all_datasets():
        #generate 10 datasets for each problem
        
        #datasets directory
        datasets_dir = "datasets"
        os.makedirs(datasets_dir, exist_ok=True)
        
        #generate points datasets
        points_files = []
        complexities = ["low", "medium", "high"]
        
        for i in range(10):
            complexity = complexities[i % 3]
            size = 100 + i * 50  #varying sizes from 100-550
            filename = f"{datasets_dir}/points_dataset_{i+1}_{complexity}.txt"
            InputGenerator.generate_points_dataset(filename, size, complexity)
            points_files.append(filename)
        
        #generate integers datasets
        integers_files = []
        for i in range(10):
            complexity = complexities[i % 3]
            size = 100 + i * 20  #varying sizes
            filename = f"{datasets_dir}/integers_dataset_{i+1}_{complexity}.txt"
            InputGenerator.generate_integers_dataset(filename, size, complexity)
            integers_files.append(filename)
        
        return points_files, integers_files
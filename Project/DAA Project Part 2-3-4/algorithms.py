import math
import time

class DivideConquerAlgorithms:
    @staticmethod
    def closest_pair_brute_force(points):
        #brute force method for closest pair (for small inputs)
        min_dist = float('inf')
        pair = None
        n = len(points)
        for i in range(n):
            for j in range(i + 1, n):
                dist = math.sqrt((points[i][0] - points[j][0])**2 + 
                               (points[i][1] - points[j][1])**2)
                if dist < min_dist:
                    min_dist = dist
                    pair = (points[i], points[j])
        return min_dist, pair
    
    @staticmethod
    def closest_pair(points):
        #divide and conquer algorithm for closest pair of points

        # Sort points by x-coordinate
        points_sorted = sorted(points, key=lambda p: p[0])
        
        def closest_pair_recursive(P):
            n = len(P)
            if n <= 3:
                return DivideConquerAlgorithms.closest_pair_brute_force(P)
            
            #divide
            mid = n // 2
            Q = P[:mid]
            R = P[mid:]
            #conquer
            dist_left, pair_left = closest_pair_recursive(Q)
            dist_right, pair_right = closest_pair_recursive(R)
            #combine
            min_dist = min(dist_left, dist_right)
            best_pair = pair_left if dist_left < dist_right else pair_right
            
            #finding pts close to the vertical line
            mid_x = P[mid][0]
            strip = [p for p in P if abs(p[0] - mid_x) < min_dist]
            strip.sort(key=lambda p: p[1])
            
            #check points in strip
            for i in range(len(strip)):
                j = i + 1
                while j < len(strip) and (strip[j][1] - strip[i][1]) < min_dist:
                    dist = math.sqrt((strip[i][0] - strip[j][0])**2 + 
                                   (strip[i][1] - strip[j][1])**2)
                    if dist < min_dist:
                        min_dist = dist
                        best_pair = (strip[i], strip[j])
                    j += 1
            
            return min_dist, best_pair
        
        return closest_pair_recursive(points_sorted)
    
    @staticmethod
    def karatsuba_multiply(x, y):
        #karatsuba algorithm for integer multiplication
        
        #base case for small numbers
        if x < 10 or y < 10:
            return x * y
        
        #calc the size of numbers
        n = max(len(str(x)), len(str(y)))
        m = n // 2
        
        #split the num(s)
        high1, low1 = x // 10**m, x % 10**m
        high2, low2 = y // 10**m, y % 10**m
        
        #recursive steps
        z0 = DivideConquerAlgorithms.karatsuba_multiply(low1, low2)
        z1 = DivideConquerAlgorithms.karatsuba_multiply((low1 + high1), (low2 + high2))
        z2 = DivideConquerAlgorithms.karatsuba_multiply(high1, high2)
        
        #combining results
        return z2 * 10**(2*m) + (z1 - z2 - z0) * 10**m + z0
    
    @staticmethod
    def standard_multiply(x, y):
        #standard multiplication for comparison
        return x * y
    
    @staticmethod
    def naive_python_multiply(x, y):
        #naive multiplication implemented in pure Python for fair comparison
        #uses repeated addition to simulate O(n^2) complexity
        if x == 0 or y == 0:
            return 0
        if x < y:
            x, y = y, x  #make y the smaller number
        
        result = 0
        #add x to result, y times (simulating naive multiplication)
        if y < 1000:
            #for small y, add repeatedly
            for _ in range(y):
                result += x
        else:
            #for large y, using a more efficient but still naive approach
            #converting to base-10 representation and multiply digit by digit
            x_digits = []
            temp_x = x
            while temp_x > 0:
                x_digits.append(temp_x % 10)
                temp_x //= 10
            
            y_digits = []
            temp_y = y
            while temp_y > 0:
                y_digits.append(temp_y % 10)
                temp_y //= 10
            
            #multiplication
            for i, y_digit in enumerate(y_digits):
                carry = 0
                partial = []
                for x_digit in x_digits:
                    product = x_digit * y_digit + carry
                    partial.append(product % 10)
                    carry = product // 10
                if carry > 0:
                    partial.append(carry)
                
                #converting partial result to integer & add to result
                partial_num = 0
                for j, digit in enumerate(partial):
                    partial_num += digit * (10 ** j)
                result += partial_num * (10 ** i)
        
        return result
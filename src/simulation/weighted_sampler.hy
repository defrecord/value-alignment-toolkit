"""
Weighted value sampling implementation based on the Values in the Wild paper.
Implements the value floor generator for sampling values according to empirical distributions.
"""

(import [collections [defaultdict]]
        [random [random choice randint]]
        [math [log]]
        [typing [Dict List Tuple Any Optional]])

(defn calculate-value-floors [values-with-weights]
  "Calculate floors (cumulative thresholds) for weighted value sampling.
  
  Args:
      values-with-weights: Dictionary mapping value names to their weights
      
  Returns:
      List of tuples (value, lower_bound, upper_bound)
  "
  (setv floors [])
  (setv cumulative 0.0)
  
  (for [[value weight] (.items values-with-weights)]
    (setv lower-bound cumulative)
    (setv cumulative (+ cumulative weight))
    (.append floors (, value lower-bound cumulative)))
  
  floors)

(defclass WeightedValueSampler []
  "Samples values based on their empirical frequency distribution.
  Implements the sampling methodology from the Values in the Wild paper."
  
  (defn __init__ [self &optional [values-with-weights None] [values-floor-path None]]
    "Initialize the sampler with value weights or load from file.
    
    Args:
        values-with-weights: Dictionary mapping value names to weights
        values-floor-path: Path to CSV file with precalculated value floors
    "
    (setv self.values-with-weights (or values-with-weights (self.get-default-weights)))
    (setv self.floors (if values-floor-path
                         (self.load-floors-from-file values-floor-path)
                         (calculate-value-floors self.values-with-weights)))
    (setv self.total-weight (get (. (get self.floors -1) 2) 0)))
  
  (defn get-default-weights [self]
    "Get default value weights from the Values in the Wild paper."
    {
      "helpfulness" 23.359
      "professionalism" 22.861
      "transparency" 17.391
      "clarity" 16.58
      "thoroughness" 14.301
      "efficiency" 6.606
      "technical excellence" 6.127
      "authenticity" 6.042
      "analytical rigor" 5.478
      "accuracy" 5.318
      ; Additional values would be included here
    })
  
  (defn load-floors-from-file [self file-path]
    "Load precomputed value floors from a CSV file.
    
    Args:
        file-path: Path to the CSV file with value floors
        
    Returns:
        List of value floor tuples
    "
    (setv floors [])
    (with [f (open file-path "r")]
      ; Skip header
      (.readline f)
      (for [line (.readlines f)]
        (setv [value lower upper] (.split (.strip line) ","))
        (.append floors (, value (float lower) (float upper)))))
    floors)
  
  (defn sample-value [self]
    "Sample a single value based on the weighted distribution.
    
    Returns:
        A sampled value name
    "
    (setv r (* (random) self.total-weight))
    
    (for [[value lower-bound upper-bound] self.floors]
      (when (and (>= r lower-bound) (< r upper-bound))
        (return value)))
    
    ; Default fallback if something goes wrong
    (get (get self.floors 0) 0))
  
  (defn sample-values [self n]
    "Sample n values with replacement.
    
    Args:
        n: Number of values to sample
        
    Returns:
        List of sampled values
    "
    (lfor _ (range n) (self.sample-value))))

; Example usage
(defmain [&rest args]
  (setv sampler (WeightedValueSampler))
  (print "Sampling 10 values based on empirical distribution:")
  (print (sampler.sample-values 10)))

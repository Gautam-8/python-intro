"""MLMath - Simple mathematical operations for machine learning."""

__version__ = "1.0.0"


def dot_product(a, b):
    """Calculate dot product of two vectors.
    
    Args:
        a, b: Lists of numbers
        
    Returns:
        Sum of element-wise products
        
    Example:
        >>> dot_product([1, 2, 3], [4, 5, 6])
        32
    """
    if len(a) != len(b):
        raise ValueError("Vectors must have same length")
    return sum(x * y for x, y in zip(a, b))


def matrix_multiply(A, B):
    """Multiply two matrices.
    
    Args:
        A, B: 2D lists representing matrices
        
    Returns:
        Product matrix as 2D list
        
    Example:
        >>> matrix_multiply([[1, 2], [3, 4]], [[5, 6], [7, 8]])
        [[19, 22], [43, 50]]
    """
    if len(A[0]) != len(B):
        raise ValueError("Incompatible matrix dimensions")
    
    result = []
    for i in range(len(A)):
        row = []
        for j in range(len(B[0])):
            row.append(sum(A[i][k] * B[k][j] for k in range(len(B))))
        result.append(row)
    return result


def conditional_probability(events):
    """Calculate conditional probabilities P(A|B) = P(A and B) / P(B).
    
    Args:
        events: Dict with event names as keys, values are dicts with 'joint' and 'marginal'
        
    Returns:
        Dict with conditional probabilities
    """
    result = {}
    for name, probs in events.items():
        if probs['marginal'] == 0:
            raise ValueError("Marginal probability cannot be zero")
        result[name] = probs['joint'] / probs['marginal']
    return result

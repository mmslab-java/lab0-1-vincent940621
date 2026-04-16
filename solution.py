The problem asks us to find the minimum circular distance between a queried index `queries[i]` and any other index `j` such that `nums[j]` is equal to `nums[queries[i]]`. If no such other index exists, the answer is -1.

Let `N` be the length of the `nums` array. The circular distance between two indices `idx1` and `idx2` is `min(abs(idx1 - idx2), N - abs(idx1 - idx2))`.

A brute-force approach for each query would involve iterating through all other `N-1` indices, checking their values, calculating distances, and finding the minimum. This would lead to an `O(Q * N)` time complexity, which is too slow given `Q, N <= 10^5`.

To optimize, we can use a pre-processing step:

1.  **Pre-processing (Building an index map):**
    We iterate through the `nums` array once and build a dictionary (or hash map) where:
    *   Keys are the unique values present in `nums`.
    *   Values are sorted lists of all indices where that particular value appears in `nums`.
    This step takes `O(N)` time. Since we iterate `nums` from `0` to `N-1` and append indices to the lists, each list will naturally be sorted.

2.  **Processing Queries:**
    For each query `q_idx` (which is `queries[i]`):
    *   Get the value `target_val = nums[q_idx]`.
    *   Retrieve the list of indices `indices_list = val_to_indices[target_val]`.
    *   **Check for uniqueness:** If `len(indices_list)` is `1` (meaning `target_val` only appears at `q_idx`), there is no other index with the same value, so the answer is -1.
    *   **Find closest elements:** If `len(indices_list) > 1`, we need to find the closest indices in `indices_list` to `q_idx`. Since `indices_list` is sorted, we can use binary search (`bisect_left` in Python) to find the position of `q_idx` within `indices_list`. Let this position be `pos_in_list`.
        *   The two candidates for the closest element (in a circular sense within `indices_list`) are the element immediately "before" `q_idx` and the element immediately "after" `q_idx`.
        *   The index of the element "before" `q_idx` is `indices_list[(pos_in_list - 1 + len(indices_list)) % len(indices_list)]`.
        *   The index of the element "after" `q_idx` is `indices_list[(pos_in_list + 1) % len(indices_list)]`.
        *   Calculate the circular distance from `q_idx` to each of these two candidates.
        *   The minimum of these two distances will be the answer for the current query.

**Example Walkthrough (Example 1: `nums = [1,3,1,4,1,3,2]`, `queries = [0,3,5]`)**

`N = 7`

1.  **Pre-processing:**
    `val_to_indices = {1: [0, 2, 4], 3: [1, 5], 4: [3], 2: [6]}`

2.  **Processing Queries:**

    *   **Query 0: `q_idx = 0`**
        *   `target_val = nums[0] = 1`.
        *   `indices_list = val_to_indices[1] = [0, 2, 4]`. `len=3`.
        *   `pos_in_list = bisect_left([0, 2, 4], 0) = 0`.
        *   `prev_candidate_idx = indices_list[(0 - 1 + 3) % 3] = indices_list[2] = 4`.
            *   Circular distance `(0, 4, 7)`: `min(abs(0-4), 7-abs(0-4)) = min(4, 3) = 3`. `min_dist = 3`.
        *   `next_candidate_idx = indices_list[(0 + 1) % 3] = indices_list[1] = 2`.
            *   Circular distance `(0, 2, 7)`: `min(abs(0-2), 7-abs(0-2)) = min(2, 5) = 2`. `min_dist = min(3, 2) = 2`.
        *   `answer.append(2)`.

    *   **Query 1: `q_idx = 3`**
        *   `target_val = nums[3] = 4`.
        *   `indices_list = val_to_indices[4] = [3]`. `len=1`.
        *   Since `len(indices_list) <= 1`, `answer.append(-1)`.

    *   **Query 2: `q_idx = 5`**
        *   `target_val = nums[5] = 3`.
        *   `indices_list = val_to_indices[3] = [1, 5]`. `len=2`.
        *   `pos_in_list = bisect_left([1, 5], 5) = 1`.
        *   `prev_candidate_idx = indices_list[(1 - 1 + 2) % 2] = indices_list[0] = 1`.
            *   Circular distance `(5, 1, 7)`: `min(abs(5-1), 7-abs(5-1)) = min(4, 3) = 3`. `min_dist = 3`.
        *   `next_candidate_idx = indices_list[(1 + 1) % 2] = indices_list[0] = 1`.
            *   Circular distance `(5, 1, 7)`: `min(abs(5-1), 7-abs(5-1)) = min(4, 3) = 3`. `min_dist = min(3, 3) = 3`.
        *   `answer.append(3)`.

Resulting `answer = [2, -1, 3]`.

**Complexity Analysis:**

*   **Time Complexity:**
    *   Pre-processing: `O(N)` to build the `val_to_indices` dictionary.
    *   Queries: For each of `Q` queries, we perform a dictionary lookup (`O(1)` on average) and a `bisect_left` operation on a list of indices. In the worst case, a value might appear `N` times, making the list length `N`. `bisect_left` takes `O(log K)` where `K` is the length of `indices_list`. So, `O(log N)` in the worst case per query.
    *   Total time complexity: `O(N + Q log N)`. With `N, Q <= 10^5`, this is efficient enough (`10^5 + 10^5 * log(10^5) approx 10^5 + 10^5 * 17 = 1.8 * 10^6` operations).

*   **Space Complexity:**
    *   `val_to_indices` dictionary: In the worst case, all `N` indices are stored across all lists (e.g., if all elements are distinct or all are the same). So, `O(N)` space.
    *   `answer` array: `O(Q)` space.
    *   Total space complexity: `O(N + Q)`.

This approach fits within the given constraints.


import collections
import bisect

class Solution:
    def closestEqualElementQueries(self, nums: list[int], queries: list[int]) -> list[int]:
        N = len(nums)
        
        # Step 1: Pre-process the nums array
        # Create a dictionary where keys are values from nums
        # and values are sorted lists of indices where that value appears.
        # collections.defaultdict(list) simplifies adding elements to lists.
        val_to_indices = collections.defaultdict(list)
        for i, num in enumerate(nums):
            val_to_indices[num].append(i)
        
        answer = []
        
        # Step 2: Process each query
        for q_idx in queries:
            target_val = nums[q_idx]
            indices_list = val_to_indices[target_val]
            
            # If the value appears only once in nums, there's no other equal element.
            if len(indices_list) <= 1:
                answer.append(-1)
                continue
            
            # Initialize minimum distance to infinity
            min_dist = float('inf')
            
            # Find the position of q_idx in the sorted indices_list.
            # bisect_left returns an insertion point. If q_idx is present,
            # it returns the index of the first occurrence. Since each index
            # is unique in nums, q_idx will be at a unique position in indices_list.
            pos_in_list = bisect.bisect_left(indices_list, q_idx)
            
            # Consider the element immediately "before" q_idx in the circular list of indices
            # The modulo operator handles wrapping around to the end of the list.
            prev_candidate_idx = indices_list[(pos_in_list - 1 + len(indices_list)) % len(indices_list)]
            
            # Calculate the circular distance between q_idx and prev_candidate_idx
            # The distance between i and j in a circular array of length N is min(|i-j|, N - |i-j|)
            diff_prev = abs(q_idx - prev_candidate_idx)
            min_dist = min(min_dist, min(diff_prev, N - diff_prev))
            
            # Consider the element immediately "after" q_idx in the circular list of indices
            # The modulo operator handles wrapping around to the beginning of the list.
            next_candidate_idx = indices_list[(pos_in_list + 1) % len(indices_list)]
            
            # Calculate the circular distance between q_idx and next_candidate_idx
            diff_next = abs(q_idx - next_candidate_idx)
            min_dist = min(min_dist, min(diff_next, N - diff_next))
            
            answer.append(min_dist)
            
        return answer


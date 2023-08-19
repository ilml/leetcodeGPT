import os
import openai

openai.api_key = "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"

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "user",
      "content": "Two Sum \n\n\nGiven an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.\n\nYou can return the answer in any order.\n\n \nExample 1:\n\nInput: nums = [2,7,11,15], target = 9\nOutput: [0,1]\nExplanation: Because nums[0] + nums[1] == 9, we return [0, 1].\n\n\nExample 2:\n\nInput: nums = [3,2,4], target = 6\nOutput: [1,2]\n\n\nExample 3:\n\nInput: nums = [3,3], target = 6\nOutput: [0,1]\n\n\n \nConstraints:\n\n\n        2 <= nums.length <= 10⁴\n        -10⁹ <= nums[i] <= 10⁹\n        -10⁹ <= target <= 10⁹\n        Only one valid answer exists.\n\n\n \nFollow-up: Can you come up with an algorithm that is less than O(n²) time complexity?\nReturn a solution starting with the following code:\nclass Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:"
    }
  ],
  temperature=1,
  max_tokens=1000,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
print(response)

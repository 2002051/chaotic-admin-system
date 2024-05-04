from django.db.models.signals import pre_save, post_save


def func1(*args, **kwargs):
    print("func1", args, kwargs)
    # func1 () {'signal': <django.db.models.signals.ModelSignal object at 0x000001F66F3A99D0>, 'sender': <class 'app01.models.StudentInfo'>, 'instance': <StudentInfo: StudentInfo object (11)>, 'created': True, 'update_fields': None, 'raw': False, 'using': 'default'}


post_save.connect(func1)

# @post_save.connect   # 等价于post_save.connect(func2)
# def func2(*args, **kwargs):
#     print("func2", args, kwargs)
from app01.mine_signals import my_signal


def mine_func(*args, **kwargs):
    print('mine_func', args, kwargs)


my_signal.connect(mine_func)


if __name__ == '__main__':
    # list1 = [11,22,33]
    # list2 = list1
    # list1.append(5555)
    # print(list1,list2)
    class MyClass:

        def modify_data(self, new_data):
            # 使用形参赋值给 self.data，会修改原始对象的属性
            self.data = new_data
            self.data = self.data + 1
            print(self.data, new_data)


    # obj = MyClass()
    # obj.modify_data(2)
    # list1 = [11,22,3,22,44,55]
    # list1.remove(22)
    # print(list1)
    import copy
    class Solution:
        def twoSum(self, nums, target):
            res = []
            for index1, value1 in enumerate(nums):
                nums2 = copy.deepcopy(nums)
                index2 = 0
                value2 = target - value1
                nums2.remove(value1)
                if value2 in nums2:
                    index2 = nums2.index(value2) + 1
                    res.append(index1)
                    res.append(index2)

                    break
            return res


    obj = Solution()
    res = obj.twoSum([3, 2, 4], target=6)
    print(res)
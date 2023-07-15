numCourses = 2
prerequisites = [[1,0]]


def canFinish(numCourses, prerequisites):
    course_dict = { course : [] for course in range(numCourses)}
    check_set = set()
    for course, prer in prerequisites:
        course_dict[course].append(prer)

    def dfs(course):
        if not course_dict[course]:
            return True
        if course in check_set:
            return False
        check_set.add(course)
        for item in course_dict[course]:
            if not dfs(item): return False
        check_set.remove(course)
        course_dict[course] = []
        return True

    for course in range(numCourses):
        if not dfs(course): return False
    return True

print(canFinish(numCourses, prerequisites))
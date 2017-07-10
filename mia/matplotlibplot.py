import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5, 6, 7, 8]
y = [5, 2, 4, 2, 5, 3, 2, 5]


plt.scatter(x, y, label="SkitScat", color='k', marker='*')
plt.xlabel("x")
plt.ylabel('y')
plt.title("Wow a title!")
plt.legend()
plt.show()

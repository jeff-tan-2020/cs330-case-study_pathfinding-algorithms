import csv
from datetime import timedelta

from t1 import T1
from t2 import T2
from t3 import T3
from t4 import T4
from t5 import T5

if __name__ == "__main__":
  filename = "results/t5runtimes_data.csv"

  with open(filename, 'w') as file:
    writer = csv.writer(file)

    writer.writerow(["task", "trial", "total_runtime", "queue_runtime"])

    for i in range(1, 6):
      
      print("Initializing trial " + str(i))

      # total, queue = T1(i)
      # writer.writerow([1, i, total, queue])
      # print("Trial " + str(i) + " for T1 complete; total runtime " + str(timedelta(seconds=total)) + "; queue runtime " + str(timedelta(seconds=queue)))

      # total, queue = T2(i)
      # writer.writerow([2, i, total, queue])
      # print("Trial " + str(i) + " for T2 complete; total runtime " + str(timedelta(seconds=total)) + "; queue runtime " + str(timedelta(seconds=queue)))

      # total, queue = T3(i)
      # writer.writerow([3, i, total, queue])
      # print("Trial " + str(i) + " for T3 complete; total runtime " + str(timedelta(seconds=total)) + "; queue runtime " + str(timedelta(seconds=queue)))

      # total, queue = T4(i)
      # # writer.writerow([4, i, total, queue])
      # print("Trial " + str(i) + " for T4 complete; total runtime " + str(timedelta(seconds=total)) + "; queue runtime " + str(timedelta(seconds=queue)))

      total, queue = T5(i)
      writer.writerow([5, i, total, queue])
      print("Trial " + str(i) + " for T5 complete; total runtime " + str(timedelta(seconds=total)) + "; queue runtime " + str(timedelta(seconds=queue)))
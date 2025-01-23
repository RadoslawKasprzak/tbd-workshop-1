0. The goal of phase 2b is to perform benchmarking/scalability tests of sample three-tier lakehouse solution.

1. In main.tf, change machine_type at:

```
module "dataproc" {
  depends_on   = [module.vpc]
  source       = "github.com/bdg-tbd/tbd-workshop-1.git?ref=v1.0.36/modules/dataproc"
  project_name = var.project_name
  region       = var.region
  subnet       = module.vpc.subnets[local.notebook_subnet_id].id
  machine_type = "e2-standard-2"
}
```

and subsititute "e2-standard-2" with "e2-standard-4".

2. If needed request to increase cpu quotas (e.g. to 30 CPUs): 
https://console.cloud.google.com/apis/api/compute.googleapis.com/quotas?project=tbd-2023z-9918

3. Using tbd-tpc-di notebook perform dbt run with different number of executors, i.e., 1, 2, and 5, by changing:
```
 "spark.executor.instances": "2"
```

in profiles.yml.

4. In the notebook, collect console output from dbt run, then parse it and retrieve total execution time and execution times of processing each model. Save the results from each number of executors. 

logs can be found at
tbd-workshop-1/dbt_etl_performance_testing/data

5. Analyze the performance and scalability of execution times of each model. Visualize and discucss the final results.

Visualization of the results:

![task-time-2](https://github.com/user-attachments/assets/d3363e5c-a213-4201-b233-346458448784)
![task-time-4](https://github.com/user-attachments/assets/bc5a452c-bd6e-4434-a74f-67f2797d7cb1)
![task-time-8](https://github.com/user-attachments/assets/ef870e93-4af5-4450-8508-8d2144199323)

![total-time-2](https://github.com/user-attachments/assets/c0088b25-9ea5-455b-bd70-2a456a696852)
![total-time-4](https://github.com/user-attachments/assets/8fddbe2d-70ea-4d80-bb6b-f1156e22127d)
![total-time-8](https://github.com/user-attachments/assets/ddb21b52-9ea3-4de3-95c0-3d07386413a8)


Conclusion:
We don't see improvement from increasing the number of executors. Contrary to the assumption that more is better, dbt ran on 2 executors scored the best result with a time of 68 minutes. 4 and 8 executors finished the task in respectively 78 and 74 minutes. Main difference can be seen in the time taken for processing the gold layer.
More executors might not equal better performance as the resources are constant and not every task benefits from just splitting the workload among higher number of executors. The time decrease of the execution of the tasks from the gold layer for 2 executors might be explained by the fact that this layer often includes power intensive operations like for example joins which can be preformed faster using an executor with an access to more computing power. When the power is split among other executors dbt could experience a bottleneck. Other thing to remember is that more executors mean more time spent coordinating.
If a better performance is needed a better approach might be to increase the processing power instead of the number of executors.

kubectl scale --replicas=2 statefulset specjbb-group-preset-small
kubectl scale --replicas=4 statefulset specjbb-group-preset-medium
kubectl scale --replicas=8 statefulset specjbb-group-preset-big
kubectl scale --replicas=2 statefulset specjbb-controller-preset-small specjbb-controller-preset-medium specjbb-controller-preset-big

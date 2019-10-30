echo -------------------------------- FLUENTD --------------------------------------------------
kubectl delete serviceaccount --all -n fluentd
kubectl delete ds --all -n fluentd
kubectl delete cm --all -n fluentd
kubectl delete svc --all -n fluentd
kubectl delete rolebinding --all -n fluentd
kubectl delete role --all -n fluentd
kubectl delete servicemonitor.monitoring.coreos.com/fluentd -n fluentd
echo '---------------- Remaining objects:'
kubectl api-resources --verbs=list --namespaced -o name | grep -v events | xargs -n 1 kubectl get --show-kind --ignore-not-found -n fluentd

echo ---------------------------------- GRAFANA -------------------------------------------------------------------
kubectl delete deploy --all -n grafana
kubectl delete svc --all -n grafana
kubectl delete cm --all -n grafana
kubectl delete rolebinding --all -n grafana
kubectl delete role --all -n grafana
echo '---------------- Remaining objects:'
kubectl api-resources --verbs=list --namespaced -o name | grep -v events | xargs -n 1 kubectl get --show-kind --ignore-not-found  -n grafana

echo ---------------------------------- KUBE-STATE-METRICS -------------------------------------------------------------------
kubectl delete deploy --all -n kube-state-metrics
kubectl delete svc --all -n kube-state-metrics
kubectl delete cm --all -n kube-state-metrics
kubectl delete rolebinding --all -n kube-state-metrics
kubectl delete role --all -n kube-state-metrics
echo '---------------- Remaining objects:'
kubectl api-resources --verbs=list --namespaced -o name | grep -v events | xargs -n 1 kubectl get --show-kind --ignore-not-found  -n kube-state-metrics

echo ---------------------------------- PROMETHEUS ------------------------------------------------------------------
kubectl delete deploy --all -n prometheus
kubectl delete sts --all -n prometheus
kubectl delete serviceaccount --all -n prometheus
kubectl delete svc --all -n prometheus
kubectl delete cm --all -n prometheus
kubectl delete rolebinding --all -n prometheus
kubectl delete role --all -n prometheus
kubectl delete crd alertmanagers.monitoring.coreos.com
kubectl delete crd podmonitors.monitoring.coreos.com
kubectl delete crd prometheuses.monitoring.coreos.com
kubectl delete crd prometheusrules.monitoring.coreos.com
kubectl delete crd servicemonitors.monitoring.coreos.com
echo '---------------- CRDs:'
kubectl get customresourcedefinitions
echo '---------------- Remaining objects:'
kubectl api-resources --verbs=list --namespaced -o name | grep -v events | xargs -n 1 kubectl get --show-kind --ignore-not-found  -n prometheus
echo ------------------------------------ WCA ----------------------------------------------------------------
kubectl delete ds --all -n wca
kubectl delete serviceaccount --all -n wca
kubectl delete svc --all -n wca
kubectl delete cm --all -n wca
kubectl delete rolebinding --all -n wca
kubectl delete role --all -n wca
kubectl delete servicemonitor.monitoring.coreos.com/wca -n wca
echo '---------------- Remaining objects:'
kubectl api-resources --verbs=list --namespaced -o name | grep -v events | xargs -n 1 kubectl get --show-kind --ignore-not-found  -n wca


echo ------------------------------------ Cluster scoped roles and bindings ----------------------------------------------------------------
kubectl delete clusterrolebinding prometheus
kubectl delete clusterrole prometheus
kubectl delete clusterrolebinding prometheus-operator
kubectl delete clusterrole prometheus-operator
kubectl delete clusterrolebinding fluentd
kubectl delete clusterrole fluentd
kubectl delete clusterrolebinding wca
kubectl delete clusterrole wca


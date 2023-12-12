# NATS-Application

Make following changes to the apps direcotry of your bundle repository.

1. Create a file with name like nats-template.yaml in apps directory
2. Modify the file with following content

## NATS Application to send and receive messages

```yaml
---
apiVersion: core.oam.dev/v1beta1
kind: Application
metadata:
  name: natsapp                                                                     # <Change the component name if needed>
  namespace: vela-system
spec:
  components:
  - name: natsapp
    type: webservice
    properties:
      image: cr.siemens.com/score/infrastructure/container-images/oss-images/nats-test-app:v1
      imagePullSecrets: 
      - score-docker-secret
      env:
      - name: NATS_CHART_NAME
        value: score-nats                                                           # <Change the Chart name if needed>
      - name: NAMESPACE
        value: vela-system
      ports:
      - port: 5000
        name: http
        protocol: TCP
    traits:
    - type: score-ingress
      properties:
        domainRoutes:
        - domain: natsapp.${domain}
          httpRoutes:
            - path: "/"
              service: natsapp
              port: 5000
              createService: true
        ingressClass: "prod-kong-ingress"
```
